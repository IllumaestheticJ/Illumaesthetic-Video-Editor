#!/bin/bash
# ILLUMAESTHETIC logo end card: 1080x1920 30 fps, logo 78 % of width on pure black, slow 3 % push,
# fade to black over the last 1.6 s (the score's reverb tail). Hard cut in on the bar-14 downbeat.
set -e
LOGO=${1:-remotion/public/illumaesthetic_logo.png}; OUT=${2:-/home/user/media/work/a90/logo_card.mp4}; DUR=${3:-6.0}
ffmpeg -y -v error -f lavfi -i "color=c=black:s=1080x1920:r=30:d=$DUR" -loop 1 -framerate 30 -t $DUR -i "$LOGO" -filter_complex \
"[1:v]scale=842:-1:flags=lanczos,format=rgba,scale=w='iw*(1+0.03*t/$DUR)':h=-1:eval=frame:flags=lanczos[l];[0:v][l]overlay=x='(W-w)/2':y='(H-h)/2-40':eval=frame:format=auto,fade=t=out:st=$(python -c "print($DUR-1.6)"):d=1.6,format=yuv420p[v]" \
-map "[v]" -c:v libx264 -crf 14 -preset slow -t $DUR "$OUT"
echo "$OUT"
