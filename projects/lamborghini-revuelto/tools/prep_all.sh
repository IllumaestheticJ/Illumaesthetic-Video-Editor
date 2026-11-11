#!/bin/bash
# levelled STLs (lev/) -> footprint crop -> floor cut (z<8 mm) -> Blender .blend, all pinned to the full car's
# prep transform with --like (blend/car_4mm.json) so every part/state stays registered.
#   tools/prep_all.sh name [name ...]      (names of lev/<name>.stl; full car is prepped separately)
set -e
M=/home/user/media/lamborghini-revuelto; T=$(dirname "$0")
mkdir -p $M/clean $M/blend
for n in "$@"; do
  python -m ive crop $M/lev/$n.stl $M/clean/${n}_c.stl --footprint-from $M/lev/full_car_4mm.stl > /dev/null
  python $T/floorcut.py $M/clean/${n}_c.stl $M/clean/$n.stl && rm $M/clean/${n}_c.stl
  python -m ive prep -- --scan $M/clean/$n.stl --out $M/blend/$n.blend --units mm --like $M/blend/car_4mm.json --drop-islands ${ISL:-800} 2>&1 | grep IVE_PREP | cut -c1-200
done
