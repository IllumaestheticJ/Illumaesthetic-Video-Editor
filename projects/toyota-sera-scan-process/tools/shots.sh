#!/bin/bash
# Scan shots for the Sera scan-process reel. Usage: shots.sh preview|final [shot ...]
# preview = 20 % res, 4 spp, 6 fps; final = 75 % res, 12 spp, 15 fps (brief). Serial, one Blender at a time.
set -e
cd /home/user/Illumaesthetic-Video-Editor
W=/home/user/media/work/sera; P=projects/toyota-sera-scan-process
MODE=$1; shift; ORB=${ORB:-35}
if [ "$MODE" = final ]; then Q="--res-pct 75 --samples 12 --fps 15"; OUT=$W/renders/final; else Q="--res-pct 20 --samples 4 --fps 6"; OUT=$W/renders/prev; fi
python -m ive lookat $W/cam_rear.json --loc=1.55,-6.4,1.3 --target=-0.25,-1.9,0.35 --focal 40 --sensor 23.3 --size 1080x1920 >/dev/null
python -m ive lookat $W/cam_front_wide.json --loc=3.30,5.70,1.55 --target=0.62,2.05,1.10 --focal 46 --sensor 23.3 --size 1080x1920 >/dev/null
python -m ive lookat $W/cam_foff.json --loc=3.49,5.41,1.40 --target=0.55,1.75,0.05 --focal 38 --sensor 23.3 --size 1080x1920 >/dev/null
python -m ive lookat $W/cam_fbeam.json --loc=1.86,2.30,0.70 --target=0.54,1.25,0.36 --focal 30 --sensor 23.3 --size 1080x1920 >/dev/null
python -m ive lookat $W/cam_doorsv3.json --loc=3.6,1.6,2.3 --target=0.0,-0.1,0.85 --focal 28 --sensor 23.3 --size 1080x1920 >/dev/null
python -m ive lookat $W/cam_roff.json --loc=-0.01,-6.32,1.40 --target=-0.45,-1.75,0.05 --focal 38 --sensor 23.3 --size 1080x1920 >/dev/null
python -m ive lookat $W/cam_rbeam.json --loc=0.36,-3.30,0.85 --target=-0.18,-1.45,0.50 --focal 30 --sensor 23.3 --size 1080x1920 >/dev/null
for s in "${@:-s1 s3 s5 s6 s7}"; do
  case $s in
  s1) python -m ive render -- --scene $W/full.blend --camera $P/match/cam_open.json --look silver --move push --move-amount 0.10 --ease ease_in_out --seconds 2.4 $Q --out $OUT/s1_open ;;
  s3) python -m ive render -- --scene $W/compB.blend --camera $W/cam_rear.json --look silver --move orbit --move-amount -12 --ease ease_in_out --seconds 3.0 $Q \
        --explode "$W/rbump_2mm.blend:-0.258,-0.966,-0.75:0.05:0.45:z180:0.40:0.95" --out $OUT/s3_rear ;;
  s5) python -m ive render -- --scene $W/compA.blend --camera $P/match/cam_front.json --look silver --move push --move-amount 0.04 --ease ease_out --seconds 1.2 $Q --out $OUT/s5_front ;;
  s6) python -m ive render -- --scene $W/compA.blend --camera $W/cam_front_wide.json --look silver --move orbit --move-amount 10 --ease ease_in_out --seconds 3.0 $Q \
        --explode "$W/fbump_2mm.blend:0.232,0.869,1.15:0.05:0.45:z180:0.42:0.95" --out $OUT/s6_frontx ;;
  s7) python -m ive render -- --scene $W/xbase.blend --camera $P/match/cam_xray_start.json --look xray --move orbit --move-amount 40 --look-at 0,0,0.7 --ease ease_in_out --seconds 4.8 $Q \
        --explode "$W/fbump_2mm.blend:0.116,0.435,0.95:r0.08:0.55" --explode "$W/rbump_2mm.blend:-0.400,-1.497,0.6:r0.15:0.62" \
        --morph-to-clay 0.80,1.0 --morph-bg 0.0080,0.0090,0.0080 --clay-color 0.05,0.05,0.05 --out $OUT/s7_xray ;;
  f_off) python -m ive render -- --scene $W/compA.blend --camera $W/cam_foff.json --look silver --move push --move-amount 0.08 --ease ease_in_out --seconds 2.6 $Q \
        --explode "$W/fbump_2mm.blend:0.181,0.676,-0.80:0.08:0.45:z170:0.40:0.85:0.06,0.24,0.05" --out $OUT/v3_f_off ;;
  f_beam) python -m ive render -- --scene $W/compA.blend --camera $W/cam_fbeam.json --look silver --move push --move-amount 0.04 --ease ease_out --seconds 2.0 $Q --out $OUT/v3_f_beam ;;
  doors) python -m ive render -- --scene $W/doors.blend --camera $W/cam_doorsv3.json --look silver --move orbit --move-amount -20 --look-at=0,-0.1,0.9 --ease ease_in_out --seconds 2.6 $Q --out $OUT/v3_doors ;;
  r_off) python -m ive render -- --scene $W/compB.blend --camera $W/cam_roff.json --look silver --move push --move-amount 0.08 --ease ease_in_out --seconds 2.6 $Q \
        --explode "$W/rbump_2mm.blend:-0.181,-0.676,-0.85:0.08:0.45:z170:0.40:0.85:-0.04,-0.14,0.0" --out $OUT/v3_r_off ;;
  r_beam) python -m ive render -- --scene $W/compB.blend --camera $W/cam_rbeam.json --look silver --move push --move-amount 0.04 --ease ease_out --seconds 2.0 $Q --out $OUT/v3_r_beam ;;
  x3) python -m ive render -- --scene $W/xbase.blend --camera $P/match/cam_xray_start.json --look xray --move orbit --move-amount 40 --look-at=0,0,0.7 --ease ease_in_out --seconds 3.6 $Q \
        --explode "$W/fbump_2mm.blend:0.116,0.435,0.95:r0.0:0.167" --explode "$W/rbump_2mm.blend:-0.400,-1.497,0.6:r0.0:0.333" \
        --morph-to-clay 0.83,1.0 --morph-bg 0.0080,0.0090,0.0080 --clay-color 0.05,0.05,0.05 --out $OUT/v3_xray ;;
  f_design) python -m ive render -- --scene $W/xbase.blend --camera $W/cam_foff.json --look silver --move push --move-amount 0.10 --ease ease_in_out --seconds 2.0 $Q \
        --explode "$W/kit_front_p.blend:0.181,0.676,-0.80:r0.05:0.60" --out $OUT/v4_f_design ;;
  r_design) python -m ive render -- --scene $W/xbase.blend --camera $W/cam_roff.json --look silver --move push --move-amount 0.10 --ease ease_in_out --seconds 2.0 $Q \
        --explode "$W/kit_rear_p.blend:-0.181,-0.676,-0.85:r0.05:0.60" --explode "$W/kit_front_p.blend:0,0,0:0:1" --out $OUT/v4_r_design ;;
  r_design5) python -m ive render -- --scene $W/xbase.blend --camera $W/cam_roff.json --look silver --move push --move-amount 0.10 --ease ease_in_out --seconds 2.0 $Q \
        --explode "$W/kit_rear_p.blend:-0.181,-0.676,-0.85:r0.0:0.45" --explode "$W/kit_duck.blend:0,0,0.6:r0.40:0.85" --explode "$W/kit_front_p.blend:0,0,0:0:1" --out $OUT/v5_r_design ;;
  kit_final) python -m ive render -- --scene $W/kitbase.blend --camera $P/match/cam_fin_start.json --look silver --move push --move-amount 0.318182 --look-at=0,0,1.5 --ease ease_in_out --seconds 2.0 $Q \
        --explode "$W/kit_front_p.blend:0,0,0:0:1" --explode "$W/kit_rear_p.blend:0,0,0:0:1" --explode "$W/kit_duck.blend:0,0,0:0:1" \
        --explode "$W/kit_skirtL.blend:-0.58,0.155,0:r0.0:0.50" --explode "$W/kit_skirtR.blend:0.58,-0.155,0:r0.0:0.50" --out $OUT/v5_kit_final ;;
  esac
  echo "DONE $s $(date +%T)"
done
