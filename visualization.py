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

    data = load_data()
    for t, timestep in enumerate(data['terrain_timeline']):
        fig = plt.figure()
        water_height = []
        for row in timestep:
            line = []
            for cell in row:
                if(cell['height_of_water'] > 0 ):
                    line.append(-1*cell['height_of_water'])
                else:
                    line.append(cell['height_of_terrain']+cell['peat_bog_thickness'])
                # line.append(cell['height_of_water'])
            water_height.append(line)
            # print(line)
        water_height = np.array(water_height)
        # make a color map of fixed colors
        cmap = mpl.colors.ListedColormap(['#023858', '#045a8d', '#3690c0', '#fff7ec','#fee8c8','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#b30000','#7f0000'])
        bounds=[-6, -4,-2, 0, 2, 4, 6,8,10,12,14,16]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        # tell imshow about color map so that only set colors are used
        img = plt.imshow(water_height,interpolation='nearest', cmap = cmap,norm=norm)

        # make a color bar
        plt.colorbar(img,cmap=cmap, norm=norm,boundaries=bounds,ticks=bounds)
        
        plt.savefig('images/{}.png'.format(t))
        plt.close()
        # plt.show()

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
    plot_heatmap()