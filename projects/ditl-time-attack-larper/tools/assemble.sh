#!/bin/bash
# assemble.sh <out.mp4> <shot> [<shot> ...] [-- audio.wav] : frames/sNN/*.png -> 1080x1920 (1:1 picture under the title band, game crunch), hard cuts.
O=/home/user/media/ditl-time-attack-larper/frames; out=$1; shift; shots=(); aud=""
while [ $# -gt 0 ]; do if [ "$1" == "--" ]; then aud=$2; break; fi; shots+=($1); shift; done
VF="scale=1080:1080:flags=bicubic,unsharp=7:7:1.6:7:7:0.0,eq=saturation=1.25:contrast=1.08,format=rgb24,lutrgb=r='round(val/20)*20':g='round(val/20)*20':b='round(val/20)*20',pad=1080:1920:0:420:black,drawtext=fontfile=/usr/share/fonts/opentype/inter/Inter-Regular.otf:text='Day in the life of an':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=196,drawtext=fontfile=/usr/share/fonts/opentype/inter/Inter-Regular.otf:text='average track guy':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=264"
T=$(mktemp -d); : > $T/list.txt
for n in "${shots[@]}"; do
  d=$O/s$(printf %02d $n); ffmpeg -v error -y -framerate 30 -start_number 1 -i $d/%04d.png -vf "$VF" -c:v libx264 -pix_fmt yuv420p -crf 17 -r 30 $T/s$n.mp4
  echo "file '$T/s$n.mp4'" >> $T/list.txt
done
if [ -n "$aud" ]; then
  ffmpeg -v error -y -f concat -safe 0 -i $T/list.txt -c copy $T/v.mp4 && ffmpeg -v error -y -i $T/v.mp4 -i "$aud" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest "$out"
else
  ffmpeg -v error -y -f concat -safe 0 -i $T/list.txt -c copy "$out"
fi
rm -rf $T; ffprobe -v error -show_entries format=duration -of csv=p=0 "$out"
