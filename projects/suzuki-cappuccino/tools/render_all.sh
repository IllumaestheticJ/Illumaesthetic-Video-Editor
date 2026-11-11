#!/bin/bash
# Final renders, one Blender at a time (75 % res, 12 spp, 15 fps - set in shots.py). Resumable: existing frames are skipped.
cd "$(dirname "$0")"
for n in ${@:-s01_side s02_front34 s03_rear34 s04_wheel s05_lamp s06_frontopen s07_trunk s08_top s09_explode s10_float s11_reassemble}; do
  s=$(date +%s); blender -b -P shot.py -- /home/user/media/work/cappuccino/shots/$n.json > /home/user/media/work/cappuccino/render_$n.log 2>&1
  echo "$n $(ls /home/user/media/work/renders/cappuccino/$n | wc -l) frames $(( $(date +%s)-s )) s"
done
echo RENDERDONE
