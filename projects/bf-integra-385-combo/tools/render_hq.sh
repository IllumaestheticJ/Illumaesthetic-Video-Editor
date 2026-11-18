#!/bin/bash
# FINAL: 1080x1920, true 60 fps (native, keys remapped x2), 32 spp + denoise, 3 mm scan. Resumable (skips existing frames).
R=/home/user/media/bf-integra-385-combo/work/render_hq
cd "$(dirname "$0")"
for s in 1 2 3 4 7 8 9; do
  mkdir -p $R/s$s
  echo "$(date -u +%H:%M) start shot $s"
  blender -b --factory-startup -P shots.py -- --shot $s --out $R/s$s --res-pct 100 --samples 32 --step 1 --fps60 \
    --reg-dir /home/user/media/bf-integra-385-combo/work/reg3 >> $R/s$s.log 2>&1
  echo "$(date -u +%H:%M) shot $s done $(ls $R/s$s | wc -l) frames"
done
echo ALL_DONE
