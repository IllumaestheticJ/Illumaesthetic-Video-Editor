"""v5: camera for one of Ron's renders, for the 1:1 cut scan+kit -> render.

    python match_render2.py <render.jpg> <ron camera name> <out.json> <crop_w>
Start = Ron's own camera from 'Honda Civic Sedan 2022-render.blend' (ron_cams.json) moved into the scan frame with
kit/ron_to_scan.json. The delivered stills were framed differently from the .blend (test: right direction, 1.25x too big,
shifted), so position / rotation / focal are refined on silhouette IoU + the centres of the two largest gold rims
(render: gold blobs; scan: outer-face centres of Ron's rims in kit/parts2). Points = scan car + kit as placed for v5.
Writes the solve, an overlay, and the shot.py camera key for a 1080x1920 frame showing <crop_w> px of the 1920 render.
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
img_p, cam_name, out_p, WC = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
root = np.array(json.load(open(f"{M}/prep/car4.json"))["root_location"])
T = json.load(open(f"{M}/kit/ron_to_scan.json")); RT = np.array(T["R"]); tT = np.array(T["t"])
ld = lambda n: read(f"{M}/kit/parts2/{n}.stl")["v"].mean(1) * 0.001 + root
pts = []
for f in ["car_nowheels", "front_lip", "skirt_L", "skirt_R", "rear_apron", "wing"] + [f"rim_{w}" for w in ("FL", "FR", "RL", "RR")]:
    v = ld(f)
    if f == "car_nowheels":
        a = (v - tT) @ RT; v = v[a[:, 2] > 0.22]          # no underbody (Ron's level frame)
    pts.append(v[:: max(1, len(v) // 60000)])
P = np.concatenate(pts)
im = np.asarray(Image.open(img_p).convert("L"), np.float32); N = im.shape[0]
mask_full = ndi.binary_fill_holes(ndi.binary_closing(im > 80, iterations=10))
lab, n = ndi.label(mask_full); mask_full = lab == (1 + np.argmax(ndi.sum(mask_full, lab, range(1, n + 1))))
rgb = np.asarray(Image.open(img_p).convert("RGB"), np.float32)
gold = ndi.binary_fill_holes(ndi.binary_closing((rgb[..., 0] > 1.4 * rgb[..., 2]) & (rgb[..., 0] > 90) & (rgb[..., 1] > 70), iterations=10))
gl, gn = ndi.label(gold); gs = ndi.sum(gold, gl, range(1, gn + 1)); top = np.argsort(gs)[-2:] + 1
W2 = np.array([ndi.center_of_mass(gl == i)[::-1] for i in top])
c = json.load(open("/home/user/media/work/civic/match/ron_cams.json"))["cams"][cam_name]; Mw = np.array(c["M"])
C0 = RT @ Mw[:3, 3] + tT; R0 = np.stack([RT @ Mw[:3, 0], RT @ Mw[:3, 1], RT @ Mw[:3, 2]])   # rows: right, up, back
p0 = np.r_[C0, Rot.from_matrix(R0).as_rotvec(), c["lens"] / c["sensor_w"] / 1.25]


def proj(p, X):
    q = (X - p[:3]) @ Rot.from_rotvec(p[3:6]).as_matrix().T
    return 0.5 + p[6] * q[:, 0] / -q[:, 2], 0.5 - p[6] * q[:, 1] / -q[:, 2], -q[:, 2]


# wheel 3D: outer-face centres of the rims on the side the camera sees; matched to the blobs by image x order
side = "L" if C0[0] < 0 else "R"; W3 = []
for w in ("F" + side, "R" + side):
    v = ld(f"rim_{w}"); x = v[:, 0] * (-1 if side == "L" else 1); face = v[x > np.percentile(x, 80)]
    W3.append([face[:, 0].mean(), (v[:, 1].min() + v[:, 1].max()) / 2, (v[:, 2].min() + v[:, 2].max()) / 2])
W3 = np.array(W3); u0, _, _ = proj(p0, W3); W3 = W3[np.argsort(u0)]; W2 = W2[np.argsort(W2[:, 0])]
print("wheel px", W2.round(1).tolist())


def sil(p, size, r):
    u, v, z = proj(p, P); u = u * size; v = v * size
    ok = (z > 0.1) & (u >= 0) & (u < size) & (v >= 0) & (v < size)
    m = np.zeros((size, size), bool); m[v[ok].astype(int), u[ok].astype(int)] = True
    return ndi.binary_fill_holes(ndi.binary_closing(ndi.binary_dilation(m, iterations=r), iterations=2))


def werr(p):
    u, v, _ = proj(p, W3); return np.linalg.norm(np.c_[u, v] * N - W2, axis=1)


def cost(p, size, r, tgt):
    m = sil(p, size, r); return 1 - (m & tgt).sum() / max(1, (m | tgt).sum()) + 4.0 * werr(p).mean() / N


p = p0
for size, r in ((240, 2), (480, 2), (960, 3)):
    tgt = np.asarray(Image.fromarray(mask_full).resize((size, size), Image.NEAREST))
    p = minimize(cost, p, args=(size, r, tgt), method="Powell", options={"xtol": 5e-4, "ftol": 1e-5, "maxiter": 8000}).x
    m0 = sil(p, size, r); print(size, "IoU %.4f" % ((m0 & tgt).sum() / (m0 | tgt).sum()), "wheel err px", werr(p).round(1), "f", round(p[6], 3), "dist", round(float(np.linalg.norm(p[:3])), 2))
R = Rot.from_rotvec(p[3:6]).as_matrix(); fwd = -R[2]; up = R[1]
r0 = np.cross(fwd, [0, 0, 1.0]); r0 /= np.linalg.norm(r0); u0v = np.cross(r0, fwd)
key = {"loc": p[:3].round(4).tolist(), "target": (p[:3] + fwd * 10).round(4).tolist(), "focal": round(float(p[6]) * N / WC * 20.25, 3),
       "roll": round(float(np.degrees(np.arctan2(-up @ r0, up @ u0v))), 3)}
json.dump({"key": key, "crop_w": WC, "render": img_p, "iou": float((m0 & tgt).sum() / (m0 | tgt).sum()), "wheel_err_px": werr(p).tolist()}, open(out_p, "w"), indent=1)
edge = m0 ^ ndi.binary_erosion(m0, iterations=2); ov = np.asarray(Image.open(img_p).convert("RGB").resize((960, 960))).copy(); ov[edge] = (0, 255, 255)
Image.fromarray(ov).save(out_p.replace(".json", "_overlay.jpg"), quality=92); print(key)
