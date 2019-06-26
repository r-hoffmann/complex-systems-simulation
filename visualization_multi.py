import sys
from TerrainPlotterMulti import TerrainPlotterMulti

if __name__ == "__main__":
    filenames = []
    for i in 'abcdef':
        filenames.append('output_24{}.json'.format(i))

    plotter = TerrainPlotterMulti(filenames, show=False, save_to_filesystem=True, path_to_outputs= "./")