"""Solve the camera that makes the scan + fitted kit overlap Ron's render (Final-Sedan-FL) 1:1.

    python match_render.py <render.jpg> <out.json>
No hand-picked landmarks: the render's car mask (bright pixels, closed) is matched by the silhouette of the projected
scan + kit points (prepped frame). 7 parameters (camera position, rotation vector, focal) optimised on IoU, coarse to fine,
started from a front-right 3/4 guess. Writes the camera for a square frame of the render's size (pinhole, principal point
at the centre) plus a check overlay.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stlio import read  # noqa: E402

M = "/home/user/media/honda-civic-11"
img_p, out_p = sys.argv[1:3]
root = np.array(json.load(open(f"{M}/prep/car4.json"))["root_location"])
pts = []
for f in ["car_nowheels", "front_lip", "side_skirts", "rear_lip", "sport_wing", "rims_L", "rims_R"]:   # tyres are black on the black floor in the render: left out of both silhouettes
    v = read(f"{M}/kit/parts/{f}.stl")["v"].mean(1) * 0.001 + root
    if f == "car_nowheels":
        v = v[v[:, 2] > 0.30 + 0.055 * (v[:, 1] < 0) * -v[:, 1]]   # no underbody (the scan car is pitched: rear sits higher)
    pts.append(v[:: max(1, len(v) // 60000)])
P = np.concatenate(pts)
im = np.asarray(Image.open(img_p).convert("L"), np.float32)
N = im.shape[0]
mask_full = ndi.binary_fill_holes(ndi.binary_closing(im > 80, iterations=10))   # > 80: the lit floor band (20-50) stays out
lab, n = ndi.label(mask_full); mask_full = lab == (1 + np.argmax(ndi.sum(mask_full, lab, range(1, n + 1))))
ys, xs = np.nonzero(mask_full); print("mask bbox", xs.min(), xs.max(), ys.min(), ys.max())


def project(p, size):
    C, rv, f = p[:3], p[3:6], p[6]
    R = Rot.from_rotvec(rv).as_matrix()          # world -> camera (camera looks along -Z, +Y up)
    q = (P - C) @ R.T
    z = -q[:, 2]
    u = size / 2 + f * size * q[:, 0] / z
    v = size / 2 - f * size * q[:, 1] / z
    return u, v, z


def sil(p, size, r):
    u, v, z = project(p, size)
    ok = (z > 0.1) & (u >= 0) & (u < size) & (v >= 0) & (v < size)
    m = np.zeros((size, size), bool); m[v[ok].astype(int), u[ok].astype(int)] = True
    return ndi.binary_fill_holes(ndi.binary_closing(ndi.binary_dilation(m, iterations=r), iterations=2))


# landmarks: the two visible (right-side) wheel centres. Render: centroids of the gold rim blobs. Scan: centre of each
# fitted rim's outer face. Silhouette alone left focal/yaw ambiguous (wheels 60 px off at IoU 0.88).
rgb = np.asarray(Image.open(img_p).convert("RGB"), np.float32)
gold = ndi.binary_fill_holes(ndi.binary_closing((rgb[..., 0] > 1.4 * rgb[..., 2]) & (rgb[..., 0] > 90) & (rgb[..., 1] > 70), iterations=10))
gl, gn = ndi.label(gold); gs = ndi.sum(gold, gl, range(1, gn + 1)); top = np.argsort(gs)[-2:] + 1
W2 = np.array(sorted([ndi.center_of_mass(gl == i)[::-1] for i in top]))      # rear (left in image), front
rr = read(f"{M}/kit/parts/rims_R.stl")["v"].mean(1) * 0.001 + root
W3 = []
for sel in (rr[:, 1] < 0, rr[:, 1] > 0):                                       # rear, front
    w = rr[sel]; face = w[w[:, 0] > np.percentile(w[:, 0], 80)]
    W3.append([face[:, 0].mean(), (w[:, 1].min() + w[:, 1].max()) / 2, (w[:, 2].min() + w[:, 2].max()) / 2])
W3 = np.array(W3); print("wheel px (render)", W2.round(1), "wheel 3D", W3.round(3))


def wheel_err(p):
    C, rv, f = p[:3], p[3:6], p[6]
    q = (W3 - C) @ Rot.from_rotvec(rv).as_matrix().T
    uv = np.c_[0.5 + f * q[:, 0] / -q[:, 2], 0.5 - f * q[:, 1] / -q[:, 2]] * N
    return np.linalg.norm(uv - W2, axis=1)


def cost(p, size, r, tgt):
    m = sil(p, size, r)
    return 1 - (m & tgt).sum() / max(1, (m | tgt).sum()) + 4.0 * wheel_err(p).mean() / N


def look(C, T):
    fwd = (T - C) / np.linalg.norm(T - C); right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return Rot.from_matrix(np.stack([right, up, -fwd])).as_rotvec()


if os.path.exists(out_p):       # refine a previous solve
    q = json.load(open(out_p)); p = np.r_[q["loc"], Rot.from_matrix(np.array(q["R_world_to_cam"])).as_rotvec(), q["focal_frac_of_width"]]
else:
    a = np.radians(-30); T = np.array([0.1, 0.0, 0.75]); C = T + 9 * np.array([-np.sin(a), np.cos(a), 0]); C[2] = 0.5
    p = np.r_[C, look(C, T), 1.0]
for size, r in ((240, 2), (480, 2)):
    tgt = np.asarray(Image.fromarray(mask_full).resize((size, size), Image.NEAREST))
    res = minimize(cost, p, args=(size, r, tgt), method="Powell", options={"xtol": 1e-3, "ftol": 1e-4, "maxiter": 6000})
    p = res.x; print(size, "IoU %.4f" % (1 - res.fun), "C", p[:3].round(2), "f", round(p[6], 3))
tgt = np.asarray(Image.fromarray(mask_full).resize((960, 960), Image.NEAREST))
res = minimize(cost, p, args=(960, 3, tgt), method="Powell", options={"xtol": 5e-4, "ftol": 1e-5, "maxiter": 8000})
p = res.x; print("final cost %.4f" % res.fun, "wheel err px (of %d)" % N, wheel_err(p).round(1))
m0 = sil(p, 960, 3); print("final IoU %.4f" % ((m0 & tgt).sum() / (m0 | tgt).sum()))
R = Rot.from_rotvec(p[3:6]).as_matrix()
json.dump({"loc": p[:3].tolist(), "R_world_to_cam": R.tolist(), "focal_frac_of_width": float(p[6]), "size": int(N),
           "iou": float((m0 & tgt).sum() / (m0 | tgt).sum()), "render": img_p}, open(out_p, "w"), indent=1)
m = sil(p, 960, 3); edge = m ^ ndi.binary_erosion(m, iterations=2)
ov = np.asarray(Image.open(img_p).convert("RGB").resize((960, 960))).copy(); ov[edge] = (0, 255, 255)
te = tgt ^ ndi.binary_erosion(tgt, iterations=2); ov[te & ~edge] = (255, 120, 0)
Image.fromarray(ov).save(out_p.replace(".json", "_overlay.jpg"), quality=92)
