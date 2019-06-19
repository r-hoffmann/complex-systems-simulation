import copy
import numpy as np
from numpy.random import normal
from TerrainGenerator import TerrainGenerator

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
        self.concentration_of_nutrients = self.parameters['concentration_of_nutrients']
        self.generator_type = self.parameters['generator_type']
        self.generator_parameters = self.parameters['generator_parameters']
        if original:
            self.generate_terrain()
    
    def generate_terrain(self):
        self.terrain = []
        generator = TerrainGenerator(self.width, self.height, self.slope)
        terrain_heights = generator.generate(self.generator_type, self.generator_parameters)

        for y, terrain_heights_line in enumerate(terrain_heights):
            line = []
            for x, terrain_height in enumerate(terrain_heights_line):
                terrain_block = TerrainBlock(x, y, self, terrain_height, self.concentration_of_nutrients)
                line.append(terrain_block)
            self.terrain.append(line)
        assert self.width * self.height == len(self.terrain) * len(self.terrain[0]), "Width and height do no correspond to given cell parameters {}x{}!={}x{}".format(self.width, self.height, len(self.terrain), len(self.terrain[0]))
    
    def cells(self):
        for line in self.terrain:
            for cell in line:
                yield cell

    def get_cell(self, x, y):
        # assert x == self.terrain[y][x].x and y == self.terrain[y][x].y,"Flipped x and y."
        return self.terrain[y][x]

    def get_summary(self):
        # @todo: normalize these values?
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
    def __init__(self, x, y, terrain, height_of_terrain, concentration_of_nutrients):
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
        self.height_of_terrain = height_of_terrain
        self.height_of_water = 0
        self.concentration_of_nutrients = concentration_of_nutrients
        self.peat_bog_thickness = 0
        
    def neighbours(self):
        for n_x in [self.x - 1, self.x, self.x + 1]:
            for n_y in [self.y - 1, self.y, self.y + 1]:
                if (not (n_x==self.x and n_y==self.y)) and self.terrain.width>n_x>=0 and self.terrain.height>n_y>=0:
                    yield self.terrain.get_cell(n_x, n_y)

    @property
    def total_height(self):
        return self.height_of_terrain + self.peat_bog_thickness + self.height_of_water

    @property
    def non_dispersible_height(self):
        return self.height_of_terrain + self.peat_bog_thickness

    def get_water_flow(self, cells_receiving_water=None):
        if self.height_of_water == 0:
            return []
        # uses notation from paper
        if cells_receiving_water==None:
            cells_receiving_water = list(self.neighbours())

        q_sum = self.total_height + sum([cell.total_height for cell in cells_receiving_water])
        average = q_sum / (len(cells_receiving_water) + 1)
        for cell in cells_receiving_water:
            if cell.total_height > average:
                cells_receiving_water.remove(cell)
                return self.get_water_flow(cells_receiving_water)

        water_flow = []
        water_lost = 0
        for cell in cells_receiving_water:
            water_lost += (average - cell.total_height)
            water_flow.append({
                'from': self,
                'to': cell,
                'water': average - cell.total_height
            })
        if water_lost > self.height_of_water:
            ratio_fix = self.height_of_water / water_lost
            water_flow = []
            for cell in cells_receiving_water:
                water_flow.append({
                    'from': self,
                    'to': cell,
                    'water': (average - cell.total_height) * ratio_fix
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
