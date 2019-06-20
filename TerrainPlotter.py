import json, math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

class TerrainPlotter(object):
    def __init__(self, filename='output.json', show=True, save_to_filesystem=False):
        self.filename = filename
        self.load_data()
        self.show = show
        self.save_to_filesystem = save_to_filesystem
    
    def load_data(self):
        with open(self.filename) as json_file:  
            self.data = json.load(json_file)

    def plot_heatmap(self):
        for t, timestep in enumerate(self.data['terrain_timeline']):
            fig = plt.figure()
            water_height = []
            for row in timestep:
                line = []
                for cell in row:
                    if cell['water'] > 0:
                        line.append(-1*cell['water'])
                    else:
                        line.append(cell['terrain']+cell['peat'])
                    # line.append(cell['water'])
                water_height.append(line)
                # print(line)
            water_height = np.array(water_height)
            # make a color map of fixed colors
            cmap = mpl.colors.ListedColormap(['#023858', '#045a8d', '#3690c0', '#fff7ec','#fee8c8','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#b30000','#7f0000'])
            bounds=[-6, -4,-2, 0, 2, 4, 6, 8, 10, 12, 14, 16]
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

            # tell imshow about color map so that only set colors are used
            img = plt.imshow(water_height,interpolation='nearest', cmap = cmap,norm=norm)

            # make a color bar
            plt.colorbar(img,cmap=cmap, norm=norm,boundaries=bounds,ticks=bounds)
            
            if self.save_to_filesystem:
                plt.savefig('images/{:05d}.png'.format(t))
            if self.show:
                plt.show()
            plt.close()

    def plot_hist_water(self):
        for timestep in self.data['terrain_timeline']:
            water_heights = []
            for row in timestep[0:2]:
                for cell in row:
                    water_heights.append(cell['water'])
            plt.hist(water_heights, density=True)
            print(min(water_heights), max(water_heights))
            if self.show:
                plt.show()

    def plot_all_heights(self):
        for t, timestep in enumerate(self.data['terrain_timeline']):
            concentration_of_nutrients = []
            peat_heights = []
            water_heights = []
            for row in timestep:
                concentration_of_nutrients_line = []
                peat_heights_line = []
                water_heights_line = []
                for cell in row:
                    water_heights_line.append(cell['water'])
                    concentration_of_nutrients_line.append(cell['nutrients'])
                    peat_heights_line.append(cell['peat'])

                concentration_of_nutrients.append(concentration_of_nutrients_line)
                peat_heights.append(peat_heights_line)
                water_heights.append(water_heights_line)

            concentration_of_nutrients = np.array(concentration_of_nutrients)
            peat_heights = np.array(peat_heights)
            water_heights = np.array(water_heights)

            # make a color map of fixed colors
            cmap_terrain = mpl.cm.autumn_r
            norm_terrain = mpl.colors.Normalize(vmin=0, vmax=.03)
            
            cmap_peat = mpl.cm.Greens
            norm_peat = mpl.colors.Normalize(vmin=peat_heights.min(), vmax=peat_heights.max())

            cmap_water = mpl.cm.Blues
            norm_water = mpl.colors.Normalize(vmin=0, vmax=.5)
                                                
            fig, (ax1, ax2, ax3) = plt.subplots(figsize=(12, 3), ncols=3)

            ax1.set_title('Concentration of nutrients')
            pos1 = ax1.imshow(concentration_of_nutrients, interpolation='nearest', cmap=cmap_terrain, norm=norm_terrain)
            fig.colorbar(pos1, ax=ax1)
            
            ax2.set_title('Height of peat')
            pos2 = ax2.imshow(peat_heights, interpolation='nearest', cmap=cmap_peat, norm=norm_peat)
            fig.colorbar(pos2, ax=ax2)
            
            ax3.set_title('Height of water')
            pos3 = ax3.imshow(water_heights, interpolation='nearest', cmap=cmap_water, norm=norm_water)
            fig.colorbar(pos3, ax=ax3)

            if self.save_to_filesystem:
                plt.savefig('images/{:05}.png'.format(t))
            if self.show:
                plt.show()
            plt.close()

    def plot_last_heights(self):
        timestep = self.data['terrain_timeline'][-1]
        t = len(self.data['terrain_timeline'])-1
        terrain_heights = []
        peat_heights = []
        water_heights = []
        for row in timestep:
            terrain_heights_line = []
            peat_heights_line = []
            water_heights_line = []
            for cell in row:
                terrain_heights_line.append(cell['terrain'])
                peat_heights_line.append(cell['peat'])
                # if cell['water'] > 0:
                #     water_heights_line.append(1)
                # else:
                #     water_heights_line.append(0)
                water_heights_line.append(cell['water'])

            terrain_heights.append(terrain_heights_line)
            peat_heights.append(peat_heights_line)
            water_heights.append(water_heights_line)

        terrain_heights = np.array(terrain_heights)
        peat_heights = np.array(peat_heights)
        water_heights = np.array(water_heights)

        # make a color map of fixed colors
        cmap_terrain = mpl.cm.autumn_r
        norm_terrain = mpl.colors.Normalize(vmin=terrain_heights.min(), vmax=terrain_heights.max())
        
        cmap_peat = mpl.cm.Greens
        norm_peat = mpl.colors.Normalize(vmin=peat_heights.min(), vmax=peat_heights.max())

        cmap_water = mpl.cm.Blues
        norm_water = mpl.colors.Normalize(vmin=0, vmax=.5)
                                            
        fig, (ax1, ax2, ax3) = plt.subplots(figsize=(12, 3), ncols=3)

        ax1.set_title('Height of terrain')
        pos1 = ax1.imshow(terrain_heights, interpolation='nearest', cmap=cmap_terrain, norm=norm_terrain)
        fig.colorbar(pos1, ax=ax1)
        
        ax2.set_title('Height of peat')
        pos2 = ax2.imshow(peat_heights, interpolation='nearest', cmap=cmap_peat, norm=norm_peat)
        fig.colorbar(pos2, ax=ax2)
        
        ax3.set_title('Height of water')
        pos3 = ax3.imshow(water_heights, interpolation='nearest', cmap=cmap_water, norm=norm_water)
        fig.colorbar(pos3, ax=ax3)

        if self.save_to_filesystem:
            plt.savefig('images/{:05}.png'.format(t))
        plt.show()