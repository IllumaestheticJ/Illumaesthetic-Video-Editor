"""Exploded-view base for the Cappuccino (all inputs levelled + cropped, mm, one frame):
  base = full car - hood - trunk lid - car tris within TRIM mm of the front/rear bumper part scans
         + 'Front Bumper Off, Hood Open' tris > ADD mm from that trimmed car (engine bay, radiator, crash structure)
         + 'Rear End All Removed' tris > ADD mm from it (rear panel, exhaust, boot floor)
  minus each state's open lid (state points > 30 mm above the car's own surface: the propped lids, which our
  hinged lid parts replace). Also writes the front bumper with the turn-signal lamps cut out (lamps are their own part).
  composite.py car.stl hood.stl trunk.stl fb.stl rb.stl lights.stl fboho.stl rear.stl outdir"""
import struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
def cen(t): return t["v"].mean(1)
def save(p, r): open(p, "wb").write(b"ive cappuccino composite".ljust(80) + struct.pack("<I", len(r)) + r.tobytes()); print(p, len(r))
TRIM, ADD = 6.0, 6.0
car, hood, trunk, fb, rb, li, fbo, rear = (load(p) for p in sys.argv[1:9]); od = sys.argv[9]
cc = cen(car)
rm = np.zeros(len(car), bool)
for part, r in ((hood, 4.0), (trunk, 4.0), (fb, TRIM), (rb, TRIM), (li, TRIM)):
    d, _ = cKDTree(cen(part)).query(cc, distance_upper_bound=r + 1); rm |= d <= r
kc = car[~rm]; print("car trimmed", int(rm.sum()), "of", len(car))
# roofline of the full car per 40 mm cell (to drop the states' propped-open lids)
cell = 40.0
key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
def roof(p):
    k = key(p[:, :2]); i = np.clip(np.searchsorted(u, k), 0, len(u) - 1); return np.where(u[i] == k, top[i], -1e9)
T = cKDTree(cen(kc)[::2])
adds = []
for name, st in (("fboho", fbo), ("rear", rear)):
    sc = cen(st)
    d, _ = T.query(sc, distance_upper_bound=ADD + 1)
    lid_up = sc[:, 2] > roof(sc) + 30
    a = (d > ADD) & ~lid_up
    print(name, "added", int(a.sum()), "dropped open lid", int(lid_up.sum())); adds.append(st[a])
save(f"{od}/base.stl", np.concatenate([kc] + adds))
d, _ = cKDTree(cen(li)).query(cen(fb), distance_upper_bound=TRIM + 1)
save(f"{od}/fb_nolights.stl", fb[d > TRIM])
