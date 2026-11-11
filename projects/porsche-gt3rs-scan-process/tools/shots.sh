#!/bin/bash
# Scan shots for the GT3 RS scan-process reel. Usage: shots.sh <shot> [res_pct samples]   (finals: 75 12 @ 15 fps)
# Cameras: camA = 1:1 solve on v_0130_125744 @4.5 s (head-on), camC = 1:1 solve on v_0130_125720 @5.3 s (right side),
#          x2 = hand-placed rear-left 3/4, x3_start -> orbits onto cam_listing (silhouette fit to the listing's 360 viewer).
set -e
cd "$(dirname "$0")/../../.."
W=/home/user/media/work/gt3rs; P=$W/parts; R=projects/porsche-gt3rs-scan-process/tools/render.sh
PCT=${2:-75}; SPP=${3:-12}; OUT=${OUT:-$W/renders}; mkdir -p $OUT
SIL="--look silver --res-pct $PCT --samples $SPP --fps 15"
XR="--look xray --accent 0.70,0.74,0.80 --part-look silver --res-pct $PCT --samples $SPP --fps 15"
ALL="front_lower_lip front_grille_trim front_bumper_strake hood_vent_fins_x3 fender_vent rear_qpanel_intake_1 rear_diffuser_1 rear_diffuser_trim_outer rear_bumper_strake side_skirt_upper side_skirt_strake rear_qpanel_intake_2"
rest() { for p in $ALL; do case " $* " in *" $p "*) ;; *) echo -n " --explode $P/$p.blend:0,0,0:0:1";; esac; done; }
LA=1.0,-0.45,0.6
case $1 in
s1) # 1:1 match (head-on), silver, front wheels off like the real car; slow pull (3.83 s)
  $R --scene $W/car_noFW.blend --camera $W/cams/camA.json --out $OUT/s1/ $SIL --seconds 3.9 --move pull --move-amount 0.12 --look-at $LA --ease ease_out ;;
x1a) # same view continues in x-ray. v2 (review): parts end in clear background (below / above the car in screen space);
    # only the fender vent spins (its back shows the mounting structure) - lip, grille trim, strakes, hood fins just translate (3.9 s)
  # v2b (director): fender vent stays home here - it is the side shot's feature (was a speck in this view, shown twice)
  M="front_lower_lip front_grille_trim front_bumper_strake hood_vent_fins_x3"
  $R --scene $W/car_carved_noFW.blend --camera $W/cams/x1a_start.json --out $OUT/x1a/ $XR --seconds 3.9 --move pull --move-amount 0.18 --look-at $LA --ease ease_in_out \
   --explode "$P/front_lower_lip.blend:0.1,0,-0.38:0.05:0.4" \
   --explode "$P/front_grille_trim.blend:0.15,0,-0.68:0.08:0.45" \
   --explode "$P/front_bumper_strake.blend:0.05,0,-0.5:0.08:0.42" \
   --explode "$P/hood_vent_fins_x3.blend:0,0,0.55:0.1:0.45" $(rest $M) ;;
s2) # 1:1 match (right side, wheel arch) on the drop, silver hold (1.0 s)
  $R --scene $W/car_noFW.blend --camera $W/cams/camC.json --out $OUT/s2/ $SIL --seconds 1.1 ;;
xs2) # same camera, x-ray: rear-quarter intake + fender vent lift UP into clear background (not toward the lens) and spin -
    # both have useful backsides (clips / mounting structure). v2b: pull only 0.10 (car stays big); the intake (2.5 m from the lens)
    # flies forward-up toward the camera into clear space so it reads at ~7 % of frame width (3.8 s)
  M="rear_qpanel_intake_1 fender_vent"
  $R --scene $W/car_carved_noFW.blend --camera $W/cams/camC.json --out $OUT/xs2/ $XR --seconds 3.8 --move pull --move-amount 0.10 --look-at=-0.4,-0.9,0.8 --ease ease_in_out \
   --explode "$P/rear_qpanel_intake_1.blend:1.2,-1.0,0.7:0.06:0.42:z180:0.45:0.95" \
   --explode "$P/fender_vent.blend:0,-0.15,0.6:0.1:0.45:z-180:0.48:0.95" $(rest $M) ;;
x2b) # rear-left 3/4 (4.0 s). v2: rear strake goes DOWN-left instead of up over the deck (was 68% on the body); diffuser + trim
    # drop (top side visible from above, no spin); skirt translates; spins only on rear strake, skirt strake, intake (useful backs)
  M="rear_diffuser_1 rear_diffuser_trim_outer rear_bumper_strake side_skirt_upper side_skirt_strake rear_qpanel_intake_2"
  $R --scene $W/car_carved_noFW.blend --camera $W/cams/x2.json --out $OUT/x2b/ $XR --seconds 4.0 --move orbit --move-amount -12 --ease ease_in_out \
   --explode "$P/rear_diffuser_1.blend:-0.1,0,-0.55:0.05:0.42" \
   --explode "$P/rear_diffuser_trim_outer.blend:-0.1,0,-0.75:0.08:0.45" \
   --explode "$P/rear_bumper_strake.blend:0.15,0.35,-0.6:0.08:0.45:z180:0.45:0.95" \
   --explode "$P/side_skirt_upper.blend:0.1,0.3,-0.75:0.1:0.45" \
   --explode "$P/side_skirt_strake.blend:0.1,0.35,0.55:0.1:0.45:z180:0.48:0.95" \
   --explode "$P/rear_qpanel_intake_2.blend:0,0.2,0.6:0.12:0.48:z-180:0.5:0.95" $(rest $M) ;;
x3) # v2: start offsets searched per part (tools/explode_check.py logic) so each starts in clear background from x3_start.
    # reassembly: everything (incl. the front wheels) translates home on the dense kicks (27.32 27.72 28.25 29.14 29.52 30.13 from
    # shot start 26.38); orbit ends on cam_listing; morph to the listing's grey before the dissolve (6.2 s)
  L=6.2; f() { python3 -c "print(round($1/$L,4))"; }
  $R --scene $W/car_carved_noFW.blend --camera $W/cams/x3_start.json --out $OUT/x3/ $XR --seconds $L --move orbit --move-amount 30 --ease ease_in_out --look-at 0,0,0.6 \
   --morph-to-clay $(f 4.35),$(f 5.3) --morph-bg 0.012,0.014,0.013 --clay-color 0.06,0.06,0.06 \
   --explode "$P/front_lower_lip.blend:0,0,0.7:r$(f 0.14):$(f 0.94)" \
   --explode "$P/front_grille_trim.blend:0,0,0.7:r$(f 0.14):$(f 0.94)" \
   --explode "$P/wheel_FR.blend:0,-0.6,0:r$(f 0.14):$(f 0.94)" \
   --explode "$P/wheel_FL.blend:0,0.6,0:r$(f 0.14):$(f 0.94)" \
   --explode "$P/front_bumper_strake.blend:0,0,0.9:r$(f 0.54):$(f 1.34)" \
   --explode "$P/hood_vent_fins_x3.blend:0,-0.35,0.35:r$(f 0.54):$(f 1.34)" \
   --explode "$P/fender_vent.blend:0,-0.35,-0.35:r$(f 1.07):$(f 1.87)" \
   --explode "$P/rear_qpanel_intake_1.blend:0,-0.49,-0.49:r$(f 1.07):$(f 1.87)" \
   --explode "$P/rear_diffuser_1.blend:0,0,-0.5:r$(f 1.96):$(f 2.76)" \
   --explode "$P/rear_diffuser_trim_outer.blend:0,0,-0.5:r$(f 1.96):$(f 2.76)" \
   --explode "$P/rear_bumper_strake.blend:0,0.35,-0.35:r$(f 2.34):$(f 3.14)" \
   --explode "$P/side_skirt_upper.blend:0,0,-0.9:r$(f 2.34):$(f 3.14)" \
   --explode "$P/side_skirt_strake.blend:0,0.64,0.64:r$(f 2.95):$(f 3.75)" \
   --explode "$P/rear_qpanel_intake_2.blend:0,0,0.5:r$(f 2.95):$(f 3.75)" ;;
esac
