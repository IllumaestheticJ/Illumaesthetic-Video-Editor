#!/bin/bash
# Final renders, one at a time (75 %, 12 spp, 15 fps). usage: render_queue.sh s1_front34 s2_rear34 ...
cd "$(dirname "$0")/../../.."
for n in "$@"; do
  s=$(python projects/lexus-is350/tools/shots.py final $n)
  echo "== $n $(date +%T)"
  blender -b -P projects/lexus-is350/tools/shot.py -- $s 2>&1 | grep -E "IVE_RENDER_DONE|Error|Traceback|Killed"
  echo "-- $n done $(date +%T) frames: $(ls /home/user/media/lexus-is350/renders/final/$n | wc -l)"
done
echo QUEUE_DONE
