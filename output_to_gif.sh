if [ $# -eq 0 ]
  then
    echo "Please supply experiment parameter"
    exit 1
fi
python3 visualization.py $1
ffmpeg -i images/%05d_2$1.png -vf palettegen -y images/palette$1.png
ffmpeg -framerate 100 -i images/%05d_2$1.png -i images/palette$1.png -lavfi "paletteuse,setpts=6*PTS" -y images/animated_$1.gif 