#!/bin/bash
# true 30 fps native renders (interpolated to 60 in the assembly); one shot at a time; re-run resumes
cd /home/user/Illumaesthetic-Video-Editor/projects/suzuki-cappuccino/tools
for s in x1_layers x2_reassemble s2_frontbumper s3_engine s5_rear s1_whole; do
  blender -b -P shot.py -- /home/user/media/work/cappuccino/shots30/$s.json > /home/user/media/work/cappuccino/render30_$s.log 2>&1
  echo "$s $(ls /home/user/media/work/renders/cappuccino_v6_30/$s 2>/dev/null | wc -l) frames"
done
echo RENDERDONE30
