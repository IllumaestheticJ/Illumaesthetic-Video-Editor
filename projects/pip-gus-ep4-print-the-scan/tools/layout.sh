#!/bin/bash
# Low-res layout pass: render the given frames (default: 3 per shot - start, middle, end) at SCALE (0.3) / SPP (2) into
# MEDIA/look_layout, then a labelled contact sheet. Usage: tools/layout.sh [frames,...]
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; M=/home/user/media/pip-gus-ep4-print-the-scan; O=$M/look_layout
TLJ="$HERE/../ep4_timeline.json"
FR=${1:-$(python3 -c "
import json;t=json.load(open('$TLJ'))
print(','.join(str(x) for s in t['shots'] for x in (s['f0']+3,(s['f0']+s['f1'])//2,s['f1']-3)))")}
rm -rf "$O"; mkdir -p "$O"
cd "$HERE/../../scan-tedium-explainer-reel/tools"
blender -b --factory-startup -P partA_scene.py -- --exec "$HERE/ep4_anim.py" --out "$O" --timeline "$TLJ" \
  --frames "$FR" --scale ${SCALE:-0.3} --spp ${SPP:-2} 2>&1 | grep "\[ep4\]" | tail -3
python3 - "$O" <<'PY'
import sys,glob,os
from PIL import Image,ImageDraw
o=sys.argv[1];fs=sorted(glob.glob(o+'/E*/*.png'),key=lambda f:int(os.path.basename(f)[:4]))
ims=[Image.open(f) for f in fs];w,h=ims[0].size;n=9;rows=(len(ims)+n-1)//n
S=Image.new('RGB',(w*n,(h+18)*rows),'white');d=ImageDraw.Draw(S)
for i,(f,im) in enumerate(zip(fs,ims)):
    x,y=(i%n)*w,(i//n)*(h+18);S.paste(im,(x,y+18));d.text((x+3,y+3),os.path.basename(os.path.dirname(f))+' '+os.path.basename(f)[:4],fill='black')
S.save(o+'/sheet.jpg',quality=85);print(o+'/sheet.jpg',len(ims))
PY
