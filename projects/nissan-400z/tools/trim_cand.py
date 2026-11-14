"""Candidates for trim_stock.py: stock triangles within --near mm of any listed kit part (Blender's Python has no scipy)."""
import argparse
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("base"); ap.add_argument("out"); ap.add_argument("--parts", nargs="+", required=True); ap.add_argument("--near", type=float, default=80.0)
a = ap.parse_args(); K = "/home/user/media/nissan-400z/kit/lev"
c = np.fromfile(a.base, dtype=TRI, offset=84)["v"].mean(1)
kc = np.concatenate([np.fromfile(f"{K}/{p}.stl", dtype=TRI, offset=84)["v"].mean(1) for p in a.parts])
d, _ = cKDTree(kc).query(c, distance_upper_bound=a.near)
idx = np.where(np.isfinite(d))[0]; np.save(a.out, idx); print("candidates", len(idx))
