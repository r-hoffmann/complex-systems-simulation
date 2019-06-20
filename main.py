import json
from Model import Model
from TerrainPlotter import TerrainPlotter

def test_each_terrain():
    from TerrainGenerator import TerrainGenerator
    width = 100
    height = 100
    generator = TerrainGenerator(width, height)
    print('hill_grid')
    hill_grid = generator.generate('hill_grid')
    assert len(hill_grid)==width and len(hill_grid[0])==height, "Something wrong with hill_grid dimensions {}x{}!={}x{}".format(width,height,len(hill_grid),len(hill_grid[0]))

    print('fractal_height_map')
    fractal_height_map = generator.generate('fractal_height_map')
    assert len(fractal_height_map)==width and len(fractal_height_map[0])==height, "Something wrong with fractal_height_map dimensions {}x{}!={}x{}".format(width,height,len(fractal_height_map),len(fractal_height_map[0]))

    print('pnoise2')
    pnoise2 = generator.generate('pnoise2')
    assert len(pnoise2)==width and len(pnoise2[0])==height, "Something wrong with pnoise2 dimensions {}x{}!={}x{}".format(width,height,len(pnoise2),len(pnoise2[0]))

if __name__ == "__main__":
    model = Model()
    model.run()

    plotter = TerrainPlotter(filename='output.json', save_to_filesystem=True, show=False)
    plotter.plot_last_heights()

