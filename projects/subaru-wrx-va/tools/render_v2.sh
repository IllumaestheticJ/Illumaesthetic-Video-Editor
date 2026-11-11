#!/bin/bash
# v2 shots (director.md), one Blender job at a time, persistent data off, per-frame luma check after each.
D=$(cd "$(dirname "$0")/.." && pwd); R=/home/user/media/subaru-wrx-va/renders; mkdir -p $R
for s in ${@:-n1_bumper n2_scoop n4a_reassemble n4b_clean n3_wing n_side}; do
  t0=$(date +%s)
  blender -b -P $D/tools/shots.py -- --shot $D/shots/$s.json --out $R/$s --fps 15 --res-pct 75 --samples 12 --no-persist > $R/$s.log 2>&1
  dark=$(python3 -c "
import glob; from PIL import Image; import numpy as np
v=[np.asarray(Image.open(f).convert('L').reduce(4)).mean() for f in sorted(glob.glob('$R/$s/*.png'))]
print(len(v), round(min(v),1), round(max(v),1), [i+1 for i,x in enumerate(v) if x < 0.5*np.median(v)])")
  echo "$s done in $(( $(date +%s) - t0 )) s; frames min max dark: $dark"
done
