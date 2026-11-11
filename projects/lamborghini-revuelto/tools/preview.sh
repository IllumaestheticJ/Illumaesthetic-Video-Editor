#!/bin/bash
# Framing check at 30 % res / 8 spp: first, middle and last frame of each shot, tiled into one sheet.
#   tools/preview.sh s1_side s2_front34 ...    -> /home/user/media/work/revuelto/preview/<shot>.png + sheet.png
set -e
S=/home/user/media/work/revuelto/shots; P=/home/user/media/work/revuelto/preview; mkdir -p $P
for n in "$@"; do
  N=$(python -c "import json;d=json.load(open('$S/$n.json'));print(max(1,round(d['seconds']*d['fps'])))")
  rm -rf $P/$n; blender -b -P $(dirname $0)/shot.py -- $S/$n.json --res-pct 30 --samples 8 --frames 1,$(( (N+1)/2 )),$N --out $P/$n 2>&1 | grep -E "Error|IVE_SHOT" || true
  ffmpeg -loglevel error -y -pattern_type glob -i "$P/$n/f_*.png" -vf "tile=3x1" $P/$n.png
done
ls $P/*.png
