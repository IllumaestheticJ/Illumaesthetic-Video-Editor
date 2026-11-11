#!/bin/bash
# Final scan shots for the MR2 Spyder scan-process reel. Serial (one Blender at a time), 75% res, 12 spp, 15 fps.
set -e
cd /home/user/Illumaesthetic-Video-Editor
P=projects/toyota-mr2-spyder-scan-process; S=/home/user/media/work/mr2/scan; O=/home/user/media/work/mr2/renders
COMMON="--res 1080x1920 --res-pct 75 --samples 12 --fps 15"
r() { name=$1; shift; [ -f $O/$name/done ] && return; rm -rf $O/$name; python -m ive render -- "$@" $COMMON --out $O/$name/ > $O/$name.log 2>&1; touch $O/$name/done; echo "$(date +%T) $name done"; }
mkdir -p $O
# A: 1:1 from the front-3/4 scanning frame (DJI_0030 74.0 s); slow push-in
r sA2 --scene $S/topdown.blend --camera $P/match/camA.json --seconds 3.4 --move pull --move-amount 0.9 --ease ease_in_out
# B: 1:1 from the rear scanning frame (DJI_0030 56.0 s); gentle push
r sB --scene $S/topdown.blend --camera $P/match/camB.json --seconds 2.4 --move push --move-amount 0.06 --ease ease_in_out
# C: rear-end state scan (lid open) - lid lifts off, spins about Z: underside (ribs) then louvred top
r sC --scene $S/rear_open_nolid.blend --camera $P/match/cam_C.json --seconds 4.5 --move orbit --move-amount -22 --ease ease_in_out --look-at 0,-1.0,0.8 --explode "$S/lid_open.blend:0,-0.15,0.55:0.05:0.35:z180:0.35:0.9"
# X: x-ray reassembly - closed lid translates back into place; orbit ends on the listing hero pose, morphs to listing grey
r sX --scene $S/topdown_nolid.blend --camera $P/match/cam_xray_start.json --seconds 2.75 --move orbit --move-amount 50 --ease ease_in_out --look-at 0,0,0.55 --look xray --morph-to-clay 0.62,1.0 --clay-color 0.075,0.078,0.075 --morph-bg 0.012,0.015,0.012 --explode "$S/lid_closed.blend:0,0,0.7:r0.08:0.55"
echo ALL DONE
