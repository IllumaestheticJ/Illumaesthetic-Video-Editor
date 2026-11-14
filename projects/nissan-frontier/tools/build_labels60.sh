#!/bin/bash
# 60 fps label overlays from the 60 fps render anchors: build_labels60.sh <shot> ...
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  n=$(python -c "import json;print(json.load(open('projects/nissan-frontier/timing_v12.json'))['frames']['$s'])")
  python projects/nissan-frontier/tools/labels.py /home/user/media/nissan-frontier/specs/${s}_60_anchors.json \
    projects/nissan-frontier/timing_v12.json /home/user/media/work/frontier/out/labels60_$s.mov --shot $s --secs $(python -c "print($n/60)") --fps 60
done
