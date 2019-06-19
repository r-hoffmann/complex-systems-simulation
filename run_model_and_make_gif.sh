python3 main.py
rm images/*
python3 visualization.py
convert -delay 10 -loop 0 $(ls images/*.png | sort -V) images/animated.gif