#!/bin/bash
# Waits for the cartoon render, then renders the Civic scan shot from the solved cam_A (silver house look, 15 fps,
# 2.0 s, 10 deg ease-in-out orbit; the cut starts from rest).
while pgrep -f "partA_scene[.]py" >/dev/null; do sleep 60; done
cd /home/user/Illumaesthetic-Video-Editor
S=/home/user/media/civic11
nice python -m ive render -- --scene $S/scan/ek.blend --camera projects/honda-civic-11-scan-process/match/cam_A.json \
  --out /home/user/media/ep1/scan_civic --look silver --fps 15 --seconds 2.0 --move orbit --move-amount 10 \
  --ease ease_in_out --samples 16 >> /home/user/media/ep1/logs/scan.log 2>&1
echo "scan done $(date -u +%H:%M:%S)" >> /home/user/media/ep1/logs/scan.log
