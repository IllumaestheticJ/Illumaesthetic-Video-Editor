#!/bin/bash
# Render final shots one at a time (75 % res, 12 spp, 15 fps). usage: render_final.sh shot [shot ...]
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  spec=$(python projects/porsche-gt3rs-992/tools/shots.py final $s)
  rm -rf /home/user/media/work/gt3/renders/final/$s
  echo "start $s $(date +%T)"
  blender -b -P projects/porsche-gt3rs-992/tools/shot.py -- $spec > /home/user/media/work/gt3/log_$s.txt 2>&1
  echo "done $s $(date +%T) $(ls /home/user/media/work/gt3/renders/final/$s | wc -l) frames"
done
