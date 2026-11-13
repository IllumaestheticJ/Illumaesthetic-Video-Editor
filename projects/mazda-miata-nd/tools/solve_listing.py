"""Solve the listing 360-viewer camera from the car's silhouette (point-cloud projection, IoU fit).
Gives the orbit (azimuth a, elevation e, distance d about target c in the prepped frame) that the reassembly shot must
end on, so the scan frame shrinks onto the listing's car 1:1 (user: "the 1:1 to the mobile site doesn't match").
  solve_listing.py screenshot.png out.json"""
import sys, json, numpy as np
from PIL import Image
from scipy.ndimage import binary_closing, binary_fill_holes
from scipy.optimize import minimize
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
W = "/home/user/media/work/miata"
CROP = (180, 320, 1000, 700)  # viewer area in the 1179x1980 screenshot, logos below excluded
im = np.asarray(Image.open(sys.argv[1]).convert("L")).astype(float)[CROP[1]:CROP[3], CROP[0]:CROP[2]]
tgt = binary_fill_holes(binary_closing(im > 62, iterations=3)); tgt[:25] = False
Ht, Wt = tgt.shape
L = json.load(open(f"{W}/prep/car4.json")); root = np.array(L["root_location"])
P = np.fromfile(f"{W}/lvl/car6_clean.stl", dtype=TRI, offset=84)["v"].mean(1) * 0.001 + root
P = P[np.random.default_rng(0).choice(len(P), 250000, replace=False)]
import os
if os.environ.get("MIRROR"): P[:, 0] *= -1
C = np.array([0, 0, 0.55])

def cam(a, e, d):
    a, e = np.radians(a), np.radians(e)
    loc = C + d * np.array([np.cos(e) * np.sin(a), -np.cos(e) * np.cos(a), np.sin(e)])
    f = (C - loc) / np.linalg.norm(C - loc); r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, f)
    return loc, f, r, u

def mask(p):
    a, e, d, s, tx, ty = p
    loc, f, r, u = cam(a, e, d); q = P - loc
    z = q @ f; x = (q @ r) / z; y = (q @ u) / z
    U = (s * x + tx).astype(int); V = (-s * y + ty).astype(int)
    ok = (U >= 0) & (U < Wt) & (V >= 0) & (V < Ht)
    m = np.zeros((Ht, Wt), bool); m[V[ok], U[ok]] = True
    return binary_fill_holes(binary_closing(m, iterations=2))

def cost(p):
    m = mask(p); return 1 - (m & tgt).sum() / max(1, (m | tgt).sum())

ys, xs = np.where(tgt); cx, cy = xs.mean(), ys.mean(); wpx = xs.max() - xs.min()
def fit_scale(a, e, d):
    """scale + offset from bbox match for a given orbit (removes 3 dof from the search)"""
    loc, f, r, u = cam(a, e, d); q = P - loc; z = q @ f; x = (q @ r) / z; y = (q @ u) / z
    s = (xs.max() - xs.min()) / (x.max() - x.min())
    return [a, e, d, s, xs.min() - s * x.min(), ys.min() + s * y.max()]
grid = []
for a in range(185, 246, 4):
    for e in range(10, 40, 4):
        for d in (5, 7, 10, 15):
            p = fit_scale(a, e, d); grid.append((cost(p), p))
grid.sort(key=lambda g: g[0])
print("grid best", [(round(c, 3), np.round(p[:3], 1).tolist()) for c, p in grid[:5]])
r = None
for c0, p0 in grid[:4]:
    rr = minimize(cost, p0, method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.02, "fatol": 1e-5})
    if r is None or rr.fun < r.fun: r = rr
a, e, d, s, tx, ty = r.x; loc, f, rr, u = cam(a, e, d)
print("IoU", round(1 - r.fun, 4), "a e d", round(a, 2), round(e, 2), round(d, 2))
m = mask(r.x); ov = np.zeros((Ht, Wt, 3), np.uint8); ov[..., 0] = tgt * 255; ov[..., 1] = m * 255
Image.fromarray(ov).save(f"{W}/chk/listing_fit.png")
json.dump({"a": a, "e": e, "d": d, "s": s, "tx": tx, "ty": ty, "target": C.tolist(), "loc": loc.tolist(), "iou": 1 - r.fun,
           "crop": CROP, "note": "s = px per unit tan (u=x/z) in screenshot px; viewer crop origin = crop[0:2]"},
          open(sys.argv[2], "w"), indent=1)
