#!/bin/bash
# v2 final renders, one Blender at a time (75 % res, 12 spp, 15 fps, persistent data OFF). Resumable.
cd "$(dirname "$0")"
for n in ${@:-s1_whole s2_frontbumper s3_engine s5_rear x1_layers x2_reassemble}; do
  s=$(date +%s); blender -b -P shot.py -- /home/user/media/work/cappuccino/shots_v2/$n.json > /home/user/media/work/cappuccino/render_v2_$n.log 2>&1
  echo "$n $(ls /home/user/media/work/renders/cappuccino_v2/$n | wc -l) frames $(( $(date +%s)-s )) s"
done
echo RENDERDONE
