#!/bin/bash
# Render final shots one at a time (Blender, Cycles CPU, 75 % res, 12 spp, 15 fps). Usage: MODE=final3 render_queue.sh shot [shot ...]
# MODE=final (v2 whole-car s*, renders/final2) | final3 (v2 brief m*, renders/final3). Persistent data is off for shots with moving parts.
cd "$(dirname "$0")/../../.."
MODE=${MODE:-final3}; OUTD=$([ "$MODE" = final3 ] && echo final3 || echo final2)
for n in "$@"; do
  spec=$(python projects/mazda-3-gen4/tools/shots.py "$MODE" "$n")
  echo "$(date +%T) start $n"
  blender -b -P projects/mazda-3-gen4/tools/shot.py -- "$spec" > /home/user/media/work/m3/renders/log_$n.txt 2>&1 || echo "FAIL $n"
  echo "$(date +%T) done $n $(ls /home/user/media/work/m3/renders/$OUTD/$n | wc -l) frames"
done
echo ALLDONE
