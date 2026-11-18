#!/bin/bash
# Pop the next "shot frames" chunk from v60_chunks.txt and render it (one background job per chunk, < 2 h each).
Q=/home/user/media/bf-clearance-shelf-drop/v60_chunks.txt
read -r s f < <(head -1 $Q) || exit 0
[ -z "$s" ] && { echo QUEUE_EMPTY; exit 0; }
SHOTS=$s FRAMES=$f bash $(dirname $0)/render_v60.sh >> /home/user/media/bf-clearance-shelf-drop/render_v60_queue.log 2>&1 && sed -i 1d $Q
# restart protection (owner workflow): one Drive archive per finished chunk
a=${f%-*}; b=${f#*-}; D=/home/user/media/bf-clearance-shelf-drop/renders_v60/$s
files=$(for i in $(seq $a $b); do printf "$D/f_%04d.png " $i; done)
python /home/user/Illumaesthetic-Video-Editor/scripts/vdrive.py save bf-clearance-shelf-drop frames60_${s}_$f $files 2>&1 | tail -1
python /home/user/Illumaesthetic-Video-Editor/scripts/vdrive.py save bf-clearance-shelf-drop workdir /home/user/media/bf-clearance-shelf-drop/work_v0 $Q 2>&1 | tail -1
echo "chunk $s $f done; left: $(wc -l < $Q)"
