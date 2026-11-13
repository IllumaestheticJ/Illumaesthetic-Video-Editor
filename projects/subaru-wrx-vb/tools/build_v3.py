"""v3 base + parts for the WRX VB (raw Artec mm, all in the full car's frame). Reviewer v2 notes: the front bumper
comes apart further (grille, lower garnish, shell are separate scans), the trunk opens (VB Trunk = lid propped open),
and the front bumper's cut-out was ragged.

    python projects/subaru-wrx-vb/tools/build_v3.py <dec dir> <comp dir> <prep car4.json> <old hinge.json>

1. composite.py rules (car minus panels within 9 mm, + new geometry from the panel-off state scans), with the bumper
   split into shell / grille / garnish (v2 removed 'Inside, Parts included' = all three, then flew the garnish twice).
2. Front clean-up (the v2 ragged cut): the bumper part scans cover only ~50 % of the bumper skin on the car, so v2 left
   bumper slivers. In the bumper zone a car triangle is also removed when the bumper-off state scans saw *behind* it
   (state data in the same x/z column further back) but have nothing within 12 mm of it: that skin is gone once the
   bumper is off. Limited to within 80 mm of the bumper part scans so fenders/headlights are never touched.
3. Trunk lid: closed footprint = the open-lid capture ('VB Trunk', points > 30 mm above the closed car) rotated back
   about the fitted hinge; car deck triangles within 25 mm of it form the mask, mirrored about the centre line and
   hole-filled on a 15 mm grid. Hinge refit on the complete skin. Base gets the tub from 'Rear Bumper Trunk Open'
   + the non-lid part of 'VB Trunk'.
Writes comp/b3.stl, b3_lid.stl, b3_plate.stl and b3_hinge.json (prepped frame, m).
"""
import json
import struct
import subprocess
import sys

import numpy as np
from scipy import ndimage
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
D, C, LIKE, OLDH = sys.argv[1:5]
ROOT = "/home/user/Illumaesthetic-Video-Editor"


def load(p):
    return np.fromfile(p if p.endswith(".stl") else f"{D}/{p}.stl", dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"wrx v3".ljust(80))
        f.write(struct.pack("<I", len(m)))
        m.tofile(f)
    print("wrote", p, len(m), flush=True)


like = json.load(open(LIKE))
S, RL = like["unit_scale"], np.array(like["root_location"])

# 1. composite
parts = ["front_bumper_inside_parts_removed", "front_grille", "front_bumper_lower_garnish", "rear_bumper_updated",
         "front_flare", "door_flare", "rear_flare", "side_skirt_only"]
fills = ["front_removed_all", "bumpers_removed", "rear_bumper_removed", "duckbill_scan", "side_skirt_off_doors_open"]
subprocess.run(["python", f"{ROOT}/projects/ferrari-296/tools/composite.py", f"{C}/b3_step1.stl",
                "--car", f"{D}/car4_clean_np.stl", "--remove", *[f"{D}/{p}.stl" for p in parts],
                "--fill", *[f"{D}/{f}.stl" for f in fills], "--zone-pad", "60"], check=True)
base = load(f"{C}/b3_step1.stl")
car = load("car4_clean_np")
carc = car["v"].mean(1).astype(float)
tcar = cKDTree(carc)

# 2. front clean-up (only original car triangles are candidates; fill triangles are new geometry and stay)
bc = base["v"].mean(1).astype(float)
dcar, _ = tcar.query(bc, distance_upper_bound=1.0)
orig = dcar < 0.5
fp = np.vstack([load(p)["v"].reshape(-1, 3) for p in parts[:3]]).astype(float)
dpart, _ = cKDTree(fp[::3]).query(bc, distance_upper_bound=80)
plate = (bc[:, 1] < -2345) & (np.abs(bc[:, 0] + 50) < 350) & (bc[:, 2] > 150) & (bc[:, 2] < 700)  # split_plate box
near = orig & (dpart < 80) & ~plate
st = np.vstack([load(f)["v"].mean(1) for f in ("front_removed_all", "bumpers_removed")]).astype(float)
st = st[st[:, 1] < fp[:, 1].max() + 200]
dst, _ = cKDTree(st).query(bc[near], distance_upper_bound=12)
G = 20.0
key = lambda p: np.floor(p[:, 0] / G).astype(np.int64) * 1_000_000 + np.floor(p[:, 2] / G).astype(np.int64)
ku, inv = np.unique(key(st), return_inverse=True)
ymax = np.full(len(ku), -1e9)
np.maximum.at(ymax, inv, st[:, 1])  # rear-most state point per x/z column (front = -y)
kq = key(bc[near])
j = np.clip(np.searchsorted(ku, kq), 0, len(ku) - 1)
behind = np.where(ku[j] == kq, ymax[j], -1e9) > bc[near][:, 1] + 15
gone = np.zeros(len(base), bool)
gone[np.where(near)[0][(dst > 12) & behind]] = True
print("front clean-up removes", int(gone.sum()), "of", int(near.sum()), "candidates", flush=True)
base = base[~gone]
bc = bc[~gone]

# 3. trunk lid
H = json.load(open(OLDH))
to_raw = lambda p: (np.asarray(p) - RL) / S
xc = 0.5 * (carc[:, 0].min() + carc[:, 0].max())
tr = load("trunk")
tc = tr["v"].mean(1).astype(float)
cell = 40.0
k2 = lambda p: np.floor(p[:, 0] / cell).astype(np.int64) * 100000 + np.floor(p[:, 1] / cell).astype(np.int64)
u, inv = np.unique(k2(carc), return_inverse=True)
top = np.full(len(u), -1e9)
np.maximum.at(top, inv, carc[:, 2])
kt = k2(tc)
i = np.clip(np.searchsorted(u, kt), 0, len(u) - 1)
is_open = tc[:, 2] > np.where(u[i] == kt, top[i], -1e9) + 30
openp = tc[is_open]


def R_of(ang, ax):
    ax = np.asarray(ax, float) / np.linalg.norm(ax)
    return Rot.from_rotvec(np.radians(ang) * ax).as_matrix()


def lid_mask(hc, ax, ang):
    closed = (openp - hc) @ R_of(-ang, ax).T + hc
    zone = (bc[:, 1] > closed[:, 1].min() - 40) & (bc[:, 2] > closed[:, 2].min() - 60)
    d, _ = cKDTree(closed).query(bc, distance_upper_bound=25)
    hit = zone & (d < 25)
    g = 15.0
    gx = np.floor(np.abs(bc[:, 0] - xc) / g).astype(int)
    gy = np.floor((bc[:, 1] - 1000) / g).astype(int)
    ok = zone & (gy >= 0)
    grid = np.zeros((gx[ok].max() + 3, gy[ok].max() + 3), bool)
    grid[gx[hit], gy[hit]] = True
    grid = ndimage.binary_closing(grid, iterations=3)
    grid = ndimage.binary_fill_holes(grid)
    grid = ndimage.binary_opening(grid, iterations=1)
    lab, n = ndimage.label(grid)
    if n > 1:
        sizes = ndimage.sum(grid, lab, range(1, n + 1))
        grid = lab == (1 + int(np.argmax(sizes)))
    m = ok.copy()
    m[ok] = grid[gx[ok], gy[ok]]
    # top skin only: within 35 mm of the highest surface in its column
    k = gx * 100000 + gy
    uk, iv = np.unique(k[m], return_inverse=True)
    tz = np.full(len(uk), -1e9)
    np.maximum.at(tz, iv, bc[m, 2])
    mm = np.where(m)[0]
    m[mm[bc[mm, 2] < tz[iv] - 35]] = False
    return m


hc0 = to_raw(H["pivot"])
lid = lid_mask(hc0, H["axis"], H["open_deg"])
print("lid tris", int(lid.sum()), "x", bc[lid, 0].min().round(), bc[lid, 0].max().round(),
      "y", bc[lid, 1].min().round(), bc[lid, 1].max().round(), flush=True)
rng = np.random.default_rng(0)
Lp = bc[lid][rng.choice(int(lid.sum()), min(4000, int(lid.sum())), replace=False)]
T = cKDTree(openp)


def xf(p, P):
    yh, zh, ang, tz, ty = p
    return (P - [xc, yh, zh]) @ R_of(ang, [1.0, ty, tz]).T + [xc, yh, zh]


cost = lambda p: np.mean(np.minimum(T.query(xf(p, Lp))[0], 60))
p0 = [hc0[1], hc0[2], H["open_deg"], 0, 0]
best = minimize(cost, p0, method="Nelder-Mead", options={"maxiter": 2000, "xatol": 0.3, "fatol": 0.01})
for a0 in (-40, 40):
    r = minimize(cost, [p0[0], p0[1], p0[2] + a0, 0, 0], method="Nelder-Mead", options={"maxiter": 2000})
    if r.fun < best.fun:
        best = r
p = best.x
dd = T.query(xf(p, Lp))[0]
print("hinge refit", p.round(3), "median", np.median(dd).round(2), "<10mm", (dd < 10).mean().round(3), flush=True)
yh, zh, ang, tz, ty = p
ax = np.array([1.0, ty, tz]) / np.linalg.norm([1.0, ty, tz])
hc = np.array([xc, yh, zh])
lid = lid_mask(hc, ax, ang)
skin = base[lid]
opentris = tr[is_open].copy()
opentris["v"] = ((opentris["v"].astype(float) - hc) @ R_of(-ang, ax).T + hc).astype("<f4")
ds, _ = cKDTree(skin["v"].mean(1)).query(opentris["v"].mean(1), distance_upper_bound=20)
save(f"{C}/b3_lid.stl", np.concatenate([skin, opentris[ds > 6]]))
pieces = [base[~lid]]
lc = bc[lid]
lo, hi = lc.min(0) - [80, 80, 400], lc.max(0) + [80, 80, 0]
tb = cKDTree(bc[~lid][::2])
acc = None
for name, m in (("rear_bumper_trunk_open", load("rear_bumper_trunk_open")), ("trunk(non-lid)", tr[~is_open])):
    c = m["v"].mean(1).astype(float)
    inz = np.all((c >= lo) & (c <= hi), axis=1)
    dn, _ = tb.query(c[inz], distance_upper_bound=20)
    ok = dn > 7
    if acc is not None:
        ok &= cKDTree(acc).query(c[inz], distance_upper_bound=20)[0] > 6
    sel = np.zeros(len(m), bool)
    sel[np.where(inz)[0][ok]] = True
    acc = c[sel] if acc is None else np.concatenate([acc, c[sel]])
    print(name, "fill +", int(sel.sum()), flush=True)
    pieces.append(m[sel])
save(f"{C}/b3_nolid.stl", np.concatenate(pieces))
subprocess.run(["python", f"{ROOT}/projects/subaru-wrx-vb/tools/split_plate.py", f"{C}/b3_nolid.stl",
                f"{C}/b3.stl", f"{C}/b3_plate.stl"], check=True)
json.dump({"pivot": (hc * S + RL).tolist(), "axis": ax.tolist(), "open_deg": float(ang),
           "fit_median_mm": float(np.median(dd)), "fit_within10mm": float((dd < 10).mean())},
          open(f"{C}/b3_hinge.json", "w"), indent=1)
