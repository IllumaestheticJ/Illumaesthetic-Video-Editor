#!/bin/bash
# Resumable Ep 8 cartoon render: one Blender process per shot, one at a time (frames already on disk are skipped).
#   tools/render_ep8.sh [A1 A2 ...]    env: SCALE SPP
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOLS="$HERE/../../scan-tedium-explainer-reel/tools"
FR=/home/user/media/pip-gus-ep7-materials/frames; LOG=/home/user/media/pip-gus-ep7-materials/render.log
mkdir -p "$FR"
for sh in ${*:-A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12}; do
  echo "[render] $(date -u +%H:%M:%S) $sh start" >> "$LOG"
  (cd "$TOOLS" && nice -n 5 blender -b --factory-startup -P partA_scene.py -- --exec "$HERE/ep8_anim.py" \
     --timeline "$HERE/../ep8_timeline.json" --out "$FR" --ep8shots "$sh" --scale "${SCALE:-1.0}" --spp "${SPP:-8}" --threads 4) \
     2>&1 | grep -E "\[ep8\]|Traceback|Error" >> "$LOG"
done
echo "[render] $(date -u +%H:%M:%S) all done" >> "$LOG"
