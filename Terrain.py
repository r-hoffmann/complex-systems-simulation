class Terrain(object):
    def __init__(self, height=None, width=None, parameters=None):
        """
            @todo: parameters pre-defined or generated on the run with some hyperparameters? i.e. distributions with certain characteristics?
        """
        self.height = height
        self.width = width
        self.parameters = parameters
        self.generate_terrain()
    
    def generate_terrain(self):
        self.terrain = []
        print(self.height, self.width)
        for y in range(self.height):
            line = []
            for x in range(self.width):
                terrain_block = TerrainBlock(x, y, self, self.parameters)
                line.append(terrain_block)
            self.terrain.append(line)
    
    def cells(self):
        for line in self.terrain:
            for cell in line:
                yield cell


class TerrainBlock(object):
    def __init__(self, i, j, terrain, parameters):
        """
            parameters should be a dict with keys:
                height_of_terrain
                height_of_water
                concentration_of_nutrients
                peat_bog_thickness
        """
        self.i = i
        self.j = j
        self.terrain = terrain
        self.height_of_terrain = parameters['height_of_terrain']
        self.height_of_water = parameters['height_of_water']
        self.concentration_of_nutrients = parameters['concentration_of_nutrients']
        self.peat_bog_thickness = parameters['peat_bog_thickness']

    def neighbours(self):
        for n_i in [self.i-1, self.i, self.i+1]:
            for n_j in [self.j-1, self.j, self.j+1]:
                if n_i!=n_j and self.terrain.width>n_i>0 and self.terrain.height>n_j>0:
                    yield [n_i, n_j]