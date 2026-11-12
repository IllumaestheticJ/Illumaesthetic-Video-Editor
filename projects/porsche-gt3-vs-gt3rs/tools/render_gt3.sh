#!/bin/bash
# GT3 panel finals, one at a time, resumable. usage: render_gt3.sh shot [shot ...]
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  spec=$(python projects/porsche-gt3-vs-gt3rs/tools/shots_gt3.py final $s)
  echo "start $s $(date +%T)"
  blender -b -P projects/porsche-gt3-vs-gt3rs/tools/shot.py -- $spec > /home/user/media/work/gt3vs/log_$s.txt 2>&1
  echo "done $s $(date +%T) $(ls /home/user/media/work/gt3vs/renders/final/$s | wc -l) frames"
done
