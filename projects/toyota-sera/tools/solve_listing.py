"""Solve the camera of the Sera listing's 360 viewer on the mobile page from the car silhouette (point-cloud projection,
IoU fit; ported from projects/mazda-miata-nd/tools/solve_listing.py with a full 360-degree azimuth search).

    python3 solve_listing.py screenshot.png out.json [--k 0.55]

Orbit about C in the prepped (Blender) frame: loc = C + d*(cos e sin a, -cos e cos a, sin e); a=0 looks from the nose (-Y).
Screenshot px = s * (x/z) + tx, ty - s * (y/z). The render (1080x1920, horizontal sensor 20.25 mm) scaled by k with its
top-left at (ox, oy) in screenshot px lands 1:1 on the listing car when focal = s / k * 20.25 / 1080 (written to out.json
with ox/oy, ready for cta_card.py --map and the end camera of the reassembly shot).
"""
import json
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import binary_closing, binary_fill_holes, label
from scipy.optimize import minimize

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = "/home/user/media/toyota-sera"
CROP = (200, 340, 930, 680)  # viewer area in the 1179x2097 screenshot: below the 360/Photos buttons, above the watermark
shot, out = sys.argv[1], sys.argv[2]
K = float(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else 0.55

im = np.asarray(Image.open(shot).convert("L")).astype(float)[CROP[1]:CROP[3], CROP[0]:CROP[2]]
tgt = binary_fill_holes(binary_closing(im > 62, iterations=3))
lab, _ = label(tgt)
sz = np.bincount(lab.ravel()); sz[0] = 0
tgt = lab == sz.argmax()
Ht, Wt = tgt.shape
L = json.load(open(f"{M}/prep/car4.json"))
root = np.array(L["root_location"])
P = np.fromfile(f"{M}/clean/car4.stl", dtype=TRI, offset=84)["v"].mean(1) * 0.001 + root
P = P[np.random.default_rng(0).choice(len(P), 120000, replace=False)]
C = np.array([0, 0, 0.6])


def cam(a, e, d):
    a, e = np.radians(a), np.radians(e)
    loc = C + d * np.array([np.cos(e) * np.sin(a), -np.cos(e) * np.cos(a), np.sin(e)])
    f = (C - loc) / np.linalg.norm(C - loc)
    r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r)
    return loc, f, r, np.cross(r, f)


def proj(a, e, d):
    loc, f, r, u = cam(a, e, d)
    q = P - loc; z = q @ f
    return (q @ r) / z, (q @ u) / z


def mask(p):
    a, e, d, s, tx, ty = p
    x, y = proj(a, e, d)
    U = (s * x + tx).astype(int); V = (-s * y + ty).astype(int)
    ok = (U >= 0) & (U < Wt) & (V >= 0) & (V < Ht)
    m = np.zeros((Ht, Wt), bool); m[V[ok], U[ok]] = True
    return binary_fill_holes(binary_closing(m, iterations=2))


def cost(p):
    m = mask(p)
    return 1 - (m & tgt).sum() / max(1, (m | tgt).sum())


ys, xs = np.where(tgt)


def fit_scale(a, e, d):
    x, y = proj(a, e, d)
    s = (xs.max() - xs.min()) / (x.max() - x.min())
    return [a, e, d, s, xs.min() - s * x.min(), ys.min() + s * y.max()]


grid = []
for a in range(0, 360, 6):
    for e in range(6, 42, 5):
        for d in (5, 8, 12):
            p = fit_scale(a, e, d)
            grid.append((cost(p), p))
grid.sort(key=lambda g: g[0])
print("grid best", [(round(c, 3), np.round(p[:3], 1).tolist()) for c, p in grid[:6]])
best = None
for _, p0 in grid[:4]:
    rr = minimize(cost, p0, method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.02, "fatol": 1e-5})
    if best is None or rr.fun < best.fun:
        best = rr
a, e, d, s, tx, ty = best.x
loc = cam(a, e, d)[0]
iou = 1 - best.fun
print("IoU", round(iou, 4), "a e d", round(a, 2), round(e, 2), round(d, 2))
m = mask(best.x)
ov = np.zeros((Ht, Wt, 3), np.uint8); ov[..., 0] = tgt * 255; ov[..., 1] = m * 255
Image.fromarray(ov).save(out.replace(".json", "_fit.png"))
# screenshot-absolute principal point, then the render -> screenshot map for scale K
TX, TY = tx + CROP[0], ty + CROP[1]
F = s / K  # render px per unit tan
json.dump({"a": a, "e": e, "d": d, "s": s, "tx": TX, "ty": TY, "target": C.tolist(), "loc": loc.tolist(), "iou": iou,
           "k": K, "focal": F * 20.25 / 1080, "sensor": 20.25, "ox": TX - 540 * K, "oy": TY - 960 * K,
           "crop": CROP, "note": "render 1080x1920 scaled by k, top-left at (ox, oy) in screenshot px = listing car"},
          open(out, "w"), indent=1)
print(out)
