#!/bin/bash
# render_v10.sh : v1.0 slow-reader timing - every text section re-rendered over its longer window
cd /home/user/Illumaesthetic-Video-Editor
R=/home/user/media/bf-gr-corolla-track/renders_v10
for s in s6_cardv2 s8_cardv1 s7_side s9_canards s3_hl s4_lip s5_liphl; do
  echo "$(date +%T) start $s"
  blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- $s $R/$s ${PCT:-50} ${SPP:-12} > /home/user/media/bf-gr-corolla-track/log/r10_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png 2>/dev/null | wc -l) frames"
done
echo ALL_DONE_V10
