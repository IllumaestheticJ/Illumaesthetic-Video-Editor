"""v4: cut the hood skin and the left tail-lamp skin out of the v3.2 body (same rule as recut_v3: a car triangle leaves only if
it lies on the loose part scan, <= ON mm, 12 mm majority vote). Hood scan is already in the car frame; lamp parts are registered
by reg_lamp3 / reg_lamp_inner (lens_L3, housing_L, insert_L in /home/user/media/work/a90/lamp/).
    python projects/a90-supra/tools/cut_v4.py  -> v3/body4.stl, v3/skin_hood.stl, v3/skin_lamp.stl"""
import os, struct, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from build_v3 import TRI, OUT, islands
W = "/home/user/media/work/a90/"
ON = 4.0
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
def save(m, p):
    with open(p, "wb") as f:
        f.write(b"ive cut_v4".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
body = load(OUT + "body.stl")
for name, src in [("hood", W + "v3/hood_15.stl"), ("lamp", W + "lamp/lens_L3.stl")]:
    part = load(src); pc = part["v"].mean(1).astype(np.float32)
    lo, hi = pc.min(0) - 50, pc.max(0) + 50
    c = body["v"].mean(1).astype(np.float32)
    cand = np.flatnonzero(np.all((c > lo) & (c < hi), axis=1))
    dp = cKDTree(pc).query(c[cand], distance_upper_bound=40.0, workers=4)[0]
    on = dp <= ON
    n_all = cKDTree(c[cand]).query_ball_point(c[cand], 12.0, workers=4, return_length=True)
    n_on = cKDTree(c[cand][on]).query_ball_point(c[cand], 12.0, workers=4, return_length=True)
    frac = n_on / np.maximum(n_all, 1)
    rem = np.where(frac > 0.6, True, np.where(frac < 0.4, False, on))
    off = np.zeros(len(body), bool); off[cand[rem]] = True
    kept = body[~off]
    # specks the cut leaves on the part (< 300 tris, within 20 mm of it) travel with the skin
    lab = islands(kept); size = np.bincount(lab)
    sm = np.flatnonzero(size[lab] < 300)
    d2 = cKDTree(pc).query(kept["v"][sm].mean(1).astype(np.float32), distance_upper_bound=20.0, workers=4)[0]
    sp = np.zeros(len(kept), bool); sp[sm[np.isfinite(d2)]] = True
    skin = np.concatenate([body[off], kept[sp]]); body = kept[~sp]
    save(skin, OUT + f"skin_{name}.stl"); print(name, "skin", len(skin), "body", len(body), flush=True)
save(body, OUT + "body4.stl")
