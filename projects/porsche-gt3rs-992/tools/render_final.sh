#!/bin/bash
# Render final shots one at a time (75 % res, 12 spp, 15 fps). usage: [RESUME=1] render_final.sh shot [shot ...]
# RESUME=1 keeps finished frames and renders only the missing ones.
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  case $s in v6_*) spec=$(python projects/porsche-gt3rs-992/tools/shots_v6.py final $s);; v5_*|m_*) spec=$(python projects/porsche-gt3rs-992/tools/shots_v5.py final $s);; v3_*) spec=$(python projects/porsche-gt3rs-992/tools/shots_v3.py final $s);; v2_*) spec=$(python projects/porsche-gt3rs-992/tools/shots_v2.py final $s);; *) spec=$(python projects/porsche-gt3rs-992/tools/shots.py final $s);; esac
  [ -z "$RESUME" ] && rm -rf /home/user/media/work/gt3/renders/final/$s
  echo "start $s $(date +%T)"
  blender -b -P projects/porsche-gt3rs-992/tools/shot.py -- $spec > /home/user/media/work/gt3/log_$s.txt 2>&1
  echo "done $s $(date +%T) $(ls /home/user/media/work/gt3/renders/final/$s | wc -l) frames"
done
