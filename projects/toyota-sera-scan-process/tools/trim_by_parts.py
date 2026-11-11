"""Remove full-car triangles lying on a part's surface (within --tol mm of the part scan), so the part
scans can translate back into a clean full car (x-ray reassembly) without the state scans' other changes.
    python tools/trim_by_parts.py full.stl out.stl part1.stl [part2.stl ...] [--tol 12]"""
import argparse, numpy as np
from scipy.spatial import cKDTree
T = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("full"); ap.add_argument("out"); ap.add_argument("parts", nargs="+")
ap.add_argument("--tol", type=float, default=12.0); a = ap.parse_args()
F = np.fromfile(a.full, dtype=T, offset=84); c = F["v"].mean(1)
keep = np.ones(len(F), bool)
for p in a.parts:
    P = np.fromfile(p, dtype=T, offset=84)["v"].reshape(-1, 3)
    d, _ = cKDTree(P[::2]).query(c, distance_upper_bound=a.tol)
    keep &= ~np.isfinite(d)
out = F[keep]
with open(a.out, "wb") as f:
    f.write(b"tools/trim_by_parts.py".ljust(80)); f.write(np.uint32(len(out)).tobytes()); out.tofile(f)
print({"in": int(len(F)), "removed": int((~keep).sum()), "out": int(len(out))})
