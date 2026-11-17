#!/bin/bash
# Resumable Ep 4 Part A render: one Blender process per shot (3 tries), frames skipped when already on disk.
#   tools/render_partA.sh [E1 E2 ...]   env: SCALE SPP      log: MEDIA/logs/render_partA.log
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; M=/home/user/media/pip-gus-ep4-print-the-scan
FR=$M/frames; LOG=$M/logs/render_partA.log; mkdir -p "$FR" "$M/logs"
SHOTS=${*:-E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 E11 E12}
cd "$HERE/../../scan-tedium-explainer-reel/tools"
for sh in $SHOTS; do
  for try in 1 2 3; do
    echo "[render] $(date -u +%H:%M:%S) $sh try $try" >> "$LOG"
    nice -n 5 /usr/local/bin/blender -b --factory-startup -P partA_scene.py -- --exec "$HERE/ep4_anim.py" --out "$FR" \
      --timeline "$HERE/../ep4_timeline.json" --shots "$sh" --scale "${SCALE:-1.0}" --spp "${SPP:-8}" >> "$LOG" 2>&1 && break
  done
done
echo "[render] $(date -u +%H:%M:%S) all done" >> "$LOG"
