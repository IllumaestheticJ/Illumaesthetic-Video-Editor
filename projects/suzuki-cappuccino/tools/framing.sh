#!/bin/bash
# Framing check: first / middle / last frame of each shot at 30 % res, 8 spp -> one contact sheet per shot.
# usage: framing.sh [shot names...]   (default: all JSONs in /home/user/media/work/cappuccino/shots)
S=/home/user/media/work/cappuccino/shots; O=/home/user/media/work/cappuccino/framing; mkdir -p $O
cd "$(dirname "$0")"
names=${@:-$(ls $S | sed 's/.json//')}
for n in $names; do
  N=$(python -c "import json;d=json.load(open('$S/$n.json'));print(max(1,round(d['seconds']*d['fps'])))")
  blender -b -P shot.py -- $S/$n.json --res-pct 30 --samples 8 --frames 1,$(( (N+1)/2 )),$N --out $O/$n >/dev/null 2>&1
  python -c "
from PIL import Image; import glob
fs=sorted(glob.glob('$O/$n/f_*.png')); ims=[Image.open(f) for f in fs]
c=Image.new('RGB',(sum(i.width+6 for i in ims),ims[0].height)); x=0
for i in ims: c.paste(i,(x,0)); x+=i.width+6
c.save('$O/$n.jpg')"
  echo $n
done
