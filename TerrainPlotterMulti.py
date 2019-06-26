import json, math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import colors
import os




class TerrainPlotterMulti(object):
    def __init__(self, filenames, show=True, save_to_filesystem=False, path_to_outputs= "./Experiments/Plot_Experiment/"):
        self.filenames = filenames
        self.show = show
        self.save_to_filesystem = save_to_filesystem
        self.measure_ratio_water_land_timeline_list = []
        self.measure_settlement_efficiency_timeline_list = []
        self.peat_timeline_list = []
        self.total_water_timeline_list = []
        self.water_in_timeline_list = []
        self.water_out_timeline_list = []
        self.river_timeline_list = []
        self.path = path_to_outputs

        self.flow()
        self.plot_multiline_plots()

    def flow(self):
        for filename in self.filenames:
            self.load_data(self.path+filename)
            self.get_measures()

    def load_data(self, filename):
        with open(filename) as json_file:  
            self.data = json.load(json_file)
        

    def get_measures(self):
        self.measure_ratio_water_land_timeline_list.append(self.data['measure_ratio_water_land_timeline'])
        self.measure_settlement_efficiency_timeline_list.append(self.data['measure_settlement_efficiency_timeline'])
        self.peat_timeline_list.append(self.data['peat_timeline'])
        self.total_water_timeline_list.append(self.data['water_timeline'])
        self.water_in_timeline_list.append(self.data['water_in_timeline'])
        self.water_out_timeline_list.append(self.data['water_out_timeline'])
        self.river_timeline_list.append(self.data['river_timeline'][-1])


    def plot_multiline_plots(self):
        fig, ax = plt.subplots(figsize=(12, 6), ncols=3, nrows=2)
        for i in range(len(self.filenames)):

            measure_ratio_water_land_timeline = self.measure_ratio_water_land_timeline_list[i]
            measure_settlement_efficiency_timeline = self.measure_settlement_efficiency_timeline_list[i]
            peat_timeline = self.peat_timeline_list[i]
            total_water_timeline = self.total_water_timeline_list[i]
            water_in_timeline = self.water_in_timeline_list[i]
            water_out_timeline = self.water_out_timeline_list[i]
            river_timeline = self.river_timeline_list[i]


            ax[0, 0].set_title('Ratio between water and land', y=-0.01)
            pos1 = ax[0, 0].plot(measure_ratio_water_land_timeline)
            
            ax[0, 1].set_title('Settlement efficiency', y=-0.01)
            pos2 = ax[0, 1].plot(measure_settlement_efficiency_timeline)
            
            ax[0, 2].set_title('Total peat', y=-0.01)
            pos3 = ax[0, 2].plot(peat_timeline)

            ax[1,0].set_title('Total Water', y=-0.01)
            pos4 = ax[1, 0].plot(total_water_timeline)

            ax[1,1].set_title('Water Flow Out of System', y=-0.01)
            pos5 = ax[1, 1].plot(water_out_timeline, label="out")
            # pos5 = ax[1, 1].plot(water_in_timeline, label="in")

            ax[1,2].set_title('River Distribution', y=-0.01)
            # pos6 = ax[1,2].bar(np.arange(len(river_smooth)), river_smooth, align='edge',facecolor='steelblue', edgecolor='steelblue')
            pos6 = ax[1,2].plot(river_timeline)
            

        if self.save_to_filesystem:
            plt.savefig('Final_Images/multi_line_plot.png')
        if self.show:
            plt.show()


plotter = TerrainPlotterMulti(filenames=["output_1.json","output_2.json","output_3.json","output_4.json"], save_to_filesystem=True, show=False, path_to_outputs = "./Experiments/Plot_Experiment/")
