#!/bin/bash
# Render final shots one at a time (never in parallel): render_queue.sh s1_turntable s2_rear ...
cd /home/user/Illumaesthetic-Video-Editor
W=/home/user/media/work/miata
for n in "$@"; do
  s=$(python projects/mazda-miata-nd/tools/shots.py final $n)
  rm -rf $W/renders/final/$n
  echo "$n start $(date +%T)"
  /usr/local/bin/blender -b -P projects/mazda-miata-nd/tools/shot.py -- $s > $W/renders/$n.log 2>&1
  echo "$n done $(date +%T) frames $(ls $W/renders/final/$n | wc -l)"
done
echo QUEUE_DONE
