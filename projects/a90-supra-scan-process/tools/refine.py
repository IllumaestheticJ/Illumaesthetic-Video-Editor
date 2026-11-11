"""LM-refine a camera from a known-good nearby camera (useExtrinsicGuess), fixed focal, optional height lock.
usage: python refine.py points.json init_cam.json out_cam.json [--back M] [--height Z]
--back moves the initial camera back along its view axis (the car-to-car camera fell back between frames);
--height locks camera Z (sweep a few values and compare onions - lessons: height is weakly observed on one face)."""
import argparse, json, math
import numpy as np, cv2
from scipy.optimize import least_squares
import sys; sys.path.insert(0, ".")
from ive.solve import CV_TO_BLENDER_CAM, _intrinsics, _matrix_to_euler_xyz, grade
ap = argparse.ArgumentParser(); ap.add_argument("points"); ap.add_argument("init"); ap.add_argument("out")
ap.add_argument("--back", type=float, default=0.0); ap.add_argument("--height", type=float, default=None)
ap.add_argument("--drop", default="")
a = ap.parse_args()
d = json.load(open(a.points)); c0 = json.load(open(a.init))
pts = [p for p in d["points"] if p["name"] not in a.drop.split(",")]
obj = np.array([p["xyz"] for p in pts], float); img = np.array([p["px"] for p in pts], float)
w, h = d["image_size"]; fx = d["focal_mm"] / d["sensor_width_mm"] * w; K = _intrinsics(fx, w, h)
Rb = np.array(c0["blender"]["rotation_matrix"]); loc = np.array(c0["blender"]["location"]) - Rb[:, 2] * -1 * 0  # placeholder
fwd = -Rb[:, 2]; loc = np.array(c0["blender"]["location"]) - fwd * a.back
Rcv = (Rb @ CV_TO_BLENDER_CAM).T  # world->cam
rvec0, _ = cv2.Rodrigues(Rcv)
def unpack(x):
    rv = x[:3]; C = x[3:6].copy()
    if a.height is not None: C[2] = a.height
    R, _ = cv2.Rodrigues(rv); t = -R @ C
    return rv, t, R, C
def res(x):
    rv, t, R, C = unpack(x)
    pr, _ = cv2.projectPoints(obj, rv, t, K, None)
    return (pr.reshape(-1, 2) - img).ravel()
x0 = np.r_[rvec0.ravel(), loc]
if a.height is not None: x0[5] = a.height
r = least_squares(res, x0, method="lm")
rv, t, R, C = unpack(r.x)
err = np.linalg.norm(res(r.x).reshape(-1, 2), axis=1); rmse = float(np.sqrt(np.mean(err ** 2)))
Rw = R.T @ CV_TO_BLENDER_CAM
out = {"image_size": [w, h], "fx_px": fx, "focal_mm": d["focal_mm"], "sensor_width_mm": d["sensor_width_mm"], "shift_x": 0.0, "shift_y": 0.0,
       "blender": {"location": C.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rw), "rotation_matrix": Rw.tolist()},
       "rmse_px": rmse, "per_point_error_px": {p["name"]: round(float(e), 2) for p, e in zip(pts, err)}, "quality": grade(rmse, w),
       "method": f"LM from {a.init} back {a.back} m" + (f", height locked {a.height} m" if a.height is not None else "")}
json.dump(out, open(a.out, "w"), indent=1)
print(round(rmse, 2), [round(v, 3) for v in C], out["per_point_error_px"])
