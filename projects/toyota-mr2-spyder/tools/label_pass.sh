#!/bin/bash
# Composite the ScanHUD label overlay (ProRes 4444 alpha) over the concat-assembled reel; audio copied.
#   tools/label_pass.sh in.mp4 hud.mov out.mp4
set -e
ffmpeg -v error -y -i "$1" -i "$2" -filter_complex "[0:v][1:v]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 16 -preset slow -c:a copy -movflags +faststart "$3"
