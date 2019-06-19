from TerrainPlotter import TerrainPlotter

if __name__ == "__main__":
    plotter = TerrainPlotter(save_to_filesystem=True, show=False)
    plotter.plot_all_heights()