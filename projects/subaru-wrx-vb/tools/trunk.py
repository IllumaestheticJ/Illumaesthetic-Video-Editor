"""Trunk-open parts from the WRX VB state scans (raw Artec mm, all in the full car's frame).

    python projects/subaru-wrx-vb/tools/trunk.py <dec dir> <out dir> <prep car4.json>

1. Closed lid = full-car triangles > 8 mm from the 'No Trunk' state scan (the lid was off) in the rear deck zone.
   'No Trunk' only covers x > -120 mm, so the lid mask is built on the covered half and mirrored about the car's
   centre line (the lid is symmetric) on a 15 mm (|x - xc|, y) grid.
2. Open lid = points of the 'VB Trunk' scan (lid captured propped open) higher than the closed car + 30 mm.
3. Hinge fit (Huracan tools/hinge.py approach): axis ~X through (y_h, z_h) with small tilts + angle, mapping the
   closed lid onto the open lid (truncated mean distance).
4. Writes lid.stl = closed lid skin + the trunk scan's lid inner frame rotated back to the closed pose (only the
   triangles > 6 mm from the skin), base_trunk.stl = car minus lid + new geometry from 'Rear Bumper Trunk Open'
   and the non-lid part of 'VB Trunk' (tub, seals), and hinge.json in the prepped Blender frame (m).
"""
import json
import struct
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
D, O, LIKE = sys.argv[1], sys.argv[2], sys.argv[3]


def load(n):
    return np.fromfile(f"{D}/{n}.stl", dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"wrx trunk".ljust(80))
        f.write(struct.pack("<I", len(m)))
        m.tofile(f)
    print("wrote", p, len(m))


car = load("car4_clean")
cc = car["v"].mean(1).astype(float)
xc = 0.5 * (cc[:, 0].min() + cc[:, 0].max())
nt = load("no_trunk")["v"].mean(1).astype(float)
d, _ = cKDTree(nt).query(cc, distance_upper_bound=40)
zone = (cc[:, 1] > 1150) & (cc[:, 2] > 850)
# covered column: 'No Trunk' has geometry >= 40 mm below this point in the same 30 mm XY column (the tub seen
# with the lid off), but nothing within 8 mm (the lid skin itself is gone)
C = 30.0
kc = lambda p: np.floor(p[:, 0] / C).astype(np.int64) * 100000 + np.floor(p[:, 1] / C).astype(np.int64)
un, invn = np.unique(kc(nt), return_inverse=True)
ntop = np.full(len(un), -1e9)
np.maximum.at(ntop, invn, nt[:, 2])
kq = kc(cc)
j = np.clip(np.searchsorted(un, kq), 0, len(un) - 1)
below = np.where(un[j] == kq, ntop[j], 1e9)
half = zone & (cc[:, 0] > xc + 20) & (cc[:, 0] < nt[:, 0].max() - 30) & (d > 8) & (below < cc[:, 2] - 40)
# grid mask on (|x-xc|, y), mirrored; keep cells with enough hits and the top surface only
G = 15.0
key = lambda x, y: (np.floor(np.abs(x - xc) / G).astype(np.int64) * 100000 + np.floor(y / G).astype(np.int64))
cells, cnt = np.unique(key(cc[half, 0], cc[half, 1]), return_counts=True)
cells = cells[cnt >= 2]
lid = zone & np.isin(key(cc[:, 0], cc[:, 1]), cells)
# lid is the top skin: drop anything far below the local top surface (tail lights / bumper under the lid edge)
print("lid tris", int(lid.sum()), "y", cc[lid, 1].min().round(), cc[lid, 1].max().round(), "z", cc[lid, 2].min().round(),
      cc[lid, 2].max().round(), "x", cc[lid, 0].min().round(), cc[lid, 0].max().round())

# open lid points
tr = load("trunk")
tc = tr["v"].mean(1).astype(float)
cell = 40.0
k2 = lambda p: np.floor(p[:, 0] / cell).astype(np.int64) * 100000 + np.floor(p[:, 1] / cell).astype(np.int64)
u, inv = np.unique(k2(cc), return_inverse=True)
top = np.full(len(u), -1e9)
np.maximum.at(top, inv, cc[:, 2])
kt = k2(tc)
i = np.clip(np.searchsorted(u, kt), 0, len(u) - 1)
roof = np.where(u[i] == kt, top[i], -1e9)
is_open = tc[:, 2] > roof + 30
openp = tc[is_open]
print("open lid pts", len(openp), "y", openp[:, 1].min().round(), openp[:, 1].max().round(), "z", openp[:, 2].max().round())

rng = np.random.default_rng(0)
L = cc[lid][rng.choice(int(lid.sum()), min(3000, int(lid.sum())), replace=False)]
T = cKDTree(openp)


def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz])
    ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix()
    c = np.array([xc, yh, zh])
    return (P - c) @ R.T + c


def cost(p):
    dd, _ = T.query(xf(p, L))
    return np.mean(np.minimum(dd, 60))


y0 = cc[lid, 1].min()
z0 = cc[lid][cc[lid, 1] < y0 + 60][:, 2].mean()
grid = sorted((cost([y0 + dy, z0 + dz, a, 0, 0]), a, dy, dz)
              for a in range(-100, 101, 5) for dy in (-150, -50, 50, 150) for dz in (-150, -50, 50))
print("grid best", [tuple(round(v, 1) for v in g) for g in grid[:3]])
best = None
for c0, a, dy, dz in grid[:4]:
    r = minimize(cost, [y0 + dy, z0 + dz, a, 0, 0], method="Nelder-Mead",
                 options={"maxiter": 1500, "xatol": 0.3, "fatol": 0.01})
    if best is None or r.fun < best.fun:
        best = r
p = best.x
dd, _ = T.query(xf(p, L))
print("fit", p.round(3), "mean", round(best.fun, 2), "median", np.median(dd).round(2), "mm, <10mm",
      (dd < 10).mean().round(3))

# lid part: closed skin + the trunk scan's open-lid inner frame rotated back closed
yh, zh, ang, tz, ty = p
ax = np.array([1.0, ty, tz])
ax /= np.linalg.norm(ax)
Rinv = Rot.from_rotvec(np.radians(-ang) * ax).as_matrix()
hc = np.array([xc, yh, zh])
opentris = tr[is_open].copy()
v = opentris["v"].astype(float)
opentris["v"] = ((v - hc) @ Rinv.T + hc).astype("<f4")
skin = car[lid]
ds, _ = cKDTree(skin["v"].mean(1)).query(opentris["v"].mean(1), distance_upper_bound=20)
inner = opentris[ds > 6]
save(f"{O}/lid.stl", np.concatenate([skin, inner]))
save(f"{O}/lid_skin.stl", skin)

# base: car minus lid + new geometry under it
pieces = [car[~lid]]
tcar = cKDTree(cc[~lid][::2])
acc = None
lo = cc[lid].min(0) - [80, 80, 400]
hi = cc[lid].max(0) + [80, 80, 0]
for name, m in (("rear_bumper_trunk_open", load("rear_bumper_trunk_open")), ("trunk(non-lid)", tr[~is_open])):
    c = m["v"].mean(1).astype(float)
    inz = np.all((c >= lo) & (c <= hi), axis=1)
    dn, _ = tcar.query(c[inz], distance_upper_bound=20)
    ok = dn > 7
    if acc is not None:
        d2, _ = cKDTree(acc).query(c[inz], distance_upper_bound=20)
        ok &= d2 > 6
    sel = np.zeros(len(m), bool)
    sel[np.where(inz)[0][ok]] = True
    acc = c[sel] if acc is None else np.concatenate([acc, c[sel]])
    print(name, "fill +", int(sel.sum()))
    pieces.append(m[sel])
save(f"{O}/base_trunk.stl", np.concatenate(pieces))

like = json.load(open(LIKE))
s, rl = like["unit_scale"], np.array(like["root_location"])
out = {"pivot": (hc * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(ang),
       "fit_median_mm": float(np.median(dd)), "fit_within10mm": float((dd < 10).mean())}
json.dump(out, open(f"{O}/hinge.json", "w"), indent=1)
print(out)
