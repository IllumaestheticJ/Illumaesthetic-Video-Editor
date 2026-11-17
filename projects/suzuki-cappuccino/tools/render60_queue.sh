#!/bin/bash
# true 60 fps, native (no interpolation), one shot at a time; re-running resumes (shot.py skips existing frames)
cd /home/user/Illumaesthetic-Video-Editor/projects/suzuki-cappuccino/tools
for s in s2_frontbumper s3_engine x1_layers x2_reassemble s5_rear s1_whole; do
  blender -b -P shot.py -- /home/user/media/work/cappuccino/shots60/$s.json > /home/user/media/work/cappuccino/render60_$s.log 2>&1
  echo "$s $(ls /home/user/media/work/renders/cappuccino_v6_60/$s 2>/dev/null | wc -l) frames"
done
echo RENDERDONE60
