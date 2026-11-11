"""Keep the N largest connected components of an STL (vertices welded at 0.01 mm).  largest.py in.stl out.stl [N] [min_tris]"""
import struct, sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
N = int(sys.argv[3]) if len(sys.argv) > 3 else 1
mn = int(sys.argv[4]) if len(sys.argv) > 4 else 0
v = np.round(m["v"].reshape(-1, 3) * 100).astype(np.int64)
_, vid = np.unique(v, axis=0, return_inverse=True); vid = vid.reshape(-1, 3)
nv = vid.max() + 1
e = np.concatenate([vid[:, [0, 1]], vid[:, [1, 2]]])
g = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(nv, nv))
k, lab = connected_components(g, directed=False)
tl = lab[vid[:, 0]]
cnt = np.bincount(tl)
order = np.argsort(-cnt)
keep = [c for c in order[:N] if cnt[c] >= mn]
print("components", k, "top sizes", cnt[order[:8]].tolist())
sel = np.isin(tl, keep)
o = m[sel]
with open(sys.argv[2], "wb") as f:
    f.write(b"largest".ljust(80)); f.write(struct.pack("<I", len(o))); o.tofile(f)
print("kept", len(o), "bbox", o["v"].reshape(-1,3).min(0).round(), o["v"].reshape(-1,3).max(0).round())
