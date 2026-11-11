#!/bin/bash
# Final renders, one Blender job at a time (75 % res, 12 spp, 15 fps; assemble interpolates to 30).
#   tools/render_queue.sh s1_side s2_front34 ...
S=/home/user/media/work/revuelto/shots
for n in "$@"; do
  echo "START $n $(date +%T)"
  blender -b -P $(dirname $0)/shot.py -- $S/$n.json 2>&1 | grep -E --line-buffered "IVE_SHOT|Error|Killed" 
  echo "END $n $(date +%T) frames=$(ls /home/user/media/work/renders/revuelto/$n | wc -l)"
done
echo QUEUE_DONE
