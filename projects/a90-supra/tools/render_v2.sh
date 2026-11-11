#!/bin/bash
# A90 v2 finals: shots_v2/*.json, 1080x1920 @ 75 %, 12 spp, 15 fps, persistent data auto (off when parts move),
# 40-frame chunks in fresh Blender processes (one job at a time), then a per-frame luma scan that re-renders
# any frame darker than 60 % of its neighbours' median (v1 s08 lighting dropout).
D=$(cd "$(dirname "$0")/.." && pwd); R=/home/user/media/work/a90/renders_v2; mkdir -p $R
SHOTS=${@:-v01_whole v03_fbump v04_fcorner v05_side v06_rbump v07_rcorner v08_lineup v09a_reasm v09b_clean}
for s in $SHOTS; do
  N=$(python -c "import json;print(max(1,int(round(json.load(open('$D/shots_v2/$s.json'))['seconds']*15))))")
  t0=$(date +%s)
  for a in $(seq 1 40 $N); do b=$((a+39)); [ $b -gt $N ] && b=$N
    blender -b -P $D/tools/shots.py -- --shot $D/shots_v2/$s.json --out $R/$s --fps 15 --res-pct 75 --samples 12 --frames $a-$b >> $R/$s.log 2>&1
  done
  for pass in 1 2; do
    BAD=$(python - $R/$s <<'PY'
import sys,glob,numpy as np
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+"/f_*.png")); m=np.array([np.asarray(Image.open(f).convert("L").resize((90,160)),float).mean() for f in fs])
bad=[int(fs[i][-8:-4]) for i in range(len(m)) if m[i] < 0.6*np.median(m[max(0,i-6):i+7])]
print(" ".join(map(str,bad)))
PY
)
    [ -z "$BAD" ] && break
    echo "$s dark frames: $BAD (pass $pass)"
    for f in $BAD; do rm -f $R/$s/f_$(printf %04d $f).png; blender -b -P $D/tools/shots.py -- --shot $D/shots_v2/$s.json --out $R/$s --fps 15 --res-pct 75 --samples 12 --frames $f-$f >> $R/$s.log 2>&1; done
  done
  echo "$s done in $(( $(date +%s) - t0 )) s, $(ls $R/$s/*.png | wc -l)/$N frames"
done
