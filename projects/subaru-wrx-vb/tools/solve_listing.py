"""Solve the listing 360-viewer camera from the car's silhouette (point-cloud projection, IoU fit) - adapted from
mazda-miata-nd/tools/solve_listing.py: paths as arguments, a full 360 deg azimuth grid, both mirror states, a camera
ROLL (the WRX spin sheet is shot on a tilted orbit) and an interior-edge score (silhouette IoU alone barely constrains
distance, roll trades against elevation, and it cannot tell a mirrored car at all).

  solve_listing.py <screenshot.png> <car.stl> <prep.json> <out.json> <overlay_prefix>
        [--crop x0,y0,x1,y1] [--thr 55] [--fill 0.84] [--step 6] [--tz Z] [--mirror auto|0|1]
        [--refine-only a,e,d,roll] [--scan 'roll:-6,-3,0,3,6;d:8,10,13,18'] [--edge-refine]

screenshot : mobile listing capture, 1179x2097 (a SOLVE-ONLY capture with the viewer toolbar hidden is fine: same layout)
car.stl    : raw scan (binary STL, mm); prepped = raw * unit_scale + root_location (prep.json)
prepped frame: front = -Y, car's right = -X, Z up.

Model: pinhole at loc = T + d*(cos e sin a, -cos e cos a, sin e) looking at T, i.e. az 0 = straight in front of the car,
az 90 = camera on +X (the car's LEFT side), az 180 = behind. Un-rolled camera axes: f = forward, r = f x Z (right),
u = r x f (up). Roll rho (deg, + = picture turns counter-clockwise on screen): right' = cos r - sin u, up' = sin r + cos u.
Screenshot px: U = crop.x0 + tx + s*x'/z, V = crop.y0 + ty - s*y'/z (s = px per unit tangent). (tx, ty) is where the
look-at target lands: the fit is a camera looking at T with a lens shift; a shot camera at loc looking at T WITHOUT shift
gives the same picture translated.

Output map {k, ox, oy} for cta_card.py --map assumes the scan shot's LAST FRAME is rendered 1080x1920 from
C(t, loc, target, focal) with no lens shift AND with the solved roll (camera up = up_vector), so the look-at target sits
at the frame centre (540, 960):
  focal_36 = 36 * (s / k) / 1080   (mm, 36 mm-wide sensor, horizontal fit)
  ox = crop.x0 + tx - 540 k,  oy = crop.y0 + ty - 960 k
k is free (it only trades against focal): chosen so the car's bbox is --fill of the 1080 frame width.
"""
import argparse, json
import numpy as np
from PIL import Image
from scipy.ndimage import (minimum_filter, grey_dilation, binary_closing, binary_fill_holes, binary_erosion, label, sobel,
                           gaussian_filter)
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation

ap = argparse.ArgumentParser()
ap.add_argument("screenshot"); ap.add_argument("stl"); ap.add_argument("prep"); ap.add_argument("out"); ap.add_argument("overlay")
ap.add_argument("--crop", default="199,177,980,762", help="viewer sheet rect in screenshot px (ia-spin__sheet rect x3)")
ap.add_argument("--thr", type=float, default=55)
ap.add_argument("--fill", type=float, default=0.84)
ap.add_argument("--step", type=int, default=6)
ap.add_argument("--tz", type=float, default=None, help="look-at height (default: bbox mid height)")
ap.add_argument("--mirror", default="auto", help="auto = both states, pick by IoU + interior edges; 0/1 = force. CHECK the "
                "side-by-side images: on a symmetric car the scores are within noise (WRX: the fuel door decided it)")
ap.add_argument("--refine-only", default=None, help="a,e,d,roll: skip the grid")
ap.add_argument("--scan", default=None, help="'roll:-9,-6,-3,0,3,6,9;d:8,10,13,18': refit the rest at each fixed value, keep the best "
                "IoU + 0.5*edgeNCC (Nelder-Mead alone does not find the roll / distance)")
ap.add_argument("--edge-refine", action="store_true", help="final Nelder-Mead on IoU + interior edge NCC")
A = ap.parse_args()
CROP = tuple(int(v) for v in A.crop.split(","))
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])

rgb = np.asarray(Image.open(A.screenshot).convert("RGB"))[CROP[1]:CROP[3], CROP[0]:CROP[2]]
im = rgb.astype(float).mean(2)
lab, n = label(binary_closing(im > A.thr, iterations=2))
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
isub = rng.choice(len(Pall), min(len(Pall), 900000), replace=False); Ps, Ns = Pall[isub], Nall[isub]  # shading
T = np.array([0.0, 0.0, A.tz if A.tz is not None else float(Pall[:, 2].min() + Pall[:, 2].max()) / 2])
MIR = np.array([-1.0, 1.0, 1.0])
MIRS = (0, 1) if A.mirror == "auto" else (int(A.mirror),)


def cam(a, e, d, rho=0.0):
    a, e, rho = np.radians(a), np.radians(e), np.radians(rho)
    loc = T + d * np.array([np.cos(e) * np.sin(a), -np.cos(e) * np.cos(a), np.sin(e)])
    f = (T - loc) / np.linalg.norm(T - loc); r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, f)
    return loc, f, np.cos(rho) * r - np.sin(rho) * u, np.sin(rho) * r + np.cos(rho) * u


def proj(P, a, e, d, rho=0.0):
    loc, f, r, u = cam(a, e, d, rho); q = P - loc; z = q @ f
    return (q @ r) / z, (q @ u) / z, z


def mask(p, P, close=2):
    a, e, d, s, tx, ty, rho = p
    x, y, z = proj(P, a, e, d, rho)
    U = np.rint(s * x + tx).astype(int); V = np.rint(-s * y + ty).astype(int)
    ok = (U >= 0) & (U < Wt) & (V >= 0) & (V < Ht)
    m = np.zeros((Ht, Wt), bool); m[V[ok], U[ok]] = True
    return binary_fill_holes(binary_closing(m, iterations=close))


def cost(p, P, close=2):
    if p[2] < 2.5 or not (-5 < p[1] < 89) or abs(p[6]) > 45: return 1.0
    m = mask(p, P, close); return 1 - (m & tgt).sum() / max(1, (m | tgt).sum())


def fit_scale(P, a, e, d, rho=0.0):
    """scale + offset from a bbox match for a given orbit (removes 3 dof from the grid)"""
    x, y, z = proj(P, a, e, d, rho)
    s = (xs.max() - xs.min()) / (x.max() - x.min())
    return [a, e, d, s, xs.min() - s * x.min(), ys.min() + s * y.max(), rho]


def shade(p, mir, P=None, N=None):
    """z-buffered point splat of the triangle centroids, lambert-shaded: the scan roughly as the viewer shows it"""
    if P is None: P, N = Pall, Nall
    if mir: P = P * MIR; N = N * MIR
    a, e, d, s, tx, ty, rho = p
    loc, f, r, u = cam(a, e, d, rho)
    x, y, z = proj(P, a, e, d, rho)
    U = np.rint(s * x + tx).astype(int); V = np.rint(-s * y + ty).astype(int)
    lt = 0.35 * r + 0.55 * u - 0.75 * f; lt /= np.linalg.norm(lt)
    lam = np.abs(N @ lt)
    ok = (U >= 0) & (U < Wt) & (V >= 0) & (V < Ht)
    U, V, z, lam = U[ok], V[ok], z[ok], lam[ok]
    zb = np.full((Ht, Wt), np.inf); np.minimum.at(zb, (V, U), z)
    zb = minimum_filter(zb, 3)
    near = z <= zb[V, U] + 0.12                     # front skin only (the far side of the car is > 1 m behind)
    acc = np.zeros((Ht, Wt)); cnt = np.zeros((Ht, Wt))
    np.add.at(acc, (V[near], U[near]), 0.25 + 0.75 * lam[near]); np.add.at(cnt, (V[near], U[near]), 1)
    cov = cnt > 0
    img = np.where(cov, acc / np.maximum(cnt, 1), 0)
    hole = binary_fill_holes(binary_closing(cov, iterations=2)) & ~cov
    img = np.where(hole, grey_dilation(img, size=5), img)
    return img, cov | hole


def edges(g, sig=1.5):
    g = gaussian_filter(g, sig); return np.hypot(sobel(g, 0), sobel(g, 1))


def ncc(a, b, m):
    a = a[m] - a[m].mean(); b = b[m] - b[m].mean(); return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum() + 1e-9))


inner = binary_erosion(tgt, iterations=6)
et = edges(im / 255.0)


def edge_score(p, mir, full=False):
    sh, cov = shade(p, mir) if full else shade(p, mir, Ps, Ns)
    return ncc(edges(sh), et, inner)


def combo(p, mir, P):
    return cost(p, P) + 0.5 * (1 - edge_score(p, mir))


NM = dict(method="Nelder-Mead")
STEP = np.array([3.0, 3.0, 1.0, 0.0, 4.0, 4.0, 2.0])   # initial simplex steps: az, el, d, (3 % of s), tx, ty, roll


def simplex(x0, idx=range(7)):
    x0 = np.asarray(x0, float); st = STEP.copy(); st[3] = 0.03 * x0[3]; idx = list(idx)
    return np.vstack([x0[idx], x0[idx] + np.diag(st[idx])])


def scan(mir, name, col, values):
    """refit everything else at each fixed value of one parameter (distance or roll); score IoU + interior edges"""
    Pr = Pf * MIR if mir else Pf; x0 = np.array(best[mir].x); free = [i for i in range(7) if i != col]; rows = []
    for val in values:
        def fn(q):
            p = np.empty(7); p[free] = q; p[col] = val; return cost(p, Pr)
        p0 = np.array(fit_scale(Pr, *(val if i == col else x0[i] for i in (0, 1, 2, 6))))
        rr = minimize(fn, p0[free], options={"maxiter": 700, "xatol": 0.02, "fatol": 1e-5, "initial_simplex": simplex(p0, free)}, **NM)
        p = np.empty(7); p[free] = rr.x; p[col] = val
        es = edge_score(p, mir); rows.append((1 - rr.fun, es, p))
        print(f"   {name} scan mirror={mir} {name}={val:6.2f}: IoU {1 - rr.fun:.4f} edgeNCC {es:.3f} a,e,d,roll = {np.round(p[[0, 1, 2, 6]], 2).tolist()}")
    rows.append((1 - cost(x0, Pr), edge_score(x0, mir), x0))   # the incumbent stays unless a scan value beats it
    bi = max(rows, key=lambda r_: r_[0] + 0.5 * r_[1])
    best[mir].x = np.array(bi[2]); best[mir].fun = 1 - bi[0]
best = {}
for mir in MIRS:
    Pg = Pc * MIR if mir else Pc; Pr = Pf * MIR if mir else Pf
    if A.refine_only:
        a0, e0, d0, r0 = [float(v) for v in A.refine_only.split(",")]
        seeds = [fit_scale(Pr, a0, e0, d0, r0)]
    else:
        grid = []
        for a in range(0, 360, A.step):          # FULL circle (Miata's first fit locked onto the wrong rear quarter)
            for e in range(3, 48, 5):
                for d in (4.5, 7, 11, 18):
                    p = fit_scale(Pg, a, e, d); grid.append((cost(p, Pg, 3), p))
        grid.sort(key=lambda g: g[0])
        print(f"mirror={mir} grid (roll 0) best", [(round(1 - c, 3), np.round(p[:3], 1).tolist()) for c, p in grid[:6]])
        for q in range(4):                        # how much worse the other quarters are
            gq = [g for g in grid if q * 90 <= g[1][0] < (q + 1) * 90]
            print(f"   az {q*90:3d}-{q*90+90:3d}: best IoU {1 - gq[0][0]:.3f} at {np.round(gq[0][1][:3], 1).tolist()}")
        seeds, seen = [], []
        for c, p in grid:                         # distinct seeds (>= 20 deg apart in az), each with 3 roll starts
            if all(min(abs(p[0] - q), 360 - abs(p[0] - q)) > 20 for q in seen):
                seen.append(p[0]); seeds += [fit_scale(Pr, p[0], p[1], p[2], rho) for rho in (-8, 0, 8)]
            if len(seen) == 3: break
    r = None
    for p0 in seeds:
        rr = minimize(cost, p0, args=(Pr,), options={"maxiter": 1200, "xatol": 0.02, "fatol": 1e-5, "initial_simplex": simplex(p0)}, **NM)
        rr = minimize(cost, rr.x, args=(Pr,), options={"maxiter": 700, "xatol": 0.01, "fatol": 1e-6}, **NM)
        print(f"   mirror={mir} seed az {p0[0]:.0f} roll {p0[6]:+.0f} -> IoU {1 - rr.fun:.4f} a,e,d,roll = "
              f"{np.round(rr.x[[0, 1, 2, 6]], 2).tolist()}")
        if r is None or rr.fun < r.fun: r = rr
    best[mir] = r

for spec in (A.scan or "").split(";"):          # e.g. "roll:-9,-6,-3,0,3,6,9;d:8,10,13,18;roll:..." applied in order
    if spec:
        nm_, vals = spec.split(":")
        for mir in list(best): scan(mir, nm_, {"d": 2, "roll": 6, "el": 1}[nm_], [float(v) for v in vals.split(",")])
if A.edge_refine:
    for mir in list(best):
        Pr = Pf * MIR if mir else Pf; x0 = best[mir].x
        rr = minimize(combo, x0, args=(mir, Pr), options={"maxiter": 220, "xatol": 0.02, "fatol": 1e-5, "initial_simplex": simplex(x0) if False else np.vstack([x0, x0 + np.diag([1.0, 1.0, 0.7, 0.01 * x0[3], 1.5, 1.5, 0.8])])}, **NM)
        best[mir].x = rr.x; best[mir].fun = cost(rr.x, Pr)
        print(f"   edge-refine mirror={mir}: IoU {1 - best[mir].fun:.4f} a,e,d,roll = {np.round(rr.x[[0, 1, 2, 6]], 2).tolist()}")

res = {}
for mir, r in best.items():
    sh, cov = shade(r.x, mir)
    res[mir] = {"iou": 1 - r.fun, "edge_ncc": ncc(edges(sh), et, inner),
                "shade_ncc": ncc(gaussian_filter(sh, 1.5), gaussian_filter(im, 1.5), inner)}
    print(f"mirror={mir}: IoU {1 - r.fun:.4f}  edge-NCC inside car {res[mir]['edge_ncc']:.3f}  shading-NCC {res[mir]['shade_ncc']:.3f}")
    # overlays at the screenshot's own resolution, saved x2 so wheels / glass / lamps can be judged
    m = mask(r.x, Pf * MIR if mir else Pf)
    g3 = np.repeat((np.clip(sh, 0, 1) * 200)[..., None], 3, 2).astype(np.uint8)
    up = lambda arr: Image.fromarray(arr.astype(np.uint8)).resize((Wt * 2, Ht * 2), Image.LANCZOS)
    ov = rgb.copy().astype(float)
    ee = edges(sh, 1.0); ee = ee / (np.percentile(ee[cov], 97) + 1e-9)
    ov[..., 0] = np.clip(ov[..., 0] + 255 * np.clip(ee, 0, 1) * 0.9, 0, 255)       # scan shading edges = red
    ov[m ^ binary_erosion(m, iterations=2)] = (0, 255, 80)                          # scan silhouette = green
    up(ov).save(f"{A.overlay}_m{mir}_edges.png")
    Image.fromarray(np.concatenate([rgb, g3], 0)).save(f"{A.overlay}_m{mir}_side.png")
    yy, xx = np.mgrid[0:Ht, 0:Wt]
    up(np.where((((yy // 20) % 2) == 0)[..., None], rgb, g3)).save(f"{A.overlay}_m{mir}_strips.png")   # 20 px bands listing/scan
    chk = np.zeros((Ht, Wt, 3), np.uint8); chk[..., 0] = tgt * 255; chk[..., 1] = m * 255
    Image.fromarray(chk).save(f"{A.overlay}_m{mir}_iou.png")

mir = max(res, key=lambda k: res[k]["edge_ncc"] + res[k]["iou"])
a, e, d, s, tx, ty, rho = best[mir].x
a %= 360
loc, f, rr, u = cam(a, e, d, rho)
P = Pall * MIR if mir else Pall
x, y, z = proj(P, a, e, d, rho)
bw = s * (x.max() - x.min())                       # car bbox width, screenshot px
k = bw / (A.fill * 1080)
focal36 = 36 * (s / k) / 1080
ox = CROP[0] + tx - 540 * k; oy = CROP[1] + ty - 960 * k
fx = s / k                                         # frame px per unit tangent
bbox_frame = [540 + fx * x.min(), 960 - fx * y.max(), 540 + fx * x.max(), 960 - fx * y.min()]
Rm = np.column_stack([rr, u, -f])                  # Blender camera local axes (X right, Y up, -Z view) in world
out = {
    "convention": "prepped frame (raw*unit_scale+root_location): front=-Y, car right=-X, Z up. loc = target + d*(cos el sin az, "
                  "-cos el cos az, sin el); az 0 = in front of the car, 90 = car's left side (+X), 180 = behind. Camera at loc "
                  "looks at target, no lens shift, so target projects to the 1080x1920 frame centre (540,960); camera up = "
                  "up_vector (roll_deg about the view axis, + = picture turns counter-clockwise; plain look-at with Z up is "
                  "roll 0). focal_mm_sensor36 is for sensor_width 36 mm, sensor_fit HORIZONTAL (frame width 1080); shot.py "
                  "uses HORIZONTAL fit with spec camera.sensor (default 20.25): set \"sensor\": 36 with focal_mm_sensor36, or "
                  "keep 20.25 with focal_mm_sensor20_25.",
    "mirror_x": bool(mir), "az": a, "el": e, "distance": d, "roll_deg": rho, "target": T.tolist(), "loc": loc.tolist(),
    "up_vector": u.tolist(), "blender_rotation_euler_xyz_deg": Rotation.from_matrix(Rm).as_euler("xyz", degrees=True).tolist(),
    "focal_mm_sensor36": focal36, "focal_mm_sensor20_25": focal36 * 20.25 / 36,
    "iou": res[mir]["iou"], "edge_ncc": res[mir]["edge_ncc"],
    "states": {str(m_): res[m_] | {"az": float(best[m_].x[0] % 360), "el": float(best[m_].x[1]), "d": float(best[m_].x[2]),
                                    "roll": float(best[m_].x[6])} for m_ in res},
    "map": {"k": k, "ox": ox, "oy": oy},
    "map_note": "1080x1920 last frame (rendered WITH the roll) scaled by k, top-left at (ox,oy) in screenshot px (1179x2097), "
                "lands on the listing car. If the frame is rendered with a plain Z-up look-at instead, rotate it by roll_deg "
                "counter-clockwise about its centre (540,960) before applying the map.",
    "car_bbox_in_frame_px": [round(v_, 1) for v_ in bbox_frame], "fill": A.fill,
    "screenshot_fit": {"s": s, "tx": tx, "ty": ty, "crop": CROP, "target_px": [CROP[0] + tx, CROP[1] + ty],
                       "viewer_focal_mm_sensor36_for_sheet_width": 36 * s / (CROP[2] - CROP[0])},
    "screenshot": A.screenshot, "stl": A.stl, "prep": A.prep,
}
json.dump(out, open(A.out, "w"), indent=1)
print(json.dumps({k_: out[k_] for k_ in ("mirror_x", "az", "el", "distance", "roll_deg", "target", "loc", "up_vector",
                 "focal_mm_sensor36", "focal_mm_sensor20_25", "iou", "edge_ncc", "map", "car_bbox_in_frame_px")}, indent=1))
