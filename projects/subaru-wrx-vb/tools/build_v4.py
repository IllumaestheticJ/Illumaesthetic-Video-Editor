"""v4 base + parts for the WRX VB from the mesh-smoothed masks of tools/seg_v4.py (reviewer v3 notes: the trunk was
not cut correctly, the front bumper had a ton of artifacts, the bumper should come off first and then come apart).

    python projects/subaru-wrx-vb/tools/build_v4.py <dec dir> <comp4 dir> <comp dir (b3_hinge.json)> <prep car4.json>

1. composite.py for the side and rear panels only (rear bumper, flares, skirt; fills from their panel-off states).
2. Front: every original car triangle in seg 'front' is removed (one smooth region, no speckle, no leftover skin);
   the hole is filled from the bumper-off state scans (Front Removed All first, then Bumpers Removed), only where they
   are > 6 mm from what the base keeps (no double skins = no mottling), small fill islands (< 150 tris) dropped.
   The licence plate (car triangles in the plate box) is saved as its own part to ride with the bumper.
   The car's own bumper skin (seg 'front' minus the plate) is saved too: it is the bumper as it sits on the car.
3. Lid: lid = car[seg 'lid'] (deck + rear face, smooth edge) + the open-lid capture's inner frame rotated closed;
   the base gets the tub from 'Rear Bumper Trunk Open' and the non-lid part of 'VB Trunk' (> 7 mm from the base).
Writes comp4/b4.stl, b4_lid.stl, b4_plate.stl, b4_fskin.stl.
"""
import json
import struct
import subprocess
import sys

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
D, C4, C3, LIKE = sys.argv[1:5]
ROOT = "/home/user/Illumaesthetic-Video-Editor"


def load(p):
    return np.fromfile(p if p.endswith(".stl") else f"{D}/{p}.stl", dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"wrx v4".ljust(80))
        f.write(struct.pack("<I", len(m)))
        m.tofile(f)
    print("wrote", p, len(m), flush=True)


def islands(m, min_tris):
    """keep triangles of mesh m in connected components (shared vertices) of >= min_tris"""
    v = m["v"].reshape(-1, 3)
    _, vid = np.unique(v, axis=0, return_inverse=True)
    n = len(m)
    TV = sparse.csr_matrix((np.ones(3 * n), (np.repeat(np.arange(n), 3), vid.ravel())))
    k, lab = connected_components(TV @ TV.T, directed=False)
    return np.bincount(lab, minlength=k)[lab] >= min_tris


car = load("car4_clean_np")
cc = car["v"].mean(1).astype(float)
seg = np.load(f"{C4}/seg_v4.npz")
front, lid = seg["front"], seg["lid"]
plate = (cc[:, 1] < -2345) & (np.abs(cc[:, 0] + 50) < 350) & (cc[:, 2] > 150) & (cc[:, 2] < 700)

# 1. side + rear panels
parts = ["rear_bumper_updated", "front_flare", "door_flare", "rear_flare", "side_skirt_only"]
fills = ["rear_bumper_removed", "bumpers_removed", "duckbill_scan", "side_skirt_off_doors_open"]
subprocess.run(["python", f"{ROOT}/projects/ferrari-296/tools/composite.py", f"{C4}/b4_step1.stl",
                "--car", f"{D}/car4_clean_np.stl", "--remove", *[f"{D}/{p}.stl" for p in parts],
                "--fill", *[f"{D}/{f}.stl" for f in fills], "--zone-pad", "60"], check=True)
base = load(f"{C4}/b4_step1.stl")
bc = base["v"].mean(1).astype(float)
dcar, icar = cKDTree(cc).query(bc, distance_upper_bound=0.01)
orig = dcar < 0.01
icar = np.where(orig, icar, 0)
in_front = orig & front[icar]
in_lid = orig & lid[icar]
in_plate = orig & plate[icar]
print("base", len(base), "front", int(in_front.sum()), "lid", int(in_lid.sum()), "plate", int(in_plate.sum()), flush=True)

save(f"{C4}/b4_plate.stl", car[plate])
save(f"{C4}/b4_fskin.stl", car[front & ~plate])

# 3 (first, so the front fill test sees the final base). lid
H = json.load(open(f"{C3}/b3_hinge.json"))
like = json.load(open(LIKE))
S, RL = like["unit_scale"], np.array(like["root_location"])
hc = (np.array(H["pivot"]) - RL) / S
ax = np.array(H["axis"]) / np.linalg.norm(H["axis"])
Rm = Rot.from_rotvec(-np.radians(H["open_deg"]) * ax).as_matrix()
tr = load("trunk")
tc = tr["v"].mean(1).astype(float)
k2 = lambda p: np.floor(p[:, 0] / 40).astype(np.int64) * 100000 + np.floor(p[:, 1] / 40).astype(np.int64)
u, inv = np.unique(k2(cc), return_inverse=True)
top = np.full(len(u), -1e9)
np.maximum.at(top, inv, cc[:, 2])
kt = k2(tc)
i = np.clip(np.searchsorted(u, kt), 0, len(u) - 1)
is_open = tc[:, 2] > np.where(u[i] == kt, top[i], -1e9) + 30
skin = car[lid]
inner = tr[is_open].copy()
inner["v"] = ((inner["v"].astype(float) - hc) @ Rm.T + hc).astype("<f4")
ds, _ = cKDTree(skin["v"].mean(1)).query(inner["v"].mean(1), distance_upper_bound=20)
inner = inner[ds > 6]
inner = inner[islands(inner, 100)]
save(f"{C4}/b4_lid.stl", np.concatenate([skin, inner]))

keep = ~(in_front | in_lid | in_plate)
pieces = [base[keep]]
kept_c = bc[keep]
tkeep = cKDTree(kept_c[::2])
lc = cc[lid]
lo, hi = lc.min(0) - [80, 80, 400], lc.max(0) + [80, 80, 0]
acc = None
for name, m in (("rear_bumper_trunk_open", load("rear_bumper_trunk_open")), ("trunk(non-lid)", tr[~is_open])):
    c = m["v"].mean(1).astype(float)
    inz = np.all((c >= lo) & (c <= hi), axis=1)
    dn, _ = tkeep.query(c[inz], distance_upper_bound=20)
    ok = dn > 7
    if acc is not None:
        ok &= cKDTree(acc).query(c[inz], distance_upper_bound=20)[0] > 6
    sel = np.zeros(len(m), bool)
    sel[np.where(inz)[0][ok]] = True
    sub = m[sel]
    sub = sub[islands(sub, 100)]
    acc = sub["v"].mean(1) if acc is None else np.concatenate([acc, sub["v"].mean(1)])
    print(name, "tub fill +", len(sub), flush=True)
    pieces.append(sub)

# 2. front fill
fc = cc[front | plate]
lo, hi = fc.min(0) - 40, fc.max(0) + [40, 40, 0]
acc = None
for name in ("front_removed_all", "bumpers_removed"):
    m = load(name)
    c = m["v"].mean(1).astype(float)
    inz = np.all((c >= lo) & (c <= hi), axis=1)
    dn, _ = tkeep.query(c[inz], distance_upper_bound=20)
    ok = dn > 6
    if acc is not None:
        ok &= cKDTree(acc).query(c[inz], distance_upper_bound=20)[0] > 6
    sel = np.zeros(len(m), bool)
    sel[np.where(inz)[0][ok]] = True
    sub = m[sel]
    sub = sub[islands(sub, 150)]
    acc = sub["v"].mean(1) if acc is None else np.concatenate([acc, sub["v"].mean(1)])
    print(name, "front fill +", len(sub), flush=True)
    pieces.append(sub)
save(f"{C4}/b4.stl", np.concatenate(pieces))
