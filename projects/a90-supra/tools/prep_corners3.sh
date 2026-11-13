#!/bin/bash
# v3 corners from corners3.py: cut the front wheel scan's false inner skin, prep every part (full res) + one merged,
# 1.5 mm decimated blend per corner for the shots where that corner is not the subject.
cd "$(dirname "$0")/../../.."; W=/home/user/media/work/a90; C=$W/corners3; B=$W/blend3
python - <<'PY'
import numpy as np, json, struct, os, glob
TRI=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")])
d=json.load(open("projects/a90-supra/match/corners3.json")); C="/home/user/media/work/a90/corners3/"
def save(m,p):
    with open(p,"wb") as f: f.write(b"ive corners3".ljust(80)); f.write(struct.pack("<I",len(m))); m.tofile(f)
for c in ("FR","FL"):
    a=d["FR"]["articulation"]; ctr=np.array(a["wheel_centre"]); ax=np.array(a["spin_axis_outboard"])
    if c=="FL": ctr[1]*=-1; ax[1]*=-1
    ax/=np.linalg.norm(ax)
    src=C+c+"_wheel.stl"; bak=C+"."+c+"_wheel_raw.stl"
    if not os.path.exists(bak): os.rename(src,bak)
    m=np.fromfile(bak,dtype=TRI,offset=84); p=m["v"].mean(1)-ctr; u=p@ax; r=np.linalg.norm(p-np.outer(u,ax),axis=1)
    bad=(r>150)&(r<250)&(u<25); save(m[~bad],src); print(c,"wheel: false inner skin tris removed",int(bad.sum()),"of",len(m))
for c in ("FR","FL","RR","RL"):
    ms=[np.fromfile(f,dtype=TRI,offset=84) for f in sorted(glob.glob(C+c+"_*.stl"))]
    save(np.concatenate(ms),C+".all_"+c+".stl")
PY
prep(){ flock $W/blender.lock python -m ive prep -- --scan "$1" --out $B/$2.blend --like $W/blend/car.json >/dev/null 2>&1; }
for c in FR FL RR RL; do python -m ive decimate --cell 1.5 $C/.all_$c.stl $C/.all_${c}_15.stl >/dev/null; prep $C/.all_${c}_15.stl k_${c}_all; done
for c in FR RR; do for f in $C/${c}_*.stl; do n=$(basename $f .stl); prep $f k_$n; done; done
ls $B/k_* | wc -l; echo PREP_C3_DONE
