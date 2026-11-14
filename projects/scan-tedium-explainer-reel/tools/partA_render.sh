#!/bin/bash
# Resumable Part A render: one Blender process at a time, shot by shot. Skips shots already encoded and frames already on disk.
# After each shot: black/unlit check + ProRes encode + PNGs deleted (partA_encode.py); flagged frames are re-rendered (3 tries).
#   tools/partA_render.sh [S1 S2 ...]      (default: all shots)   env: SCALE SPP
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
W=/home/user/media/work/scan-tedium
FR=$W/frames; MOV=$W/shots; LOG=$W/logs/render_partA.log
mkdir -p "$FR" "$MOV" "$W/logs"
SHOTS=${*:-S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 S11 S12}
for sh in $SHOTS; do
  for try in 1 2 3; do
    python3 "$HERE/partA_encode.py" --frames "$FR" --shot "$sh" --movs "$MOV" >> "$LOG" 2>&1; rc=$?
    [ $rc -eq 0 ] && break
    echo "[render] $(date -u +%H:%M:%S) $sh try $try (encode rc $rc)" >> "$LOG"
    (cd "$HERE" && nice -n 5 /usr/local/bin/blender -b --factory-startup -P partA_scene.py -- --animate --out "$FR" \
       --timeline "$HERE/../partA_timeline.json" --shots "$sh" --scale "${SCALE:-1.0}" --spp "${SPP:-8}" --threads 4) >> "$LOG" 2>&1
  done
  python3 "$HERE/partA_encode.py" --frames "$FR" --shot "$sh" --movs "$MOV" >> "$LOG" 2>&1 || echo "[render] $sh FAILED" >> "$LOG"
done
echo "[render] $(date -u +%H:%M:%S) all done" >> "$LOG"
