import sys
from TerrainPlotter import TerrainPlotter

if __name__ == "__main__":
    if len(sys.argv)>1:
        plotter = TerrainPlotter(filename='output_{}.json'.format(sys.argv[1]), save_to_filesystem=True, show=False)
    else:
        plotter = TerrainPlotter(filename='output_34a.json', save_to_filesystem=True, show=False)

    plotter.plot_3d()