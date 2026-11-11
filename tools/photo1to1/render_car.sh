#!/bin/bash
# render_car.sh CAR : canvas plans + scan(+kit) and CGI renders for angles A,B,C, then the zoom-out layers
set -e
C=$1; T=/home/user/Illumaesthetic-Video-Editor/tools/photo1to1; D=/home/user/media/cars/$C; mkdir -p $D/layers
cd /home/user/Illumaesthetic-Video-Editor
for a in A B C; do
  python $T/canvas.py $C $a
  [ -f $D/layers/${a}_scan_canvas.png ] || python -m ive render -- --scene $D/scan/scan.blend --explode "$D/scan/parts.blend:0,0,0" \
     --camera $D/match/cam_${a}_canvas.json --out $D/layers/${a}_scan_canvas.png --look silver --samples ${SPP_SCAN:-32} 2>&1 | grep -E "IVE_RENDER|Error" || true
  [ -f $D/layers/${a}_cgi_canvas.png ] || blender -b "/home/user/media/fg2/cgi/FG2 Race Lip.blend" -P $T/cgi_render.py -- $C $D/match/cam_${a}_canvas.json $D/layers/${a}_cgi_canvas.png 1.0 ${SPP_CGI:-40} 2>&1 | grep -E "IVE_CGI|Error" || true
done
python $T/kb_zoomout.py $C A Az 4.9 && python $T/kb_zoomout.py $C B Bz 4.9 && python $T/kb_zoomout.py $C C Cz 4.9
echo RENDERED $C
