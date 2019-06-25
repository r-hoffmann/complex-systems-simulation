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

            river_smooth = self.data['river_timeline'][t]
            
            # make a color map of fixed colors
            cmap_terrain = mpl.cm.autumn_r
            norm_terrain = mpl.colors.Normalize(vmin=0, vmax=.03)
            
            cmap_peat = mpl.cm.Greens
            norm_peat = mpl.colors.Normalize(vmin=peat_heights.min(), vmax=peat_heights.max())

            cmap_water = mpl.cm.Blues
            norm_water = mpl.colors.Normalize(vmin=0, vmax=.01)
                                                
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(figsize=(16, 3), ncols=4)

            ax1.set_title('Concentration of nutrients')
            pos1 = ax1.imshow(concentration_of_nutrients, interpolation='nearest', cmap=cmap_terrain, norm=norm_terrain)
            fig.colorbar(pos1, ax=ax1)
            
            ax2.set_title('timestep {}\nHeight of peat'.format(t))
            pos2 = ax2.imshow(peat_heights, interpolation='nearest', cmap=cmap_peat, norm=norm_peat)
            fig.colorbar(pos2, ax=ax2)
            
            ax3.set_title('Height of water')
            pos3 = ax3.imshow(water_heights, interpolation='nearest', cmap=cmap_water, norm=norm_water)
            fig.colorbar(pos3, ax=ax3)

            ax4.set_title('smooth river')
            ax4.bar(np.arange(len(river_smooth)),river_smooth, align='edge',facecolor='steelblue', edgecolor='steelblue')

            if self.save_to_filesystem:
                plt.savefig('images/{:05}.png'.format(t))
            if self.show:
                plt.show()
            plt.close()

    def plot_all_heights_with_measures(self):
        for t, timestep in enumerate(self.data['terrain_timeline']):
            concentration_of_nutrients = []
            peat_heights = []
            water_heights = []

            measure_ratio_water_land_timeline = self.data['measure_ratio_water_land_timeline'][:t]
            measure_settlement_efficiency_timeline = self.data['measure_settlement_efficiency_timeline'][:t]
            peat_timeline = self.data['peat_timeline'][:t]

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

            river_smooth = self.data['river_timeline'][t]
            
            # make a color map of fixed colors
            cmap_terrain = mpl.cm.autumn_r
            norm_terrain = mpl.colors.Normalize(vmin=0, vmax=.03)
            
            cmap_peat = mpl.cm.Greens
            norm_peat = mpl.colors.Normalize(vmin=peat_heights.min(), vmax=peat_heights.max())

            cmap_water = mpl.cm.Blues
            norm_water = mpl.colors.Normalize(vmin=0, vmax=.01)
                                                
            fig, ax = plt.subplots(figsize=(12, 6), ncols=3, nrows=2)

            ax[0, 0].set_title('Concentration of nutrients')
            pos1 = ax[0, 0].imshow(concentration_of_nutrients, interpolation='nearest', cmap=cmap_terrain, norm=norm_terrain)
            fig.colorbar(pos1, ax=ax[0, 0])
            
            ax[0, 1].set_title('timestep {}\nHeight of peat'.format(t))
            pos2 = ax[0, 1].imshow(peat_heights, interpolation='nearest', cmap=cmap_peat, norm=norm_peat)
            fig.colorbar(pos2, ax=ax[0, 1])
            
            ax[0, 2].set_title('Height of water')
            pos3 = ax[0, 2].imshow(water_heights, interpolation='nearest', cmap=cmap_water, norm=norm_water)
            fig.colorbar(pos3, ax=ax[0, 2])

            ax[1, 0].set_title('Ratio between water and land', y=-0.01)
            pos1 = ax[1, 0].plot(measure_ratio_water_land_timeline)
            
            ax[1, 1].set_title('Settlement efficiency', y=-0.01)
            pos2 = ax[1, 1].plot(measure_settlement_efficiency_timeline)
            
            ax[1, 2].set_title('Total peat', y=-0.01)
            pos3 = ax[1, 2].plot(peat_timeline)

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
                water_heights_line.append(cell['water'])

            terrain_heights.append(terrain_heights_line)
            peat_heights.append(peat_heights_line)
            water_heights.append(water_heights_line)

        terrain_heights = np.array(terrain_heights)
        peat_heights = np.array(peat_heights)
        water_heights = np.array(water_heights)

        hard_terrain_heights = terrain_heights + peat_heights

        all_terrain = np.zeros((100, 100))
        print(all_terrain.shape)
        for x, row in enumerate(water_heights):
            for y, water in enumerate(row):
                if water > 0:
                    all_terrain[x][y] = water + hard_terrain_heights[x][y]
                else:
                    all_terrain[x][y] = hard_terrain_heights[x][y] - 0.5
        
        print(all_terrain.shape)

                
            

        # make a color map of fixed colors
        cmap_terrain = mpl.cm.autumn_r
        norm_terrain = mpl.colors.Normalize(vmin=terrain_heights.min(), vmax=terrain_heights.max())
        
        # cmap_peat = mpl.cm.Greens
        # norm_peat = mpl.colors.Normalize(vmin=peat_heights.min(), vmax=peat_heights.max())

        # cmap_water = mpl.cm.Blues
        # norm_water = mpl.colors.Normalize(vmin=0, vmax=.5)


        # fig3D, (ax1, ax2, ax3) = plt.subplots(figsize=(12, 3), ncols=3)

        cmap_terrain = mpl.cm.Greens_r
        norm_terrain = mpl.colors.Normalize(vmin=hard_terrain_heights.min(), vmax=hard_terrain_heights.max())
        
        cmap_water_all_terrain = mpl.cm.Blues
        norm_water_all_terrain = mpl.colors.Normalize(vmin=0, vmax=5)

        X = np.arange(0,100)
        Y = np.arange(0,100)
        Z = hard_terrain_heights
        Z_water = all_terrain

        fig3D = plt.figure()
        ax1 = Axes3D(fig3D)
        ax1.view_init(elev=10, azim=110)
        ax1.contour3D(X, Y, Z, 1000, cmap=cmap_terrain)
        ax1.contour3D(X, Y, Z_water, 1000, c=water_heights, cmap=cmap_water_all_terrain, norm=norm_water_all_terrain)



        # print(X.shape, Y.shape, Z.shape)
        # ax1.scatter(xs=X, ys=Y, zs=Z_water)

        ax1.set_title('3D Terrain Visualization')
        ax1.grid(False)
        ax1.set_zlim3d(0, 50)

        # ax2 = plt.axes(projection='3d')
        # ax2.contour3D(np.arange(0,100), np.arange(0,100), peat_heights, 50, cmap=cmap_peat)
        # ax2.set_title('peat')

        # ax3 = plt.axes(projection='3d')
        # ax3.contour3D(np.arange(0,100), np.arange(0,100), terrain_heights, 50, cmap=cmap_terrain)
        # ax3.set_title('terrain')


        # plt.show()
        # fig, (ax1, ax2, ax3) = plt.subplots(figsize=(12, 3), ncols=3)

        # ax1.set_title('Height of terrain')
        # pos1 = ax1.imshow(terrain_heights, interpolation='nearest', cmap=cmap_terrain, norm=norm_terrain)
        # fig.colorbar(pos1, ax=ax1)
        
        # ax2.set_title('Height of peat')
        # pos2 = ax2.imshow(peat_heights, interpolation='nearest', cmap=cmap_peat, norm=norm_peat)
        # fig.colorbar(pos2, ax=ax2)
        
        # ax3.set_title('Height of water')
        # pos3 = ax3.imshow(water_heights, interpolation='nearest', cmap=cmap_water, norm=norm_water)
        # fig.colorbar(pos3, ax=ax3)

        if self.save_to_filesystem:
            plt.savefig('images/{:05}.png'.format(t))
        plt.show()