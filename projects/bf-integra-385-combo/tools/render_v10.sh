#!/bin/bash
# v1.0: kraft cardboard box with the Epsilon+ wordmark, neutral studio (shots 1-4)
R=/home/user/media/bf-integra-385-combo/work/render_v10
cd "$(dirname "$0")"
for s in 1 2 3 4; do
  mkdir -p $R/s$s
  blender -b --factory-startup -P shots.py -- --shot $s --out $R/s$s --res-pct 50 --samples 16 --step 2 > $R/s$s.log 2>&1
  echo "shot $s done $(ls $R/s$s | wc -l) frames"
done
echo ALL_DONE
