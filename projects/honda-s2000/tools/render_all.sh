#!/bin/bash
# Render final scan shots one at a time (never in parallel - lessons: serialise heavy jobs). Usage: render_all.sh [shot ...]
cd "$(dirname "$0")/../../.."
for f in $(python projects/honda-s2000/tools/shots.py final "$@"); do
  n=$(basename $f _final.json); echo "$(date +%T) start $n"
  blender -b -P projects/honda-s2000/tools/shot.py -- $f > /home/user/media/work/s2k/renders/$n.log 2>&1
  echo "$(date +%T) done $n $(ls /home/user/media/work/s2k/renders/final/$n | wc -l) frames"
done
