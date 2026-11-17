#!/bin/bash
# Ep 7 cartoon render: one Blender process at a time, shot by shot, resumable (frames already on disk are skipped).
#   tools/render_all.sh [S1 S2 ...]    env: SCALE (1.0) SPP (8)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
W=/home/user/media/work/ep7
FR=$W/frames; LOG=$W/logs/render.log
mkdir -p "$FR" "$W/logs"
SHOTS=${*:-S1 S2 S3 S4 S5 S6 S7 S8 S9 S10}
for sh in $SHOTS; do
  for try in 1 2 3; do
    echo "[render] $(date -u +%H:%M:%S) $sh try $try" >> "$LOG"
    (cd "$HERE" && nice -n 5 /usr/local/bin/blender -b --factory-startup -P ep7_scene.py -- --out "$FR" \
       --timeline "$HERE/../ep7_timeline.json" --tagdir "$W/tex" --shots "$sh" --scale "${SCALE:-1.0}" --spp "${SPP:-8}") >> "$LOG" 2>&1
    python3 - "$HERE/../ep7_timeline.json" "$FR" "$sh" <<'PY' && break
import json, os, sys
tl = json.load(open(sys.argv[1])); sh = sys.argv[3]
s = [x for x in tl["shots"] if x["id"] == sh][0]
miss = [f for f in range(s["f0"], s["f1"]) if not os.path.exists(os.path.join(sys.argv[2], sh, f"{f:04d}.png"))]
print(f"[render] {sh}: {len(miss)} missing"); sys.exit(1 if miss else 0)
PY
  done
done
echo "[render] $(date -u +%H:%M:%S) all done" >> "$LOG"
