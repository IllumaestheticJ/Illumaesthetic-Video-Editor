#!/bin/bash
# Decimate placed corner parts (1.5 mm), merge per corner (and a wheel-less 'brakes+springs' set), prep --like car.json
W=/home/user/media/work/a90; C=$W/corners; cd "$(dirname "$0")/../../.."
for f in $C/??_*.stl; do n=$(basename $f .stl); python -m ive decimate $f $C/dec_$n.stl --cell 1.5 >/dev/null; done
for side in FR FL RR RL; do for set in all nowheel; do python - "$C" "$side" "$set" <<'PY'
import sys,glob,numpy as np,struct
TRI=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")])
C,side,st=sys.argv[1:4]
fs=[f for f in sorted(glob.glob(f"{C}/dec_{side}_*.stl")) if st=="all" or "wheel" not in f]
m=np.concatenate([np.fromfile(f,dtype=TRI,offset=84) for f in fs])
open(f"{C}/corner_{side}_{st}.stl","wb").write(b"ive".ljust(80)+struct.pack("<I",len(m))+m.tobytes())
PY
python -m ive prep -- --scan $C/corner_${side}_${set}.stl --out $W/blend/corner_${side}_${set}.blend --like $W/blend/car.json >/dev/null; done; done
echo built
