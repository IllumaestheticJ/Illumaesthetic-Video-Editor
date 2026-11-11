#!/bin/bash
# Final renders, one Blender at a time (75 % res, 12 spp, 15 fps; assemble interpolates to 30).
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  sp=$(python projects/mazda-miata-na/tools/shots.py final $s)
  echo "$(date +%T) start $s"
  blender -b -P projects/mazda-miata-na/tools/shot.py -- $sp > /home/user/media/work/miata/renders/final_$s.log 2>&1
  echo "$(date +%T) done $s $(ls /home/user/media/work/miata/renders/final/$s | wc -l) frames"
done
