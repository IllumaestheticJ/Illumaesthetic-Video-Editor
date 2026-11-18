#!/bin/bash
# render_v08.sh : v0.8 re-renders (continuous opening s12, 10-kick cards, s9 re-timed); others link to v03/v05/v06
cd /home/user/Illumaesthetic-Video-Editor
R=/home/user/media/bf-gr-corolla-track/renders_v08
for s in s12_open s6_cardv2 s8_cardv1 s9_canards; do
  echo "$(date +%T) start $s"
  blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- $s $R/$s ${PCT:-50} ${SPP:-12} > /home/user/media/bf-gr-corolla-track/log/r8_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png 2>/dev/null | wc -l) frames"
done
echo ALL_DONE_V08
