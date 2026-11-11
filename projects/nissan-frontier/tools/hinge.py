"""Fit the hood hinge from the open-hood slivers captured in the state scans (levelled mm).
'Fender Flares Removed' and 'Bumper and Hood Removed' both contain fragments of the hood propped open (points > 40 mm
off the full truck above the cowl). Rotate the closed hood (parts/hood.stl) about an X axis at (y0, z0) by theta and
minimise the median one-sided distance sliver -> rotated hood (Cappuccino lesson). Writes projects/nissan-frontier/hinge.json.
"""
import json, itertools
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
X = "/home/user/media/nissan-frontier/parts"
hood = np.fromfile(f"{X}/hood.stl", dtype=TRI, offset=84)["v"].mean(1)[::6].astype(np.float64)
res = {}
for k in ("fla", "bhr"):
    s = np.fromfile(f"{X}/openhood_{k}.stl", dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    s = s[s[:, 2] > 1330]  # above the cowl clutter; the raised part of the hood only
    def cost(y0, z0, th):
        c, si = np.cos(np.radians(th)), np.sin(np.radians(th))
        y = hood[:, 1] - y0; z = hood[:, 2] - z0
        h = np.stack([hood[:, 0], y0 + y * c + z * si, z0 - y * si + z * c], 1)  # +theta lifts the nose (y<y0) up
        d, _ = cKDTree(h).query(s)
        return np.median(d), (d < 15).mean()
    best = min(((cost(y0, z0, th)[0], y0, z0, th) for y0, z0, th in itertools.product(range(-2340, -2180, 20), range(1180, 1320, 20), range(16, 62, 2))))
    _, y0, z0, th = best
    best = min(((cost(a, b, t)[0], a, b, t) for a, b, t in itertools.product(range(y0 - 15, y0 + 16, 5), range(z0 - 15, z0 + 16, 5), np.arange(th - 1.5, th + 1.6, 0.5))))
    med, frac = cost(*best[1:])
    res[k] = {"y0_mm": best[1], "z0_mm": best[2], "theta_deg": float(best[3]), "median_mm": round(float(med), 2), "within15mm": round(float(frac), 3), "n": len(s)}
    print(k, res[k])
json.dump(res, open("projects/nissan-frontier/hinge.json", "w"), indent=1)
