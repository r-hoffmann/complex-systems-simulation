import noise
import numpy as np
from scipy.misc import toimage

def terrain():
        shape = (100,100)
        scale = 100
        octaves = 10
        persistence = 0.5
        lacunarity = 2.0

        world = np.zeros(shape)
        for i in range(shape[0]):
        for j in range(shape[1]):
                world[i][j] = (noise.pnoise2(i/scale, 
                                        j/scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        repeatx=1024, 
                                        repeaty=1024, 
                                        base=0))+1**2
                
        return np.array(world)
                
        # toimage(world).show()