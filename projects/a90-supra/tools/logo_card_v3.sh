#!/bin/bash
# A90 v3 end card: ILLUMAESTHETIC logo 700 px wide (65 % of 1080; smaller cards were "too small" on other reels),
# centred on pure black. In on bar 19 beat 4: fade in 0.3 s, hold, fade out with the audio over the last 1.4 s.
set -e
LOGO=${1:-remotion/public/illumaesthetic_logo.png}; OUT=${2:-/home/user/media/work/a90/logo_card_v3.mp4}; DUR=${3:-3.3333}
ffmpeg -y -v error -f lavfi -i "color=c=black:s=1080x1920:r=30:d=$DUR" -loop 1 -framerate 30 -t $DUR -i "$LOGO" -filter_complex \
"[1:v]scale=700:-1:flags=lanczos,format=rgba[l];[0:v][l]overlay=x=(W-w)/2:y=(H-h)/2:format=auto,fade=t=in:st=0:d=0.3,fade=t=out:st=$(python3 -c "print($DUR-1.4)"):d=1.4,format=yuv420p[v]" \
-map "[v]" -c:v libx264 -crf 14 -preset slow -t $DUR "$OUT"
echo "$OUT"
