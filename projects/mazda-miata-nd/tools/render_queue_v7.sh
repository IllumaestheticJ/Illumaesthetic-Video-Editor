#!/bin/bash
# v3 finals, one at a time; then a per-frame luma scan. render_queue_v3.sh shot ...
cd /home/user/Illumaesthetic-Video-Editor
W=/home/user/media/work/miata
for n in "$@"; do
  s=$(python projects/mazda-miata-nd/tools/shots_v7.py final $n)
  [ "$n" != v3_x_home_clean ] && rm -rf $W/renders_v7/final/$n
  echo "$n start $(date +%T)"
  /usr/local/bin/blender -b -P projects/mazda-miata-nd/tools/shot.py -- $s > $W/renders_v7/$n.log 2>&1
  echo "$n done $(date +%T)"
done
echo QUEUE_DONE
