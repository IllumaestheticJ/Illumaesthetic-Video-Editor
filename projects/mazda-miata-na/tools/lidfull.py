"""Lid part = skin cut from the full car + the underside captured in the open-state scan, rotated back to closed
about the fitted hinge (so the part opens to exactly the captured pose and shows real ribs from below).
    lidfull.py skin.stl state.stl hinge.json out.stl --zmin 930 [--ymax -500 | --ymin 900]
Open-lid triangles in the state scan: above the car's roofline (+30 mm on a 40 mm grid) and z > --zmin."""
import argparse, json, struct, numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("skin"); ap.add_argument("state"); ap.add_argument("hinge"); ap.add_argument("out")
ap.add_argument("--car", default="/home/user/media/mazda-miata-na/lev/car4_np.stl")
ap.add_argument("--zmin", type=float, default=0); ap.add_argument("--ymin", type=float, default=-1e9); ap.add_argument("--ymax", type=float, default=1e9)
ap.add_argument("--dup", type=float, default=8.0)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)
skin, st, car = L(a.skin), L(a.state), L(a.car)
cc = car["v"].mean(1); sc = st["v"].mean(1)
cell = 40.0; key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
ks = key(sc[:, :2]); i = np.clip(np.searchsorted(u, ks), 0, len(u) - 1); roof = np.where(u[i] == ks, top[i], -1e9)
sel = (sc[:, 2] > roof + 30) & (sc[:, 2] > a.zmin) & (sc[:, 1] > a.ymin) & (sc[:, 1] < a.ymax)
op = st[sel].copy()
h = json.load(open(a.hinge)); yh, zh, ang = h["raw_mm"]
R = Rot.from_rotvec(np.radians(-ang) * np.array([1.0, 0, 0])).as_matrix(); c0 = np.array([0, yh, zh])
op["v"] = ((op["v"].reshape(-1, 3).astype(np.float64) - c0) @ R.T + c0).reshape(-1, 3, 3).astype(np.float32)
op["n"] = (op["n"].astype(np.float64) @ R.T).astype(np.float32)
sv = skin["v"].astype(np.float64); scn = sv.mean(1)
sn = np.cross(sv[:, 1] - sv[:, 0], sv[:, 2] - sv[:, 0]); sn /= np.linalg.norm(sn, axis=1, keepdims=True) + 1e-12
sn *= np.sign(sn[:, 2] + 0.5 * sn[:, 1] * np.sign(scn[:, 1]))[:, None]  # outward: up, or away from the car centre (rear face)
oc = op["v"].mean(1)
d, j = cKDTree(scn).query(oc)
signed = np.einsum("ij,ij->i", oc - scn[j], sn[j])
under = op[signed < -a.dup]   # only geometry BELOW the skin (ribs, inner panel); captured top skin is dropped
out = np.concatenate([skin, under])
with open(a.out, "wb") as f:
    f.write(b"ive lidfull".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
print(a.out, "skin", len(skin), "+ underside", len(under), "(open-lid tris", len(op), ")")
