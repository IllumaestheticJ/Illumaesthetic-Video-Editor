"""Fog light / corner marker units (user v5: "include ... front fog light/corner marker data too").

    python3 light_parts.py   -> clean/light_left.stl, clean/light_right.stl, clean/front_bumper_nolights.stl

'Toyota Sera light.stl' holds the two units (one per front corner, ~16 x 18 x 8 cm, z ~350 mm), registered with the
front bumper part scan (median 3.8 mm; every full-car tri near them belongs to the bumper) - they are the bumper's
sub-parts. Split into the two units (20 mm connectivity of tri centroids) and cut the bumper scan where they sit
(tris within 6 mm of a unit), so the bumper shows its openings once the units pull out.
"""
import struct
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
C = "/home/user/media/toyota-sera/clean/"


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"toyota-sera light_parts".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)


li = np.fromfile(C + "light_3mm.stl", dtype=TRI, offset=84); c = li["v"].mean(1)
pr = cKDTree(c).query_pairs(20, output_type="ndarray")
n, lab = connected_components(coo_matrix((np.ones(len(pr)), (pr[:, 0], pr[:, 1])), shape=(len(c), len(c))), directed=False)
big = np.argsort(-np.bincount(lab))[:2]
for k in big:
    side = "left" if c[lab == k, 0].mean() > 0 else "right"  # +X = car's left (orbit convention: -90 = right = -X)
    save(C + f"light_{side}.stl", li[lab == k]); print(side, (lab == k).sum(), c[lab == k].mean(0).round())
fb = np.fromfile(C + "front_bumper_3mm.stl", dtype=TRI, offset=84)
d, _ = cKDTree(c).query(fb["v"].mean(1), distance_upper_bound=12)
save(C + "front_bumper_nolights.stl", fb[d > 6]); print("bumper", len(fb), "->", int((d > 6).sum()))
