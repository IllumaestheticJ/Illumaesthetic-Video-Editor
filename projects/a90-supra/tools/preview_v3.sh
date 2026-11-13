#!/bin/bash
# fast Workbench previews (first / mid / last + extra fractions) of v3 shots -> /home/user/media/work/a90/prev3/<shot>_<tag>.jpg
D=$(cd "$(dirname "$0")/.." && pwd); W=/home/user/media/work/a90; T=$(date +%H%M%S)
for s in "$@"; do
  flock $W/blender.lock blender -b -P $D/tools/shots3.py -- --shot $D/shots_v3/$s.json --out $W/prev3/${s} --res-pct 40 --preview --stills ${FR:-0,0.25,0.5,0.75,1} 2>&1 | grep -E "Error|Traceback" | grep -v EGL
  ffmpeg -loglevel error -y $(for f in $(echo ${FR:-0,0.25,0.5,0.75,1} | tr , ' '); do printf -- "-i $W/prev3/${s}_%.2f.png " $f; done) -filter_complex hstack=inputs=$(echo ${FR:-0,0.25,0.5,0.75,1} | tr , '\n' | wc -l) $W/prev3/${s}_$T.jpg && echo $W/prev3/${s}_$T.jpg
done
