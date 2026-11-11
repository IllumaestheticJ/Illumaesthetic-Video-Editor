#!/bin/bash
# Final scan shots, one Blender at a time: 75 % res, 12 spp, 15 fps (assemble interpolates to 30).
cd "$(dirname "$0")/../../.."
P=projects/c5-corvette-scan-process
for s in "$@"; do
  blender -b -P $P/tools/shot.py -- $P/shots/$s.json --res-pct 75 --samples 12 > /home/user/media/work/c5/renders/log_$s.txt 2>&1
  echo "done $s $(date -u +%T)"
done
