from Terrain import Terrain

class Model(object):
    def __init__(self, height=None, width=None, parameters=None):
        self.terrain = Terrain(height, width, parameters)
    
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
                cell.concentration_of_nutrients = max([1])

    def calculate_peat_growth(self):
        raise NotImplementedError()