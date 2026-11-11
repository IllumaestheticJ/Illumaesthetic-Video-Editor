#!/bin/bash
# Re-render a frame range of a final shot in fresh Blender processes (chunks), overwriting the frames in place.
# Used after s8_explode went black from frame 57 on in one long persistent-data render (fresh renders are fine).
# usage: rerender.sh <shot> <first> <last> [chunk]
cd "$(dirname "$0")/../../.."
s=$1; a=$2; b=$3; n=${4:-25}
sp=$(python projects/mazda-miata-na/tools/shots.py final $s)
for ((i=a; i<=b; i+=n)); do
  j=$(( i+n-1 < b ? i+n-1 : b ))
  python -c "import json,sys;d=json.load(open('$sp'));d['frames']=list(range($i,$j+1));json.dump(d,open('$sp.chunk','w'))"
  blender -b -P projects/ferrari-296/tools/shot.py -- $sp.chunk > /home/user/media/work/miata/renders/rerender_${s}_$i.log 2>&1
  echo "$(date +%T) $s $i-$j"
done
echo DONE
