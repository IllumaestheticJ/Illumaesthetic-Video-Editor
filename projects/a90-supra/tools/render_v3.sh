#!/bin/bash
# A90 v3 finals. Resumable: frames on disk are skipped, each shot renders in 30-frame chunks in fresh Blender processes
# (one job at a time, flock), then a luma scan re-renders any frame darker than 60 % of its neighbours (lighting dropout).
#   render_v3.sh shot [shot ...]      output: /home/user/media/work/a90/renders_v3/<shot>/f_####.png
D=$(cd "$(dirname "$0")/.." && pwd); W=/home/user/media/work/a90; R=$W/renders_v3; mkdir -p $R
for s in "$@"; do
  read N A B < <(python - <<PY
import json;d=json.load(open("$D/shots_v3/$s.json"));n=max(1,int(round(d["seconds"]*d["fps"])))
a,b=(int(x) for x in d.get("_render_frames","1-%d"%n).split("-"));print(n,a,b)
PY
)
  t0=$(date +%s); find $R/$s -name "f_*.png" -size 0 -delete 2>/dev/null   # placeholders left by an interrupted run
  for a in $(seq $A 30 $B); do b=$((a+29)); [ $b -gt $B ] && b=$B
    have=$(for f in $(seq $a $b); do [ -s $R/$s/f_$(printf %04d $f).png ] && echo 1; done | wc -l)
    [ $have -eq $((b-a+1)) ] && continue
    flock $W/blender.lock blender -b -P $D/tools/shots3.py -- --shot $D/shots_v3/$s.json --out $R/$s --res-pct 75 --samples 12 --frames $a-$b >> $R/$s.log 2>&1
  done
  for pass in 1 2; do
    BAD=$(python - $R/$s <<'PY'
import sys,glob,numpy as np
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+"/f_*.png")); m=np.array([np.asarray(Image.open(f).convert("L").resize((90,160)),float).mean() for f in fs])
print(" ".join(str(int(fs[i][-8:-4])) for i in range(len(m)) if m[i] < 0.6*np.median(m[max(0,i-6):i+7])))
PY
)
    [ -z "$BAD" ] && break
    echo "$s dark frames: $BAD (pass $pass)"
    for f in $BAD; do rm -f $R/$s/f_$(printf %04d $f).png; flock $W/blender.lock blender -b -P $D/tools/shots3.py -- --shot $D/shots_v3/$s.json --out $R/$s --res-pct 75 --samples 12 --frames $f-$f >> $R/$s.log 2>&1; done
  done
  echo "$s done in $(( $(date +%s) - t0 )) s, $(ls $R/$s/*.png 2>/dev/null | wc -l)/$((B-A+1)) frames"
done
