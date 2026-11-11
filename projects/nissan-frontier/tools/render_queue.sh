#!/bin/bash
# Final renders, one Blender at a time (75 % res, 12 spp, 15 fps; assemble interpolates to 30).
#   render_queue.sh s1_front34 s2_rear34 ...
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  t0=$(date +%s)
  blender -b -P projects/nissan-frontier/tools/shot.py -- $(python projects/nissan-frontier/tools/${SHOTS:-shots}.py final $s) > /home/user/media/nissan-frontier/chk/final_$s.log 2>&1
  echo "$s done rc=$? $(( $(date +%s)-t0 ))s frames=$(ls /home/user/media/work/frontier/renders/final/$s | wc -l)"
done
echo QUEUEDONE
