import sys
from TerrainPlotter import TerrainPlotter

if __name__ == "__main__":
    if len(sys.argv)>0:
        plotter = TerrainPlotter(filename='output_{}.json'.format(sys.argv[1]), save_to_filesystem=True, show=False)
    else:
        plotter = TerrainPlotter(filename='output_21f.json', save_to_filesystem=True, show=False)

    plotter.plot_all_heights_with_measures()