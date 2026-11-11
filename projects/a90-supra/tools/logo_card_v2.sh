#!/bin/bash
# A90 v2 end card (Temerario ending): small ILLUMAESTHETIC logo, 25 % of width (270 px) centred on pure black,
# 3.5 s = reel 38.0-41.5: black 0.2 s, fade in 0.2-0.9 (38.2-38.9), hold, fade out 2.6-3.5 (40.6-41.5).
set -e
LOGO=${1:-remotion/public/illumaesthetic_logo.png}; OUT=${2:-/home/user/media/work/a90/logo_card_v2.mp4}
ffmpeg -y -v error -f lavfi -i "color=c=black:s=1080x1920:r=30:d=3.5" -loop 1 -framerate 30 -t 3.5 -i "$LOGO" -filter_complex \
"[1:v]scale=270:-1:flags=lanczos,format=rgba[l];[0:v][l]overlay=x=(W-w)/2:y=(H-h)/2:format=auto,fade=t=in:st=0.2:d=0.7,fade=t=out:st=2.6:d=0.9,format=yuv420p[v]" \
-map "[v]" -c:v libx264 -crf 14 -preset slow -t 3.5 "$OUT"
echo "$OUT"
