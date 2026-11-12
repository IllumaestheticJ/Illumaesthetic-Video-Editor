#!/bin/bash
# Render shot JSONs one at a time (serialise heavy jobs - lessons). Usage: render_queue.sh s1_side s2_front34 ...
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  echo "START $s $(date +%T)"
  blender -b -P projects/toyota-mr2-spyder/tools/shot3.py -- /home/user/media/work/mr2/shots/$s.json 2>&1 | grep -E "IVE_SHOT_DONE|Error|Traceback|Killed"
  echo "END $s $(date +%T) frames=$(ls /home/user/media/work/renders/mr2/$s 2>/dev/null | wc -l)"
done
echo QUEUE_DONE
