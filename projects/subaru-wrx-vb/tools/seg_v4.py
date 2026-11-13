"""v4 segmentation of the full car mesh (raw Artec mm) into front-bumper skin and trunk-lid skin, by state-scan
difference on the car's own surface (v3 used point distances to the part scans and a 15 mm grid: speckled hood /
headlights, mottled double skins at the front, stair-stepped lid). Writes <out>/seg_v4.npz with boolean masks over
car4_clean_np triangles: 'front' (bumper skin + car geometry seen behind it, gone when the bumper is off) and 'lid'.

    python projects/subaru-wrx-vb/tools/seg_v4.py <dec dir> <out dir> <prep car4.json> <comp/b3_hinge.json>

Front: candidates are car triangles near the bumper part scans (assembly, shell, grille, garnish; 15 mm) or inside the
bumper's front-view footprint (15 mm columns) between its front face and 40 mm behind its back face. A candidate stays
when the bumper-off state scans have a surface within 4 mm (it exists unchanged with the bumper off: headlights,
fenders, structure seen through the grille). The mask is then smoothed on the mesh (vertex-ring majority, 4 passes)
and small islands are absorbed, so the cut follows the bumper's real edge instead of speckling.
Lid: car triangles within 15 mm of the open-lid capture rotated closed about the fitted hinge (deck AND rear face),
mirrored about the centre line, smoothed the same way, small islands absorbed, largest component kept.
('No Trunk' looked like a lid-off state but is the left rear quarter only, so it cannot define the lid.)
"""
import sys

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
D, OUT, LIKE, HINGE = sys.argv[1:5]
SEED = 15.0
load = lambda n: np.fromfile(f"{D}/{n}.stl", dtype=TRI, offset=84)

car = load("car4_clean_np")
V = car["v"].reshape(-1, 3)
uv, vid = np.unique(V, axis=0, return_inverse=True)
F = vid.reshape(-1, 3)
nT, nV = len(F), len(uv)
TV = sparse.csr_matrix((np.ones(3 * nT), (np.repeat(np.arange(nT), 3), F.ravel())), shape=(nT, nV))
VT = TV.T.tocsr()
deg = np.asarray(VT.sum(1)).ravel()
cc = car["v"].mean(1).astype(float)
print("car", nT, "tris", nV, "verts", flush=True)


def smooth(m, passes=4):
    m = m.astype(float)
    for _ in range(passes):
        vm = (VT @ m) / np.maximum(deg, 1)
        m = ((TV @ vm) / 3 > 0.5).astype(float)
    return m > 0.5


def components(sel):
    idx = np.where(sel)[0]
    sub = TV[idx]
    A = sub @ sub.T
    n, lab = connected_components(A, directed=False)
    return idx, n, lab


def absorb(mask, max_island):
    """Flip small connected islands of either label (on the mesh) to the surrounding label."""
    for val in (False, True):
        idx, n, lab = components(mask == val)
        sizes = np.bincount(lab, minlength=n)
        small = sizes[lab] < max_island
        mask[idx[small]] = not val
    return mask


def erode(m, n):
    for _ in range(n):
        vfull = (VT @ m.astype(float)) >= deg - 0.5
        m = (TV @ vfull.astype(float)) > 2.5
    return m


def dilate(m, n):
    for _ in range(n):
        vany = (VT @ m.astype(float)) > 0.5
        m = (TV @ vany.astype(float)) > 0.5
    return m


def absorb_holes(mask, max_hole):
    idx, n, lab = components(~mask)
    sizes = np.bincount(lab, minlength=n)
    mask[idx[sizes[lab] < max_hole]] = True
    return mask


def column_ext(p, G, axes=(0, 2)):
    k = np.floor(p[:, axes[0]] / G).astype(np.int64) * 1_000_000 + np.floor(p[:, axes[1]] / G).astype(np.int64)
    return k


# ---------- front
bset = np.vstack([load(n)["v"].mean(1) for n in ("front_bumper_inside_parts_included",
                  "front_bumper_inside_parts_removed", "front_grille", "front_bumper_lower_garnish")]).astype(float)
st = np.vstack([load(n)["v"].mean(1) for n in ("front_removed_all", "bumpers_removed")]).astype(float)
st = st[st[:, 1] < -1100]
zone = (cc[:, 1] < bset[:, 1].max() + 60) & (cc[:, 2] < bset[:, 2].max() + 40)
zi = np.where(zone)[0]
db, _ = cKDTree(bset[::2]).query(cc[zi], distance_upper_bound=15)
G = 15.0
kb = column_ext(bset, G)
ku, inv = np.unique(kb, return_inverse=True)
ylo = np.full(len(ku), 1e9); yhi = np.full(len(ku), -1e9)
np.minimum.at(ylo, inv, bset[:, 1]); np.maximum.at(yhi, inv, bset[:, 1])
kq = column_ext(cc[zi], G)
j = np.clip(np.searchsorted(ku, kq), 0, len(ku) - 1)
hit = ku[j] == kq
yq = cc[zi, 1]
incol = hit & (yq > ylo[j] - 30) & (yq < yhi[j] + 40)
ds, _ = cKDTree(st).query(cc[zi], distance_upper_bound=4)
cand = (db < 15) | incol
front = np.zeros(nT, bool)
front[zi[cand & (ds >= 4)]] = True
print("front raw", int(front.sum()), flush=True)
front = smooth(front)
front &= zone
front = absorb(front, 400)
print("front final", int(front.sum()), flush=True)

# ---------- lid
# seed = the 'VB Trunk' open-lid capture (points > 30 mm above the closed car) rotated closed about the refitted hinge
# (comp/b3_hinge.json, median 6.7 mm); it includes the lid's rear face, which v3's top-skin filter left on the car.
import json
from scipy.spatial.transform import Rotation as Rot
H = json.load(open(HINGE))
like = json.load(open(LIKE))
S, RL = like["unit_scale"], np.array(like["root_location"])
hc = (np.array(H["pivot"]) - RL) / S
ax = np.array(H["axis"]) / np.linalg.norm(H["axis"])
tc = load("trunk")["v"].mean(1).astype(float)
k2 = lambda p: np.floor(p[:, 0] / 40).astype(np.int64) * 100000 + np.floor(p[:, 1] / 40).astype(np.int64)
u, inv = np.unique(k2(cc), return_inverse=True)
top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
kt = k2(tc); i = np.clip(np.searchsorted(u, kt), 0, len(u) - 1)
openp = tc[tc[:, 2] > np.where(u[i] == kt, top[i], -1e9) + 30]
closed = (openp - hc) @ Rot.from_rotvec(-np.radians(H["open_deg"]) * ax).as_matrix().T + hc
rz = (cc[:, 1] > closed[:, 1].min() - 60) & (cc[:, 2] > closed[:, 2].min() - 60)
ri = np.where(rz)[0]
dl, _ = cKDTree(closed).query(cc[ri], distance_upper_bound=SEED)
seed = dl < SEED
xc = 0.5 * (cc[:, 0].min() + cc[:, 0].max())
L = cc[ri][seed]
mir = cc[ri].copy(); mir[:, 0] = 2 * xc - mir[:, 0]
dm, _ = cKDTree(L).query(mir, distance_upper_bound=10)
lid = np.zeros(nT, bool)
lid[ri[seed | (dm < 10)]] = True
print("lid seed", int(seed.sum()), "with mirror", int(lid.sum()), flush=True)
lid = smooth(lid, 6)
lid = absorb(lid, 1500)
lid = dilate(erode(lid, 6), 6) & lid  # opening: drops thin spikes along the tail-light edge
lid = absorb_holes(lid, 40000)  # the centre (badge/camera) area the open capture missed rides with the lid
idx, n, lab = components(lid)
if n > 1:
    big = np.argmax(np.bincount(lab))
    lid[idx[lab != big]] = False
print("lid final", int(lid.sum()), "x", cc[lid, 0].min().round(), cc[lid, 0].max().round(), "y",
      cc[lid, 1].min().round(), cc[lid, 1].max().round(), "z", cc[lid, 2].min().round(), cc[lid, 2].max().round(),
      flush=True)
np.savez_compressed(f"{OUT}/seg_v4.npz", front=front, lid=lid)
