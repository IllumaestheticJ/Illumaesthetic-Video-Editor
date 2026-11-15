#!/bin/bash
# 60 fps raw queue, one Blender at a time, resumable: render60.sh shot ...
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  spec=$(python projects/nissan-frontier/tools/render60.py $s)
  if [ -z "$spec" ]; then echo "$s complete"; continue; fi
  t0=$(date +%s)
  blender -b -P projects/nissan-frontier/tools/shot.py -- $spec > /home/user/media/nissan-frontier/chk/final60_$s.log 2>&1
  echo "$s rc=$? $(( $(date +%s)-t0 ))s frames=$(ls /home/user/media/work/frontier/renders/final60/$s | wc -l)"
done
echo QUEUEDONE
