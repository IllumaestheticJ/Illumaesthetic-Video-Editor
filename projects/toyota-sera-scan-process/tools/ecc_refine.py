"""Refine a near-correct camera by 2D alignment of the scan render to the real frame.
ECC (similarity) on blurred gradient-magnitude images, masked to a region of the real frame
where the car is visible. The 2D fit is folded back into the camera: scale -> focal,
translation -> lens shift, rotation -> roll about the view axis. Valid for small corrections
(viewpoint already close); always confirm with an onion render.

    python tools/ecc_refine.py frame.png render.png cam_in.json cam_out.json --mask x0,y0,x1,y1 [--work 960]
render.png must be rendered from cam_in.json (any res; it is resized to the frame)."""
import argparse, json, math, cv2, numpy as np
ap = argparse.ArgumentParser()
ap.add_argument("frame"); ap.add_argument("render"); ap.add_argument("cam"); ap.add_argument("out")
ap.add_argument("--mask", required=True, help="x0,y0,x1,y1 in frame pixels (car visible, no occluders)")
ap.add_argument("--work", type=int, default=960)
a = ap.parse_args()
f = cv2.imread(a.frame, 0); H, W = f.shape; s = a.work / W
r = cv2.resize(cv2.imread(a.render, 0), (W, H))
def grad(im):
    im = cv2.GaussianBlur(cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32), (0, 0), 1.5)
    g = cv2.magnitude(cv2.Sobel(im, cv2.CV_32F, 1, 0), cv2.Sobel(im, cv2.CV_32F, 0, 1))
    g = np.log1p(g); g = cv2.GaussianBlur(g, (0, 0), 3)
    return (g - g.mean()) / (g.std() + 1e-6)
G1, G2 = grad(f), grad(r)
m = np.zeros(G1.shape, np.uint8); x0, y0, x1, y1 = (int(float(v) * s) for v in a.mask.split(","))
m[y0:y1, x0:x1] = 255
# brute force: for each scale, find where the real car patch best matches the scaled render
x0f, y0f, x1f, y1f = x0, y0, x1, y1
T = G1[y0f:y1f, x0f:x1f]
best = (-2, None)
for sc_ in np.arange(0.80, 1.20, 0.005):
    R = cv2.resize(G2, None, fx=sc_, fy=sc_)
    if R.shape[0] < T.shape[0] or R.shape[1] < T.shape[1]:
        continue
    res = cv2.matchTemplate(R, T, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(res)
    if mv > best[0]:
        best = (mv, (sc_, ml))
cc, (scb, (mx, my)) = best[0], best[1]
# frame point (x0f,y0f) <-> scaled-render point (mx,my): render coords r = (frame - (x0f,y0f) + (mx,my)) / scb  (work px)
A0 = np.eye(2) / scb; t0 = (np.array([mx, my]) - np.array([x0f, y0f])) / scb
warp = np.hstack([A0, t0[:, None] * 1.0]).astype(np.float32)
# warp maps frame coords -> render coords: r(warp @ [x,y,1]) ~ f(x,y). Decompose to similarity.
A = warp[:, :2].astype(float); t = warp[:, 2].astype(float) / s
sc = math.sqrt(abs(np.linalg.det(A))); rot = math.atan2(A[1, 0], A[0, 0])
cam = json.load(open(a.cam))
# A render point p_r appears at frame point p_f = A^-1 (p_r - t). Principal point moves accordingly.
cx_r = W / 2 - cam.get("shift_x", 0) * W; cy_r = H / 2 + cam.get("shift_y", 0) * W
Ai = np.linalg.inv(A); pf = Ai @ (np.array([cx_r, cy_r]) - t)
out = dict(cam)
out["focal_mm"] = cam["focal_mm"] / sc
out["fx_px"] = out["focal_mm"] / cam["sensor_width_mm"] * W
out["shift_x"] = -(pf[0] - W / 2) / W
out["shift_y"] = (pf[1] - H / 2) / W
# roll: rotate camera about its view axis by -rot
M = np.array(cam["blender"]["rotation_matrix"]); c, sn = math.cos(-rot), math.sin(-rot)
Rz = np.array([[c, -sn, 0], [sn, c, 0], [0, 0, 1]]); M2 = M @ Rz
from_ive = __import__("sys").path.insert(0, "/home/user/Illumaesthetic-Video-Editor")
from ive.solve import _matrix_to_euler_xyz
out["blender"] = dict(cam["blender"]); out["blender"]["rotation_matrix"] = M2.tolist()
out["blender"]["rotation_euler"] = _matrix_to_euler_xyz(M2)
out["ecc"] = {"cc": float(cc), "scale": sc, "rot_deg": math.degrees(rot), "t_px": t.tolist()}
json.dump(out, open(a.out, "w"), indent=2)
print(json.dumps(out["ecc"]), "focal", round(out["focal_mm"], 2), "shift", round(out["shift_x"], 4), round(out["shift_y"], 4))
