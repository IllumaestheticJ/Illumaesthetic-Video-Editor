"""Drop debris islands without Blender (Blender OOMs on the 5-8M tri SW20 scans when it does this).
Welds vertices (0.01 mm grid), labels connected components, keeps components with >= MIN tris that rise above
ZMIN mm (ground scraps never do). usage: islands.py in.stl out.stl [MIN=3000] [ZMIN=150]"""
import struct, sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
src, dst = sys.argv[1], sys.argv[2]; MIN = int(sys.argv[3]) if len(sys.argv) > 3 else 3000; ZMIN = float(sys.argv[4]) if len(sys.argv) > 4 else 150
m = np.fromfile(src, dtype=TRI, offset=84); n = len(m)
q = np.round(m["v"].reshape(-1, 3) * 100).astype(np.int64)
_, vid = np.unique(q, axis=0, return_inverse=True); vid = vid.reshape(n, 3)
nv = vid.max() + 1
rows = np.concatenate([vid[:, 0], vid[:, 1]]); cols = np.concatenate([vid[:, 1], vid[:, 2]])
g = coo_matrix((np.ones(len(rows), np.int8), (rows, cols)), shape=(nv, nv))
k, lab = connected_components(g, directed=False)
tl = lab[vid[:, 0]]
cnt = np.bincount(tl, minlength=k)
zmax = np.full(k, -1e9); np.maximum.at(zmax, tl, m["v"][:, :, 2].max(1))
keepc = (cnt >= MIN) & (zmax > ZMIN)
keep = keepc[tl]
print(f"components {k}, kept {keepc.sum()} ({keep.sum()} of {n} tris); biggest {np.sort(cnt)[-5:]}")
with open(dst, "wb") as f:
    f.write(b"ive islands".ljust(80)); f.write(struct.pack("<I", int(keep.sum()))); m[keep].tofile(f)
