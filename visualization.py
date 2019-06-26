import sys
from TerrainPlotter import TerrainPlotter

if __name__ == "__main__":
    plotter = TerrainPlotter(filename='output_21f.json', save_to_filesystem=True, show=False)
    # plotter = TerrainPlotter(filename='output.json', save_to_filesystem=True, show=False)

    plotter.plot_all_heights_with_measures()