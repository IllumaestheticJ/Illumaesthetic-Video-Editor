#!/bin/bash
# Pop the next "shot frames" chunk from v60_chunks.txt and render it (one background job per chunk, < 2 h each).
Q=/home/user/media/bf-clearance-shelf-drop/v60_chunks.txt
read -r s f < <(head -1 $Q) || exit 0
[ -z "$s" ] && { echo QUEUE_EMPTY; exit 0; }
SHOTS=$s FRAMES=$f bash $(dirname $0)/render_v60.sh >> /home/user/media/bf-clearance-shelf-drop/render_v60_queue.log 2>&1 && sed -i 1d $Q
echo "chunk $s $f done; left: $(wc -l < $Q)"
