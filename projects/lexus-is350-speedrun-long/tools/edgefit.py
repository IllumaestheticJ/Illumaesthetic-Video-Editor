"""Refine a 1:1 camera by 2D-3D edge alignment (no correspondences needed once the camera is close).

    python edgefit.py cam.json irl.png render.png rays.json out_cam.json [--mask x0,y0,x1,y1] [--fixf]

render.png = full-res render from cam.json (same size as irl.png). rays.json = {"p<i>": [x,y,z] | null} from a raycast of
the render's edge pixels (see sample mode). Optimises rvec, tvec and focal so the 3D edge points land on the IRL Canny edge
distance field (truncated at 12 px, so highlights/clutter cannot drag the fit). Reports median / p75 edge distance in px.

    python edgefit.py sample render.png N out_pixels.txt [--mask ...]   # pick N render edge pixels -> "p0:x,y;p1:x,y..."
"""
import json
import sys

import cv2
import numpy as np
from scipy.optimize import minimize


def edges(img, lo, hi):
    g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 1.5)
    return cv2.Canny(g, lo, hi)


def mask_arg():
    if "--mask" in sys.argv:
        return [int(v) for v in sys.argv[sys.argv.index("--mask") + 1].split(",")]
    return None


def sample():
    r = cv2.imread(sys.argv[2]); n = int(sys.argv[3])
    e = edges(r, 20, 60)
    m = mask_arg()
    ys, xs = np.nonzero(e)
    keep = (xs > 4) & (ys > 4) & (xs < e.shape[1] - 5) & (ys < e.shape[0] - 5)
    if m:
        keep &= (xs >= m[0]) & (ys >= m[1]) & (xs < m[2]) & (ys < m[3])
    xs, ys = xs[keep], ys[keep]
    idx = np.random.default_rng(0).choice(len(xs), min(n, len(xs)), replace=False)
    open(sys.argv[4], "w").write(";".join(f"p{i}:{xs[j]},{ys[j]}" for i, j in enumerate(idx)))
    print("sampled", len(idx), "of", len(xs))


def fit():
    cam = json.load(open(sys.argv[1])); irl = cv2.imread(sys.argv[2])
    rays = json.load(open(sys.argv[4]))
    P = np.array([v for v in rays.values() if v], float)
    h, w = irl.shape[:2]
    e = edges(irl, 30, 80)
    m = mask_arg()
    if m:
        mm = np.zeros_like(e); mm[m[1]:m[3], m[0]:m[2]] = 1; e = e * mm
    dt = cv2.distanceTransform((e == 0).astype(np.uint8), cv2.DIST_L2, 5)
    T = 12.0
    rv0 = np.array(cam["opencv"]["rvec"], float); tv0 = np.array(cam["opencv"]["tvec"], float); f0 = cam["fx_px"]
    fixf = "--fixf" in sys.argv

    def proj(x):
        rv, tv = x[:3], x[3:6]; f = f0 if fixf else x[6]
        K = np.array([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]])
        uv, _ = cv2.projectPoints(P, rv, tv, K, None)
        return uv.reshape(-1, 2)

    def cost(x):
        uv = proj(x)
        ok = (uv[:, 0] >= 0) & (uv[:, 1] >= 0) & (uv[:, 0] < w - 1) & (uv[:, 1] < h - 1)
        d = np.full(len(uv), T)
        d[ok] = np.minimum(dt[uv[ok, 1].astype(int), uv[ok, 0].astype(int)], T)
        return float(np.mean(d ** 2))

    def stats(x):
        uv = proj(x); ok = (uv[:, 0] >= 0) & (uv[:, 1] >= 0) & (uv[:, 0] < w - 1) & (uv[:, 1] < h - 1)
        d = dt[uv[ok, 1].astype(int), uv[ok, 0].astype(int)]
        return np.median(d), np.percentile(d, 75)

    x0 = np.r_[rv0, tv0] if fixf else np.r_[rv0, tv0, f0]
    print("before: median %.1f px  p75 %.1f px  (%d pts)" % (*stats(x0), len(P)))
    best = x0
    for scale in (1.0, 0.3):           # coarse then fine
        steps = np.r_[[0.01 * scale] * 3, [0.03 * scale] * 3] if fixf else np.r_[[0.01 * scale] * 3, [0.03 * scale] * 3, [30 * scale]]
        r = minimize(lambda z: cost(best + z * steps), np.zeros_like(best), method="Powell",
                     options={"maxiter": 4000, "xtol": 1e-3, "ftol": 1e-4})
        best = best + r.x * steps
    med, p75 = stats(best)
    print("after:  median %.1f px  p75 %.1f px" % (med, p75))
    rv, tv = best[:3], best[3:6]; f = f0 if fixf else best[6]
    R = cv2.Rodrigues(rv)[0]
    sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor")
    from ive.solve import _matrix_to_euler_xyz, CV_TO_BLENDER_CAM
    Rc2w = R.T @ CV_TO_BLENDER_CAM
    loc = -R.T @ tv
    out = dict(cam)
    out.update({"fx_px": float(f), "focal_mm": float(f / w * cam["sensor_width_mm"]),
                "blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rc2w), "rotation_matrix": Rc2w.tolist()},
                "opencv": {"rvec": rv.tolist(), "tvec": tv.tolist()},
                "edgefit": {"median_px": float(med), "p75_px": float(p75), "points": int(len(P))}})
    json.dump(out, open(sys.argv[5], "w"), indent=2)
    print("focal %.2f mm  loc %s" % (out["focal_mm"], np.round(loc, 3)))


if __name__ == "__main__":
    sample() if sys.argv[1] == "sample" else fit()
