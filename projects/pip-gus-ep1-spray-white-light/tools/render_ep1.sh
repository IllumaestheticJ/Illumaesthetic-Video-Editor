#!/bin/bash
# Resumable Ep 1 cartoon render: one Blender process per shot, one at a time; frames on disk are skipped.
#   tools/render_ep1.sh [A B ...]    env: EVERY (default 2 = on twos), SCALE (1.0), SPP (8)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PILOT="$HERE/../../scan-tedium-explainer-reel/tools"
OUT=/home/user/media/ep1/frames; LOG=/home/user/media/ep1/logs/render.log
mkdir -p "$OUT"
for sh in ${*:-A B C D E F G H I J K L M}; do
  for try in 1 2; do
    (cd "$PILOT" && nice -n 5 /usr/local/bin/blender -b --factory-startup -P partA_scene.py -- --exec "$HERE/ep1_scene.py" \
       --out "$OUT" --tl "$HERE/../ep1_timeline.json" --shots "$sh" --every "${EVERY:-2}" --scale "${SCALE:-1.0}" \
       --spp "${SPP:-8}" --threads 4) 2>&1 | grep -E "\[ep1\]|Error|Traceback" >> "$LOG"
  done
  echo "[render] $(date -u +%H:%M:%S) $sh finished" >> "$LOG"
done
echo "[render] $(date -u +%H:%M:%S) all done" >> "$LOG"
