"""Refine a camera by aligning scan depth-discontinuity edges to the real frame's Canny edges (for frames where the
car fills the frame, so silhouette refinement can't work). Fixed focal; optimises 6 DOF from a starting camera.
usage: edgefit.py frame.png cam_in.json scan_prepped.stl prep.json cam_out.json "mask x0,y0,x1,y1;..." [W=270]"""
import json, sys, numpy as np, cv2
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor")
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz
from scipy.optimize import minimize
from scipy.ndimage import distance_transform_edt
frame, cin, stl, prep, cout, masks = sys.argv[1:7]; Wd = int(sys.argv[7]) if len(sys.argv) > 7 else 270
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
pj = json.load(open(prep)); sc = pj["unit_scale"]; rl = np.array(pj["root_location"])
m = np.fromfile(stl, dtype=TRI, offset=84)
rng = np.random.default_rng(0); idx = rng.choice(len(m), min(len(m), 600000), replace=False)
V = m["v"][idx].reshape(-1, 3).astype(np.float64) * sc
# prep: centre XY, floor to 0 -> the .json root_location is where the mesh origin sits after normalisation
lo = V.min(0)
V = V + rl if False else V
img = cv2.imread(frame); H0, W0 = img.shape[:2]; s = Wd / W0; Hd = int(round(H0 * s))
g = cv2.cvtColor(cv2.resize(img, (Wd, Hd), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
E = cv2.Canny(cv2.GaussianBlur(g, (3, 3), 0), 40, 110) > 0
valid = np.ones_like(E)
for r in masks.split(";"):
    if r.strip():
        x0, y0, x1, y1 = (int(int(v) * s) for v in r.split(",")); valid[y0:y1, x0:x1] = 0; E[y0:y1, x0:x1] = 0
DT_img = distance_transform_edt(~E)
cam = json.load(open(cin)); fx = cam["fx_px"] * s
K = np.array([[fx, 0, Wd / 2], [0, fx, Hd / 2], [0, 0, 1.0]])
def render_edges(rv, tv):
    R = cv2.Rodrigues(rv)[0]; Pc = V @ R.T + tv; z = Pc[:, 2]; ok = z > 0.05
    u = (Pc[ok, 0] / z[ok] * fx + Wd / 2).astype(int); v = (Pc[ok, 1] / z[ok] * fx + Hd / 2).astype(int); zz = z[ok]
    k = (u >= 0) & (u < Wd) & (v >= 0) & (v < Hd); u, v, zz = u[k], v[k], zz[k]
    D = np.full((Hd, Wd), 50.0); np.minimum.at(D, (v, u), zz)
    D = cv2.erode(D, np.ones((3, 3)))  # close splat holes (min filter = nearest)
    lg = np.log(D); gx = cv2.Sobel(lg, cv2.CV_64F, 1, 0, ksize=3); gy = cv2.Sobel(lg, cv2.CV_64F, 0, 1, ksize=3)
    return (np.hypot(gx, gy) > 0.35) & (valid > 0)
def cost(p):
    rv = p[:3]; tv = p[3:]
    Er = render_edges(rv, tv)
    if Er.sum() < 50: return 1e3
    a = np.minimum(DT_img[Er], 12).mean()
    b = np.minimum(distance_transform_edt(~Er)[E & (valid > 0)], 12).mean()
    return 0.5 * a + 0.5 * b
# NOTE: prepped .blend coordinates = (raw_mm * scale) + root_location  (see scan_prep.py)
V = V + rl
p0 = np.concatenate([np.array(cam["opencv"]["rvec"]), np.array(cam["opencv"]["tvec"])])
print("start cost", cost(p0))
best = p0
for step in [float(x) for x in __import__("os").environ.get("EF_STEPS","0.06,0.03,0.012").split(",")]:
    r = minimize(cost, best, method="Powell", options={"xtol": 1e-4, "ftol": 1e-4, "maxfev": 600, "direc": np.diag([step] * 3 + [step * 2] * 3)})
    best = r.x; print("step", step, "cost", r.fun)
R = cv2.Rodrigues(best[:3])[0]; tv = best[3:]; loc = -R.T @ tv
Rcw = R.T @ CV_TO_BLENDER_CAM.T  # inverse of R_w2c_cv = (R_c2w_blender @ CV_TO_BLENDER_CAM).T
out = dict(cam); out["opencv"] = {"rvec": best[:3].tolist(), "tvec": tv.tolist()}
out["blender"] = {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rcw), "rotation_matrix": Rcw.tolist()}
json.dump(out, open(cout, "w"), indent=2); print("loc", loc.round(3))
dbg = np.dstack([E * 255, render_edges(best[:3], tv) * 255, np.zeros_like(E, np.uint8)]).astype(np.uint8)
cv2.imwrite(cout.replace(".json", "_edges.png"), cv2.resize(dbg, (Wd * 2, Hd * 2), interpolation=cv2.INTER_NEAREST))
