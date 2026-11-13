"""Nest the lookbook kit into the scan (v4; replaces kit_nest.py's 3D-radius cut, which is kept only for STOCK/sample).
Pass A removes the lookbook's stock pieces by footprint, pass B removes scan skin that still COVERS a kit part.

Depth test from 200 directions (4 mm orthographic pixels): a scan triangle goes to cut_<part> when, seen along a direction
the part's surface faces (n.view > 0.93), it sits 2-30 mm in front of that surface. The model-to-scan fit is 6.8 mm median
and the kit sits inside the stock skin in places (duckbill, spats, eyelids), so the scan otherwise hides the part.
    python kit_nest2.py      (rewrites nest/<obj>_keep.stl, adds to nest/cut_<part>__<obj>.stl)"""
import itertools, json, os, sys
import numpy as np
from scipy.ndimage import maximum_filter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stlio import read, write
from kit_nest import sample  # noqa

M = "/home/user/media/toyota-mr2-spyder"; O = f"{M}/nest"; PX = 4.0; NEAR, FAR, FACE = 2.0, 30.0, 0.93
PARTS = ["duckbill", "rear_spats", "eyelids", "front_bumper", "side_skirts", "hood_vents", "diffuser", "hardtop", "tc_wing_kit"]
_k = np.arange(200) + 0.5; _ph = np.arccos(1 - 2 * _k / 200); _th = np.pi * (1 + 5 ** 0.5) * _k
DIRS = list(np.stack([np.cos(_th) * np.sin(_ph), np.sin(_th) * np.sin(_ph), np.cos(_ph)], 1))   # 200 even directions; FACE 0.93 keeps the
# lateral reach of the cut under ~12 mm (26 axis directions at 0.7 / 40 mm left 20-30 mm black seams round the vents and eyelids)


def basis(w):
    a = np.array([0, 0, 1.0]) if abs(w[2]) < 0.9 else np.array([1.0, 0, 0])
    u = np.cross(a, w); u /= np.linalg.norm(u); return u, np.cross(w, u)


def psample(d, step=2.0):
    v = d["v"].astype(np.float64); a, b, c = v[:, 0], v[:, 1], v[:, 2]
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    n = np.maximum(1, (area / (step * step)).astype(int)); idx = np.repeat(np.arange(len(v)), n)
    r = np.random.default_rng(1).random((len(idx), 2)); s = np.sqrt(r[:, 0]); u, w = 1 - s, s * r[:, 1]
    nn = np.cross(b - a, c - a); nn /= np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-9)
    return a[idx] * u[:, None] + b[idx] * (s - w)[:, None] + c[idx] * w[:, None], nn[idx]


from kit_nest import STOCK  # noqa
SRC = sys.argv[1] if len(sys.argv) > 1 else "dec"     # "dec" = start from the uncut scan objects
SCAN = {"base": "base_L", "hood": "hood_L", "lid": "rearlid_L"}
# pass A: the lookbook's stock pieces, by FOOTPRINT (scan within +-30 mm of the stock surface, seen within 10 deg of its normal:
#         no lateral margin, so the scan butts against the part edge - a 3D radius left 15 mm black seams round the vents).
# pass B: scan still covering a kit part (2-20 mm in front of it, within 21 deg).
PASSES = [(p, ss, -30.0, 30.0, 0.985) for p, ss in STOCK.items()] + [(p, ["part_" + p], NEAR, 20.0, FACE) for p in PARTS]
geo = {}
for p, ss, *_ in PASSES:
    for n in ss:
        if n not in geo:
            geo[n] = psample(read(f"{M}/kit/scan/{n}.stl"))
os.makedirs(O, exist_ok=True); rep = {}
for obj in ("base", "hood", "lid"):
    d = read(f"{M}/dec/{SCAN[obj]}.stl"); c = d["v"].astype(np.float64).mean(1); owner = np.full(len(c), -1); names = []
    for i, (p, ss, near, far, face) in enumerate(PASSES):
        names.append(p)
        P = np.vstack([geo[n][0] for n in ss]); N = np.vstack([geo[n][1] for n in ss]); lo, hi = P.min(0) - 60, P.max(0) + 60
        cand = np.where(np.all((c > lo) & (c < hi), axis=1) & (owner < 0))[0]
        if not len(cand):
            continue
        hit = np.zeros(len(cand), bool)
        for w in DIRS:                                  # w points from the surface toward the viewer
            f = N @ w > face
            if f.sum() < 200:
                continue
            u, v = basis(w); Q = P[f]
            x = np.floor(Q @ u / PX).astype(int); y = np.floor(Q @ v / PX).astype(int); z = Q @ w
            x0, y0 = x.min() - 1, y.min() - 1; W, H = x.max() - x0 + 2, y.max() - y0 + 2
            dep = np.full((W, H), -np.inf); np.maximum.at(dep, (x - x0, y - y0), z)          # outermost surface per pixel
            dep = maximum_filter(dep, size=3)                   # close 1-px sampling holes (left scan flecks inside the vents)
            cx = np.floor(c[cand] @ u / PX).astype(int) - x0; cy = np.floor(c[cand] @ v / PX).astype(int) - y0
            ok = (cx >= 0) & (cx < W) & (cy >= 0) & (cy < H); pd = np.full(len(cand), -np.inf); pd[ok] = dep[cx[ok], cy[ok]]
            dz = c[cand] @ w - pd
            hit |= (dz > near) & (dz < far)
        owner[cand[hit]] = i
    for p in dict.fromkeys(names):
        m = np.isin(owner, [i for i, n in enumerate(names) if n == p])
        if m.sum() > 50:
            write(f"{O}/cut_{p}__{obj}.stl", d[m]); rep[f"cut_{p}__{obj}"] = int(m.sum())
        else:
            owner[m] = -1
    write(f"{O}/{obj}_keep.stl", d[owner < 0]); rep[f"{obj}_keep"] = int((owner < 0).sum())
json.dump(rep, open(f"{O}/nest2.json", "w"), indent=1); print(json.dumps(rep))
