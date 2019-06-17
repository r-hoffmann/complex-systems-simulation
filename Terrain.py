class Terrain(object):
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
        self.height = self.parameters['height']
        self.width = self.parameters['width']
        self.slope = self.parameters['slope']
        self.generate_terrain()
    
    def generate_terrain(self):
        self.terrain = []
        for i, line in enumerate(self.parameters['cells']):
            line = []
            for j, cell_parameters in enumerate(line):
                terrain_block = TerrainBlock(i, j, self, cell_parameters)
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

        self.q # content of a cell 'i' of the neighborhood
        self.p # amount which can be distributed to neighboring cells
        

    
    def neighbours(self):
        for n_i in [self.i-1, self.i, self.i+1]:
            for n_j in [self.j-1, self.j, self.j+1]:
                if n_i!=n_j and self.terrain.width>n_i>0 and self.terrain.height>n_j>0:
                    yield [n_i, n_j]
    
    def get_p(self):
        ''' amount which can be distributed to neighboring cells '''
        for neighbour in self.neighbours():
            self.p += neighbour.f

