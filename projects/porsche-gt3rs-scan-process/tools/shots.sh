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
x1a) # v2 brief (section focus + cropping): cut-in to a head-on camera framed on the front bumper section (xf: car fills the width); only that
    # assembly comes off - lip + corner strakes drop forward-down into clear background below the car; no spins (thin shells,
    # backs not useful). Grille trim, hood fins and fender vent stay home (vent is the side shot's subject) (3.9 s)
  M="front_lower_lip front_bumper_strake"
  $R --scene $W/car_carved_noFW.blend --camera $W/cams/xf.json --out $OUT/x1a/ $XR --seconds 3.9 --move push --move-amount 0.06 --look-at 2.0,-0.45,0.05 --ease ease_in_out \
   --explode "$P/front_lower_lip.blend:0.15,0,-0.45:0.08:0.5" \
   --explode "$P/front_bumper_strake.blend:0.08,0,-0.28:0.12:0.55" $(rest $M) ;;
s2) # 1:1 match (right side, wheel arch) on the drop, silver hold (1.0 s)
  $R --scene $W/car_noFW.blend --camera $W/cams/camC.json --out $OUT/s2/ $SIL --seconds 1.1 ;;
xs2) # v2 brief: from the 1:1 side camera, PUSH IN on the front fender section; the fender vent comes off up-out toward the lens
    # into clear background (~540 px wide) and spins to show its mounting structure (useful back). Intake stays home (3.8 s)
  M="fender_vent"
  $R --scene $W/car_carved_noFW.blend --camera $W/cams/camC.json --out $OUT/xs2/ $XR --seconds 3.8 --move push --move-amount 0.25 --look-at 1.1,-1.16,0.85 --ease ease_in_out \
   --explode "$P/fender_vent.blend:-0.35,-0.35,0.2:0.08:0.45:z-180:0.48:0.95" $(rest $M) ;;
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
x2r) # v2 brief: rear section, near-straight rear view framed on the diffuser assembly, slow push; diffuser + diffuser trim drop
    # (no spin), rear bumper strake comes out left and spins (mounting brackets on its back). Skirt/intakes stay home (3.9 s)
  M="rear_diffuser_1 rear_diffuser_trim_outer rear_bumper_strake"
  $R --scene $W/car_carved_noFW.blend --camera $W/cams/x2r.json --out $OUT/x2r/ $XR --seconds 3.9 --move push --move-amount 0.08 --look-at=-1.8,0.05,0.5 --ease ease_in_out \
   --explode "$P/rear_diffuser_1.blend:0,0,-0.45:0.06:0.45" \
   --explode "$P/rear_diffuser_trim_outer.blend:-0.15,0,-0.7:0.1:0.5" \
   --explode "$P/rear_bumper_strake.blend:-0.25,0.2,-0.3:0.1:0.5:z180:0.52:0.95" $(rest $M) ;;
x3) # v2 brief: only the parts that came off in this reel (lip, front strakes, fender vent, diffuser, trim, rear strake) +
    # the front wheels translate home; every other part scan sits in place (silver). v2: start offsets searched per part (tools/explode_check.py logic) so each starts in clear background from x3_start.
    # reassembly: everything (incl. the front wheels) translates home on the dense kicks (27.32 27.72 28.25 29.14 29.52 30.13 from
    # shot start 26.279: 27.217 27.569 28.156 29.094 29.448 30.033); orbit ends on cam_listing; morph to the listing's grey before the dissolve (6.2 s)
  L=6.2; f() { python3 -c "print(round($1/$L,4))"; }
  $R --scene $W/car_carved_noFW.blend --camera $W/cams/x3_start.json --out $OUT/x3/ $XR --seconds $L --move orbit --move-amount 30 --ease ease_in_out --look-at 0,0,0.6 \
   --morph-to-clay $(f 4.35),$(f 5.3) --morph-bg 0.012,0.014,0.013 --clay-color 0.06,0.06,0.06 \
   --explode "$P/front_lower_lip.blend:0,0,0.7:r$(f 0.14):$(f 0.94)" \
   --explode "$P/wheel_FR.blend:0,-0.6,0:r$(f 0.14):$(f 0.94)" \
   --explode "$P/wheel_FL.blend:0,0.6,0:r$(f 0.14):$(f 0.94)" \
   --explode "$P/front_bumper_strake.blend:0,0,0.9:r$(f 0.49):$(f 1.29)" \
   --explode "$P/fender_vent.blend:0,-0.35,-0.35:r$(f 1.08):$(f 1.88)" \
   --explode "$P/rear_diffuser_1.blend:0,0,-0.5:r$(f 2.02):$(f 2.82)" \
   --explode "$P/rear_diffuser_trim_outer.blend:0,0,-0.5:r$(f 2.37):$(f 3.17)" \
   --explode "$P/rear_bumper_strake.blend:0,0.35,-0.35:r$(f 2.95):$(f 3.75)" $(rest front_lower_lip front_bumper_strake fender_vent rear_diffuser_1 rear_diffuser_trim_outer rear_bumper_strake) ;;
esac
