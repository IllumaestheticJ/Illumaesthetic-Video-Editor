#!/bin/bash
# Reproduce the Miata scan prep after fetch+decimate (see clips.md). Levelled mm in $W/lvl*, prepped in $W/prep.
set -e
cd /home/user/Illumaesthetic-Video-Editor
T=projects/mazda-miata-nd/tools; W=/home/user/media/work/miata; D=/home/user/media/mazda-miata-nd/scans/dec; L=$W/lvlp
python $T/level.py fit $D/car_6mm.stl $W/level.json
for c in 4 3 2; do python $T/level.py apply $W/level.json $D/car_${c}mm.stl $W/lvl/car_${c}mm.stl; python -m ive crop $W/lvl/car_${c}mm.stl $W/lvl/car${c}_clean.stl; done
for f in $D/*.stl; do b=$(basename $f); case $b in car_*) continue;; esac; python $T/level.py apply $W/level.json $f $L/$b; done
python -m ive prep -- --scan $W/lvl/car4_clean.stl --out $W/prep/car4.blend --units mm --drop-islands 3000
python $T/hinge.py $W/lvl/car4_clean.stl $L/fbumperoff_hoodopen_3mm.stl $W/hinge/hood --end front
python $T/hinge.py $W/lvl/car4_clean.stl $L/rear_trunkopen_bumperoff_3mm.stl $W/hinge/trunk --end rear
python $T/extract.py $W/lvl/car4_clean.stl $W/parts/hood.stl --cy -1.0 --zmin 0.55 --poly "150,300 340,355 530,398 740,350 928,292 926,835 752,1015 330,1020 158,880"
python $T/extract.py $W/lvl/car4_clean.stl $W/parts/trunk.stl --cy 1.0 --zmin 0.7 --poly "268,160 800,160 866,432 200,432"
python $T/diff.py $W/lvl/car4_clean.stl $L/skirt_off_3mm.stl $W/diff/skirtbox --thr 8 --near 200 --box=-900,-450,-690,925,40,360
cp $W/diff/skirtbox_gone.stl $W/parts/skirt.stl; cp $L/fbumper_3mm.stl $W/parts/fbumper.stl; cp $L/rbumper_inside_3mm.stl $W/parts/rbumper.stl
# mirrors_2mm split at levelled x=124 (car centreline) -> mirror_r / mirror_l; skirt_off minus tris below the skirt (z<173 mm) -> skirt_off_nostands
# composites: see editlog (projects/ferrari-296/tools/composite.py --cut 12)
