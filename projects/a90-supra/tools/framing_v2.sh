#!/bin/bash
# v2 framing check: 30 % stills of shots_v2/<id>.json at 5 fractions (one Blender job at a time) + a contact sheet per shot.
# usage: framing_v2.sh "v01_whole v02_face ..." [fractions]
D=$(cd "$(dirname "$0")/.." && pwd); F=/home/user/media/work/a90/plan; mkdir -p $F
FR=${2:-0,0.25,0.5,0.75,1}
for s in $1; do
  t=$(date +%s)
  blender -b -P $D/tools/shots.py -- --shot $D/shots_v2/$s.json --out $F/$s --stills $FR --res-pct 30 --samples 8 >$F/$s.log 2>&1 || echo "FAIL $s"
  python3 - "$s" "$FR" "$F" "$D" <<'PY'
import sys, json
from PIL import Image, ImageDraw
s, fr, F, D = sys.argv[1], [float(x) for x in sys.argv[2].split(",")], sys.argv[3], sys.argv[4]
sp = json.load(open(f"{D}/shots_v2/{s}.json")); T0, T1 = sp["_window"]
ims = [Image.open(f"{F}/{s}_{x:.2f}.png") for x in fr]
w, h = ims[0].size; S = Image.new("RGB", (w * len(ims), h + 18), (60, 60, 60))
for i, (x, im) in enumerate(zip(fr, ims)):
    S.paste(im, (i * w, 18)); ImageDraw.Draw(S).text((i * w + 4, 3), f"{s} t={x} ({T0 + x * (T1 - T0):.2f}s)", fill=(255, 90, 90))
    ImageDraw.Draw(S).rectangle([i * w, 18, i * w + w - 1, 18 + h - 1], outline=(90, 90, 90))
S.save(f"{F}/sheet_{s}.jpg")
PY
  echo "$s $(( $(date +%s)-t ))s"
done
