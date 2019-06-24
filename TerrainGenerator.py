import math, noise, random
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

class TerrainGenerator(object):
    def __init__(self, width=100, height=100, slope=0.05):
        self.width = width
        self.height = height
        self.slope = slope

    def generate(self, grid_type='hill_grid', parameters={}):
        type_to_function = {
            'flat': self.flat,
            'hill_grid': self.generate_hill_grid,
            'fractal_height_map': self.generate_fractal_height_map,
            'pnoise2': self.generate_pnoise2
        }
        grid = type_to_function[grid_type](parameters)
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                grid[y][x] = cell + (self.slope * (self.height / 1000)) * (self.height - y)
        return grid

    def flat(self):
        return [[0 for x in range(self.width)] for y in range(self.height)]

    def generate_hill_grid(self, parameters):
        # @todo should accept non-rectangular sizes
        h = HillGrid(ITER=50, SIZE=100)
        return h.grid
    
    def generate_fractal_height_map(self, parameters):
        # @todo should accept non-rectangular sizes
        g_size = 100 #//must be power of 2
        g = Grid(g_size, g_size)
        f = FractalHeightmap(g, 1, 10, max_depth=math.sqrt(g_size))
        return g.data
    
    def generate_pnoise2(self, parameters):
        shape = (self.width, self.height)
        scale = 1000
        octaves = 10
        persistence = .3
        lacunarity = 100

        world = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                world[i][j] = noise.pnoise2(i/scale, 
                                        j/scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        repeatx=1024, 
                                        repeaty=1024, 
                                        base=0)
        world = parameters['roughness'] * (world - world.min()) / world.max()
        return world

class HillGrid:
    def __init__(self, KRADIUS =(1.0/5.0), ITER=200, SIZE=40):
        self.KRADIUS = KRADIUS
        self.ITER = ITER
        self.SIZE = SIZE

        self.grid = [[0 for x in range(self.SIZE)] for y in range(self.SIZE)]

        self.MAX = self.SIZE * self.KRADIUS
        for _ in range(self.ITER):
            self.step()

    def __getitem__(self,n):
        return self.grid[n]

    def step(self):
        point = [random.randint(0,self.SIZE-1),random.randint(0,self.SIZE-1)]
        radius = random.uniform(0,self.MAX)

        x2 = point[0]
        y2 = point[1]    

        for x in range(self.SIZE):
            for y in range(self.SIZE):
                z = (radius**2) - ( math.pow(x2-x,2) + math.pow(y2-y,2) )
                if z >= 0:
                    self.grid[x][y] += int(z)

class Grid(object):
    def __init__(self, x, y):
        self.size_x = x
        self.size_y = y
        self.data = [[0 for _ in range(x)] for _ in range(y)]

    def make(self,coordinate,value):
        self.data[int(coordinate.x)][int(coordinate.y)] = value

    def make_new(self,coordinate,value):
        if self.data[int(coordinate.x)][int(coordinate.y)] == 0:
            self.make(coordinate, value)

    def get(self,coordinate):
        return self.data[int(coordinate.x)][int(coordinate.y)]

class FractalHeightmap(object):
    '''populates a 'grid' with a fractal heightmap'''
    def __init__(self, grid, rng_seed, roughness,
                 corner_seeds=[(0,0), (100,100), (0,0), (100,100)],
                 max_depth=3):
        self.coord = namedtuple('Coord','x y')
        self.grid = grid
        self.max_depth = max_depth
        self._set_initial_corners(corner_seeds)
        self.roughness = roughness
        self.generate_heightmap([self.coord(0,0),
                                 self.coord(self.grid.size_x - 1, 0),
                                 self.coord(0, self.grid.size_y - 1),
                                 self.coord(self.grid.size_x - 1, self.grid.size_y - 1)], 
                                 1)

    def _set_initial_corners(self, corner_seeds):
        tl,tr,bl,br = corner_seeds
        seeds = [[tl, tr], [bl, br]]
        for x_idx, x in enumerate([0, self.grid.size_x - 1]):
            for y_idx, y in enumerate([0, self.grid.size_y - 1]):
                try:
                    minval, maxval = seeds[x_idx][y_idx]
                    val = minval + random.random() * (maxval - minval)
                except ValueError:
                    val=seeds[x_idx][y_idx]
                self.grid.make_new(self.coord(x, y), val)

    def generate_heightmap(self, corners,depth):
        '''corners = (Coord(),Coord(),Coord(),Coord() / tl/tr/bl/br'''
        if depth > self.max_depth: 
            return

        tl,tr,bl,br = corners
        center = self.coord(tl.x + ((tr.x - tl.x) / 2), tr.y + ((br.y - tr.y) / 2))

        #define edge center coordinates
        top_c = self.coord(tl.x + (tr.x - tl.x) / 2, tl.y)
        left_c = self.coord(tl.x, tl.y + (bl.y - tl.y) / 2)
        right_c = self.coord(tr.x, tr.y + (br.y - tr.y) / 2)
        bot_c = self.coord(bl.x + (br.x - bl.x) / 2, bl.y)

        #calc the center and edge_center heights
        avg = sum([self.grid.get(tl),
                self.grid.get(tr),
                self.grid.get(bl),
                self.grid.get(br)]
                ) / 4.0  ###NOTE, we can choose to use the current corners, the new edge-centers, or all
                #currenty we use the current corners
                #then do the edge centers
        offset = (random.random() - 0.5) * self.roughness 
        self.grid.make_new(center, avg + offset)

        #top_c
        avg = sum([self.grid.get(tl),
                self.grid.get(tr)]
                ) / 2.0
        offset = (random.random() - 0.5) * self.roughness
        self.grid.make_new(top_c, avg + offset)

        #left_c
        avg = sum([self.grid.get(tl),
                 self.grid.get(bl)]
                ) / 2.0
        offset = (random.random() - 0.5) * self.roughness
        self.grid.make_new(left_c, avg + offset)

        #right_c        
        avg = sum([self.grid.get(tr),
                 self.grid.get(br)]
                ) / 2.0
        offset = (random.random() - 0.5) * self.roughness
        self.grid.make_new(right_c, avg + offset)

        #bot_c
        avg=sum([self.grid.get(bl),
                 self.grid.get(br)]
                ) / 2.0
        offset = (random.random() - 0.5) * self.roughness
        self.grid.make_new(bot_c, avg + offset)

        self.generate_heightmap((tl, top_c, left_c, center), depth + 1)
        self.generate_heightmap((top_c, tr, center, right_c), depth + 1)
        self.generate_heightmap((left_c, center, bl, bot_c), depth + 1)
        self.generate_heightmap((center, right_c, bot_c, br), depth + 1)
