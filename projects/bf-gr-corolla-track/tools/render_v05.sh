#!/bin/bash
# render_v05.sh : v0.5 re-renders only (higher lip camera s4/s5, product line-up cards s6/s8); other shots link to renders_v03
cd /home/user/Illumaesthetic-Video-Editor
R=/home/user/media/bf-gr-corolla-track/renders_v05
for s in s6_cardv2 s8_cardv1 s4_lip s5_liphl; do
  echo "$(date +%T) start $s"
  blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- $s $R/$s ${PCT:-50} ${SPP:-12} > /home/user/media/bf-gr-corolla-track/log/r5_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png 2>/dev/null | wc -l) frames"
done
echo ALL_DONE_V05
