"""Which car triangles does each state scan NOT have (= panels removed / moved in that state)?
  diffzones.py car.stl state.stl out.stl [--near part.stl ...]   (writes car tris > D mm from the state; optional
  --near keeps only those within D of a part scan, --far drops those within D of a part scan; --ymin/--ymax (mm) first restrict to the state's covered zone)"""
import sys, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
a = sys.argv[1:]; D = 8.0
car, st, out = load(a[0]), load(a[1]), a[2]
cc = car["v"].mean(1)
d, _ = cKDTree(st["v"].mean(1)).query(cc, distance_upper_bound=D + 1)
keep = d > D
i = 3
while i < len(a) and a[i] in ("--ymin", "--ymax"):
    keep &= (cc[:, 1] > float(a[i + 1])) if a[i] == "--ymin" else (cc[:, 1] < float(a[i + 1])); i += 2
while i < len(a):
    m = cKDTree(load(a[i + 1])["v"].mean(1)).query(cc, distance_upper_bound=D + 1)[0] <= D
    keep &= m if a[i] == "--near" else ~m
    i += 2
r = car[keep]
open(out, "wb").write(b"diff".ljust(80) + struct.pack("<I", len(r)) + r.tobytes())
print(out, len(r), "bbox", r["v"].reshape(-1, 3).min(0).round(), r["v"].reshape(-1, 3).max(0).round())
