#!/bin/bash
# v3 render meshes: full-res blends for hero shots + 4 mm lite copies for wides, all prepped --like the car (one frame).
cd "$(dirname "$0")/../../.."; W=/home/user/media/work/a90; V=$W/v3; B=$W/blend3
prep(){ [ -s $B/$2.blend ] || flock $W/blender.lock python -m ive prep -- --scan "$1" --out $B/$2.blend --like $W/blend/car.json >/dev/null 2>&1; echo "$2 $(ls -la $B/$2.blend | awk '{print $5}')"; }
[ -s $V/fill_rbump_15.stl ] || python -m ive decimate --cell 1.5 $V/fill_rbump.stl $V/fill_rbump_15.stl >/dev/null
for n in body fill_fbump fill_fduct fill_fender fill_dtrim fill_skirts part_fbump part_fender part_dtrim part_uskirt part_lskirt part_rbump; do prep $V/$n.stl $n; done
prep $V/fill_rbump_15.stl fill_rbump
for n in body fill_fbump fill_fender fill_dtrim fill_skirts fill_rbump part_fbump part_fender part_dtrim part_uskirt part_lskirt part_rbump; do
  [ -s $V/lite/$n.stl ] || python -m ive decimate --cell 4 $V/$n.stl $V/lite/$n.stl >/dev/null; prep $V/lite/$n.stl L_$n; done
S2=/home/user/media/a90-supra/scans2
prep "$S2/chassis/Supra Radar Cover (600k).stl" radar_cover
prep "$S2/chassis/Supra Radar Mounting Grille (2.2M).stl" radar_grille
prep "$S2/interior/Interior_(2.4m).stl" interior
prep "$S2/interior/Center Console (700k).stl" console
for c in FR FL RR RL; do for p in wheel rotor caliper coilover spring damper; do [ -f $W/corners/${c}_$p.stl ] && prep $W/corners/${c}_$p.stl c_${c}_$p; done; done
echo PREP_V3_DONE
