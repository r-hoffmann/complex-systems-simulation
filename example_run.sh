cp ./example/configuration_*.json ./
python3 main.py example
python3 main.py examplesettlement
python3 visualization.py examplesettlement
ffmpeg -i images/%05d_2examplesettlement.png -vf palettegen -y images/paletteexamplesettlement.png
ffmpeg -framerate 100 -i images/%05d_2examplesettlement.png -i images/paletteexamplesettlement.png -lavfi "paletteuse,setpts=6*PTS" -y images/animated_examplesettlement.gif 