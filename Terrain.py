import copy

class Terrain(object):
    def __init__(self, parameters=None, original=True):
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
        if original:
            self.generate_terrain()
    
    def generate_terrain(self):
        self.terrain = []
        for i, cell_line_parameters in enumerate(self.parameters['cells']):
            line = []
            for j, cell_parameters in enumerate(cell_line_parameters):
                terrain_block = TerrainBlock(i, j, self, cell_parameters)
                line.append(terrain_block)
            self.terrain.append(line)
    
    def cells(self):
        for line in self.terrain:
            for cell in line:
                yield cell

    def get_cell(self, x, y):
        return self.terrain[x][y]

    def copy(self):
        new_terrain = Terrain(self.parameters, False)
        new_terrain.terrain = copy.deepcopy(self.terrain)
        return new_terrain

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

        self.q = None # content of a cell 'i' of the neighborhood
        self.p = None # amount which can be distributed to neighboring cells
        
    def neighbours(self):
        for n_i in [self.i-1, self.i, self.i+1]:
            for n_j in [self.j-1, self.j, self.j+1]:
                if not (n_i==self.i and n_j==self.j) and self.terrain.width>n_i>=0 and self.terrain.height>n_j>=0:
                    yield self.terrain.get_cell(n_i, n_j)

    @property
    def total_height(self):
        return self.height_of_terrain + self.peat_bog_thickness + self.height_of_water

    @property
    def non_dispersible_height(self):
        return self.height_of_terrain + self.peat_bog_thickness

    def get_new_waterlevel(self, cells_receiving_water=None):
        if cells_receiving_water==None:
            cells_receiving_water = [self] + list(self.neighbours())

        total_height_cells = sum([cell.total_height for cell in cells_receiving_water])
        new_average_height_cells = total_height_cells / len(cells_receiving_water)
        for cell in cells_receiving_water:
            if cell!=self and cell.total_height > new_average_height_cells:
                cells_receiving_water.remove(cell)
                return self.get_new_waterlevel(cells_receiving_water)

        return new_average_height_cells
        
    def get_p(self):
        ''' amount which can be distributed to neighboring cells '''
        for neighbour in self.neighbours():
            self.p += neighbour.f

    def __str__(self):
        return "({},{}): {} {} {} {}".format(
            self.i,
            self.j,
            self.height_of_terrain,
            self.height_of_water,
            self.concentration_of_nutrients,
            self.peat_bog_thickness)

