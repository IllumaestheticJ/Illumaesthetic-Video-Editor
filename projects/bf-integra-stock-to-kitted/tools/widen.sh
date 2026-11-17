#!/bin/sh
# Zoomed-out 9:16 from 4K landscape footage: the window (WIN px wide, 16:9-tall) is scaled to 1080 wide and placed over a
# blurred, darkened 9:16 fill of the same frame. X0 may ease from X0A to X0B over PAN seconds; CY = window centre y (4K px).
# usage: widen.sh in.mp4 out.mp4 start_s frames WIN X0A X0B CY PAN
IN=$1 OUT=$2 SS=$3 N=$4 WIN=$5 XA=$6 XB=$7 CY=$8 PAN=$9
S=$(python3 -c "print(1080/$WIN)")
FW=$(python3 -c "print(int(round(3840*$S/2)*2))"); FH=$(python3 -c "print(int(round(2160*$S/2)*2))")
Y=$(python3 -c "print(int(round(-($CY-$WIN*16/9/2)*$S)))")
ffmpeg -v error -y -ss $SS -i "$IN" -frames:v $N -filter_complex "\
[0:v]setpts=N/30/TB,split[a][b];\
[a]crop=1215:2160:1312:0,scale=1080:1920,gblur=sigma=40,eq=brightness=-0.18:saturation=0.8[bg];\
[b]scale=${FW}:${FH}:flags=lanczos[fg];\
[bg][fg]overlay=x='-($XA+($XB-$XA)*(0.5-0.5*cos(PI*min(t/$PAN\,1))))*$S':y=$Y,fps=30[v]" \
-map "[v]" -an -c:v libx264 -crf 14 -pix_fmt yuv420p -r 30 "$OUT"
