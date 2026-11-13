"""Remove from a cut panel every triangle that is still present in the state scan where the panel was opened
(it stayed on the body, so it is not panel): Miata trunk lid lost a chunk of each tail light (user, v6).
  refine_lid.py lid.stl state_open.stl out.stl [--keep 8]   (levelled mm)"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("lid"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--keep", type=float, default=8.0, help="lid tris closer than this to the open-state scan stay on the body")
a = ap.parse_args()
lid = np.fromfile(a.lid, dtype=TRI, offset=84); st = np.fromfile(a.state, dtype=TRI, offset=84)
lc = lid["v"].mean(1); d, _ = cKDTree(st["v"].mean(1)).query(lc, distance_upper_bound=a.keep + 1)
body = d < a.keep
k = lid[~body]
with open(a.out, "wb") as f: f.write(b"miata refine_lid".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
with open(a.out.replace(".stl", "_stays.stl"), "wb") as f: f.write(b"miata stays".ljust(80)); f.write(struct.pack("<I", int(body.sum()))); lid[body].tofile(f)
print("lid", len(lid), "-> stays on body", int(body.sum()), "lid kept", len(k), "stays bbox", lc[body].min(0).round() if body.any() else None, lc[body].max(0).round() if body.any() else None)
