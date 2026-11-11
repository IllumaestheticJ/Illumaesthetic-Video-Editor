#!/bin/bash
# Label overlay for each v2 shot from its final render's camera anchors: build_labels.sh <shot> ...
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  n=$(python -c "import json;print(json.load(open('projects/nissan-frontier/${TIMING:-timing_v2.json}'))['frames']['$s'])")
  python projects/nissan-frontier/tools/labels.py /home/user/media/nissan-frontier/specs/${s}_final_anchors.json \
    projects/nissan-frontier/${TIMING:-timing_v2.json} /home/user/media/work/frontier/out/labels_$s.mov --shot $s --secs $(python -c "print($n/30)")
done
