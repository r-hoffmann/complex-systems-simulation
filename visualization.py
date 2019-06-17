
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
                # if(cell['height_of_water'] > 0 ):
                #     line.append(1)
                # else:
                #     line.append(0)
                line.append(cell['height_of_water'])
            water_height.append(line)
        water_height = np.array(water_height)
        # make a color map of fixed colors
        cmap = mpl.colors.ListedColormap(['green','cyan','blue','darkblue'])
        bounds=[-1,0.01,1,5,10]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        # tell imshow about color map so that only set colors are used
        img = plt.imshow(water_height,interpolation='nearest', cmap = cmap,norm=norm)
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