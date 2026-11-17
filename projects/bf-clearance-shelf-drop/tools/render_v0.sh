#!/bin/bash
# Background queue: one Blender job at a time, preview quality (40 % res, every 2nd frame).
T=/home/user/Illumaesthetic-Video-Editor/projects/bf-clearance-shelf-drop/tools/shots_v0.py
O=/home/user/media/bf-clearance-shelf-drop/renders_v0
for s in s1 s2 s3 s4 s5; do
  mkdir -p $O/$s
  echo "start $s $(date +%T)"
  blender -b --factory-startup -P $T -- --shot $s --out $O/$s --res 0.4 --step 2 > $O/$s.log 2>&1
  echo "done $s $(date +%T) frames=$(ls $O/$s | wc -l)"
done
echo ALLDONE
