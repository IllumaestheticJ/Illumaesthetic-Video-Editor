#!/bin/bash
# Final renders, one at a time (lessons: serialise heavy jobs). Usage: render_queue.sh shot1 shot2 ...
cd /home/user/Illumaesthetic-Video-Editor
for n in "$@"; do
  s=$(python projects/subaru-wrx-vb/tools/shots.py final $n)
  echo "$(date +%T) start $n"; blender -b -P projects/subaru-wrx-vb/tools/shot.py -- $s > /home/user/media/work/wrx/renders/$n.log 2>&1; echo "$(date +%T) done $n $?"
done
