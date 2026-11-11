"""Split an STL into voxel-connected components (15 mm, 26-connectivity), write the biggest N as out_<i>.stl, print bboxes.
  split.py in.stl out_prefix [--n 6] [--vox 15]"""
import sys, struct, numpy as np
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
a = sys.argv; src, pre = a[1], a[2]
N = int(a[a.index("--n") + 1]) if "--n" in a else 6; V = float(a[a.index("--vox") + 1]) if "--vox" in a else 15
A = np.fromfile(src, dtype=TRI, offset=84); P = A["v"].mean(1)
lo = P.min(0); k = np.floor((P - lo) / V).astype(int)
g = np.zeros(k.max(0) + 1, bool); g[tuple(k.T)] = True
lab, n = ndimage.label(g, structure=np.ones((3, 3, 3))); L = lab[tuple(k.T)]
cnt = np.bincount(L, minlength=n + 1); cnt[0] = 0
for i, c in enumerate(np.argsort(-cnt)[:N]):
    if cnt[c] == 0: break
    r = A[L == c]; q = P[L == c]
    with open(f"{pre}_{i}.stl", "wb") as f:
        f.write(b"ive split".ljust(80)); f.write(struct.pack("<I", len(r))); r.tofile(f)
    print(i, len(r), "min", q.min(0).round(), "max", q.max(0).round())
