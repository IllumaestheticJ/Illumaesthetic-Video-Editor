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
for f in ["car_nowheels", "front_lip", "side_skirts", "rear_lip", "sport_wing", "rims_L", "rims_R", "tyres_L", "tyres_R"]:
    v = read(f"{M}/kit/parts/{f}.stl")["v"].mean(1) * 0.001 + root
    pts.append(v[:: max(1, len(v) // 60000)])
P = np.concatenate(pts)
im = np.asarray(Image.open(img_p).convert("L"), np.float32)
N = im.shape[0]
mask_full = ndi.binary_fill_holes(ndi.binary_closing(im > 45, iterations=12))
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


def cost(p, size, r, tgt):
    m = sil(p, size, r)
    return 1 - (m & tgt).sum() / max(1, (m | tgt).sum())


def look(C, T):
    fwd = (T - C) / np.linalg.norm(T - C); right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return Rot.from_matrix(np.stack([right, up, -fwd])).as_rotvec()


best = None
for az in (-50, -40, -30):      # camera in front-right of the car (front +Y, right +X)
    for dist in (7.0, 9.0):
        a = np.radians(az); T = np.array([0.1, 0.0, 0.75]); C = T + dist * np.array([-np.sin(a), np.cos(a), 0]) ; C[2] = 0.75
        f = 0.36 * dist / 4.7 * 1.9   # focal (fraction of image width) so the 4.7 m car fills ~73 % of the width
        p0 = np.r_[C, look(C, T), f / 1.9]
        for size, r in ((240, 2), (480, 2)):
            tgt = np.asarray(Image.fromarray(mask_full).resize((size, size), Image.NEAREST))
            res = minimize(cost, p0, args=(size, r, tgt), method="Powell", options={"xtol": 1e-3, "ftol": 1e-4, "maxiter": 6000})
            p0 = res.x
        print("start az", az, "dist", dist, "-> IoU %.4f" % (1 - res.fun), "C", res.x[:3].round(2), "f", round(res.x[6], 3))
        if best is None or res.fun < best.fun:
            best = res
p = best.x
tgt = np.asarray(Image.fromarray(mask_full).resize((960, 960), Image.NEAREST))
res = minimize(cost, p, args=(960, 3, tgt), method="Powell", options={"xtol": 5e-4, "ftol": 1e-5, "maxiter": 8000})
p = res.x; print("final IoU %.4f" % (1 - res.fun))
R = Rot.from_rotvec(p[3:6]).as_matrix()
json.dump({"loc": p[:3].tolist(), "R_world_to_cam": R.tolist(), "focal_frac_of_width": float(p[6]), "size": int(N),
           "iou": float(1 - res.fun), "render": img_p}, open(out_p, "w"), indent=1)
m = sil(p, 960, 3); edge = m ^ ndi.binary_erosion(m, iterations=2)
ov = np.asarray(Image.open(img_p).convert("RGB").resize((960, 960))).copy(); ov[edge] = (0, 255, 255)
te = tgt ^ ndi.binary_erosion(tgt, iterations=2); ov[te & ~edge] = (255, 120, 0)
Image.fromarray(ov).save(out_p.replace(".json", "_overlay.jpg"), quality=92)
