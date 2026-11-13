#!/bin/bash
# v3 renders, one at a time. Usage: render_v2.sh preview|final shot1 shot2 ...
cd /home/user/Illumaesthetic-Video-Editor
mode=$1; shift
for n in "$@"; do
  s=$(python projects/subaru-wrx-vb/tools/shots_v3.py $mode $n)
  echo "$(date +%T) start $mode $n"; blender -b -P projects/subaru-wrx-vb/tools/shot.py -- $s > /home/user/media/work/wrx/renders/${mode}_$n.log 2>&1; echo "$(date +%T) done $mode $n $?"
done
