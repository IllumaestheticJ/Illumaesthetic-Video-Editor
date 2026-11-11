#!/bin/bash
# S3 x-ray swoop, after S2 (renders one at a time).
W=/home/user/media/work/is350; M=$W/match
sleep 20; while pgrep -f "render_queue.sh|s2_rear" >/dev/null; do sleep 10; done
blender -b -P /home/user/Illumaesthetic-Video-Editor/projects/lexus-is350-scan-process/tools/path_render.py -- --scene $W/scan/base_noref.blend --camera $M/camX_A.json --cam-b $M/camP_L.json --out $W/renders/s3_xray --look xray --accent 0.78,0.8,0.84 --res-pct 75 --samples 12 --fps 15 --seconds 4.5 --morph-to-clay 0.72,0.95 --clay-color 0.11,0.115,0.11 --morph-bg 0.012,0.015,0.012 --explode "$W/scan/refl.blend:0.15,0.65,-0.12:r0.0:0.5" > $W/renders/s3.log 2>&1
