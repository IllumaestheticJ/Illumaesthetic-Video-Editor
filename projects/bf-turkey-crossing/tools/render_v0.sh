#!/bin/bash
# render_v0.sh : all 3D shots of BF10 turkey-crossing v0, one at a time (Cycles CPU, preview quality 50 %)
cd /home/user/Illumaesthetic-Video-Editor
R=${RDIR:-/home/user/media/bf-turkey-crossing/renders_v0}; L=/home/user/media/bf-turkey-crossing/log; mkdir -p $R $L
for s in ${SHOTS:-s1_cross s2_look s3_car s4_eyes s5_poof s6_feath}; do
  echo "$(date +%T) start $s"
  blender -b -P projects/bf-turkey-crossing/tools/scene.py -- $s $R/$s ${PCT:-50} ${SPP:-10} > $L/r0_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png 2>/dev/null | wc -l) frames"
done
echo ALL_DONE_V0
