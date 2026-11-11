"""Single-view solve with radial distortion (k1[,k2]): f, pose, k1 from landmark json.
Writes cam json (pinhole for the UNDISTORTED image) + 'distortion' block; undistort the IRL clip with the same k."""
import json, sys, numpy as np, cv2
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz
pj, out = sys.argv[1], sys.argv[2]; k2 = '--k2' in sys.argv
d = json.load(open(pj)); W, H = d['image_size']
O = np.array([p['xyz'] for p in d['points']], np.float32); I = np.array([p['px'] for p in d['points']], np.float32)
best = None
for f0 in [1600, 2000, 2400, 3000]:
    K = np.array([[f0, 0, W / 2], [0, f0, H / 2], [0, 0, 1]], np.float64)
    fl = cv2.CALIB_USE_INTRINSIC_GUESS | cv2.CALIB_FIX_PRINCIPAL_POINT | cv2.CALIB_FIX_ASPECT_RATIO | cv2.CALIB_ZERO_TANGENT_DIST | cv2.CALIB_FIX_K3
    if not k2: fl |= cv2.CALIB_FIX_K2
    try:
        rms, K2, D, rv, tv = cv2.calibrateCamera([O], [I], (W, H), K, np.zeros(5), flags=fl)
    except cv2.error as e:
        continue
    if best is None or rms < best[0]: best = (rms, K2, D, rv[0], tv[0])
rms, K, D, r, t = best
proj, _ = cv2.projectPoints(O, r, t, K, D); e = np.linalg.norm(proj.reshape(-1, 2) - I, axis=1)
R, _ = cv2.Rodrigues(r); loc = (-R.T @ t).ravel(); Rb = R.T @ CV_TO_BLENDER_CAM
fx = K[0, 0]
cam = {"image_size": [W, H], "fx_px": fx, "focal_mm": fx / W * d['sensor_width_mm'], "sensor_width_mm": d['sensor_width_mm'],
       "shift_x": 0.0, "shift_y": 0.0, "blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rb), "rotation_matrix": Rb.tolist()},
       "opencv": {"rvec": r.ravel().tolist(), "tvec": t.ravel().tolist()}, "rmse_px": float(np.sqrt((e ** 2).mean())),
       "per_point_error_px": {p['name']: float(v) for p, v in zip(d['points'], e)}, "distortion": D.ravel().tolist()}
json.dump(cam, open(out, 'w'), indent=2)
print(json.dumps({k: cam[k] for k in ['focal_mm', 'rmse_px', 'per_point_error_px', 'distortion']}, indent=1)); print('loc', loc.round(3))
