#!/bin/bash
# Final scan shots, one Blender at a time: 75 % res, 12 spp, 15 fps (assemble interpolates to 30).
# usage: bash render_queue.sh shot1 [shot2 ...]   (names of projects/a90-supra-scan-process/shots/*.json)
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  /usr/local/bin/blender -b -P $( case "$s" in v2_*|s3_xray) echo projects/a90-supra-scan-process/tools/xshots.py;; *) echo projects/a90-supra/tools/shots.py;; esac ) -- --shot projects/a90-supra-scan-process/shots/$s.json \
    --out /home/user/media/work/a90sp/renders/$s --res-pct 75 --samples 12 --fps 15 > /home/user/media/work/a90sp/renders/$s.log 2>&1
done
