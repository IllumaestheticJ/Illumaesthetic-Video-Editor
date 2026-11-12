#!/bin/bash
# v4: e1 framing preview, then every v4 final, strictly one Blender at a time (resume: finished frames are skipped).
cd "$(dirname "$0")/../../.."
/usr/local/bin/blender -b -P projects/toyota-gr86/tools/shot.py -- projects/toyota-gr86/shots/e1_lid_hinge_pv.json > /home/user/media/work/gr86/preview_e1.log 2>&1
echo "e1 preview $(ls /home/user/media/work/gr86/preview/e1_lid_hinge | wc -l)"
bash projects/toyota-gr86/tools/render_all.sh c1_hood_hinge c2_hood_off c3_front_bumper_off c4_front_structure d_mirror4 \
  e1_lid_hinge e2_lid_off_cargo e3_rear_bumper_off e4_rear_beam f1_reverse_light f2_plate_light h1_reassemble h2_hero
