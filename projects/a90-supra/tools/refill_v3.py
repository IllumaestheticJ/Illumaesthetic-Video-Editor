"""Re-cut state fills against the smoothed body with a tighter gap (3 mm instead of 7): the 7 mm band left a dotted line
of dark gaps between the body's cut edge and the under-panel scan in close-ups (sill, door trim, fender opening).
    python projects/a90-supra/tools/refill_v3.py dtrim skirts fender   -> rewrites v3/fill_<zone>.stl"""
import os, struct, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from build_v3 import TRI, OUT, ZONES, FLOOR_Z, islands
body = np.fromfile(OUT + "body.stl", dtype=TRI, offset=84)["v"].mean(1).astype(np.float32)
bt = cKDTree(body)
for z in sys.argv[1:]:
    state = np.concatenate([np.fromfile(p, dtype=TRI, offset=84) for p in ZONES[z][1]]); sc = state["v"].mean(1).astype(np.float32)
    skins = ["uskirt", "lskirt"] if z == "skirts" else [z]
    op = np.concatenate([np.fromfile(OUT + f"skin_{p}.stl", dtype=TRI, offset=84)["v"].mean(1) for p in skins]).astype(np.float32)
    near = np.isfinite(cKDTree(op).query(sc, distance_upper_bound=60.0, workers=2)[0])
    far = ~np.isfinite(bt.query(sc, distance_upper_bound=3.0, workers=2)[0])
    fill = state[near & far & (sc[:, 2] > FLOOR_Z)]
    lab = islands(fill); size = np.bincount(lab); fc = fill["v"].mean(1)
    att = np.bincount(lab, weights=np.isfinite(bt.query(fc, distance_upper_bound=25.0, workers=2)[0]), minlength=len(size)) > 0
    fill = fill[(size[lab] >= 400) & att[lab]]
    os.replace(OUT + f"fill_{z}.stl", OUT + f"fill_{z}_gap7.stl")
    with open(OUT + f"fill_{z}.stl", "wb") as f:
        f.write(b"ive refill".ljust(80)); f.write(struct.pack("<I", len(fill))); fill.tofile(f)
    print(z, "fill", len(fill))
