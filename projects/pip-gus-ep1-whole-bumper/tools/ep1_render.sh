#!/bin/bash
# Full Ep 1 render, resumable: one Blender process per shot, frames skipped when already on disk. env: SPP (4), SCALE (1.0)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SCN="$HERE/../../scan-tedium-explainer-reel/tools"
FR=/home/user/media/work/ep1/frames; LOG=/home/user/media/work/ep1/logs/render.log
mkdir -p "$FR" "$(dirname $LOG)"
SHOTS=${*:-E01 E02 E03 E04 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14}
for sh in $SHOTS; do
  echo "[render] $(date -u +%H:%M:%S) $sh" >> "$LOG"
  (cd "$SCN" && nice -n 5 /usr/local/bin/blender -b --factory-startup -P partA_scene.py -- --exec "$HERE/ep1_anim.py" \
     --out "$FR" --ep1shots "$sh" --spp "${SPP:-4}" --scale "${SCALE:-1.0}") 2>&1 | grep -v "EGL Error" >> "$LOG"
done
echo "[render] $(date -u +%H:%M:%S) all done" >> "$LOG"
