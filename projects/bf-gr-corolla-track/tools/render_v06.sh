#!/bin/bash
# render_v06.sh : v0.6 re-renders (pairs on the cards, 8-kick cards, 6-kick side + front canard shots); others link to v03/v05
cd /home/user/Illumaesthetic-Video-Editor
R=/home/user/media/bf-gr-corolla-track/renders_v06
for s in s6_cardv2 s8_cardv1 s9_canards s7_side; do
  echo "$(date +%T) start $s"
  blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- $s $R/$s ${PCT:-50} ${SPP:-12} > /home/user/media/bf-gr-corolla-track/log/r6_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png 2>/dev/null | wc -l) frames"
done
echo ALL_DONE_V06
