#!/bin/bash
# Final scan shots, one Blender job at a time (house rule): 1080x1920 @ 75 %, 12 spp, 15 fps (assemble interpolates to 30).
D=$(cd "$(dirname "$0")/.." && pwd); R=/home/user/media/work/a90/renders; mkdir -p $R
for s in ${@:-s01_front34 s02_rear34 s03_arch s04_headlight s05_taillight s06_side s07_topdown s08_explode}; do
  t0=$(date +%s)
  blender -b -P $D/tools/shots.py -- --shot $D/shots/$s.json --out $R/$s --fps 15 --res-pct 75 --samples 12 > $R/$s.log 2>&1
  echo "$s done in $(( $(date +%s) - t0 )) s, $(ls $R/$s | wc -l) frames"
done
