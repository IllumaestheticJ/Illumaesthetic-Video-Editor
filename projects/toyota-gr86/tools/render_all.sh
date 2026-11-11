#!/bin/bash
# Final renders, strictly one Blender at a time (75 % res, 12 spp, 15 fps; assemble interpolates to 30).
#   render_all.sh s1_front34 s2_rear34 ...
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  t0=$(date +%s)
  /usr/local/bin/blender -b -P projects/ferrari-296/tools/shot.py -- projects/toyota-gr86/shots/$s.json > /home/user/media/work/gr86/shots/$s.log 2>&1
  echo "$s $(ls /home/user/media/work/gr86/shots/$s | wc -l) frames $(( $(date +%s) - t0 )) s"
done
echo RENDERS_DONE
