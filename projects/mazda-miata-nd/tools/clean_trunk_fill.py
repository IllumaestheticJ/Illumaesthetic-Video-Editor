"""Remove rear-wing / trunk-lid residue from the trunk-open state fill (levelled mm).
hinge.py removed only the largest open-lid blob; the wing pieces stayed. Drop every state triangle that is
 (a) inside the trunk-lid footprint (car's lid triangles, 60 mm dilated in XY) and at or above the closed lid surface - 25 mm, or
 (b) anywhere in the rear half more than 30 mm above the full car's roofline (per 40 mm cell).
  clean_trunk_fill.py car.stl lid.stl state_wo_panel.stl out.stl"""
import sys, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car, lid, st = (np.fromfile(p, dtype=TRI, offset=84) for p in sys.argv[1:4])
cc, lc, sc = car["v"].mean(1), lid["v"].mean(1), st["v"].mean(1)
d, i = cKDTree(lc[:, :2]).query(sc[:, :2])
a = (d < 60) & (sc[:, 2] > lc[i, 2] - 25)
cell = 40.0
key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
ks = key(sc[:, :2]); j = np.clip(np.searchsorted(u, ks), 0, len(u) - 1); roof = np.where(u[j] == ks, top[j], 0.0)
b = (sc[:, 1] > 0) & (sc[:, 2] > roof + 30)
k = st[~(a | b)]
with open(sys.argv[4], "wb") as f: f.write(b"miata trunk fill clean".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print("dropped lid-zone", int(a.sum()), "above-roof", int((b & ~a).sum()), "->", len(k))
