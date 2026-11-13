"""v5 rear segmentation (reviewer on v4: "the rear skirt area still has leftover bumper, and the trunk is still not
accurately cut out of the car"). v4 seeded the lid from the open-lid capture, which misses the lid's rear face: on the
VB the plate panel between the tail lights IS the lid, so v4 cut the panel in half. The rear bumper was still removed by
point distance to its part scan (leftovers) and the tub fill put bumper skin back.

    python projects/subaru-wrx-vb/tools/seg_v5.py <dec dir> <comp4 dir (seg_v4.npz in, seg_v5.npz out)>

Both rear masks are state differences on the car's own mesh, like the v4 front:
lid   = car triangles with NO surface within TOL of the trunk-open state ('Rear Bumper Trunk Open': bumper on, lid
        open), where that state sees something behind/below (so unscanned areas don't count), connected to the v4 deck.
rbump = car triangles with NO surface within TOL of 'Rear Bumper Removed' (lid closed, bumper off), inside the bumper
        part scan's rear-view footprint, minus the lid.
Each mask is smoothed on the mesh, small islands absorbed. Writes seg_v5.npz: front (from v4), lid, rbump.
"""
import sys

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
D, C4 = sys.argv[1:3]
TOL = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
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
old = np.load(f"{C4}/seg_v4.npz")


def smooth(m, passes=4):
    m = m.astype(float)
    for _ in range(passes):
        m = ((TV @ ((VT @ m) / np.maximum(deg, 1))) / 3 > 0.5).astype(float)
    return m > 0.5


def components(sel):
    idx = np.where(sel)[0]
    sub = TV[idx]
    n, lab = connected_components(sub @ sub.T, directed=False)
    return idx, n, lab


def absorb(mask, max_island):
    for val in (False, True):
        idx, n, lab = components(mask == val)
        mask[idx[np.bincount(lab, minlength=n)[lab] < max_island]] = not val
    return mask


def erode(m, n):
    for _ in range(n):
        m = (TV @ ((VT @ m.astype(float)) >= deg - 0.5).astype(float)) > 2.5
    return m


def dilate(m, n):
    for _ in range(n):
        m = (TV @ ((VT @ m.astype(float)) > 0.5).astype(float)) > 0.5
    return m


def cols(p, a, b, G=12.0):
    return np.floor(p[:, a] / G).astype(np.int64) * 1_000_000 + np.floor(p[:, b] / G).astype(np.int64)


def col_range(p, a, b, depth):
    k = cols(p, a, b)
    u, inv = np.unique(k, return_inverse=True)
    lo = np.full(len(u), 1e9); hi = np.full(len(u), -1e9)
    np.minimum.at(lo, inv, p[:, depth]); np.maximum.at(hi, inv, p[:, depth])
    return u, lo, hi


def col_lookup(u, q, a, b):
    k = cols(q, a, b)
    j = np.clip(np.searchsorted(u, k), 0, len(u) - 1)
    return j, u[j] == k


xc = 0.5 * (cc[:, 0].min() + cc[:, 0].max())
vl = old["lid"]
# ---------- lid
so = load("rear_bumper_trunk_open")["v"].mean(1).astype(float)
zone = (cc[:, 1] > cc[vl, 1].min() - 60) & (cc[:, 2] > 450) & (np.abs(cc[:, 0] - xc) < 820)
lidzone = zone
zi = np.where(zone)[0]
d, _ = cKDTree(so).query(cc[zi], distance_upper_bound=TOL)
# the open state must see something below (deck: tub under it) or in front (rear face: tub/latch panel behind it)
u, lo, hi = col_range(so, 0, 1, 2)
j, hit = col_lookup(u, cc[zi], 0, 1)
below = hit & (lo[j] < cc[zi, 2] - TOL)
u, lo, hi = col_range(so, 0, 2, 1)
j, hit = col_lookup(u, cc[zi], 0, 2)
behind = hit & (lo[j] < cc[zi, 1] - TOL)
lid = np.zeros(nT, bool)
lid[zi[(d > TOL) & (below | behind)]] = True
print("lid raw", int(lid.sum()), flush=True)
sd = lid.copy()
# Deck outline: the shut lines are dark grooves on a band-passed top-view height map (1.5 mm/px). Hand-placed guide
# points (read off chk/r5/top_dog.png) are snapped to the groove minimum within +-7 px, so the cut IS the panel gap.
# The state difference alone overshot the deck's front edge onto the rear glass by 50-80 mm (tub below the glass too).
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, median_filter
R, X0, Y1 = 1.5, -950.0, 2300.0
Wp, Hp = int(1900 / R), int(950 / R)
tp = np.vstack([car["v"].reshape(-1, 3), cc]).astype(float)
tp = tp[(tp[:, 1] > 1350) & (tp[:, 2] > 600)]
pu, pv = ((tp[:, 0] - X0) / R).astype(int), ((Y1 - tp[:, 1]) / R).astype(int)
ok = (pu >= 0) & (pu < Wp) & (pv >= 0) & (pv < Hp)
zm = np.full((Hp, Wp), -1e9); np.maximum.at(zm, (pv[ok], pu[ok]), tp[ok, 2])
has = zm > -1e8
nrm = lambda sg: gaussian_filter(np.where(has, zm, 0), sg) / np.maximum(gaussian_filter(has.astype(float), sg), 1e-3)
zs = nrm(1.5)
dog = zs - nrm(5.0)
GL = [(220, 118), (203, 140), (198, 160), (188, 193), (178, 220), (173, 260), (180, 313), (200, 343)]   # left side (u, v)
GF = [(200, 343), (280, 318), (353, 300), (453, 290), (560, 287), (602, 286)]                          # front arc, left half
UC = 602.5


def snap_side(g, mirror):
    g = np.array(g, float)
    vs = np.arange(g[0, 1], g[-1, 1] + 1)
    us = np.interp(vs, g[:, 1], g[:, 0])
    if mirror:
        us = 2 * UC - us
    off = np.array([np.argmin(dog[int(v), int(round(u)) - 7:int(round(u)) + 8]) - 7 for u, v in zip(us, vs)])
    uu = us + median_filter(off.astype(float), 15, mode="nearest")
    w = np.ones(len(vs))
    for _ in range(4):   # robust cubic through the snapped points: no stair steps, outlier snaps ignored
        co = np.polyfit(vs, uu, 3, w=w)
        r = np.abs(np.polyval(co, vs) - uu)
        w = 1.0 / (1.0 + (r / 1.5) ** 2)
    return np.c_[np.polyval(co, vs), vs]


Ls, Rs = snap_side(GL, False), snap_side(GL, True)
gf = np.array(GF, float)
uf = np.arange(int(Ls[-1, 0]), int(Rs[-1, 0]) + 1)
vf = np.interp(np.where(uf <= UC, uf, 2 * UC - uf), gf[:, 0], gf[:, 1])
offf = np.array([np.argmin(dog[int(round(v)) - 7:int(round(v)) + 8, int(u)]) - 7 for u, v in zip(uf, vf)])
front_arc = np.c_[uf, vf + median_filter(offf.astype(float), 25, mode="nearest")]
poly = np.vstack([[Ls[0, 0], 30], Ls, front_arc, Rs[::-1], [Rs[0, 0], 30]])
pim = Image.new("L", (Wp, Hp), 0)
ImageDraw.Draw(pim).polygon([tuple(q) for q in poly], fill=1)
pm = np.asarray(pim).astype(bool)
np.save(f"{C4}/lid_poly_px.npy", poly)
cu = np.clip(((cc[:, 0] - X0) / R).astype(int), 0, Wp - 1); cv = np.clip(((Y1 - cc[:, 1]) / R).astype(int), 0, Hp - 1)
inpoly = pm[cv, cu] & (cc[:, 1] > 1350)
topskin = cc[:, 2] > zs[cv, cu] - 30
lid = inpoly & (topskin | sd) & (cc[:, 2] > 450)
lid = smooth(lid, 2) & inpoly
lid = absorb(lid, 1500) & inpoly
idx, n, lab = components(lid)
lid[idx[lab != np.argmax(np.bincount(lab))]] = False
idx, n, lab = components(~lid)   # holes (badge, camera, plate recess) ride with the lid
inz = np.bincount(lab, weights=(lidzone & inpoly)[idx].astype(float), minlength=n) == np.bincount(lab, minlength=n)
lid[idx[(np.bincount(lab, minlength=n)[lab] < 40000) & inz[lab]]] = True
print("lid final", int(lid.sum()), "x", cc[lid, 0].min().round(), cc[lid, 0].max().round(), "y", cc[lid, 1].min().round(),
      cc[lid, 1].max().round(), "z", cc[lid, 2].min().round(), cc[lid, 2].max().round(), flush=True)

# ---------- rear bumper
bp = load("rear_bumper_updated")["v"].mean(1).astype(float)
sr = load("rear_bumper_removed")["v"].mean(1).astype(float)
zone = (cc[:, 1] > bp[:, 1].min() - 60) & (cc[:, 2] < bp[:, 2].max() + 40)
zi = np.where(zone)[0]
d, _ = cKDTree(sr).query(cc[zi], distance_upper_bound=TOL)
db, _ = cKDTree(bp[::2]).query(cc[zi], distance_upper_bound=15)
u, lo, hi = col_range(bp, 0, 2, 1)
j, hit = col_lookup(u, cc[zi], 0, 2)
incol = hit & (cc[zi, 1] > lo[j] - 40) & (cc[zi, 1] < hi[j] + 30)
u2, lo2, hi2 = col_range(bp, 1, 2, 0)   # side view: the bumper's wrap-around ends
j2, hit2 = col_lookup(u2, cc[zi], 1, 2)
incol |= hit2 & (((cc[zi, 0] > lo2[j2] - 30) & (cc[zi, 0] < lo2[j2] + 40)) | ((cc[zi, 0] > hi2[j2] - 40) & (cc[zi, 0] < hi2[j2] + 30)))
rb = np.zeros(nT, bool)
rb[zi[((db < 15) | incol) & (d > TOL)]] = True
rb &= ~lid
print("rbump raw", int(rb.sum()), flush=True)
rb = smooth(rb, 4) & zone & ~lid
rb = absorb(rb, 400) & ~lid
print("rbump final", int(rb.sum()), flush=True)
np.savez_compressed(f"{C4}/seg_v5.npz", front=old["front"], lid=lid, rbump=rb)
