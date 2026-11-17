"""Offline (scipy) search (distance_upper_bound: lesson - unbounded cKDTree queries far from the cloud take minutes) for each hero part's fall line: the steepest straight line (vertical first, then tilted outward
in 5 deg steps) along which the part never comes within 5 mm of the scan. Writes kit/fall_dirs.json for falls.py.
    python fall_dirs.py
"""
import json, math, sys, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/projects/honda-civic-11/tools")
from stlio import read
M = "/home/user/media/bf-civic-parts-rain"
SIDE = {"front_lip": (0, -1, 0), "skirt_L": (1, 0, 0), "skirt_R": (-1, 0, 0), "rear_lip": (0, 1, 0), "wing": (0, 0, 0)}
car = read(f"{M}/kit/parts/car.stl")["v"].reshape(-1, 3).astype(np.float64)
car = np.unique(car.round(4), axis=0); kd = cKDTree(car)
D = np.r_[np.arange(0.06, 0.30, 0.01), np.arange(0.30, 2.01, 0.04)]  # from 6 cm: closer than that is the flush contact zone, not a pass-through
out = {}
for n, side in SIDE.items():
    v = np.unique(read(f"{M}/kit/parts/{n}.stl")["v"].reshape(-1, 3).astype(np.float64).round(4), axis=0)
    P = v[np.random.default_rng(1).choice(len(v), min(len(v), 6000), replace=False)]
    base = int((kd.query(P, distance_upper_bound=0.006)[0] < 0.005).sum())
    side = np.array(side, float); up = np.array((0, 0, 1.0)); res = []
    for e in range(90, 9, -5):
        if e < 90 and not side.any():
            break
        d = math.cos(math.radians(e)) * side + math.sin(math.radians(e)) * up
        worst = max(int((kd.query(P + d * s, distance_upper_bound=0.006)[0] < 0.005).sum()) for s in D)
        res.append((e, worst))
        if worst <= 2:
            break
    e, worst = min(res, key=lambda r: (r[1], -r[0])) if all(r[1] > 2 for r in res) else res[-1]
    d = math.cos(math.radians(e)) * side + math.sin(math.radians(e)) * up
    out[n] = {"elev_deg": e, "dir": d.tolist(), "hits_on_path": worst, "contact_pts_at_seat": base, "tried": res}
    print(n, out[n]["elev_deg"], "hits", worst, "seat contact", base, "tried", res)
json.dump(out, open(f"{M}/kit/fall_dirs.json", "w"), indent=1)
