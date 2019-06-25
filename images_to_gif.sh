ffmpeg -i images/%05d.png -vf palettegen -y images/palette.png
ffmpeg -framerate 100 -i images/%05d.png -i images/palette.png -lavfi "paletteuse,setpts=6*PTS" -y images/animated.gif 