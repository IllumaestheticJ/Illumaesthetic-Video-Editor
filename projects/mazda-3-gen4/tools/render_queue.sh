#!/bin/bash
# Render final shots one at a time (Blender, Cycles CPU, 75 % res, 12 spp, 15 fps). Usage: render_queue.sh shot [shot ...]
cd "$(dirname "$0")/../../.."
for n in "$@"; do
  spec=$(python projects/mazda-3-gen4/tools/shots.py final "$n")
  echo "$(date +%T) start $n"
  blender -b -P projects/ferrari-296/tools/shot.py -- "$spec" > /home/user/media/work/m3/renders/log_$n.txt 2>&1 || echo "FAIL $n"
  echo "$(date +%T) done $n $(ls /home/user/media/work/m3/renders/final2/$n | wc -l) frames"
done
