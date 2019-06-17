import json
from Terrain import Terrain

class Model(object):
    def __init__(self, parameters=None):
        """
            dict parameters should contain the following keys:
                height (int)
                width (int)
                slope (float)
                gamma (float)
                rho (float)
                mu (float)
                cells (list of lists of dict containing the keys:
                    height_of_terrain
                    height_of_water
                    concentration_of_nutrients
                    peat_bog_thickness)
        """
        self.parameters = parameters
        self.gamma = self.parameters['gamma']
        self.rho = self.parameters['rho']
        self.mu = self.parameters['mu']
        self.terrain = Terrain(parameters)
    
    def run(self, timesteps=10**3, dump_to_file=True):
        terrain_timeline = [self.terrain.get_summary()]
        for t in range(timesteps):
            print("Timestep {}".format(t+1))
            self.timestep()
            terrain_timeline.append(self.terrain.get_summary())

        summary = self.get_summary(terrain_timeline)
        if dump_to_file:
            with open('output.json', 'w') as file:
                print("Output to output.json")
                json.dump(summary, file)
        return terrain_timeline

    def step(self):
        print('step')

    def timestep(self):
        # Directly from paper
        self.calculate_flows()
        self.calculate_nutrient_dist()
        self.calculate_peat_growth()

    def calculate_flows(self):
        # mutations is the collection of f[i] in the paper
        mutations = []

        for cell in self.terrain.cells():
            water_flow = cell.get_water_flow()
            # "commit"
            mutations += water_flow

        for mutation in mutations:
            # "push"
            mutation['from'].height_of_water -= mutation['water']
            mutation['to'].height_of_water += mutation['water']
            # if mutation['water']>0:
            #     print(mutation)

    def calculate_nutrient_dist(self):
        for cell in self.terrain.cells():
            if cell.height_of_water > 0:
                cell.concentration_of_nutrients = 1
            else:
                cell.concentration_of_nutrients = max([neighbour_cell.concentration_of_nutrients for neighbour_cell in cell.neighbours()])

    def calculate_peat_growth(self):
        for cell in self.terrain.cells():
            if cell.height_of_water > 0:
                cell.peat_bog_thickness = self.mu * cell.concentration_of_nutrients
            else:
                cell.peat_bog_thickness = self.rho * cell.concentration_of_nutrients

    def get_summary(self, terrain_timeline):
        self.gamma = self.parameters['gamma']
        self.rho = self.parameters['rho']
        self.mu = self.parameters['mu']
        return {
            'gamma': self.gamma,
            'rho': self.rho,
            'mu': self.mu,
            'terrain_timeline': terrain_timeline
        }
        
