#!/bin/bash
# render_list.sh <shot> ... : renders shots one at a time with the right script (1-4 tl_shots.py, 5-15 tl_shots_b.py). No waiting on other queues.
D=$(dirname "$0"); O=/home/user/media/ditl-time-attack-larper/frames; mkdir -p $O
for n in "$@"; do
  S=$D/tl_shots.py; [ $n -ge 5 ] && S=$D/tl_shots_b.py
  rm -rf $O/s$(printf %02d $n); s=$(date +%s); /usr/local/bin/blender -b --python $S -- $n $O anim 540 10 > $O/log_s$n.txt 2>&1
  echo "shot $n done in $(( $(date +%s) - s )) s, $(ls $O/s$(printf %02d $n) 2>/dev/null | wc -l) frames"
done
