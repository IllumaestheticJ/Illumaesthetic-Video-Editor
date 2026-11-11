#!/bin/bash
# MR2 SW20 scan shots (finals): 75% res, 12 spp, 15 fps (assemble interpolates to 30). Run one at a time.
# usage: shots.sh [res_pct] [samples] [outroot] [shot...]
set -e
REPO=/home/user/Illumaesthetic-Video-Editor; P=$REPO/projects/toyota-mr2-sw20-scan-process; C=$P/match
W=/home/user/media/work/mr2; cd $W
PCT=${1:-75}; SPP=${2:-12}; OUT=${3:-$W/renders/final}; shift 3 || true
SHOTS=${@:-s1 s2 s3 s4}
R="blender -b -P $P/tools/render_plus.py --"
DOORS_OUT='--explode parts/door_L.blend:-1.0,0,0.15:0.1:0.45:z-360:0.3:0.95 --explode parts/door_R.blend:1.0,0,0.15:0.1:0.45:z360:0.3:0.95 --explode parts/ttop_L.blend:-0.3,0,0.7:0.15:0.5:z360:0.35:0.95 --explode parts/ttop_R.blend:0.3,0,0.7:0.15:0.5:z-360:0.35:0.95'
DOORS_IN='--explode parts/door_L.blend:-1.0,0,0.15:r0.1:0.75 --explode parts/door_R.blend:1.0,0,0.15:r0.1:0.75 --explode parts/ttop_L.blend:-0.3,0,0.7:r0.15:0.8 --explode parts/ttop_R.blend:0.3,0,0.7:r0.15:0.8'
for s in $SHOTS; do
  t0=$(date +%s)
  case $s in
    s1) IVE_END_CAM=$C/cam_s1_end.json $R --scene interior.blend --camera $C/cam_rear.json --out $OUT/s1_rear --look silver --res-pct $PCT --samples $SPP --fps 15 --seconds 3.3 ;;
    s2) IVE_END_CAM=$C/cam_s2_end.json $R --scene ttop.blend --camera $C/cam_side.json --out $OUT/s2_side --look silver --res-pct $PCT --samples $SPP --fps 15 --seconds 3.3 \
          --explode "parts/ttop_L.blend:-0.25,0,0.75:0.2:0.8:z-90:0.3:0.9" --explode "parts/ttop_R.blend:0.25,0,0.75:0.2:0.8:z90:0.3:0.9" ;;
    s3) IVE_END_CAM=$C/cam_s3_end.json $R --scene ttop.blend --camera $C/cam_s3_start.json --out $OUT/s3_parts --look silver --res-pct $PCT --samples $SPP --fps 15 --seconds 4.4 $DOORS_OUT ;;
    s4) IVE_END_CAM=$C/cam_s4_end.json $R --scene ttop.blend --camera $C/cam_s3_end.json --out $OUT/s4_xray --look xray --res-pct $PCT --samples $SPP --fps 15 --seconds 4.9 $DOORS_IN ;;
  esac > $OUT.$s.log 2>&1
  echo "$s done in $(( $(date +%s) - t0 )) s"
done
