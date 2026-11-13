"""Read a Blender OBJ with several 'o' objects -> npz with V (global), F (global idx), obj id per face, names."""
import sys, numpy as np
V=[]; F=[]; O=[]; names=[]
for line in open(sys.argv[1], errors="ignore"):
    if line.startswith("v "): V.append(line.split()[1:4])
    elif line.startswith("o "): names.append(line[2:].strip())
    elif line.startswith("f "):
        ids=[int(p.split("/")[0]) for p in line.split()[1:]]
        ids=[i-1 if i>0 else len(V)+i for i in ids]
        for k in range(1,len(ids)-1): F.append((ids[0],ids[k],ids[k+1])); O.append(len(names)-1)
V=np.array(V,float); F=np.array(F); O=np.array(O)
for i,n in enumerate(names):
    P=V[np.unique(F[O==i])]; print(n,"tris",(O==i).sum(),"bbox",P.min(0).round(1),P.max(0).round(1))
np.savez(sys.argv[2],V=V,F=F,obj=O,names=np.array(names))
