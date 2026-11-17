#!/bin/bash
# prep.sh : GR Corolla full-car scan (3 mm) aligned into the lookbook GLB frame (tools/photo1to1 method) + V2/V1 kit parts from the GLB
set -e
T=/home/user/Illumaesthetic-Video-Editor/tools/photo1to1; D=/home/user/media/cars/gr-corolla/scan; G=/home/user/media/cars/eps-toyota-gr-corolla-v23.glb
cd /home/user/Illumaesthetic-Video-Editor
[ -f $D/glb.npz ] || blender -b -P $T/glb_np.py -- $G $D/glb.npz $D/v2_mm.stl "part_front_lip_v2,part_side_skirts_v2,part_rear_spats_v2" 2>&1 | grep GLBNP
[ -f $D/v1.npz ] || blender -b -P $T/glb_np.py -- $G $D/v1.npz $D/v1_mm.stl "part_front_lip,part_side_skirts,part_rear_spats" 2>&1 | grep GLBNP
[ -f $D/precrop_mm.stl ] || python -m ive crop $D/gr-corolla_3mm.stl $D/precrop_mm.stl >/dev/null
[ -f $D/aligned_mm.stl ] || python $T/align_scan.py $D/precrop_mm.stl $D/glb.npz $D/aligned_mm.stl $D/align.json
python $T/align_check.py $D/aligned_mm.stl $D/glb.npz $D/align_check.png
[ -f $D/clean_mm.stl ] || python -m ive crop $D/aligned_mm.stl $D/clean_mm.stl
[ -f $D/scan.blend ] || python -m ive prep -- --scan $D/clean_mm.stl --out $D/scan.blend --units mm --no-center --drop-islands 3000 | grep -o '"faces_out": [0-9]*'
for k in v2 v1; do [ -f $D/$k.blend ] || python -m ive prep -- --scan $D/${k}_mm.stl --out $D/$k.blend --units mm --no-center | grep -o '"faces_out": [0-9]*'; done
echo PREPPED
