"""Diff the levelled full car against a state scan (mm): writes
  <out>_gone.stl  car tris farther than --thr from the state scan (panels the state removed/moved; also its coverage holes)
  <out>_new.stl   state tris farther than --thr from the car (exposed structure + panels in their moved pose)
optionally inside --box xmin,xmax,ymin,ymax,zmin,zmax (levelled mm).  diff.py car.stl state.stl out [--thr 12] [--box ...]"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
def save(p, m):
    with open(p, "wb") as f: f.write(b"miata diff".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--thr", type=float, default=12); ap.add_argument("--box"); ap.add_argument("--near", type=float, default=1e9, help="gone only if the state has geometry within this (mm): skips its coverage holes")
a = ap.parse_args()
car, st = load(a.car), load(a.state)
cc, sc = car["v"].mean(1), st["v"].mean(1)
def inbox(c):
    if not a.box: return np.ones(len(c), bool)
    b = [float(v) for v in a.box.split(",")]
    return (c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])
ib = inbox(cc); d, _ = cKDTree(sc).query(cc[ib], distance_upper_bound=max(a.thr + 1, min(a.near, 1e6)))
g = np.zeros(len(car), bool); g[np.where(ib)[0][(d > a.thr) & (d < a.near)]] = True
ib2 = inbox(sc); d2, _ = cKDTree(cc).query(sc[ib2], distance_upper_bound=a.thr + 1)
n = np.zeros(len(st), bool); n[np.where(ib2)[0][d2 > a.thr]] = True
save(a.out + "_gone.stl", car[g]); save(a.out + "_new.stl", st[n])
print(a.out, "gone", int(g.sum()), "new", int(n.sum()))
