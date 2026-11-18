#!/bin/bash
# render_v09.sh : v0.9 re-renders every shot showing the V2 rear spats (seated, spat_v2_fit.json); others link to v08
cd /home/user/Illumaesthetic-Video-Editor
R=/home/user/media/bf-gr-corolla-track/renders_v09
for s in s7_side s10_pass s6_cardv2 s12_open s3_hl; do
  echo "$(date +%T) start $s"
  blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- $s $R/$s ${PCT:-50} ${SPP:-12} > /home/user/media/bf-gr-corolla-track/log/r9_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png 2>/dev/null | wc -l) frames"
done
echo ALL_DONE_V09
