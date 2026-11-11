#!/bin/bash
# v3 finals, strictly sequential (each waits for the previous blender to exit). 75 % res, 12 spp, 15 fps.
set -e
W=/home/user/media/work/is350; M=$W/match; T=/home/user/Illumaesthetic-Video-Editor/projects/lexus-is350-scan-process/tools; R=$W/renders
python -m ive render -- --scene $W/scan/car.blend --camera $M/camW_A.json --out $R/v3_s1_front --look silver --res-pct 75 --samples 12 --fps 15 --seconds 4.0 --move push --move-amount 0.15 --ease ease_in_out > $R/v3_s1.log 2>&1
blender -b -P $T/path_render.py -- --scene $W/scan/base_noref.blend --camera $M/camW_B.json --cam-b $M/camR_end.json --out $R/v3_s2_rear --look silver --res-pct 75 --samples 12 --fps 15 --seconds 6.0 --no-persist --explode "$W/scan/refl.blend:0.05,0.20,-0.25:0.10:0.33:z180:0.36:0.80" > $R/v3_s2.log 2>&1
blender -b -P $T/path_render.py -- --scene $W/scan/base_noref.blend --camera $M/camR_end.json --cam-b $M/camP_L.json --out $R/v3_s3_xray --look xray --accent 0.78,0.8,0.84 --res-pct 75 --samples 12 --fps 15 --seconds 4.5 --no-persist --morph-to-clay 0.72,0.95 --clay-color 0.11,0.115,0.11 --morph-bg 0.012,0.015,0.012 --explode "$W/scan/refl.blend:0.05,0.20,-0.25:r0.0:0.45:z180:0.0:0.45" > $R/v3_s3.log 2>&1
echo ALL_DONE > $R/v3_done
