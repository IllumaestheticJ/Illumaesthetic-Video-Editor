"""Solve the listing 360-viewer camera from the car's silhouette (point-cloud projection, IoU fit) - adapted from
mazda-miata-nd/tools/solve_listing.py, with paths as arguments, a full 360 deg azimuth grid and both mirror states.

  solve_listing.py <screenshot.png> <car.stl> <prep.json> <out.json> <overlay_prefix>
                   [--crop x0,y0,x1,y1] [--thr 55] [--fill 0.84] [--step 6] [--tz 0.73] [--refine-only a,e,d,mirror]

screenshot : mobile listing capture, 1179x2097 (a SOLVE-ONLY capture with the viewer toolbar hidden is fine: same layout)
car.stl    : raw scan (binary STL, mm); prepped = raw * unit_scale + root_location (prep.json)
prepped frame: front = -Y, car's right = -X, Z up.

Model: pinhole at loc = T + d*(cos e sin a, -cos e cos a, sin e) looking at T (up = +Z), i.e. az 0 = straight in front of
the car, az 90 = camera on +X (the car's LEFT side), az 180 = behind. Screenshot px: U = crop.x0 + tx + s*x/z,
V = crop.y0 + ty - s*y/z (s = px per unit tangent). (tx, ty) is where the look-at target lands, so the fit is a camera
looking at T with a lens shift; a shot camera at loc looking at T WITHOUT shift gives the same picture translated.

Output map {k, ox, oy} for cta_card.py --map assumes the scan shot's LAST FRAME is rendered 1080x1920 from
C(t, loc, target, focal) with no lens shift, so the look-at target sits at the frame centre (540, 960):
  focal_36 = 36 * (s / k) / 1080   (mm, 36 mm-wide sensor, horizontal fit)
  ox = crop.x0 + tx - 540 k,  oy = crop.y0 + ty - 960 k
k is free (it only trades against focal): chosen so the car's bbox is --fill of the 1080 frame width.
"""
import argparse, json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_closing, binary_fill_holes, binary_erosion, label, sobel, gaussian_filter
from scipy.optimize import minimize

ap = argparse.ArgumentParser()
ap.add_argument("screenshot"); ap.add_argument("stl"); ap.add_argument("prep"); ap.add_argument("out"); ap.add_argument("overlay")
ap.add_argument("--crop", default="199,177,980,762", help="viewer sheet rect in screenshot px (ia-spin__sheet rect x3)")
ap.add_argument("--thr", type=float, default=55)
ap.add_argument("--fill", type=float, default=0.84)
ap.add_argument("--step", type=int, default=6)
ap.add_argument("--tz", type=float, default=None, help="look-at height (default: bbox mid height)")
ap.add_argument("--refine-only", default=None)
A = ap.parse_args()
CROP = tuple(int(v) for v in A.crop.split(","))
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])

rgb = np.asarray(Image.open(A.screenshot).convert("RGB"))[CROP[1]:CROP[3], CROP[0]:CROP[2]]
im = rgb.astype(float).mean(2)
raw = binary_closing(im > A.thr, iterations=2)
lab, n = label(raw)
sizes = np.bincount(lab.ravel()); sizes[0] = 0
tgt = binary_fill_holes(lab == sizes.argmax())  # the car = largest bright blob (UI toggle / logos are smaller)
Ht, Wt = tgt.shape
ys, xs = np.where(tgt)
print("target bbox (crop px)", xs.min(), xs.max(), ys.min(), ys.max(), "area", tgt.sum())

L = json.load(open(A.prep)); root = np.array(L["root_location"]); us = L.get("unit_scale", 0.001)
tri = np.fromfile(A.stl, dtype=TRI, offset=84)
Pall = tri["v"].mean(1).astype(np.float64) * us + root
v = tri["v"].astype(np.float64)
Nall = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); Nall /= np.maximum(1e-12, np.linalg.norm(Nall, axis=1))[:, None]
del v, tri
print("points", len(Pall), "bbox", Pall.min(0).round(3), Pall.max(0).round(3))
rng = np.random.default_rng(0)
Pc = Pall[rng.choice(len(Pall), min(len(Pall), 80000), replace=False)]    # coarse grid
Pf = Pall[rng.choice(len(Pall), min(len(Pall), 400000), replace=False)]   # refine
T = np.array([0.0, 0.0, A.tz if A.tz is not None else float(Pall[:, 2].min() + Pall[:, 2].max()) / 2])
MIR = np.array([-1.0, 1.0, 1.0])


def cam(a, e, d):
    a, e = np.radians(a), np.radians(e)
    loc = T + d * np.array([np.cos(e) * np.sin(a), -np.cos(e) * np.cos(a), np.sin(e)])
    f = (T - loc) / np.linalg.norm(T - loc); r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, f)
    return loc, f, r, u


def proj(P, a, e, d):
    loc, f, r, u = cam(a, e, d); q = P - loc; z = q @ f
    return (q @ r) / z, (q @ u) / z, z


def mask(p, P, close=2):
    a, e, d, s, tx, ty = p
    x, y, z = proj(P, a, e, d)
    U = np.rint(s * x + tx).astype(int); V = np.rint(-s * y + ty).astype(int)
    ok = (U >= 0) & (U < Wt) & (V >= 0) & (V < Ht)
    m = np.zeros((Ht, Wt), bool); m[V[ok], U[ok]] = True
    return binary_fill_holes(binary_closing(m, iterations=close))


def cost(p, P, close=2):
    if p[2] < 2.5 or not (-5 < p[1] < 89): return 1.0
    m = mask(p, P, close); return 1 - (m & tgt).sum() / max(1, (m | tgt).sum())


def fit_scale(P, a, e, d):
    """scale + offset from a bbox match for a given orbit (removes 3 dof from the grid)"""
    x, y, z = proj(P, a, e, d)
    s = (xs.max() - xs.min()) / (x.max() - x.min())
    return [a, e, d, s, xs.min() - s * x.min(), ys.min() + s * y.max()]


best = {}
for mir in (0, 1):
    Pg = Pc * MIR if mir else Pc; Pr = Pf * MIR if mir else Pf
    if A.refine_only:
        a0, e0, d0, m0 = [float(v) for v in A.refine_only.split(",")]
        if int(m0) != mir: continue
        seeds = [(0, fit_scale(Pg, a0, e0, d0))]
    else:
        grid = []
        for a in range(0, 360, A.step):          # FULL circle (Miata's first fit locked onto the wrong rear quarter)
            for e in range(3, 48, 5):
                for d in (4.5, 7, 11, 18):
                    p = fit_scale(Pg, a, e, d); grid.append((cost(p, Pg, 3), p))
        grid.sort(key=lambda g: g[0])
        print(f"mirror={mir} grid best", [(round(1 - c, 3), np.round(p[:3], 1).tolist()) for c, p in grid[:8]])
        # per-quadrant best, so the report shows how much worse the other quarters are
        for q in range(4):
            gq = [g for g in grid if q * 90 <= g[1][0] < (q + 1) * 90]
            print(f"   az {q*90:3d}-{q*90+90:3d}: best IoU {1 - gq[0][0]:.3f} at {np.round(gq[0][1][:3], 1).tolist()}")
        seeds, seen = [], []
        for c, p in grid:                         # distinct seeds (>= 20 deg apart in az)
            if all(min(abs(p[0] - q), 360 - abs(p[0] - q)) > 20 for q in seen):
                seeds.append((c, p)); seen.append(p[0])
            if len(seeds) == 3: break
    r = None
    for c0, p0 in seeds:
        rr = minimize(cost, fit_scale(Pr, *p0[:3]), args=(Pr,), method="Nelder-Mead",
                      options={"maxiter": 900, "xatol": 0.02, "fatol": 1e-5})
        rr = minimize(cost, rr.x, args=(Pr,), method="Nelder-Mead", options={"maxiter": 600, "xatol": 0.01, "fatol": 1e-6})
        print(f"   mirror={mir} seed az {p0[0]:.0f} -> IoU {1 - rr.fun:.4f} a,e,d = {np.round(rr.x[:3], 2).tolist()}")
        if r is None or rr.fun < r.fun: r = rr
    best[mir] = r


def shade(p, mir):
    """z-buffered point splat of ALL triangle centroids, lambert-shaded: the scan as the viewer would show it"""
    P = Pall * MIR if mir else Pall; N = Nall * MIR if mir else Nall
    a, e, d, s, tx, ty = p
    loc, f, r, u = cam(a, e, d)
    x, y, z = proj(P, a, e, d)
    U = np.rint(s * x + tx).astype(int); V = np.rint(-s * y + ty).astype(int)
    facing = np.abs(N @ f)
    lam = np.clip(np.abs(N @ (0.35 * r + 0.55 * u - 0.75 * f) / np.linalg.norm(0.35 * r + 0.55 * u - 0.75 * f)), 0, 1)
    ok = (U >= 1) & (U < Wt - 1) & (V >= 1) & (V < Ht - 1)
    U, V, z, lam = U[ok], V[ok], z[ok], lam[ok]
    o = np.argsort(-z)                              # far first, near overwrites
    img = np.zeros((Ht, Wt)); zb = np.full((Ht, Wt), np.inf)
    for du in (-1, 0, 1):
        for dv in (-1, 0, 1):                       # 3x3 splat, nearest wins
            zz = np.full((Ht, Wt), np.inf); np.minimum.at(zz, (V + dv, U + du), z)
            upd = zz < zb - 0.02; zb = np.where(upd, zz, zb)
    near = z <= zb[V, U] + 0.03
    img[V[o], U[o]] = 0                             # init
    oo = o[near[o]]
    img[V[oo], U[oo]] = 0.25 + 0.75 * lam[oo]
    cov = np.zeros((Ht, Wt), bool); cov[V[oo], U[oo]] = True
    img = np.where(cov, img, 0)
    return img, cov


def edges(g, sig=1.0):
    g = gaussian_filter(g, sig); return np.hypot(sobel(g, 0), sobel(g, 1))


def ncc(a, b, m):
    a = a[m] - a[m].mean(); b = b[m] - b[m].mean(); return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum() + 1e-9))


res = {}
inner = binary_erosion(tgt, iterations=6)
et = edges(im / 255.0)
for mir, r in best.items():
    sh, cov = shade(r.x, mir)
    shf = np.where(cov, sh, gaussian_filter(sh, 2))
    res[mir] = {"iou": 1 - r.fun, "edge_ncc": ncc(edges(shf), et, inner), "shade_ncc": ncc(gaussian_filter(shf, 1.5), gaussian_filter(im, 1.5), inner)}
    print(f"mirror={mir}: IoU {1 - r.fun:.4f}  edge-NCC inside car {res[mir]['edge_ncc']:.3f}  shading-NCC {res[mir]['shade_ncc']:.3f}")
    # overlays (full screenshot resolution of the viewer crop; x2 upscaled copy for looking at wheels/lamps)
    m = mask(r.x, Pf * MIR if mir else Pf)
    ov = rgb.copy().astype(float)
    silh = m ^ binary_erosion(m, iterations=2)
    ee = edges(shf); ee = ee / (np.percentile(ee[cov], 97) + 1e-9)
    ov[..., 0] = np.clip(ov[..., 0] + 255 * np.clip(ee, 0, 1) * 0.9, 0, 255)       # scan shading edges = red
    ov[silh] = (0, 255, 80)                                                          # scan silhouette = green
    Image.fromarray(ov.astype(np.uint8)).resize((Wt * 2, Ht * 2), Image.LANCZOS).save(f"{A.overlay}_m{mir}_edges.png")
    half = rgb.copy(); half[:, Wt // 2:] = 0  # placeholder to keep shapes
    side = np.concatenate([rgb, np.repeat((np.clip(shf, 0, 1) * 200)[..., None], 3, 2).astype(np.uint8)], 0)
    Image.fromarray(side).save(f"{A.overlay}_m{mir}_side.png")
    chk = np.zeros((Ht, Wt, 3), np.uint8); chk[..., 0] = tgt * 255; chk[..., 1] = m * 255
    Image.fromarray(chk).save(f"{A.overlay}_m{mir}_iou.png")
    # onion: checkerboard of listing / scan shading (24 px tiles)
    yy, xx = np.mgrid[0:Ht, 0:Wt]; cb = ((yy // 24 + xx // 24) % 2).astype(bool)
    on = np.where(cb[..., None], rgb, np.repeat((np.clip(shf, 0, 1) * 190)[..., None], 3, 2).astype(np.uint8))
    Image.fromarray(on.astype(np.uint8)).resize((Wt * 2, Ht * 2), Image.LANCZOS).save(f"{A.overlay}_m{mir}_checker.png")

# pick the state: silhouettes of a symmetric car cannot tell mirror from (-az), so use interior edge agreement
mir = max(res, key=lambda k: res[k]["edge_ncc"] + res[k]["iou"])
a, e, d, s, tx, ty = best[mir].x
a %= 360
loc, f, rr, u = cam(a, e, d)
P = Pall * MIR if mir else Pall
x, y, z = proj(P, a, e, d)
bw = s * (x.max() - x.min())                       # car bbox width, screenshot px
k = bw / (A.fill * 1080)
focal36 = 36 * (s / k) / 1080
ox = CROP[0] + tx - 540 * k; oy = CROP[1] + ty - 960 * k
fx = (s / k)                                       # frame px per unit tangent
bbox_frame = [540 + fx * x.min(), 960 - fx * y.max(), 540 + fx * x.max(), 960 - fx * y.min()]
out = {
    "convention": "prepped frame (raw*unit_scale+root_location): front=-Y, car right=-X, Z up. loc = target + d*(cos el sin az, "
                  "-cos el cos az, sin el); az 0 = in front of the car, 90 = car's left side (+X), 180 = behind. Camera looks at "
                  "target, up=+Z, no lens shift, so target projects to the 1080x1920 frame centre (540,960). focal_mm_sensor36 is "
                  "for sensor_width 36 mm with sensor_fit HORIZONTAL (frame width 1080); shot.py uses HORIZONTAL fit with "
                  "spec camera.sensor (default 20.25), so either set \"sensor\": 36 with focal_mm_sensor36 or keep 20.25 with "
                  "focal_mm_sensor20_25.",
    "mirror_x": bool(mir), "az": a, "el": e, "distance": d, "target": T.tolist(), "loc": loc.tolist(),
    "focal_mm_sensor36": focal36, "focal_mm_sensor20_25": focal36 * 20.25 / 36,
    "iou": res[mir]["iou"], "edge_ncc": res[mir]["edge_ncc"], "states": {str(m_): res[m_] | {"az": float(best[m_].x[0] % 360),
              "el": float(best[m_].x[1]), "d": float(best[m_].x[2])} for m_ in res},
    "map": {"k": k, "ox": ox, "oy": oy},
    "map_note": "1080x1920 last frame scaled by k, top-left at (ox,oy) in screenshot px (1179x2097), lands on the listing car",
    "car_bbox_in_frame_px": [round(v, 1) for v in bbox_frame], "fill": A.fill,
    "screenshot_fit": {"s": s, "tx": tx, "ty": ty, "crop": CROP, "target_px": [CROP[0] + tx, CROP[1] + ty],
                       "viewer_focal_mm_sensor36_for_sheet_width": 36 * s / (CROP[2] - CROP[0])},
    "screenshot": A.screenshot, "stl": A.stl, "prep": A.prep,
}
json.dump(out, open(A.out, "w"), indent=1)
print(json.dumps({k_: out[k_] for k_ in ("mirror_x", "az", "el", "distance", "target", "loc", "focal_mm_sensor36",
                                         "focal_mm_sensor20_25", "iou", "map", "car_bbox_in_frame_px")}, indent=1))
