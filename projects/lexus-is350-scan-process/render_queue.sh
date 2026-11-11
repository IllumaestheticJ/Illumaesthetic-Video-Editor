#!/bin/bash
# Final scan renders, one at a time (75 % res, 12 spp, 15 fps; assemble interpolates to 30).
W=/home/user/media/work/is350; M=$W/match
while pgrep -f "s1_front" >/dev/null; do sleep 10; done
python -m ive render -- --scene $W/scan/base_noref.blend --camera $M/camP_B.json --out $W/renders/s2_rear --look silver --res-pct 75 --samples 12 --fps 15 --seconds 6.0 --move rise --move-amount -0.25 --ease ease_in_out --explode "$W/scan/refl.blend:0.15,0.65,-0.12:0.08:0.40:z360:0.38:0.95" > $W/renders/s2.log 2>&1
