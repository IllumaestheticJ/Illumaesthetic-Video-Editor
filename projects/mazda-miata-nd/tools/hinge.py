"""Fit a panel hinge from a state scan that captured the panel propped OPEN (Miata hood / trunk lid).
Open panel = state-scan triangles more than --above mm over the full car's roofline (per 40 mm XY cell) on one end
(--end front: y<0 / rear: y>0), largest connected blob by XY. A rotation about an axis ~X (small tilt) is optimised
so the open panel lands on the full car's surface (closed). Writes (all levelled mm):
  <out>.json          hinge point, axis, open_deg (closed -> open), fit medians
  <out>_state_wo_panel.stl  the state scan minus the open panel (fill for composites)
  <out>_closed.stl    the captured panel moved into its closed pose (= the exploded/opening part)
  hinge.py car.stl state.stl out --end front|rear [--above 40] [--zmin 0]"""
import argparse, json, struct, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--end", required=True); ap.add_argument("--above", type=float, default=40)
ap.add_argument("--ymin", type=float, default=-1e9); ap.add_argument("--ymax", type=float, default=1e9)
a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84); st = np.fromfile(a.state, dtype=TRI, offset=84)
cc = car["v"].mean(1).astype(float); sc = st["v"].mean(1).astype(float)
cell = 40.0
key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
ks = key(sc[:, :2]); i = np.clip(np.searchsorted(u, ks), 0, len(u) - 1); roof = np.where(u[i] == ks, top[i], 0.0)
sel = (sc[:, 2] > roof + a.above) & ((sc[:, 1] < 0) if a.end == "front" else (sc[:, 1] > 0)) & (sc[:, 1] > a.ymin) & (sc[:, 1] < a.ymax)
# keep the biggest connected blob (20 mm linkage) - drops stray debris above the car
idx = np.where(sel)[0]; P = sc[idx]
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
pairs = cKDTree(P).query_pairs(20.0, output_type="ndarray")
n, lab = connected_components(coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(len(P), len(P))))
big = np.bincount(lab).argmax(); idx = idx[lab == big]; P = sc[idx]
print("open panel tris", len(idx), "bbox", P.min(0).round(), P.max(0).round())
rng = np.random.default_rng(0)
S = P[rng.choice(len(P), min(3000, len(P)), replace=False)]
T = cKDTree(cc)
def xf(p, X):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (X - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, S)); return np.mean(np.minimum(d, 60))
# hinge near the panel's lowest edge (the edge that stays on the car)
low = P[P[:, 2] < np.percentile(P[:, 2], 3)]
y0, z0 = low[:, 1].mean(), low[:, 2].mean()
grid = sorted((cost([y0 + dy, z0 + dz, ang, 0, 0]), ang, dy, dz) for ang in range(-120, 121, 5) for dy in (-150, 0, 150) for dz in (-100, 0, 100))
print("grid best", [tuple(round(v, 1) for v in g) for g in grid[:3]])
best = None
for c0, ang, dy, dz in grid[:4]:
    r = minimize(cost, [y0 + dy, z0 + dz, ang, 0, 0], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.3, "fatol": 0.01})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = T.query(xf(p, P))
print("fit", p.round(3), "median to car", np.median(d).round(2), "mm; within 8mm", (d < 8).mean().round(3))
m = st[idx].copy()
m["v"] = xf(p, m["v"].reshape(-1, 3).astype(float)).reshape(-1, 3, 3).astype(np.float32)
with open(a.out + "_closed.stl", "wb") as f: f.write(b"miata hinge".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
keep = np.ones(len(st), bool); keep[idx] = False; w = st[keep]
with open(a.out + "_state_wo_panel.stl", "wb") as f: f.write(b"miata hinge".ljust(80)); f.write(struct.pack("<I", len(w))); w.tofile(f)
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
json.dump({"p_mm": [0, p[0], p[1]], "axis": ax.tolist(), "open_deg": float(-p[2]), "closed_from_open_deg": float(p[2]),
           "fit_median_mm": float(np.median(d)), "within8": float((d < 8).mean()), "tris": int(len(idx))}, open(a.out + ".json", "w"), indent=1)
print("wrote", a.out)
