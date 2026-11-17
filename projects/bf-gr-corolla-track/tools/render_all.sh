#!/bin/bash
# render_all.sh : every 3D shot, one Blender process at a time (preview quality for v0: 50 % res, 12 spp)
cd /home/user/Illumaesthetic-Video-Editor
R=/home/user/media/bf-gr-corolla-track/renders_v0
for s in s2_push s3_scan s4_lip s5_lipscan s1_hook s6_cardv2 s8_cardv1 s7_side s9_pass; do
  n=$(ls $R/$s/f_*.png 2>/dev/null | wc -l)
  echo "$(date +%T) start $s (have $n)"
  blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- $s $R/$s ${PCT:-50} ${SPP:-12} > /home/user/media/bf-gr-corolla-track/log/r_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png | wc -l) frames"
done
echo ALL_DONE
