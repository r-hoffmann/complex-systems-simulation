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
        for x, cell_line_parameters in enumerate(self.parameters['cells']):
            line = []
            for y, cell_parameters in enumerate(cell_line_parameters):
                terrain_block = TerrainBlock(x, y, self, cell_parameters)
                line.append(terrain_block)
            self.terrain.append(line)
        assert self.width * self.height == len(self.terrain) * len(self.terrain[0]), "Width and height do no correspond to given cell parameters {}x{}!={}x{}".format(self.width, self.height, len(self.terrain), len(self.terrain[0]))
    
    def cells(self):
        for line in self.terrain:
            for cell in line:
                yield cell

    def get_cell(self, x, y):
        return self.terrain[x][y]

    def get_summary(self):
        summary = []
        for line in self.terrain:
            summary_line = []
            for cell in line:
                summary_line.append(cell.get_summary())
            summary.append(summary_line)
        return summary

    def copy(self):
        new_terrain = Terrain(self.parameters, False)
        new_terrain.terrain = copy.deepcopy(self.terrain)
        return new_terrain

class TerrainBlock(object):
    def __init__(self, x, y, terrain, parameters):
        """
            parameters should be a dict with keys:
                height_of_terrain
                height_of_water
                concentration_of_nutrients
                peat_bog_thickness
        """
        self.x = x
        self.y = y
        self.terrain = terrain
        self.height_of_terrain = parameters['height_of_terrain']
        self.height_of_water = parameters['height_of_water']
        self.concentration_of_nutrients = parameters['concentration_of_nutrients']
        self.peat_bog_thickness = parameters['peat_bog_thickness']
        
    def neighbours(self):
        neighbours = []
        if self.x > 0:
            neighbours.append(self.terrain.get_cell(self.x - 1, self.y))
        if self.y > 0:
            neighbours.append(self.terrain.get_cell(self.x, self.y - 1))
        if self.terrain.width > self.x + 1:
            neighbours.append(self.terrain.get_cell(self.x + 1, self.y))
        if self.terrain.height > self.y + 1:
            neighbours.append(self.terrain.get_cell(self.x, self.y + 1))
        return neighbours

    @property
    def total_height(self):
        return self.height_of_terrain + self.peat_bog_thickness + self.height_of_water

    @property
    def non_dispersible_height(self):
        return self.height_of_terrain + self.peat_bog_thickness

    def get_water_flow_paper(self, cells_receiving_water=None):
        # litterally the algorithm in the paper
        neighbours = self.neighbours()
        m = len(neighbours)
        eliminated = []
        for i in range(0, m):
            eliminated.append(False)
        
        new_control = True
        while new_control:
            new_control = False
            q_sum = self.height_of_water
            count = 0
            for i in range(0, m):
                if not eliminated[i]:
                    q_sum += neighbours[i].total_height
                    count += 1
            average = q_sum / count
            for i in range(0, m):
                if neighbours[i].total_height > average and not eliminated[i]:
                    new_control = True
                    eliminated[i] = True
        f = []
        print('next')
        for i in range(0, m):
            if eliminated[i]:
                f.append(0)
            f.append(max(0, average - neighbours[i].total_height))

        # end of algorithm in paper
        water_flow = []
        for i in range(0, m):
            water_flow.append({
                'from': self,
                'to': neighbours[i],
                'water': f[i]
            })
        return water_flow

    def get_water_flow(self, cells_receiving_water=None):
        # uses notation from paper
        if cells_receiving_water==None:
            cells_receiving_water = [self] + list(self.neighbours())

        q_sum = sum([cell.total_height for cell in cells_receiving_water])
        average = q_sum / len(cells_receiving_water)
        for cell in cells_receiving_water:
            if cell!=self and cell.total_height > average:
                cells_receiving_water.remove(cell)
                return self.get_water_flow(cells_receiving_water)
                
        water_flow = []
        for cell in cells_receiving_water:
            if self != cell:
                water_flow.append({
                    'from': self,
                    'to': cell,
                    'water': average - cell.total_height
                })
        return water_flow

    def get_summary(self):
        return {
                    "x": self.x,
                    "y": self.y,
                    "height_of_terrain": self.height_of_terrain,
                    "height_of_water": self.height_of_water,
                    "concentration_of_nutrients": self.concentration_of_nutrients,
                    "peat_bog_thickness": self.peat_bog_thickness
                }

    def __str__(self):
        return "({},{}): {} {} {} {}".format(
            self.x,
            self.y,
            self.height_of_terrain,
            self.height_of_water,
            self.concentration_of_nutrients,
            self.peat_bog_thickness)
    
    def __repr__(self):
        return "({},{})".format(
            self.x,
            self.y)

