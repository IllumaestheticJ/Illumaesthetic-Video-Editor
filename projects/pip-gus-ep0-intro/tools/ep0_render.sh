#!/bin/bash
# Full Ep 0 render, resumable: one Blender process per shot, frames skipped when already on disk. env: SPP (4), SCALE (1.0)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SCN="$HERE/../../scan-tedium-explainer-reel/tools"
FR=/home/user/media/work/pip-gus-ep0/frames; LOG=/home/user/media/work/pip-gus-ep0/logs/render.log
mkdir -p "$FR" "$(dirname $LOG)"
SHOTS=${*:-A B C D E F G H1 H2 H3 H4 I J K}
for sh in $SHOTS; do
  echo "[render] $(date -u +%H:%M:%S) $sh" >> "$LOG"
  (cd "$SCN" && nice -n 5 /usr/local/bin/blender -b --factory-startup -P partA_scene.py -- --exec "$HERE/ep0_anim.py" \
     --out "$FR" --ep0shots "$sh" --spp "${SPP:-4}" --scale "${SCALE:-1.0}") 2>&1 | grep -v "EGL Error" >> "$LOG"
done
echo "[render] $(date -u +%H:%M:%S) all done" >> "$LOG"
