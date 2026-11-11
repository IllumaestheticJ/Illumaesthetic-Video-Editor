#!/bin/bash
# Scan shots for the Sera scan-process reel. Usage: shots.sh preview|final [shot ...]
# preview = 20 % res, 4 spp, 6 fps; final = 75 % res, 12 spp, 15 fps (brief). Serial, one Blender at a time.
set -e
cd /home/user/Illumaesthetic-Video-Editor
W=/home/user/media/work/sera; P=projects/toyota-sera-scan-process
MODE=$1; shift
if [ "$MODE" = final ]; then Q="--res-pct 75 --samples 12 --fps 15"; OUT=$W/renders/final; else Q="--res-pct 20 --samples 4 --fps 6"; OUT=$W/renders/prev; fi
python -m ive lookat $W/cam_rear.json --loc=1.55,-6.4,1.3 --target=-0.25,-1.9,0.35 --focal 40 --sensor 23.3 --size 1080x1920 >/dev/null
python -m ive lookat $W/cam_front_wide.json --loc=3.30,5.70,1.55 --target=0.62,2.05,1.10 --focal 46 --sensor 23.3 --size 1080x1920 >/dev/null
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
  esac
  echo "DONE $s $(date +%T)"
done
