#!/bin/bash
# v3 tail clip: sH (silver) -> listing grey (second clay render, crossfade output frames 96-126) -> 0.5 s dissolve (129-144) into
# the listing WebZoom. 144 + 95 - 15 = 224 frames @30. The dissolve is scan -> web, never IRL -> scan.
R=/home/user/media/work/mr2/renders3; W=/home/user/media/work/out/webzoom_mr2_v2.mp4
for i in $(seq 1 48); do f=$R/sHc/f_$(printf %04d $i).png; [ -e $f ] || cp $R/sHc/f_0049.png $f; done
MI="minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=1080:1920:flags=lanczos,trim=end_frame=144,setpts=PTS-STARTPTS,format=gbrp"
ffmpeg -y -v error -framerate 15.102 -i $R/sH/f_%04d.png -framerate 15.102 -i $R/sHc/f_%04d.png -i $W -filter_complex \
"[0:v]$MI[a];[1:v]$MI[b];[a][b]blend=all_expr='A+(B-A)*clip((N-96)/30\,0\,1)',format=yuv420p,fps=30,settb=1/30[s];[2:v]fps=30,scale=1080:1920,format=yuv420p,settb=1/30[w];[s][w]xfade=transition=fade:duration=0.5:offset=4.3[v]" \
 -map "[v]" -c:v libx264 -crf 12 -preset fast -pix_fmt yuv420p $R/tail_v3.mp4
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $R/tail_v3.mp4
