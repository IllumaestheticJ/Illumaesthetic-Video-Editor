"""Fit the match camera to a still photo by silhouette-to-edge chamfer (plus optional landmark pairs).
Hand-picked landmarks alone solved badly on the 400Z SEMA photo (livery placement and soft body corners make
points ambiguous), so this aligns the scan's projected outline with the photo's edges.
  python fit_cam.py verts.npz photo.jpg cam_init.json cam_out.json [--points points.json] [--overlay out.png]
Camera json = shot.py convention: {loc, target, focal (sensor 36, horizontal fit), roll (deg)}."""
import argparse, json, math
import numpy as np, cv2
from scipy.optimize import minimize

def basis(loc, target, roll):
    f = np.asarray(target, float) - loc; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    a = math.radians(roll); return f, r * math.cos(a) + u * math.sin(a), u * math.cos(a) - r * math.sin(a)

def project(P, loc, target, roll, focal, W, H, pp=(0.0, 0.0)):
    f, r, u = basis(loc, target, roll); d = P - loc; z = d @ f; fx = focal / 36.0 * W
    return np.stack([W / 2 + pp[0] + fx * (d @ r) / z, H / 2 + pp[1] - fx * (d @ u) / z], 1), z

def to_params(c):
    loc = np.array(c["loc"], float); d = np.array(c["target"], float) - loc
    return np.array([*loc, math.degrees(math.atan2(d[1], d[0])), math.degrees(math.atan2(d[2], math.hypot(d[0], d[1]))),
                     c.get("roll", 0.0), c["focal"], *c.get("pp", [0.0, 0.0])]), np.linalg.norm(d)

def from_params(p, dist):
    yaw, pit = math.radians(p[3]), math.radians(p[4])
    d = np.array([math.cos(pit) * math.cos(yaw), math.cos(pit) * math.sin(yaw), math.sin(pit)])
    c = {"loc": [float(v) for v in p[:3]], "target": [float(v) for v in p[:3] + d * dist], "roll": float(p[5]), "focal": float(p[6])}
    if len(p) > 7: c["pp"] = [float(p[7]), float(p[8])]
    return c

def silhouette(P, cam, W, H, s):
    w, h = int(W * s), int(H * s); uv, z = project(P, np.array(cam["loc"]), cam["target"], cam["roll"], cam["focal"], W, H, cam.get("pp", (0, 0)))
    uv = (uv[z > 0] * s).astype(np.int32); ok = (uv[:, 0] >= 0) & (uv[:, 0] < w) & (uv[:, 1] >= 0) & (uv[:, 1] < h)
    m = np.zeros((h, w), np.uint8); m[uv[ok, 1], uv[ok, 0]] = 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # outer outline only, holes filled
    f = np.zeros_like(m); cv2.drawContours(f, cs, -1, 255, -1)
    return f

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("verts"); ap.add_argument("photo"); ap.add_argument("init"); ap.add_argument("out")
    ap.add_argument("--points"); ap.add_argument("--overlay"); ap.add_argument("--keep", type=float, default=0.25)
    ap.add_argument("--wpts", type=float, default=0.5); ap.add_argument("--fix-focal", action="store_true")
    ap.add_argument("--init-overlay", action="store_true", help="also draw the initial camera's outline (red)")
    ap.add_argument("--maxfev", type=int, default=900)
    ap.add_argument("--drop", nargs="*", default=[], help="mesh objects to leave out (e.g. a front wheel steered in the photo)")
    ap.add_argument("--ignore", nargs="*", default=[], help="x0,y0,x1,y1 full-res boxes where outlines are not compared")
    ap.add_argument("--free-pp", action="store_true", help="also fit the principal point (photo may be an off-centre crop)")
    ap.add_argument("--mask", help="photo car mask (white car); fit outline to outline, symmetric chamfer - robust to clutter")
    a = ap.parse_args()
    D = np.load(a.verts); P = np.concatenate([D[k] for k in D.files if k not in a.drop]).astype(np.float64)
    P = P[np.random.default_rng(0).random(len(P)) < a.keep]
    img = cv2.imread(a.photo); H, W = img.shape[:2]
    pts = json.load(open(a.points))["points"] if a.points else []
    X = np.array([p["xyz"] for p in pts], float).reshape(-1, 3); U = np.array([p["px"] for p in pts], float).reshape(-1, 2)
    p0, dist = to_params(json.load(open(a.init)))
    if a.free_pp and len(p0) == 7: p0 = np.r_[p0, 0.0, 0.0]
    for s, trunc, step in ((0.25, 24, 1.0), (0.5, 12, 0.4)):
        g = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(img, (int(W * s), int(H * s)), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY), (3, 3), 0)
        e = cv2.Canny(g, 40, 110)
        if a.mask:
            pm = cv2.resize(cv2.imread(a.mask, 0), (int(W * s), int(H * s)), interpolation=cv2.INTER_NEAREST)
            e = cv2.morphologyEx((pm > 127).astype(np.uint8) * 255, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
        keep = np.ones(e.shape, bool)
        for bx in a.ignore:
            x0, y0, x1, y1 = (int(float(v) * s) for v in bx.split(",")); keep[y0:y1, x0:x1] = False
        eb = (e > 0) & keep; dt = cv2.distanceTransform(255 - e, cv2.DIST_L2, 3)
        def cost(p):
            if a.fix_focal: p = np.r_[p[:6], p0f, p[6:]]
            cam = from_params(p, dist); m = silhouette(P, cam, W, H, s)
            b = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
            b &= keep
            if b.sum() < 50: return 1e3
            c = np.minimum(dt[b], trunc).mean() / s  # in full-res px
            if a.mask:  # and the photo outline back to the model outline
                dm = cv2.distanceTransform(255 - b.astype(np.uint8) * 255, cv2.DIST_L2, 3)
                c = 0.5 * (c + np.minimum(dm[eb], trunc).mean() / s)
            if len(X):
                uv, _ = project(X, np.array(cam["loc"]), cam["target"], cam["roll"], cam["focal"], W, H, cam.get("pp", (0, 0)))
                c += a.wpts * np.sqrt(((uv - U) ** 2).sum(1)).mean()
            return c
        if a.fix_focal: p0f = p0[6]
        x0 = np.r_[p0[:6], p0[7:]] if a.fix_focal else p0
        sc = np.array([0.08, 0.08, 0.05, 1.0, 0.6, 0.6, 2.0, 15.0, 15.0])[:len(x0)] * step
        r = minimize(cost, x0, method="Nelder-Mead", options={"initial_simplex": np.vstack([x0] + [x0 + np.eye(len(x0))[i] * sc[i] for i in range(len(x0))]),
                                                              "maxfev": a.maxfev, "xatol": 1e-3, "fatol": 1e-3})
        p0 = np.r_[r.x[:6], p0f, r.x[6:]] if a.fix_focal else r.x
        print(f"scale {s}: cost {r.fun:.2f} px after {r.nfev} evals", flush=True)
    cam = from_params(p0, dist); json.dump(cam, open(a.out, "w"), indent=1); print(json.dumps(cam))
    if len(X):
        uv, _ = project(X, np.array(cam["loc"]), cam["target"], cam["roll"], cam["focal"], W, H, cam.get("pp", (0, 0)))
        for p, q in zip(pts, uv): print(f"  {p['name']}: {np.linalg.norm(q - p['px']):.1f}px")
    if a.overlay:
        if a.init_overlay:
            m0 = silhouette(P, json.load(open(a.init)), W, H, 1.0); b0 = cv2.morphologyEx(m0, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
        else: b0 = None
        m = silhouette(P, cam, W, H, 1.0); b = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
        o = img.copy()
        if b0 is not None: o[b0] = (0, 0, 255)
        o[b] = (0, 255, 0); cv2.imwrite(a.overlay, o)

if __name__ == "__main__":
    main()
