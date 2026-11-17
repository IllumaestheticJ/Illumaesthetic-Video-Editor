#!/bin/bash
# v0.3: coloured opening (shots 1-4) + scan shots with the DE4 A-Spec wingless deck fill (7-8)
R=/home/user/media/bf-integra-385-combo/work/render_v03
cd "$(dirname "$0")"
for s in 7 8 1 2 3 4; do
  mkdir -p $R/s$s
  blender -b --factory-startup -P shots.py -- --shot $s --out $R/s$s --res-pct 50 --samples 16 --step 2 > $R/s$s.log 2>&1
  echo "shot $s done $(ls $R/s$s | wc -l) frames"
done
echo ALL_DONE
