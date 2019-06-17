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
    
    def run(self):
        print('test')

    def step(self):
        print('step')

    def timestep(self):
        # Directly from paper
        self.calculate_flows()
        self.calculate_nutrient_dist()
        self.calculate_peat_growth()

    def calculate_flows(self):
        raise NotImplementedError()

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
