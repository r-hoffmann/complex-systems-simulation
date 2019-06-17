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
    
    def run(self, timesteps=10, dump_to_file=True):
        self.water_out = [0]
        terrain_timeline = [self.terrain.get_summary()]
        for t in range(timesteps):
            print("Timestep {}".format(t+1))
            self.current_water_out = 0
            self.timestep()
            self.water_out.append(self.current_water_out - self.water_out[-1])
            print("Water out this step: {}".format(self.current_water_out))
            terrain_timeline.append(self.terrain.get_summary())

        summary = self.get_summary(terrain_timeline)
        if dump_to_file:
            with open('output.json', 'w') as file:
                print("Output to output.json")
                json.dump(summary, file)
        return terrain_timeline

    def timestep(self):
        # Directly from paper
        self.mutations = []
        self.supply_water()
        self.remove_water()
        self.calculate_flows()
        self.update_water()
        self.calculate_nutrient_dist()
        self.calculate_peat_growth()

    def supply_water(self):
        # @todo: Make some kind of distribution?
        for cell in self.terrain.terrain[0]:
            self.mutations.append({
                'from': None,
                'to': cell,
                'water': 100
            })

    def remove_water(self):
        # @todo: Remove all water from last row?
        for cell in self.terrain.terrain[-1]:
            self.mutations.append({
                'from': cell,
                'to': None,
                'water': cell.height_of_water
            })

    def calculate_flows(self):
        # mutations is the collection of f[i] in the paper
        for cell in self.terrain.cells():
            if cell.height_of_water>0:
                mutations = cell.get_water_flow()
                # "commit"
                self.mutations += mutations

    def update_water(self):
        mutated = 0
        max_depth = 0
        for mutation in self.mutations:
            # None cells are either inlet or outlet
            if mutation['water'] > 0:
                if mutation['from'] != None:
                    mutation['from'].height_of_water -= mutation['water']
                if mutation['to'] != None:
                    mutation['to'].height_of_water += mutation['water']
                    if mutation['to'].y > max_depth:
                        max_depth = mutation['to'].y
                else:
                    self.current_water_out += mutation['water']
                mutated += 1
            # if mutation['to'] != None and mutation['from'] != None:
            #     print(mutation, (mutation['from'].x - mutation['to'].x)**2 + (mutation['from'].y - mutation['to'].y)**2)
        print("Ran {} water mutations, max depth {}.".format(mutated, max_depth))

    def calculate_nutrient_dist(self):
        new_terrain = self.terrain.copy()
        for cell, new_cell in zip(self.terrain.cells(), new_terrain.cells()):
            if cell.height_of_water > 0:
                cell.concentration_of_nutrients = 1
            else:
                new_cell.concentration_of_nutrients = self.gamma * max([neighbour_cell.concentration_of_nutrients for neighbour_cell in cell.neighbours()])
        self.terrain = new_terrain

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
        
