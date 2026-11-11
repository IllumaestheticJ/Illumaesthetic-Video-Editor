#!/bin/bash
# 30 % framing check (first/mid/last frame) of each named shot, one at a time, then a contact strip per shot.
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  sp=$(python projects/mazda-miata-na/tools/shots.py preview $s)
  rm -rf /home/user/media/work/miata/renders/preview/$s
  blender -b -P projects/mazda-miata-na/tools/shot.py -- $sp > /home/user/media/work/miata/renders/$s.log 2>&1
  python - "$s" <<'PY'
import sys, glob
from PIL import Image
s = sys.argv[1]; fs = sorted(glob.glob(f"/home/user/media/work/miata/renders/preview/{s}/f_*.png"))
ims = [Image.open(f) for f in fs]; w, h = ims[0].size
o = Image.new("RGB", (w * len(ims), h))
for i, im in enumerate(ims): o.paste(im, (i * w, 0))
o.save(f"/home/user/media/work/miata/renders/preview/{s}.jpg"); print(f"/home/user/media/work/miata/renders/preview/{s}.jpg")
PY
done
