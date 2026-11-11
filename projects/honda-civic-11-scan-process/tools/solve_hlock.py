"""Camera solve with fixed focal AND fixed camera height (z), LM over the other 5 DOF.
usage: solve_hlock.py points.json cam_init.json out.json --z 1.3
Writes the same JSON layout as `ive solve` (blender + opencv blocks)."""
import sys, json, argparse, numpy as np, cv2
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz
from scipy.optimize import least_squares
ap = argparse.ArgumentParser(); ap.add_argument('pts'); ap.add_argument('init'); ap.add_argument('out'); ap.add_argument('--z', type=float, required=True)
a = ap.parse_args(); d = json.load(open(a.pts)); c0 = json.load(open(a.init))
W, H = d['image_size']; fx = d['focal_mm'] / d['sensor_width_mm'] * W
K = np.array([[fx, 0, W / 2], [0, fx, H / 2], [0, 0, 1]])
O = np.array([p['xyz'] for p in d['points']], float); I = np.array([p['px'] for p in d['points']], float)
r0 = np.array(c0['opencv']['rvec'], float); R0, _ = cv2.Rodrigues(r0); C0 = -R0.T @ np.array(c0['opencv']['tvec'], float)
def pose(x):
    r = x[:3]; R, _ = cv2.Rodrigues(r); C = np.array([x[3], x[4], a.z]); return r, -R @ C
def res(x):
    r, t = pose(x); q, _ = cv2.projectPoints(O, r, t, K, None); return (q.reshape(-1, 2) - I).ravel()
s = least_squares(res, np.r_[r0, C0[:2]], loss='soft_l1', f_scale=4)
r, t = pose(s.x); e = np.linalg.norm(res(s.x).reshape(-1, 2), axis=1)
R, _ = cv2.Rodrigues(r); loc = -R.T @ t; Rb = R.T @ CV_TO_BLENDER_CAM
out = {"image_size": [W, H], "fx_px": fx, "focal_mm": d['focal_mm'], "sensor_width_mm": d['sensor_width_mm'], "shift_x": 0.0, "shift_y": 0.0,
       "blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rb), "rotation_matrix": Rb.tolist()},
       "opencv": {"rvec": r.tolist(), "tvec": t.tolist()}, "rmse_px": float(np.sqrt((e ** 2).mean())),
       "per_point_error_px": dict(zip([p['name'] for p in d['points']], e.round(2).tolist())), "height_locked_m": a.z}
json.dump(out, open(a.out, 'w'), indent=2); print(f"z={a.z} rmse {out['rmse_px']:.2f}px loc {loc.round(3)}")
