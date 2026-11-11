#!/bin/bash
# Render shot specs one at a time (heavy jobs serialised). render_all.sh preview|final [shot ...]
cd "$(dirname "$0")/../../.."
MODE=$1; shift
SHOTS=${@:-s1_front34 s2_rear34 s3_wheel s4_light s5_hood s6_top s7_explode}
for s in $SHOTS; do
  t0=$(date +%s)
  blender -b -P projects/subaru-sti-blobeye/tools/shot.py -- /home/user/media/work/sti/specs/${MODE}_$s.json > /home/user/media/work/sti/log_${MODE}_$s.txt 2>&1
  echo "$s $(( $(date +%s) - t0 ))s $(grep -c 'Saved:' /home/user/media/work/sti/log_${MODE}_$s.txt) frames"
done
echo RENDER_ALL_DONE
