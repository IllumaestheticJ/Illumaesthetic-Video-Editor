#!/bin/bash
# render_v10_end.sh : v1.0 ending (user): car drives down the track, 3D logo rises from the horizon, URL slides in
cd /home/user/Illumaesthetic-Video-Editor
L=/home/user/media/bf-gr-corolla-track/log
until grep -q ALL_DONE_V10 $L/render_v10.log; do sleep 30; done
R=/home/user/media/bf-gr-corolla-track/renders_v10
echo "$(date +%T) start s10_end" >> $L/render_v10.log
blender -b -P projects/bf-gr-corolla-track/tools/shot.py -- s10_end $R/s10_end ${PCT:-50} ${SPP:-12} > $L/r10_s10_end.log 2>&1
echo "$(date +%T) done s10_end $(ls $R/s10_end/f_*.png | wc -l) frames" >> $L/render_v10.log
echo ALL_DONE_END >> $L/render_v10.log
