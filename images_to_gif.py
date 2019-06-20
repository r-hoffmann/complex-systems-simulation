import imageio
import os

filenames = os.listdir('./images/')
print(filenames)
with imageio.get_writer('./images/Animation.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread('./images/'+filename)
        writer.append_data(image)