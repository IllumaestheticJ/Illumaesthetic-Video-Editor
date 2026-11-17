#!/bin/bash
# render_v02.sh : v0.2 shots (GLB studio highlight instead of scan, canards), one Blender at a time; cards reused from v0
cd /home/user/Illumaesthetic-Video-Editor
R=/home/user/media/bf-gr-corolla-track/renders_v03
for s in s2_push s3_hl s4_lip s5_liphl s9_canards s1_hook s7_side s10_pass; do
  echo "$(date +%T) start $s"
  blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- $s $R/$s ${PCT:-50} ${SPP:-12} > /home/user/media/bf-gr-corolla-track/log/r3_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png 2>/dev/null | wc -l) frames"
done
echo ALL_DONE_V03
