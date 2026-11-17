#!/bin/bash
# Ep 3 scan shot: the 296 scan from the solved camera (match/cam.json), house silver look, 15 fps, slow push-in.
# Waits for the cartoon render to finish first (one heavy job at a time).
HERE="$(cd "$(dirname "$0")" && pwd)"
while pgrep -f render_ep3.sh >/dev/null; do sleep 30; done
cd "$HERE/../../.." && python -m ive render -- --scene /home/user/media/ep3/scan_296/car6.blend --camera "$HERE/../match/cam.json" \
  --out /home/user/media/ep3/scan_render --look silver --fps 15 --seconds 1.87 --move push --move-amount 0.06 --ease ease_out \
  --samples 16 > /home/user/media/ep3/logs/scan_render.log 2>&1
echo "[scan] done $(date -u +%H:%M:%S)" >> /home/user/media/ep3/logs/scan_render.log
