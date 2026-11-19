#!/bin/bash
# render_b.sh <shot> ... : shots 5-15 (tl_shots_b.py), one at a time, after any running render.sh finishes
D=$(dirname "$0"); O=/home/user/media/ditl-time-attack-larper/frames; mkdir -p $O
while pgrep -f "render.sh" > /dev/null; do sleep 20; done
for n in "$@"; do
  s=$(date +%s); /usr/local/bin/blender -b --python $D/tl_shots_b.py -- $n $O anim 540 10 > $O/log_s$n.txt 2>&1
  echo "shot $n done in $(( $(date +%s) - s )) s, $(ls $O/s$(printf %02d $n) 2>/dev/null | wc -l) frames"
done
