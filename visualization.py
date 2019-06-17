
    for timestep in data['terrain_timeline']:
        total_heights = []
        for row in timestep[0:2]:
            for cell in row:
                total_heights.append(cell['height_of_water'] + cell['height_of_terrain'] + cell['peat_bog_thickness'])
        plt.hist(total_heights, density=True)
        print(min(total_heights), max(total_heights))
        plt.show()

if __name__ == "__main__":
    plot_hist_total()
with open('output_100x100_smallPool.json') as json_file:  
    data = json.load(json_file)
    for timestep in data['terrain_timeline']:
        fig = plt.figure()
        water_height = []
        for row in timestep:
            line = []
            for cell in row:
                if(cell['height_of_water'] > 0 ):
                    line.append(-1*cell['height_of_water'])
                else:
                    line.append(cell['height_of_terrain'])
                # line.append(cell['height_of_water'])
            water_height.append(line)
        water_height = np.array(water_height)
        # make a color map of fixed colors
        cmap = mpl.colors.ListedColormap(['#023858', '#045a8d', '#3690c0', '#fff7ec','#fee8c8','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#b30000','#7f0000'])
        bounds=[-6, -4,-2, 0, 2, 4, 6,8,10,12,14,16]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        # tell imshow about color map so that only set colors are used
        img = plt.imshow(water_height,interpolation='nearest', cmap = cmap,norm=norm)

        # make a color bar
        plt.colorbar(img,cmap=cmap, norm=norm,boundaries=bounds,ticks=[-4,-2, 0, 2, 4, 6,8,10,12,14,16])

        plt.show()

def plot_hist_water():
    data = load_data()
    for timestep in data['terrain_timeline']:
        total_heights = []
        for row in timestep[0:2]:
            for cell in row:
                total_heights.append(cell['height_of_water'] + cell['height_of_terrain'] + cell['peat_bog_thickness'])
        plt.hist(total_heights, density=True)
        print(min(total_heights), max(total_heights))
        plt.show()

if __name__ == "__main__":
    plot_hist_total()