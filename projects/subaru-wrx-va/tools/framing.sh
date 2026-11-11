#!/bin/bash
# (copied from projects/a90-supra/tools/framing.sh, paths changed)
# Framing check: 30 % res stills at shot fractions, then one contact sheet per shot list.
# usage: framing.sh "s01_front34 s02_rear34 ..." [fractions]
D=$(cd "$(dirname "$0")/.." && pwd); F=/home/user/media/subaru-wrx-va/framing; mkdir -p $F
FR=${2:-0,0.5,1}
for s in $1; do
  blender -b -P $D/tools/shots.py -- --shot $D/shots/$s.json --out $F/$s --stills $FR --res-pct 30 --samples 8 >$F/$s.log 2>&1 || echo "FAIL $s"
done
python - "$1" "$FR" <<PY
import sys
from PIL import Image, ImageDraw
shots=sys.argv[1].split(); fr=[float(x) for x in sys.argv[2].split(",")]
ims=[[Image.open(f"$F/{s}_{x:.2f}.png") for x in fr] for s in shots]
w,h=ims[0][0].size; S=Image.new("RGB",(w*len(fr),h*len(shots)),(40,40,40))
for r,row in enumerate(ims):
  for c,im in enumerate(row):
    S.paste(im,(c*w,r*h)); ImageDraw.Draw(S).text((c*w+4,r*h+4),f"{shots[r]} {fr[c]}",fill=(255,80,80))
S.save("$F/sheet_"+"_".join(s[:3] for s in shots)+".jpg"); print("$F/sheet_"+"_".join(s[:3] for s in shots)+".jpg")
PY
