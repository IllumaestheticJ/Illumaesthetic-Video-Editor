"""Close small holes/slivers inside a panel cut from the car: car triangles (not in the panel) whose 25 mm neighbourhood is
mostly panel (>= --frac) join the panel; repeated. Stops slivers of lid skin staying on the body when the lid opens.
  fill_panel_holes.py car.stl panel.stl out.stl [--frac 0.6 --iters 4]"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("panel"); ap.add_argument("out")
ap.add_argument("--frac", type=float, default=0.6); ap.add_argument("--iters", type=int, default=4); ap.add_argument("--r", type=float, default=25)
a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84); cc = car["v"].mean(1)
pc = np.fromfile(a.panel, dtype=TRI, offset=84)["v"].mean(1)
d, i = cKDTree(cc).query(pc); inp = np.zeros(len(car), bool); inp[i[d < 0.5]] = True
lo, hi = pc.min(0) - 30, pc.max(0) + 30
zone = np.where(np.all((cc > lo) & (cc < hi), axis=1))[0]
T = cKDTree(cc[zone])
for it in range(a.iters):
    nb = T.query_ball_point(cc[zone], a.r)
    frac = np.array([inp[zone[n]].mean() if len(n) else 0 for n in nb])
    add = zone[(~inp[zone]) & (frac >= a.frac)]
    inp[add] = True
    print("iter", it, "added", len(add))
    if not len(add): break
k = car[inp]
with open(a.out, "wb") as f: f.write(b"miata fill_panel_holes".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print("panel", len(pc), "->", len(k))
