"""Split the full car into panels using the 'removed/open' state scans (all levelled, mm, same frame).
A car triangle belongs to a panel when it is > --gap mm from the state scan (the panel is not there in that
state) and inside the zone box. Prints stats; writes the panel STL and, with --rest, the car minus the panel.
  extract.py car.stl state.stl out_panel.stl --zone x0,x1,y0,y1,z0,z1 [--gap 12] [--rest rest.stl]
       [--minus other_state.stl]  (also require > gap from another state, e.g. the bumper-only scan)"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def save(p, m):
    with open(p, "wb") as f:
        f.write(b"ive extract gr86".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--zone", required=True); ap.add_argument("--gap", type=float, default=12)
ap.add_argument("--rest"); ap.add_argument("--behind", default="", help="axis the state must have geometry behind the panel along: -z, -x|x (mirrors: towards the centreline)"); ap.add_argument("--cell", type=float, default=30)
ap.add_argument("--normal", default="", help="keep only tris whose normal along this axis > 0.3, e.g. +z")
ap.add_argument("--keep-near", nargs="*", default=[],
                help="part scans: car tris within gap of these are NOT the panel (e.g. the bumper)")
a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84); c = car["v"].mean(1)
z = [float(v) for v in a.zone.split(",")]
inz = (c[:, 0] > z[0]) & (c[:, 0] < z[1]) & (c[:, 1] > z[2]) & (c[:, 1] < z[3]) & (c[:, 2] > z[4]) & (c[:, 2] < z[5])
st = np.fromfile(a.state, dtype=TRI, offset=84)["v"].mean(1)
d, _ = cKDTree(st).query(c[inz], distance_upper_bound=a.gap * 3)
sel = np.zeros(len(c), bool); sel[np.where(inz)[0][d > a.gap]] = True
if a.behind:
    ax = {"x": 0, "y": 1, "z": 2}[a.behind[-1]]
    o = [i for i in range(3) if i != ax]
    key = lambda p: np.floor(p[:, o[0]] / a.cell).astype(np.int64) * 1000003 + np.floor(p[:, o[1]] / a.cell).astype(np.int64)
    if a.behind == "-x|x":  # depth = |x| (outboard), state must have something more inboard
        dep_s, dep_c = np.abs(st[:, 0]), np.abs(c[:, 0])
        ks = key(st) * 2 + (st[:, 0] > 0); kc = key(c) * 2 + (c[:, 0] > 0)
    else:
        sg = -1 if a.behind[0] == "-" else 1
        dep_s, dep_c = -sg * st[:, ax], -sg * c[:, ax]
        ks, kc = key(st), key(c)
    u, inv = np.unique(ks, return_inverse=True); mn = np.full(len(u), np.inf); np.minimum.at(mn, inv, dep_s)
    idx = np.where(sel)[0]; kk = kc[idx]; j = np.clip(np.searchsorted(u, kk), 0, len(u) - 1)
    ok = (u[j] == kk) & (mn[j] < dep_c[idx] - a.gap)
    sel[idx[~ok]] = False
if a.normal:
    ax = {"x": 0, "y": 1, "z": 2}[a.normal[-1]]; sg = -1 if a.normal[0] == "-" else 1
    nn = car["n"][:, ax] * sg
    sel &= nn > 0.3
for k in a.keep_near:
    kp = np.fromfile(k, dtype=TRI, offset=84)["v"].mean(1)
    dk, _ = cKDTree(kp).query(c[sel], distance_upper_bound=a.gap * 2)
    idx = np.where(sel)[0]; sel[idx[dk < a.gap]] = False
print("zone", inz.sum(), "panel", sel.sum())
save(a.out, car[sel])
if a.rest: save(a.rest, car[~sel])
