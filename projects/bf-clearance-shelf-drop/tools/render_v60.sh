#!/bin/bash
# Final 60 fps queue: every frame, time remapped x2 (--fps60). One Blender job at a time.
# Same resolution as the approved v0.7: s1 0.4, carbon shots 0.6.
T=/home/user/Illumaesthetic-Video-Editor/projects/bf-clearance-shelf-drop/tools/shots_v0.py
O=/home/user/media/bf-clearance-shelf-drop/renders_v60
for s in ${SHOTS:-s1 s2 s3 s4 s5}; do
  r=0.6; [ $s = s1 ] && r=0.4
  mkdir -p $O/$s
  echo "start $s $(date +%T)"
  blender -b --factory-startup -P $T -- --shot $s --out $O/$s --res $r --fps60 ${FRAMES:+--frames $FRAMES} > $O/$s.log 2>&1
  echo "done $s $(date +%T) frames=$(ls $O/$s/*.png | wc -l)"
done
echo ALLDONE
