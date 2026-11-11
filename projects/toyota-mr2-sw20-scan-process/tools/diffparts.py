"""Parts that exist in state A (Interior: doors + T-tops on) but not in state B (T-Top Off): A triangles farther
than D mm from any B point, then connected components, each written as its own STL with a bbox summary.
usage: diffparts.py A.stl B.stl outdir [D=12] [MIN=4000]"""
import os, struct, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
A = np.fromfile(sys.argv[1], dtype=TRI, offset=84); B = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
out = sys.argv[3]; os.makedirs(out, exist_ok=True)
D = float(sys.argv[4]) if len(sys.argv) > 4 else 12; MIN = int(sys.argv[5]) if len(sys.argv) > 5 else 4000
d, _ = cKDTree(B["v"].mean(1)).query(A["v"].mean(1), distance_upper_bound=D + 1)
P = A[d > D]; n = len(P); print("diff tris", n)
q = np.round(P["v"].reshape(-1, 3) * 100).astype(np.int64); _, vid = np.unique(q, axis=0, return_inverse=True); vid = vid.reshape(n, 3)
nv = vid.max() + 1; r = np.concatenate([vid[:, 0], vid[:, 1]]); c = np.concatenate([vid[:, 1], vid[:, 2]])
k, lab = connected_components(coo_matrix((np.ones(len(r), np.int8), (r, c)), shape=(nv, nv)), directed=False)
tl = lab[vid[:, 0]]; cnt = np.bincount(tl, minlength=k)
for i, comp in enumerate(np.argsort(-cnt)):
    if cnt[comp] < MIN: break
    S = P[tl == comp]; v = S["v"].reshape(-1, 3)
    p = f"{out}/part{i:02d}.stl"
    with open(p, "wb") as f: f.write(b"ive diffparts".ljust(80)); f.write(struct.pack("<I", len(S))); S.tofile(f)
    print(p, len(S), "min", v.min(0).round(), "max", v.max(0).round())
