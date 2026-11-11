"""Keep the N largest connected pieces of an STL soup (vertices merged by exact position).
    python biggest.py in.stl out.stl [N=1]   -- isolates e.g. the hood lid from lid.py's cut (drops headlamp lenses, fender slivers)"""
import sys, struct, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84); N = int(sys.argv[3]) if len(sys.argv) > 3 else 1
v = m["v"].reshape(-1, 3); _, idx = np.unique(np.round(v, 3), axis=0, return_inverse=True); idx = idx.reshape(-1, 3)
nv = idx.max() + 1; r = np.concatenate([idx[:, 0], idx[:, 1]]); c = np.concatenate([idx[:, 1], idx[:, 2]])
_, lab = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(nv, nv)), directed=False)
tl = lab[idx[:, 0]]; cnt = np.bincount(tl); keep_l = np.argsort(cnt)[::-1][:N]
print("pieces", len(cnt), "largest", cnt[keep_l])
m = m[np.isin(tl, keep_l)]
with open(sys.argv[2], "wb") as f:
    f.write(b"gt3 biggest".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
