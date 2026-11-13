#!/bin/bash
# Framing/clipping check at 30 % res: 6 evenly spaced frames of each shot tiled into one sheet (parts must stay in frame).
#   tools/preview5.sh v4_front v4_rear ...   -> /home/user/media/work/revuelto/preview/<shot>.png
S=/home/user/media/work/revuelto/shots; P=/home/user/media/work/revuelto/preview; mkdir -p $P
for n in "$@"; do
  F=$(python -c "import json;d=json.load(open('$S/$n.json'));N=max(1,round(d['seconds']*d['fps']));print(','.join(str(round(1+(N-1)*i/5)) for i in range(6)))")
  rm -rf $P/$n; blender -b -P $(dirname $0)/shot.py -- $S/$n.json --res-pct 30 --samples 6 --frames $F --out $P/$n 2>&1 | grep -E "Error|Traceback" || true
  ffmpeg -loglevel error -y -pattern_type glob -i "$P/$n/f_*.png" -vf "tile=6x1" $P/$n.$(date +%H%M%S).png; echo "PREVIEW $n"
done
echo PREVIEW_DONE
