#!/bin/bash
# Final renders, one at a time (75 % res, 12 spp, 15 fps; assemble interpolates to 30). Resumable (skips done frames).
cd /home/user/Illumaesthetic-Video-Editor
for j in "$@"; do
  echo "START $j $(date +%T)"
  blender -b -P projects/c5-corvette/tools/shot.py -- /home/user/media/work/c5/shots/$j.json --res-pct 75 --samples 12 > /home/user/media/work/c5/$j.render.log 2>&1
  echo "DONE $j $(date +%T) frames=$(ls /home/user/media/work/renders/c5/$j | wc -l)"
done
echo ALLDONE
