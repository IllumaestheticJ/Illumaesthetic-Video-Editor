#!/bin/bash
# 30 % / 8 spp framing check: first, middle(s), last frame of each shot -> /home/user/media/work/c5/framing/<shot>.png strip
S=/home/user/media/work/c5/shots; O=/home/user/media/work/c5/framing; mkdir -p $O
for j in "$@"; do
  n=$(python -c "import json;d=json.load(open('$S/$j.json'));print(round(d['seconds']*d['fps']))")
  fr="1,$((n/3)),$((2*n/3)),$n"
  blender -b -P projects/c5-corvette/tools/shot.py -- $S/$j.json --res-pct 30 --samples 8 --frames $fr --out $O/$j > $O/$j.log 2>&1
  ffmpeg -loglevel error -y $(for f in ${fr//,/ }; do printf -- "-i $O/$j/f_%04d.png " $f; done) -filter_complex "hstack=4" $O/$j.png
  echo "$j done"
done
