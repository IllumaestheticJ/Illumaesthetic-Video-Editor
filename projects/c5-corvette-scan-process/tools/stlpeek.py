"""Quick numpy look at a binary STL: triangle count from header, bbox, and 3 depth-shaded ortho views."""
import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
def load(p):
    with open(p,"rb") as f:
        f.read(80); n=np.frombuffer(f.read(4),"<u4")[0]
        d=np.frombuffer(f.read(50*n),dtype=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")]))
    return n,d["v"].reshape(-1,3)
n,v=load(sys.argv[1]); print(sys.argv[1], "tris", n, "bbox", v.min(0).round(0), v.max(0).round(0), "ext", (v.max(0)-v.min(0)).round(0))
v=v[::3]
fig,ax=plt.subplots(1,3,figsize=(24,7),facecolor="k")
for a,(i,j,k,t) in zip(ax,[(0,1,2,"XY"),(0,2,1,"XZ"),(1,2,0,"YZ")]):
    o=np.argsort(v[:,k]); a.scatter(v[o,i],v[o,j],c=v[o,k],s=0.05,cmap="gray"); a.set_aspect("equal"); a.set_title(t,color="w"); a.set_facecolor("k")
plt.savefig(sys.argv[2],dpi=60,facecolor="k")
