#!/bin/bash
# Final scan shots, one Blender job at a time: 75 % res, 12 spp, 15 fps (assemble minterpolates to 30).
cd /home/user/Illumaesthetic-Video-Editor
W=/home/user/media/work/lola; P=projects/lola-scan-process/match; R=$W/renders; mkdir -p $R
r() { n=$1; shift; [ -f $R/$n/.done ] && return; rm -rf $R/$n; echo "$(date +%T) start $n";
  python -m ive render -- --out $R/$n/ --look silver --res-pct 75 --samples 12 --fps 15 "$@" > $R/$n.log 2>&1 && touch $R/$n/.done; echo "$(date +%T) end $n $(ls $R/$n | wc -l)"; }
r s1_A     --scene $W/scan/lola1_ext.blend --camera $P/cam_A.json --seconds 5 --move orbit --move-amount 25 --ease ease_in_out --look-at 0,0.2,0.6
r s2_B     --scene $W/scan/lola1_int.blend --explode "$W/scan/lola1_ext.blend:0,0,1.45:0.12:0.5:z360:0.45:1.0" --camera $P/cam_B.json --seconds 6.5 --move pull --move-amount 1.0 --ease ease_in_out
r s3_hero  --scene $W/scan/lola2.blend --camera $P/l2_hero.json --seconds 5 --move orbit --move-amount 30 --ease ease_in_out --look-at 0,0,0.6
r s4_wing  --scene $W/scan/lola2.blend --camera $P/l2_wing.json --seconds 3.5 --move orbit --move-amount -20 --ease ease_in_out --look-at 0,-1.9,1.0
r s5_front --scene $W/scan/lola2.blend --camera $P/l2_front.json --seconds 3 --move push --move-amount 0.12 --ease ease_out
echo ALLDONE
