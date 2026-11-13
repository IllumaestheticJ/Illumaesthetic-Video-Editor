"""Smooth the saw-toothed cut edges of the v3 body (build_v3.py forces every car triangle within 4 mm of a part scan off
the body, so the body edge copies the part scan's ragged boundary). Majority vote over 20 mm neighbourhoods, two passes,
only within 30 mm of a cut edge: teeth sticking into an opening go, notches surrounded by body come back.
    python projects/a90-supra/tools/smooth_body_v3.py   -> rewrites v3/body.stl (old one kept as body_presmooth.stl)"""
import os, struct, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from build_v3 import TRI, CAR, OUT, islands

car = np.fromfile(CAR, dtype=TRI, offset=84); cc = car["v"].mean(1)
body = np.fromfile(OUT + "body.stl", dtype=TRI, offset=84)
scrap = np.fromfile(OUT + "scrap.stl", dtype=TRI, offset=84)
def key(m):                      # exact triangle identity (body/scrap are verbatim subsets of the car file)
    return np.ascontiguousarray(m["v"]).reshape(len(m), 9).view(np.dtype((np.void, 36))).ravel()
keep = np.isin(key(car), key(body)); is_scrap = np.isin(key(car), key(scrap))
del body, scrap
removed = ~keep & ~is_scrap
cc = cc.astype(np.float32)
print("car", len(car), "body", keep.sum(), "removed", removed.sum(), "scrap", is_scrap.sum(), flush=True)
for it in range(2):
    rt = cKDTree(cc[removed])
    near_k = np.flatnonzero(keep); near_k = near_k[np.isfinite(rt.query(cc[near_k], distance_upper_bound=50.0, workers=2)[0])]
    kt = cKDTree(cc[near_k])         # only the body near an opening (not all 6.8 M triangles)
    near_r = np.flatnonzero(removed); near_r = near_r[np.isfinite(kt.query(cc[near_r], distance_upper_bound=30.0, workers=2)[0])]
    edge_k = near_k[np.isfinite(rt.query(cc[near_k], distance_upper_bound=30.0, workers=2)[0])]
    idx = np.r_[edge_k, near_r]
    nr = rt.query_ball_point(cc[idx], 20.0, workers=2, return_length=True); nk = kt.query_ball_point(cc[idx], 20.0, workers=2, return_length=True)
    frac = nr / np.maximum(nr + nk, 1)
    drop = idx[(frac > 0.55) & keep[idx]]; back = idx[(frac < 0.30) & removed[idx]]
    keep[drop] = False; removed[drop] = True; keep[back] = True; removed[back] = False
    print("pass", it, "edge tris", len(idx), "teeth dropped", len(drop), "notches restored", len(back), flush=True)
out = car[keep]; lab = islands(out); out = out[np.bincount(lab)[lab] >= 300]
if not os.path.exists(OUT + "body_presmooth.stl"):
    os.rename(OUT + "body.stl", OUT + "body_presmooth.stl")
with open(OUT + "body.stl", "wb") as f:
    f.write(b"ive smooth_body".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
print("body", len(out))
