#!/bin/bash
# A90 v4 end card (user: "add the BD Engineering logo"): ILLUMAESTHETIC 720 px wide above centre, the BD logo
# (Dropbox /Misc. Brand Logos/render_9_transparent (1).png, cropped to its alpha) 420 px below it, on pure black.
# Fade in 0.3 s, hold, fade out with the audio over the last 1.4 s.
set -e
LOGO=${1:-remotion/public/illumaesthetic_logo.png}; BD=${2:-/home/user/media/a90-supra/logos/render9.png}
OUT=${3:-/home/user/media/work/a90/logo_card_v4.mp4}; DUR=${4:-3.3667}
python3 -c "from PIL import Image;im=Image.open('$BD');im.crop(im.split()[-1].getbbox()).save('/home/user/media/work/a90/bd_crop.png')"
ffmpeg -y -v error -f lavfi -i "color=c=black:s=1080x1920:r=30:d=$DUR" -loop 1 -framerate 30 -t $DUR -i "$LOGO" -loop 1 -framerate 30 -t $DUR -i /home/user/media/work/a90/bd_crop.png -filter_complex \
"[1:v]scale=720:-1:flags=lanczos,format=rgba[l];[2:v]scale=-1:420:flags=lanczos,format=rgba[b];[0:v][l]overlay=x=(W-w)/2:y=H/2-h-90:format=auto[v1];[v1][b]overlay=x=(W-w)/2:y=H/2+20:format=auto,fade=t=in:st=0:d=0.3,fade=t=out:st=$(python3 -c "print($DUR-1.4)"):d=1.4,format=yuv420p[v]" \
-map "[v]" -c:v libx264 -crf 14 -preset slow -t $DUR "$OUT"
echo "$OUT"
