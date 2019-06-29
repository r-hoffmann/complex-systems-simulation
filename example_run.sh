cp ./example/configuration_example.json ./configuration_example.json
python3 main.py example
python3 visualization.py example
ffmpeg -i images/%05d_2example.png -vf palettegen -y images/paletteexample.png
ffmpeg -framerate 100 -i images/%05d_2example.png -i images/paletteexample.png -lavfi "paletteuse,setpts=6*PTS" -y images/animated_example.gif 