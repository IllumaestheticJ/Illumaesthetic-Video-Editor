"""Track the game's blue Miata through the car-select animation: one car-relative camera per capture frame.

    python track_car.py <a60.mp4> <nb.npz> <start_pose.npy row: f, rvec, tvec> <f0> <f1> <out.json>

Starts at the hold frame given by --seed-frame and walks outwards one frame at a time, starting each fit from
the previous pose plus its last step (Powell on 1 - IoU of the blue pixels vs the NB's painted panels).
"""
import sys, json, argparse
import cv2, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, __import__("os").path.dirname(__file__))
import sil

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("mesh"); ap.add_argument("out")
ap.add_argument("--seed-frame", type=int, required=True)
ap.add_argument("--seed-pose", required=True, help="comma list rvec,tvec")
ap.add_argument("--focal", type=float, required=True)
ap.add_argument("--first", type=int, required=True); ap.add_argument("--last", type=int, required=True)
ap.add_argument("--scale", type=float, default=0.5)
ap.add_argument("--chamfer", type=float, default=0.0)
a = ap.parse_args()
V, F, C = sil.load_mesh(a.mesh)
cap = cv2.VideoCapture(a.video)
valid = sil.valid_mask(a.scale)


def frame(i):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    return cap.read()[1]


def fit(i, p0, tries=2):
    fr = frame(i)
    obs = cv2.resize(sil.blue_mask(fr), sil.size(a.scale), interpolation=cv2.INTER_AREA)
    dt = cv2.distanceTransform((1 - obs).astype(np.uint8), cv2.DIST_L2, 3)
    best = (sil.cost(p0, V, F, C, a.focal, obs, valid, a.scale, dt, a.chamfer), np.array(p0))
    p = np.array(p0)
    for _ in range(tries):
        r = minimize(sil.cost, p, args=(V, F, C, a.focal, obs, valid, a.scale, dt, a.chamfer), method="Powell",
                     options={"xtol": 5e-4, "ftol": 1e-5, "maxfev": 350})
        if r.fun < best[0] - 1e-4:
            best = (float(r.fun), r.x); p = r.x
        else:
            break
    area = int(((obs > 0) & (valid > 0)).sum())
    return best[1], float(best[0]), area


seed = np.array([float(x) for x in a.seed_pose.split(",")])
res = {}
p, c, ar = fit(a.seed_frame, seed, 3)
res[a.seed_frame] = (p, c, ar)
for step, end in ((1, a.last), (-1, a.first)):
    prev2, prev = None, res[a.seed_frame][0]
    i = a.seed_frame + step
    while (i <= end) if step > 0 else (i >= end):
        p0 = prev if prev2 is None else prev + 0.7 * (prev - prev2)
        p, c, ar = fit(i, p0)
        if prev2 is not None:                       # also try without the extrapolation; keep the better
            pb, cb, _ = fit(i, prev, 1)
            if cb < c - 0.01:
                p, c = pb, cb
        res[i] = (p, c, ar)
        print(i, round(c, 3), ar, np.round(p, 3), flush=True)
        prev2, prev = prev, p
        i += step
json.dump({"focal_px": a.focal, "frames": {str(k): {"pose": [float(x) for x in v[0]], "cost": v[1], "area": v[2]} for k, v in sorted(res.items())}}, open(a.out, "w"))
