"""State-swap base (C5 v3): the clean car with ONE region replaced by a captured open state (door, fuel door, trunk). Outside
the region box the car is untouched (reviewer 2026-11-11: no artifacts). Inside the box:
  - car tris farther than RM mm from the state scan are removed (the closed door skin / fuel door / hatch glass)
  - state tris farther than ADD mm from the car are added, island-filtered (components < MIN tris dropped)
  swapstate.py car.stl state.stl out.stl --box xmin,xmax,ymin,ymax,zmin,zmax [--rm 20 --add 6 --min 2000 --pad 60]
--pad grows the box for the ADDED state tris only (an open door swings outside the closed footprint)."""
import argparse, struct, sys, os, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from composite2 import components, L
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--box", required=True); ap.add_argument("--rm", type=float, default=20); ap.add_argument("--add", type=float, default=6)
ap.add_argument("--min", type=int, default=2000); ap.add_argument("--pad", default="60")
a = ap.parse_args()
b = [float(v) for v in a.box.split(",")]
pad = [float(v) for v in a.pad.split(",")]; pad = pad * 6 if len(pad) == 1 else pad   # per face: x-,x+,y-,y+,z-,z+
inbox = lambda c, p=(0,) * 6: ((c[:, 0] > b[0] - p[0]) & (c[:, 0] < b[1] + p[1]) & (c[:, 1] > b[2] - p[2]) & (c[:, 1] < b[3] + p[3])
                               & (c[:, 2] > b[4] - p[4]) & (c[:, 2] < b[5] + p[5]))
car = L(a.car); cc = car["v"].mean(1); st = L(a.state); sc = st["v"].mean(1)
ib = inbox(cc)
ds, _ = cKDTree(sc).query(cc[ib], distance_upper_bound=a.rm + 1)
rm = np.zeros(len(car), bool); rm[np.where(ib)[0][ds > a.rm]] = True
kc = car[~rm]
ibs = inbox(sc, pad)
dc, _ = cKDTree(kc["v"].mean(1)).query(sc[ibs], distance_upper_bound=a.add + 1)
add = st[np.where(ibs)[0][dc > a.add]]
if len(add):
    lab = components(add); cnt = np.bincount(lab); add = add[cnt[lab] >= a.min]
print(f"car {len(car)}: removed {int(rm.sum())} in box; state added {len(add)} (of {int(ibs.sum())} in padded box)")
res = np.concatenate([kc, add])
with open(a.out, "wb") as f:
    f.write(b"ive c5 swapstate".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
