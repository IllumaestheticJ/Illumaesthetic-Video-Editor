#!/bin/bash
# render_v11.sh : v1.1 (user) - canard shot on the red car on track; end scene + "SHOP DEALS NOW" rising out of the road
cd /home/user/Illumaesthetic-Video-Editor
R=/home/user/media/bf-gr-corolla-track/renders_v11; L=/home/user/media/bf-gr-corolla-track/log
for s in s9_canards s10_end; do
  echo "$(date +%T) start $s"
  blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- $s $R/$s ${PCT:-50} ${SPP:-12} > $L/r11_$s.log 2>&1
  echo "$(date +%T) done $s $(ls $R/$s/f_*.png 2>/dev/null | wc -l) frames"
done
echo ALL_DONE_V11
