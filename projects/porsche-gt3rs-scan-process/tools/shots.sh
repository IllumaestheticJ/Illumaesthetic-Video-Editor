#!/bin/bash
# Scan shots for the GT3 RS drift -> scan reel. Usage: shots.sh <shot> [res_pct samples]  (finals: 75 12, 15 fps)
set -e
cd "$(dirname "$0")/../../.."
W=/home/user/media/work/gt3rs; P=$W/parts; R=projects/porsche-gt3rs-scan-process/tools/render.sh
PCT=${2:-75}; SPP=${3:-12}; OUT=$W/renders; mkdir -p $OUT
XR="--look xray --accent 0.70,0.74,0.80 --part-look silver --res-pct $PCT --samples $SPP --fps 15"
# parts at rest (offset 0) so every shot shows all 12 scanned aero parts in silver
FRONT="front_lower_lip front_grille_trim front_bumper_strake hood_vent_fins_x3 fender_vent rear_qpanel_intake_1"
REAR="rear_diffuser_1 rear_diffuser_trim_outer rear_bumper_strake"
SIDE="side_skirt_upper side_skirt_strake rear_qpanel_intake_2"
rest() { for p in "$@"; do echo -n " --explode $P/$p.blend:0,0,0:0:1"; done; }
case $1 in
x1) # front aero explode: out 0.08-0.45, spin left/right 0.45-0.95 (4.0 s)
  $R --scene $W/car_carved.blend --camera $W/cams/x1.json --out $OUT/x1/ $XR --seconds 4.0 --move orbit --move-amount 12 --ease ease_in_out \
   --explode "$P/front_lower_lip.blend:0.15,0,-0.4:0.08:0.42:z25:0.45:0.95" \
   --explode "$P/front_grille_trim.blend:0.25,0,-0.75:0.1:0.45:z-30:0.48:0.95" \
   --explode "$P/front_bumper_strake.blend:0.1,-0.15,-0.55:0.1:0.45:z180:0.45:0.95" \
   --explode "$P/hood_vent_fins_x3.blend:0,0,0.55:0.12:0.45:z180:0.48:0.95" \
   --explode "$P/fender_vent.blend:0,-0.1,0.85:0.12:0.45:z-180:0.45:0.95" \
   --explode "$P/rear_qpanel_intake_1.blend:0,-0.1,0.6:0.15:0.5:z180:0.5:0.95" $(rest $REAR $SIDE) ;;
x2) # rear explode (2.9 s)
  $R --scene $W/car_carved.blend --camera $W/cams/x2.json --out $OUT/x2/ $XR --seconds 2.9 --move orbit --move-amount -10 --ease ease_in_out \
   --explode "$P/rear_diffuser_1.blend:-0.1,0,-0.55:0.05:0.45:z-25:0.45:0.95" \
   --explode "$P/rear_diffuser_trim_outer.blend:-0.2,0,-0.95:0.08:0.48:z25:0.48:0.95" \
   --explode "$P/rear_bumper_strake.blend:-0.1,0.1,0.75:0.08:0.48:z180:0.45:0.95" $(rest $FRONT $SIDE) ;;
xs) # left side parts explode (4.0 s)
  $R --scene $W/car_carved.blend --camera $W/cams/xs.json --out $OUT/xs/ $XR --seconds 4.0 --move orbit --move-amount 14 --ease ease_in_out \
   --explode "$P/side_skirt_upper.blend:0,0.3,-0.45:0.08:0.45:z20:0.45:0.95" \
   --explode "$P/side_skirt_strake.blend:0,0.5,0.25:0.1:0.45:z180:0.45:0.95" \
   --explode "$P/rear_qpanel_intake_2.blend:0,0.2,0.6:0.12:0.48:z-180:0.48:0.95" $(rest $FRONT $REAR) ;;
x3) # reassembly: translate home on the dense kicks (27.32 27.72 28.25 29.14 29.52 30.13 from shot start 26.38), orbit ends on cam_listing, morph to listing grey (6.2 s)
  L=6.2; f() { python3 -c "print(round($1/$L,4))"; }
  $R --scene $W/car_carved.blend --camera $W/cams/x3_start.json --out $OUT/x3/ $XR --seconds $L --move orbit --move-amount 30 --ease ease_in_out --look-at 0,0,0.6 \
   --morph-to-clay $(f 4.35),$(f 5.3) --morph-bg 0.012,0.014,0.013 --clay-color 0.06,0.06,0.06 \
   --explode "$P/front_lower_lip.blend:0.15,0,-0.4:r$(f 0.14):$(f 0.94)" \
   --explode "$P/front_grille_trim.blend:0.25,0,-0.75:r$(f 0.14):$(f 0.94)" \
   --explode "$P/front_bumper_strake.blend:0.1,-0.15,-0.55:r$(f 0.54):$(f 1.34)" \
   --explode "$P/hood_vent_fins_x3.blend:0,0,0.55:r$(f 0.54):$(f 1.34)" \
   --explode "$P/fender_vent.blend:0,-0.1,0.85:r$(f 1.07):$(f 1.87)" \
   --explode "$P/rear_qpanel_intake_1.blend:0,-0.1,0.6:r$(f 1.07):$(f 1.87)" \
   --explode "$P/rear_diffuser_1.blend:-0.1,0,-0.55:r$(f 1.96):$(f 2.76)" \
   --explode "$P/rear_diffuser_trim_outer.blend:-0.2,0,-0.95:r$(f 1.96):$(f 2.76)" \
   --explode "$P/rear_bumper_strake.blend:-0.1,0.1,0.75:r$(f 2.34):$(f 3.14)" \
   --explode "$P/side_skirt_upper.blend:0,0.3,-0.45:r$(f 2.34):$(f 3.14)" \
   --explode "$P/side_skirt_strake.blend:0,0.5,0.25:r$(f 2.95):$(f 3.75)" \
   --explode "$P/rear_qpanel_intake_2.blend:0,0.2,0.6:r$(f 2.95):$(f 3.75)" ;;
esac
