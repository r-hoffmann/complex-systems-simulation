import json
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

def load_data(filename='output.json'):
    with open('output.json') as json_file:  
        return json.load(json_file)

def plot_heatmap():
    data = load_data()

    x = np.arange(0, 10, 1)
    y = np.arange(0, 10, 1)

with open('output_100x100_smallPool.json') as json_file:  
    data = json.load(json_file)
    for timestep in data['terrain_timeline']:
        fig = plt.figure()
        zz = []
        for row in timestep:
            line = []
            for cell in row:
                # if(cell['height_of_water'] > 0 ):
                #     line.append(1)
                # else:
                #     line.append(0)
                line.append(cell['height_of_water'])
            zz.append(line)
        zz = np.array(zz)
        # make a color map of fixed colors
        cmap = mpl.colors.ListedColormap(['green','cyan','blue','darkblue'])
        bounds=[-1,0.01,1,5,10]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        # tell imshow about color map so that only set colors are used
        img = plt.imshow(zz,interpolation='nearest', cmap = cmap,norm=norm)

        # make a color bar
        plt.colorbar(img,cmap=cmap, norm=norm,boundaries=bounds,ticks=[-5,0,5])

        plt.show()

def plot_hist_water():
    data = load_data()
    for timestep in data['terrain_timeline']:
        water_heights = []
        for row in timestep[0:2]:
            for cell in row:
                water_heights.append(cell['height_of_water'])
        plt.hist(water_heights, density=True)
        print(min(water_heights), max(water_heights))
        plt.show()

if __name__ == "__main__":
    plot_hist_water()