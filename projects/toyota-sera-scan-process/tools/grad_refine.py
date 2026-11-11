"""Camera refinement by gradient correlation: splat-render the scan (triangle centroids, z-buffered,
|n.v| shading) with OpenCV projection, compare blurred log-gradient images with the real frame
inside a mask, optimise rvec/tvec/focal/principal point (Powell, coarse-to-fine).
For frames where landmarks are unreliable (motion blur, occlusion) but the view is roughly known.

    python tools/grad_refine.py frame.png tris.npy cam_in.json cam_out.json --mask x0,y0,x1,y1[;...] [--ignore ...]
tris.npy: (N,3,3) float triangles in the prepared .blend frame (metres)."""
import argparse, json, math, sys, cv2, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor")
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz
ap = argparse.ArgumentParser(); ap.add_argument("frame"); ap.add_argument("tris"); ap.add_argument("cam"); ap.add_argument("out")
ap.add_argument("--mask", required=True); ap.add_argument("--ignore", default="")
ap.add_argument("--fix-pp", action="store_true"); a = ap.parse_args()
F0 = cv2.imread(a.frame, 0); H0, W0 = F0.shape
tr = np.load(a.tris).astype(np.float64); C = tr.mean(1)
N = np.cross(tr[:, 1] - tr[:, 0], tr[:, 2] - tr[:, 0]); N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
cam = json.load(open(a.cam)); Rb = np.array(cam["blender"]["rotation_matrix"]); loc = np.array(cam["blender"]["location"])
R = (Rb @ CV_TO_BLENDER_CAM).T; t = -R @ loc; r0, _ = cv2.Rodrigues(R); r0 = r0.ravel()
f0 = cam["focal_mm"] / cam["sensor_width_mm"] * W0
cx0 = W0 / 2 - cam.get("shift_x", 0) * W0; cy0 = H0 / 2 + cam.get("shift_y", 0) * W0
def gimg(im):
    g = cv2.magnitude(cv2.Sobel(im, cv2.CV_32F, 1, 0), cv2.Sobel(im, cv2.CV_32F, 0, 1))
    return cv2.GaussianBlur(np.log1p(g), (0, 0), 2.0)
def boxes(spec, s, shape, val):
    m = np.full(shape, not val, bool)
    for b in filter(None, spec.split(";")):
        x0, y0, x1, y1 = (int(float(v) * s) for v in b.split(",")); m[y0:y1, x0:x1] = val
    return m
def setup(w):
    s = w / W0; h = int(round(H0 * s))
    fr = cv2.resize(F0, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
    G = gimg(fr); M = boxes(a.mask, s, (h, w), True)
    if a.ignore: M &= boxes(a.ignore, s, (h, w), False)
    Gm = G[M]; Gm = (Gm - Gm.mean()) / (Gm.std() + 1e-6)
    return s, h, w, Gm, M
def render(x, s, h, w):
    r = r0 + x[:3] * 0.01; tt = t + x[3:6] * 0.02; f = f0 * math.exp(x[6] * 0.02) * s
    cx = (cx0 + x[7] * 20) * s; cy = (cy0 + x[8] * 20) * s
    Rm, _ = cv2.Rodrigues(r); Pc = C @ Rm.T + tt; z = Pc[:, 2]; ok = z > 0.1
    u = f * Pc[:, 0] / z + cx; v = f * Pc[:, 1] / z + cy
    ok &= (u >= 0) & (u < w - 1) & (v >= 0) & (v < h - 1)
    Nc = N @ Rm.T; vd = -Pc / np.linalg.norm(Pc, axis=1, keepdims=True)
    sh = np.abs((Nc * vd).sum(1))
    idx = np.nonzero(ok)[0]; idx = idx[np.argsort(-z[idx])]
    img = np.zeros((h, w), np.float32); zb = np.full((h, w), np.inf, np.float32)
    ui = np.round(u[idx]).astype(int); vi = np.round(v[idx]).astype(int)
    img[vi, ui] = 0.15 + 0.85 * sh[idx]
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    return img, (r, tt, f / s, cx / s, cy / s)
def cost(x, S):
    s, h, w, Gm, M = S
    img, _ = render(x, s, h, w)
    G = gimg(img * 255)[M]; G = (G - G.mean()) / (G.std() + 1e-6)
    return -float((G * Gm).mean())
x = np.zeros(9)
WIDTHS = (640,)
for w in WIDTHS:
    S = setup(w); print("w", w, "start", round(-cost(x, S), 4))
    fixed = [7, 8] if a.fix_pp else []
    def c2(y):
        z = x.copy(); free = [i for i in range(9) if i not in fixed]; z[free] = y; return cost(z, S)
    free = [i for i in range(9) if i not in fixed]
    res = minimize(c2, x[free], method="Powell", options={"maxiter": 3000, "xtol": 1e-2, "ftol": 1e-4})
    x[free] = res.x; print("  ->", round(-res.fun, 4), np.round(x, 2))
s, h, w, Gm, M = setup(960); img, (r, tt, f, cx, cy) = render(x, s, h, w)
Rm, _ = cv2.Rodrigues(r); loc = (-Rm.T @ tt).ravel(); Rb2 = Rm.T @ CV_TO_BLENDER_CAM
out = dict(cam); out.update({"image_size": [W0, H0], "fx_px": f, "focal_mm": f / W0 * cam["sensor_width_mm"],
    "shift_x": -(cx - W0 / 2) / W0, "shift_y": (cy - H0 / 2) / W0,
    "blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rb2), "rotation_matrix": Rb2.tolist()},
    "opencv": {"rvec": r.tolist(), "tvec": tt.tolist(), "cx": cx, "cy": cy}, "refined": "gradient correlation (tools/grad_refine.py)",
    "ncc": -cost(x, setup(960))})
json.dump(out, open(a.out, "w"), indent=2)
fr = cv2.resize(cv2.imread(a.frame), (w, h)); vis = fr.copy(); e = cv2.Canny((img * 255).astype(np.uint8), 40, 120) > 0; vis[e] = (255, 255, 0)
cv2.imwrite(a.out.replace(".json", ".grad.jpg"), vis)
print("focal_mm", round(out["focal_mm"], 2), "loc", loc.round(3), "shift", round(out["shift_x"], 4), round(out["shift_y"], 4))
