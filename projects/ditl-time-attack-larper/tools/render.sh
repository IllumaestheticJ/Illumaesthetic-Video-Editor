#!/bin/bash
# render.sh <shot> [<shot> ...] : renders shots one at a time (540 px, 10 samples + denoise) into /home/user/media/ditl-time-attack-larper/frames/sNN/
D=$(dirname "$0"); O=/home/user/media/ditl-time-attack-larper/frames; mkdir -p $O
for n in "$@"; do
  s=$(date +%s); /usr/local/bin/blender -b --python $D/tl_shots.py -- $n $O anim 540 10 > $O/log_s$n.txt 2>&1
  echo "shot $n done in $(( $(date +%s) - s )) s, $(ls $O/s$(printf %02d $n) 2>/dev/null | wc -l) frames"
done
