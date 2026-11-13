"""Split a KeyShot OBJ (relative face indices) into connected parts; print bbox per part (cm, Y up) and save
parts.npz (V, faces, part id per face, group id per face).  objparts.py file.obj out.npz"""
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
V=[]; F=[]; G=[]; M=[]; g=-1; mtl=""
for line in open(sys.argv[1], errors="ignore"):
    if line.startswith("v "): V.append(line.split()[1:4])
    elif line.startswith("g "): g+=1
    elif line.startswith("usemtl"): mtl=line.split(None,1)[1].strip()
    elif line.startswith("f "):
        ids=[int(p.split("/")[0]) for p in line.split()[1:]]
        ids=[i-1 if i>0 else len(V)+i for i in ids]
        for k in range(1,len(ids)-1): F.append((ids[0],ids[k],ids[k+1])); G.append(g); M.append(mtl)
V=np.array(V,float); F=np.array(F); G=np.array(G)
n=len(V); e=np.r_[F[:,[0,1]],F[:,[1,2]]]
A=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(n,n))
nc,lab=connected_components(A,directed=False)
fp=lab[F[:,0]]
print("verts",n,"tris",len(F),"components",nc,"bbox",V.min(0).round(1),V.max(0).round(1))
sizes=np.bincount(fp,minlength=nc)
order=np.argsort(-sizes)
for c in order:
    if sizes[c]<50: continue
    P=V[np.unique(F[fp==c])]; lo,hi=P.min(0),P.max(0); m=sorted(set(np.array(M)[fp==c]))
    print(f"part {c:4d} tris {sizes[c]:6d} x[{lo[0]:6.1f},{hi[0]:6.1f}] y[{lo[1]:5.1f},{hi[1]:5.1f}] z[{lo[2]:6.1f},{hi[2]:6.1f}] {m[0][:18]}")
print("small parts (<50 tris):",(sizes<50).sum())
np.savez(sys.argv[2],V=V,F=F,part=fp,group=G,mtl=np.array(M))
