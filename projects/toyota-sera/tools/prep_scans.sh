#!/bin/bash
# Toyota Sera scan prep. Every raw state scan: decimate (vertex clustering, out of core) -> apply the ONE levelling
# transform fitted on the full car (projects/huracan-evo/tools/level.py fit; flip_y so the nose is at -Y) ->
# crop ground with the full car's footprint -> ive prep --like car4.json (never re-normalise a part).
# States that stick out of the footprint (open door) are cropped with their own footprint instead.
#   prep_scans.sh <cell_mm> "raw1.stl" "raw2.stl" ...
set -e
cd /home/user/Illumaesthetic-Video-Editor
S=/home/user/media/toyota-sera
CELL=$1; shift
mkdir -p $S/dec $S/lev $S/clean $S/prep
for g in "$@"; do
  n=$(basename "$g" .stl | sed 's/Toyota Sera //' | tr 'A-Z' 'a-z' | sed 's/[ ,]\+/_/g')_${CELL}mm
  python -m ive decimate "$g" $S/dec/$n.stl --cell $CELL > /dev/null
  python projects/huracan-evo/tools/level.py apply $S/level.json $S/dec/$n.stl $S/lev/$n.stl > /dev/null
  case $n in
    door_open*) python -m ive crop $S/lev/$n.stl $S/clean/$n.stl > /dev/null; extra="";;  # own footprint includes the open door
    *) python -m ive crop $S/lev/$n.stl $S/clean/$n.stl --footprint-from $S/lev/full_car_4mm.stl > /dev/null; extra="";;
  esac
  echo "$n $(python -m ive prep -- --scan $S/clean/$n.stl --out $S/prep/$n.blend --units mm --like $S/prep/car4.json --drop-islands 1500 $extra | grep -o '"faces_out": [0-9]*')"
done
echo PREP_DONE
