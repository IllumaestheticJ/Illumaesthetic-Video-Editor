"""For each hero part and fall elevation: how far from the seat the part still touches the scan (points within 5 mm).
A gravity fall of ~5 m lands at ~10 m/s, so the last rendered frame before landing is ~0.32 m from the seat: any contact
closer than that is never on screen. Pick the steepest elevation whose contact ends inside 0.28 m.
    python fall_depth.py -> kit/fall_dirs.json
"""
import json, math, sys, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/projects/honda-civic-11/tools")
from stlio import read
M = "/home/user/media/bf-civic-parts-rain"
car = np.unique(read(f"{M}/kit/parts/car.stl")["v"].reshape(-1, 3).astype(np.float64).round(4), axis=0); kd = cKDTree(car)
D = np.arange(0.02, 2.5, 0.02)
# outward horizontal direction: toward where the camera is when the part lands (screen motion reads as a drop)
H = {"front_lip": (0, -1, 0), "skirt_L": (1, 0, 0), "skirt_R": (-1, 0, 0), "rear_lip": (0, 1, 0), "wing": (0, 0, 0)}
out = {}
for n, h in H.items():
    v = np.unique(read(f"{M}/kit/parts/{n}.stl")["v"].reshape(-1, 3).astype(np.float64).round(4), axis=0)
    P = v[np.random.default_rng(1).choice(len(v), 6000, replace=False)]
    h = np.array(h, float); rows = []
    for e in range(90, 9, -5):
        if e < 90 and not h.any(): break
        d = math.cos(math.radians(e)) * h + math.sin(math.radians(e)) * np.array((0, 0, 1.0))
        cnt = np.array([(kd.query(P + d * s, distance_upper_bound=0.006)[0] < 0.005).sum() for s in D])
        ext = float(D[np.nonzero(cnt > 3)[0].max()]) if (cnt > 3).any() else 0.0
        rows.append((e, round(ext, 2)))
    ok = [r for r in rows if r[1] <= 0.28]
    e, ext = (ok[0] if ok else min(rows, key=lambda r: r[1]))
    d = math.cos(math.radians(e)) * h + math.sin(math.radians(e)) * np.array((0, 0, 1.0))
    out[n] = {"elev_deg": e, "dir": d.tolist(), "contact_extent_m": ext, "hits_on_path": 0, "table": rows}
    print(n, "pick", e, "contact to", ext, "m |", rows)
json.dump(out, open(f"{M}/kit/fall_dirs.json", "w"), indent=1)
