#!/bin/bash
# still.sh <shot> <frames,comma> : render stills at 360 px and tile them (fast check)
O=/home/user/media/ditl-gr-corolla/frames/chk; mkdir -p $O; cd "$(dirname "$0")"
blender -b --python gr_shots.py -- $1 $O $2 ${3:-360} 8 2>&1 | grep -E "Error|Traceback|File \"|line [0-9]" 
n=$(printf %02d $1); ins=""; c=0; for f in ${2//,/ }; do ins="$ins -i $O/s${n}_f$(printf %03d $f).png"; c=$((c+1)); done
[ $c -gt 1 ] && ffmpeg -v error -y $ins -filter_complex "hstack=$c" $O/sheet_s$n.jpg
