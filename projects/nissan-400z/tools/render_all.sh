#!/bin/bash
# Final scan shots, one Blender job at a time (house rule): 1080x1920 @ 75 %, 12 spp, 15 fps (assemble interpolates to 30).
cd "$(dirname "$0")/../../.."
R=/home/user/media/work/z400/renders/final; mkdir -p $R
for s in ${@:-s1_front34 s2_rear34 s3_haunch s4_lamp s5_tail s6_hood s7_top s8_explode}; do
  t0=$(date +%s); rm -rf $R/$s
  blender -b -P projects/nissan-400z/tools/shot.py -- $(python projects/nissan-400z/tools/shots.py final $s) > $R/$s.log 2>&1
  echo "$s done in $(( $(date +%s) - t0 )) s, $(ls $R/$s | wc -l) frames"
done
echo RENDERS_DONE
