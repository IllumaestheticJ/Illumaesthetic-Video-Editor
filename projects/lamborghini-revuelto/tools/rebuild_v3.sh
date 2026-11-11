#!/bin/bash
# v3 geometry: everything re-cleaned with tools/clean2.py (real tyre bottoms, no ive crop), same --like frame.
set -e
cd /home/user/Illumaesthetic-Video-Editor
M=/home/user/media/lamborghini-revuelto; T=projects/lamborghini-revuelto/tools; C=$M/clean3; B=$M/blend3
PARTS="front_bumper head_lights fender side_skirt_front side_skirt_rear side_fin side_mirrors rear_bumper_forced rear_wing tail_light_r tail_light_l"
STATES="st_hood_open st_front_bumper_headlights_removed st_rear_bumper_off_tl_off st_rear_wing_removed st_fender_removed st_side_skirts_fin_removed"
for n in $PARTS $STATES; do python $T/clean2.py $M/lev/$n.stl $C/$n.stl; done
python $T/croppart.py $C/side_mirrors.stl $C/mirror_head.stl "985,1200,-850,-400,550,900"
python $T/hood.py $C/car_3mm.stl $C/st_hood_open.stl $C/hood.stl $M/comp/hood_open_pts3.npy
python $T/composite.py $C/car_3mm.stl $M/comp/base3.stl --parts $C/front_bumper.stl $C/head_lights.stl $C/hood.stl $C/fender.stl $C/side_skirt_front.stl $C/side_skirt_rear.stl $C/side_fin.stl $C/mirror_head.stl $C/rear_bumper_forced.stl $C/rear_wing.stl $C/tail_light_r.stl $C/tail_light_l.stl --states $C/st_front_bumper_headlights_removed.stl $C/st_hood_open.stl $C/st_fender_removed.stl $C/st_side_skirts_fin_removed.stl $C/st_rear_bumper_off_tl_off.stl $C/st_rear_wing_removed.stl
python -m ive decimate $M/comp/base3.stl $C/base.stl --cell 3 | grep out_tris
for n in front_bumper head_lights fender side_fin rear_bumper_forced rear_wing tail_light_r tail_light_l hood mirror_head; do
  python -m ive prep -- --scan $C/$n.stl --out $B/$n.blend --units mm --like $M/blend/car_4mm.json --drop-islands 500 | grep -o '"faces_out": [0-9]*' | sed "s/^/$n /"
done
for n in side_skirt_front side_skirt_rear; do python -m ive prep -- --scan $C/$n.stl --out $B/$n.blend --units mm --like $M/blend/car_4mm.json | grep -o '"faces_out": [0-9]*' | sed "s/^/$n /"; done
python -m ive prep -- --scan $C/base.stl --out $B/base.blend --units mm --like $M/blend/car_4mm.json --drop-islands 1500 | grep -o '"faces_out": [0-9]*' | sed "s/^/base /"
echo REBUILD3_DONE
