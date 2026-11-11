#!/bin/bash
# Render shot specs one at a time (never two Blender jobs at once - lessons: contention makes renders 6x slower).
#   render_queue.sh spec1.json spec2.json ...
cd /home/user/Illumaesthetic-Video-Editor
for s in "$@"; do
  t0=$(date +%s)
  /usr/local/bin/blender -b -P projects/toyota-sera/tools/shot.py -- "$s" 2>&1 | grep -E "IVE_RENDER_DONE|Error|rror" | tail -3
  echo "$(basename $s) $(( $(date +%s) - t0 )) s"
done
echo QUEUE_DONE
