#!/bin/bash
# One Blender at a time (two at once ran the 15 GB machine out of memory): Part B scan shots, then the Part A cartoon.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; M=/home/user/media/pip-gus-ep4-print-the-scan
cd "$M/blend"
for spec in "scan 0:56" "lip 0:42"; do
  set -- $spec
  nice -n 5 blender -b GT350_Lip.blend -P "$HERE/partB_render.py" -- --out "$M/partB" --shot $1 --frames $2 --scale 1.0 >> "$M/logs/partB.log" 2>&1
done
echo "[partB] DONE" >> "$M/logs/partB.log"
"$HERE/render_partA.sh"
