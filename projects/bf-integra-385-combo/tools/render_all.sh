#!/bin/bash
# v0 preview renders, one at a time
R=/home/user/media/bf-integra-385-combo/work/render_v0
cd "$(dirname "$0")"
for s in 1 2 3 4 5 6; do
  mkdir -p $R/s$s
  blender -b --factory-startup -P shots.py -- --shot $s --out $R/s$s --res-pct 50 --samples 16 --step 2 > $R/s$s.log 2>&1
  echo "shot $s done $(ls $R/s$s | wc -l) frames"
done
echo ALL_DONE
