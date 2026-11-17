#!/bin/bash
# Resumable Ep 3 cartoon render (same pattern as the Ep 2 session's render_ep1.sh): one Blender process per shot, one at a
# time; frames on disk are skipped.   tools/render_ep3.sh [A B ...]   env: EVERY (default 2 = on twos), SCALE, SPP
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PILOT="$HERE/../../scan-tedium-explainer-reel/tools"
OUT=/home/user/media/ep3/frames; LOG=/home/user/media/ep3/logs/render.log
mkdir -p "$OUT" "$(dirname "$LOG")"
for sh in ${*:-A B C D E F G H I J K L}; do
  EV=${EVERY:-2}; [ "$sh" = "L" ] && EV=1   # the phone push plays real footage on its screen: render every frame
  (cd "$PILOT" && nice -n 5 /usr/local/bin/blender -b --factory-startup -P partA_scene.py -- --exec "$HERE/ep3_scene.py" \
     --out "$OUT" --tl "$HERE/../ep3_timeline.json" --shots "$sh" --every "$EV" --scale "${SCALE:-1.0}" \
     --spp "${SPP:-8}" --threads 4 --phonedir /home/user/media/ep3/phone --phonef0 4) 2>&1 | grep -E "\[ep3\]|Error|Traceback" >> "$LOG"
  echo "[render] $(date -u +%H:%M:%S) $sh finished" >> "$LOG"
done
echo "[render] $(date -u +%H:%M:%S) all done" >> "$LOG"
