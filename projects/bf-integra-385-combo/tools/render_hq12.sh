#!/bin/bash
# v1.2 (owner rule "slow down for text"): re-render the lengthened shots 1, 3, 4 at final quality, true 60 fps.
# Waits for the v1.1 queue (render_hq) so only one Blender job runs at a time. Resumable: existing frames are skipped.
cd "$(dirname "$0")"
Q=/home/user/media/bf-integra-385-combo/work/render_hq/queue.log
R=/home/user/media/bf-integra-385-combo/work/render_hq12; mkdir -p $R
until grep -q ALL_DONE $Q; do sleep 60; done
for s in 1 3 4; do
  echo "$(date -u +%H:%M) start shot $s"
  find $R/s$s -name '*.png' -size 0 -delete 2>/dev/null
  blender -b --factory-startup -P shots.py -- --shot $s --out $R/s$s --res-pct 100 --samples 32 --step 1 --fps60 \
    --reg-dir /home/user/media/bf-integra-385-combo/work/reg3 >> $R/s$s.log 2>&1
  echo "$(date -u +%H:%M) shot $s done $(ls $R/s$s | wc -l) frames"
done
echo ALL_DONE
