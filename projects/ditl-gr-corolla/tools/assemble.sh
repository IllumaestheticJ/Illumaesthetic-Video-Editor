#!/bin/bash
# assemble.sh <audio.wav> <out.mp4> : all rendered shots in order, game look (crunch + banding), 1080x1920 layout with the title band
M=/home/user/media/ditl-gr-corolla; L=$M/frames/list.txt; : > $L
for n in 01 02 03 04 05 06 07 08 09 10 11 12 13 14; do for f in $M/frames/s$n/*.png; do echo "file '$f'" >> $L; echo "duration 0.0333333" >> $L; done; done
F=/usr/share/fonts/opentype/inter/Inter-Regular.otf
ffmpeg -v error -y -r 30 -f concat -safe 0 -i $L -i "$1" -vf "scale=1080:1080:flags=bicubic,unsharp=7:7:1.6:7:7:0.0,eq=saturation=1.25:contrast=1.08,format=rgb24,lutrgb=r='round(val/20)*20':g='round(val/20)*20':b='round(val/20)*20',pad=1080:1920:0:420:black,drawtext=fontfile=$F:text='Day in the life of an':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=196,drawtext=fontfile=$F:text='average GR Corolla owner':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=264,format=yuv420p" -r 30 -c:v libx264 -crf 17 -preset medium -c:a aac -b:a 256k -shortest "$2"
