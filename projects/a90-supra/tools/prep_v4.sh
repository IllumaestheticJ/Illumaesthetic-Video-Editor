#!/bin/bash
# v4 blends: strict fender re-cut + hood / left tail lamp cut out of the body + underbody plastics. All prepped --like the car.
cd "$(dirname "$0")/../../.."; W=/home/user/media/work/a90; V=$W/v3; B=$W/blend3; L=$W/lamp
prep(){ [ -s $B/$2.blend ] || flock $W/blender.lock python -m ive prep -- --scan "$1" --out $B/$2.blend --like $W/blend/car.json >/dev/null 2>&1; echo "$2 $(ls -la $B/$2.blend | awk '{print $5}')"; }
mkdir -p $B/old_v32
for n in body_c skinc_fender fillc_fender partc_fender; do [ -f $B/old_v32/$n.blend ] || { mv $B/$n.blend $B/old_v32/ 2>/dev/null; mv $B/$n.json $B/old_v32/ 2>/dev/null; }; done
prep $V/body4.stl body_c
prep $V/skin_fender.stl skinc_fender; prep $V/fill_fender.stl fillc_fender; prep $V/part_fender.stl partc_fender
prep $V/skin_hood.stl skin_hood; prep $V/hood_15.stl part_hood; prep $V/skin_lamp.stl skin_lamp
for n in lens_L3 housing_L insert_L; do prep $L/${n}_w.stl lamp_${n%%_*}; done
for f in $V/pl_*.stl; do n=$(basename $f .stl); prep $f $n; done
echo PREP_V4_DONE
