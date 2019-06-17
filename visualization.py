import json
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns

x = np.arange(0, 10, 1)
y = np.arange(0, 10, 1)

print(x)
xx, yy = np.meshgrid(x, y, sparse=True)
# z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)


with open('output.json') as json_file:  
    data = json.load(json_file)
    for timestep in data['terrain_timeline'][0:3]:
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
        print(xx)

        # plt.pcolor(zz)
        # plt.colorbar()

        plt.imshow(zz, cmap='RdBu')
        plt.show()

# figs = list(map(plt.figure, plt.get_fignums()))
# print(figs)

