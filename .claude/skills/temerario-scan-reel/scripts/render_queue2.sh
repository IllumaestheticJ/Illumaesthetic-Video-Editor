#!/bin/bash
# Resumable final-render queue (one Blender at a time): skips shots whose frame count is complete.
#   tools/render_queue2.sh v4_exh v4_front ...
S=/home/user/media/work/revuelto/shots; R=/home/user/media/work/renders/revuelto
for n in "$@"; do
  N=$(python -c "import json;d=json.load(open('$S/$n.json'));print(round(d['seconds']*d['fps']))")
  have=$(ls $R/$n 2>/dev/null | wc -l)
  if [ "$have" -ge "$N" ]; then echo "SKIP $n ($have/$N)"; continue; fi
  echo "START $n $(date +%T) need $N"; rm -rf $R/$n
  blender -b -P $(dirname $0)/shot.py -- $S/$n.json 2>&1 | grep -E --line-buffered "IVE_SHOT|Error|Killed"
  echo "END $n $(date +%T) frames=$(ls $R/$n | wc -l)"
done
echo QUEUE_DONE
