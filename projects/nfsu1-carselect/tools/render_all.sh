#!/bin/bash
# one Blender session per car along the tracked camera path, wheels turning (resumable: existing frames are skipped)
cd /home/user/media/work/nfsu1-carselect
G=/home/user/media/nfsu1-carselect/glbs; P=/home/user/Illumaesthetic-Video-Editor/projects/nfsu1-carselect
C="--res 1608x904 --samples 16 --ground none --rig-json $P/rig_garage.json --tail-glow 2.5"
for car in "$@"; do case $car in
 na) blender -b -P $P/tools/render_car.py -- --glb $G/eps-mazda-mx5-na-v15.glb --livery livery_ak4some --hide body_front_bumper_stock,trim_front_bumper_stock,body_side_skirts_stock,trim_side_skirts_stock --cam-anim track/cams_spin_na.json $C --out renders/na ;;
 corolla) blender -b -P $P/tools/render_car.py -- --glb $G/eps-toyota-gr-corolla-v23.glb --livery livery_castrol --hide body_roof_spoiler_stock,part_front_lip,part_front_lip_2025,part_side_skirts,part_rear_spats,part_spoiler_extension --cam-anim track/cams_spin_corolla.json $C --out renders/corolla ;;
 delsol) blender -b -P $P/tools/render_car.py -- --glb $G/eps-honda-del-sol-v18.glb --hide body_front_fenders_stock,body_rear_quarters_stock --cam-anim track/cams_spin_delsol.json $C --out renders/delsol ;;
 frs) blender -b -P $P/tools/render_car.py -- --frs-green "/home/user/media/nfsu1-carselect/frs_green/GT2 Animation FRS-green.blend" --frs-parts $G/eps-toyota-86-zn6-v13.glb,$G/eps-mazda-rx8-v11.glb --cam-anim track/cams_spin_frs.json $C --out renders/frs ;;
esac; done
