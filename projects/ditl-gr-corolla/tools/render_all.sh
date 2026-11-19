#!/bin/bash
# render_all.sh [shots...] : render the listed shots (default all 14), one at a time, 540 px, 14 samples
O=/home/user/media/ditl-gr-corolla/frames; cd "$(dirname "$0")"
for n in ${@:-1 2 3 4 5 6 7 8 9 10 11 12 13 14}; do
  d=$O/s$(printf %02d $n); rm -rf $d; mkdir -p $d
  blender -b --python gr_shots.py -- $n $O anim 540 14 > $O/log_$n.txt 2>&1; echo "shot $n done $(ls $d | wc -l) frames $(date +%H:%M:%S)"
done
