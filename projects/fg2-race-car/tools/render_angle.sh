#!/bin/bash
# render_angle.sh NAME  -> scan (silver + lip) and CGI (Ecky's blend, + wing if IVE_EXTRA_STL) stills at photo res
set -e
N=$1; W=/home/user/media/work/fg2/match; L=/home/user/media/work/fg2/layers
cd /home/user/Illumaesthetic-Video-Editor
python -m ive render -- --scene /home/user/media/work/fg2/scan/fg2_lq.blend --explode "/home/user/media/work/fg2/scan/lip.blend:0,0,0" \
  --camera $W/cam_${N}_${CAM:-final}.json --out $L/${N}_scan${SUF}.png --look silver --samples ${SPP_SCAN:-32} 2>&1 | grep -E "IVE|Error" || true
blender -b "/home/user/media/fg2/cgi/FG2 Race Lip.blend" -P projects/fg2-race-car/tools/cgi_render.py -- $W/cam_${N}_${CAM:-final}.json $L/${N}_cgi${SUF}.png 1.0 ${SPP_CGI:-48} 2>&1 | grep -E "IVE_CGI|Error" || true
echo DONE $N
