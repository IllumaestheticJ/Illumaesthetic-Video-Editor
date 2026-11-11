#!/bin/bash
# Final renders, one at a time (75 % res, 12 spp, 15 fps). Usage: render_all.sh [shot ...]
cd "$(dirname "$0")/../../.."
for s in $(python projects/lexus-is300/tools/shots.py final "$@"); do
  n=$(basename "$s" _final.json); t0=$(date +%s)
  blender -b -P projects/lexus-is300/tools/shot.py -- "$s" > /home/user/media/work/is300/renders/$n.log 2>&1
  echo "$n exit=$? $(( $(date +%s) - t0 ))s frames=$(ls /home/user/media/work/is300/renders/final/$n | wc -l)"
done
echo ALL_DONE
