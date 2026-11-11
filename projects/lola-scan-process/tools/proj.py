"""Fast numpy projection of a prepared scan (mesh_np.py npz) onto a real frame, for camera solving.

usage:
  proj.py overlay frame.png mesh.npz cam.json out.jpg          # cyan silhouette edge + filled tint
  proj.py look out_cam.json --loc x,y,z --target x,y,z --focal-px f [--roll deg] [--size 1080x1920]
  proj.py refine frame.png mesh.npz cam_in.json cam_out.json [--points pts.json] [--fix-f] [--ignore boxes]
          silhouette chamfer (GrabCut of the real car seeded by the projection) + landmark term

Cameras are ive camera JSON (opencv rvec/tvec + fx_px + blender block), so `ive render --camera` works.
"""
import sys, json, argparse
import numpy as np, cv2
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz


def cam_from_rt(rvec, tvec, fx, size, sensor=36.0, extra=None):
    R, _ = cv2.Rodrigues(np.asarray(rvec, float))
    t = np.asarray(tvec, float).reshape(3)
    loc = (-R.T @ t)
    Rb = R.T @ CV_TO_BLENDER_CAM
    w, h = size
    c = {"image_size": [w, h], "fx_px": float(fx), "focal_mm": float(fx) * sensor / w, "sensor_width_mm": sensor,
         "shift_x": 0.0, "shift_y": 0.0,
         "blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rb), "rotation_matrix": Rb.tolist()},
         "opencv": {"rvec": np.asarray(rvec, float).reshape(3).tolist(), "tvec": t.tolist()}}
    if extra:
        c.update(extra)
    return c


def look(loc, target, f, size, roll=0.0):
    loc = np.asarray(loc, float); fwd = np.asarray(target, float) - loc; fwd /= np.linalg.norm(fwd)
    up = np.array([0, 0, 1.0]); right = np.cross(fwd, up); right /= np.linalg.norm(right); down = np.cross(fwd, right)
    R = np.stack([right, down, fwd])  # world->cv camera rows
    if roll:
        a = np.radians(roll); Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]]); R = Rz @ R
    rvec, _ = cv2.Rodrigues(R); tvec = -R @ loc
    return cam_from_rt(rvec.reshape(3), tvec, f, size)


def K_of(cam, scale=1.0):
    w, h = cam["image_size"]; f = cam["fx_px"] * scale
    cx = (w / 2 - cam.get("shift_x", 0) * max(w, h)) * scale
    cy = (h / 2 + cam.get("shift_y", 0) * max(w, h)) * scale
    return np.array([[f, 0, cx], [0, f, cy], [0, 0, 1.0]])


def silhouette(V, F, rvec, tvec, K, w, h):
    p, _ = cv2.projectPoints(V, np.asarray(rvec, float), np.asarray(tvec, float), K, None)
    p = np.round(p.reshape(-1, 2) * 4).astype(np.int32)
    R, _ = cv2.Rodrigues(np.asarray(rvec, float)); z = (V @ R.T + np.asarray(tvec, float).reshape(1, 3))[:, 2]
    good = (z[F] > 0.05).all(1)
    m = np.zeros((h, w), np.uint8); cv2.fillPoly(m, list(p[F[good]]), 255, shift=2)
    return cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))


def overlay(frame, mesh, cam, out, pts=None):
    img = cv2.imread(frame); h, w = img.shape[:2]; m = np.load(mesh)
    sil = silhouette(m["v"], m["f"], cam["opencv"]["rvec"], cam["opencv"]["tvec"], K_of(cam), w, h)
    tint = img.copy(); tint[sil > 0] = (0.55 * tint[sil > 0] + 0.45 * np.array([255, 200, 0])).astype(np.uint8)
    e = cv2.morphologyEx(sil, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0; tint[e] = (255, 255, 0)
    if pts:
        P = json.load(open(pts))["points"]
        X = np.array([p["xyz"] for p in P], float)
        pr, _ = cv2.projectPoints(X, np.array(cam["opencv"]["rvec"]), np.array(cam["opencv"]["tvec"]), K_of(cam), None)
        for p, q in zip(P, pr.reshape(-1, 2)):
            cv2.circle(tint, tuple(int(v) for v in p["px"]), 7, (0, 255, 0), 2)
            cv2.line(tint, tuple(int(v) for v in p["px"]), tuple(int(v) for v in q), (0, 0, 255), 2)
            cv2.putText(tint, p["name"], tuple(int(v) + 8 for v in p["px"]), 0, 0.6, (0, 255, 0), 2)
    for x in range(0, w, 100):
        cv2.line(tint, (x, 0), (x, 12), (255, 255, 255), 1)
    for y in range(0, h, 100):
        cv2.line(tint, (0, y), (12, y), (255, 255, 255), 1)
    cv2.imwrite(out, tint, [cv2.IMWRITE_JPEG_QUALITY, 88])


def refine(frame, mesh, cam, out, pts=None, wpts=0.5, fix_f=False, ignore="", work=540, T=14, fix_h=None):
    from scipy.optimize import minimize
    img = cv2.imread(frame); H0, W0 = img.shape[:2]; s = work / W0
    small = cv2.resize(img, (work, int(H0 * s)), interpolation=cv2.INTER_AREA); h, w = small.shape[:2]
    m = np.load(mesh); V, F = m["v"], m["f"]
    r0 = np.array(cam["opencv"]["rvec"], float); t0 = np.array(cam["opencv"]["tvec"], float); f0 = cam["fx_px"]
    def Kf(f): return np.array([[f * s, 0, w / 2], [0, f * s, h / 2], [0, 0, 1]])
    m0 = silhouette(V, F, r0, t0, Kf(f0), w, h)
    gc = np.full((h, w), cv2.GC_BGD, np.uint8)
    gc[cv2.dilate(m0, np.ones((41, 41))) > 0] = cv2.GC_PR_BGD
    gc[cv2.dilate(m0, np.ones((9, 9))) > 0] = cv2.GC_PR_FGD
    gc[cv2.erode(m0, np.ones((21, 21))) > 0] = cv2.GC_FGD
    bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(small, gc, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
    pm = np.where((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(pm)
    if n > 1: pm = np.where(lab == 1 + np.argmax(st[1:, 4]), 255, 0).astype(np.uint8)
    edge = lambda mk: cv2.morphologyEx(mk, cv2.MORPH_GRADIENT, np.ones((3, 3))) > 0
    keep = np.ones((h, w), bool)
    for b in [x for x in ignore.split(";") if x]:
        x0, y0, x1, y1 = [int(float(v) * s) for v in b.split(",")]; keep[y0:y1, x0:x1] = False
    keep[:2, :] = keep[-2:, :] = False; keep[:, :2] = keep[:, -2:] = False  # frame border is not a car edge
    pe = edge(pm) & keep
    dp = np.minimum(cv2.distanceTransform((~pe).astype(np.uint8), cv2.DIST_L2, 3), T)
    P = json.load(open(pts))["points"] if pts else []
    X = np.array([p["xyz"] for p in P], float); U = np.array([p["px"] for p in P], float) * s
    def unpack(x):
        r = r0 + x[:3]; t = t0 + x[3:6]; f = f0 if fix_f else f0 * np.exp(x[6]); return r, t, f
    def cost(x):
        r, t, f = unpack(x)
        ms = silhouette(V, F, r, t, Kf(f), w, h); se = edge(ms) & keep
        if se.sum() < 10: return 1e6
        ds = np.minimum(cv2.distanceTransform((~se).astype(np.uint8), cv2.DIST_L2, 3), T)
        c = dp[se].mean() + ds[pe].mean()
        if len(P):
            pr, _ = cv2.projectPoints(X, r, t, Kf(f), None); c += wpts * np.sqrt(np.mean(np.sum((pr.reshape(-1, 2) - U) ** 2, 1)))
        if fix_h is not None:
            R, _ = cv2.Rodrigues(r); c += 50 * abs((-R.T @ t)[2] - fix_h)
        return c
    x0 = np.zeros(7)
    res = minimize(cost, x0, method="Powell", options={"maxiter": 4000, "xtol": 1e-4, "ftol": 1e-4})
    r, t, f = unpack(res.x)
    c = cam_from_rt(r, t, f, cam["image_size"], extra={"refine_cost": float(res.fun)})
    if len(P):
        pr, _ = cv2.projectPoints(X, r, t, K_of(c), None)
        c["rmse_px"] = float(np.sqrt(np.mean(np.sum((pr.reshape(-1, 2) - np.array([p["px"] for p in P])) ** 2, 1))))
    json.dump(c, open(out, "w"), indent=1)
    cv2.imwrite(out.replace(".json", "_mask.png"), pm)
    print(json.dumps({"cost0": float(cost(np.zeros(7))), "cost": float(res.fun), "fx": f, "loc": c["blender"]["location"], "rmse": c.get("rmse_px")}))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "overlay":
        a = sys.argv[2:]; overlay(a[0], a[1], json.load(open(a[2])), a[3], a[4] if len(a) > 4 else None)
    elif cmd == "look":
        ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--loc"); ap.add_argument("--target")
        ap.add_argument("--focal-px", type=float); ap.add_argument("--roll", type=float, default=0); ap.add_argument("--size", default="1080x1920")
        a = ap.parse_args(sys.argv[2:]); sz = [int(v) for v in a.size.split("x")]
        c = look([float(v) for v in a.loc.split(",")], [float(v) for v in a.target.split(",")], a.focal_px, sz, a.roll)
        json.dump(c, open(a.out, "w"), indent=1)
    elif cmd == "refine":
        ap = argparse.ArgumentParser(); ap.add_argument("frame"); ap.add_argument("mesh"); ap.add_argument("cam"); ap.add_argument("out")
        ap.add_argument("--points"); ap.add_argument("--wpts", type=float, default=0.5); ap.add_argument("--fix-f", action="store_true")
        ap.add_argument("--ignore", default=""); ap.add_argument("--fix-h", type=float)
        a = ap.parse_args(sys.argv[2:])
        refine(a.frame, a.mesh, json.load(open(a.cam)), a.out, a.points, a.wpts, a.fix_f, a.ignore, fix_h=a.fix_h)
