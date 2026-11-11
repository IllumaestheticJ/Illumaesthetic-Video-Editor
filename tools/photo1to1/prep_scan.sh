#!/bin/bash
# prep_scan.sh CAR : model export -> scan alignment -> ground crop -> Blender prep (scan + kit parts), all in model frame
set -e
C=$1; T=/home/user/Illumaesthetic-Video-Editor/tools/photo1to1; D=/home/user/media/cars/$C/scan
cd /home/user/Illumaesthetic-Video-Editor
KIT=$(python -c "import json;print(','.join(json.load(open('$T/cars.json'))['$C']['kit']))")
GLB=$(python -c "import json;print(json.load(open('$T/cars.json'))['$C']['glb'])")
[ -f $D/glb.npz ] || blender -b -P $T/glb_np.py -- /home/user/media/cars/$GLB $D/glb.npz $D/parts_mm.stl "$KIT" 2>&1 | grep GLBNP
[ -f $D/precrop_mm.stl ] || python -m ive crop $D/${C}_3mm.stl $D/precrop_mm.stl >/dev/null
[ -f $D/aligned_mm.stl ] || python $T/align_scan.py $D/precrop_mm.stl $D/glb.npz $D/aligned_mm.stl $D/align.json
python $T/align_check.py $D/aligned_mm.stl $D/glb.npz $D/align_check.png
python -m ive crop $D/aligned_mm.stl $D/clean_mm.stl | python -c "import json,sys;d=json.load(sys.stdin);print('CROP',d['in'],'->',d['out'])"
python -m ive prep -- --scan $D/clean_mm.stl --out $D/scan.blend --units mm --no-center --drop-islands 3000 | grep -o '"faces_out": [0-9]*'
python -m ive prep -- --scan $D/parts_mm.stl --out $D/parts.blend --units mm --no-center | grep -o '"faces_out": [0-9]*'
python - <<PY
import numpy as np
f=open('$D/clean_mm.stl','rb'); f.seek(80); n=np.frombuffer(f.read(4),np.uint32)[0]
v=np.fromfile(f,np.dtype([('n','<f4',3),('v','<f4',(3,3)),('a','<u2')]),count=n)['v'].reshape(-1,3)/1000
np.savez('$D/scan_small.npz',v=v[::7])
PY
echo PREPPED $C
