#!/bin/bash
# Final renders, one Blender at a time (75 % res, 12 spp, 15 fps). usage: render_all.sh shot [shot ...]
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  spec=$(python projects/mazda-miata-nc/tools/shots.py final $s)
  t0=$(date +%s); blender -b -P projects/mazda-miata-nc/tools/shot.py -- $spec > /home/user/media/work/miata/log_$s.txt 2>&1
  echo "$s done in $(( $(date +%s) - t0 )) s"
done
