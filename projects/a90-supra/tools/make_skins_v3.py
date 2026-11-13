"""Fitted-state skins: the car scan's OWN triangles for each removable panel (everything build_v3/smooth_body cut from
the body near that panel, including the small islands dropped as scrap). body_s + skins = the original car scan, so a
panel that has not moved yet is seamless; the separate panel scan takes over on the frame it starts to move.
    python projects/a90-supra/tools/make_skins_v3.py  -> v3/skin_<part>.stl"""
import os, struct, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from build_v3 import TRI, CAR, OUT

def key(m):
    return np.ascontiguousarray(m["v"]).reshape(len(m), 9).view(np.dtype((np.void, 36))).ravel()
car = np.fromfile(CAR, dtype=TRI, offset=84)
body = np.fromfile(OUT + "body.stl", dtype=TRI, offset=84)
off = car[~np.isin(key(car), key(body))]; del car, body
c = off["v"].mean(1).astype(np.float32)
parts = ["fbump", "fender", "dtrim", "uskirt", "lskirt", "rbump"]
d = np.stack([cKDTree(np.fromfile(OUT + f"lite/part_{p}.stl", dtype=TRI, offset=84)["v"].mean(1)).query(c, distance_upper_bound=130.0, workers=2)[0] for p in parts])
near = np.isfinite(d).any(0); who = d.argmin(0)
print("off-body tris", len(off), "near a panel", int(near.sum()), "dropped elsewhere (scan scraps)", int((~near).sum()))
for i, p in enumerate(parts):
    m = off[near & (who == i)]
    with open(OUT + f"skin_{p}.stl", "wb") as f:
        f.write(b"ive skins".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
    print(p, len(m))
