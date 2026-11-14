"""Stock front bumper off: car minus the triangles lying on the loose bumper scan (<= cut mm), plus the
bumper-removed state only where it is > fill mm from the kept car and from the bumper, inside the bumper box,
below the hood line (the state was captured hood-off). Writes car_nobump.stl and front_fill.stl (design frame, mm).
bumpercut.py car.stl bumper.stl brem.stl outdir [--cut 6] [--fill 8] [--zmax 640]"""
import argparse, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); [ap.add_argument(x) for x in ("car", "bumper", "brem", "outdir")]
ap.add_argument("--cut", type=float, default=6); ap.add_argument("--fill", type=float, default=8); ap.add_argument("--zmax", type=float, default=640)
a = ap.parse_args()
def L(p): return np.fromfile(p, dtype=TRI, offset=84)
def W(p, d):
    with open(p, "wb") as f: f.write(b"\0" * 80); f.write(np.uint32(len(d)).tobytes()); d.tofile(f)
car, bum, brem = L(a.car), L(a.bumper), L(a.brem)
bv = bum["v"].reshape(-1, 3); lo, hi = bv.min(0) - 60, bv.max(0) + 60
Tb = cKDTree(bv[::2])
cc = car["v"].mean(1); inbox = np.all((cc > lo) & (cc < hi), 1)
d = np.full(len(car), np.inf); d[inbox] = Tb.query(cc[inbox], distance_upper_bound=40)[0]
on = d <= a.cut
# majority-close pin holes: a tri whose 3 vertices are each near removed tris goes too
print("car tris on bumper", on.sum())
kept = car[~on]; W(f"{a.outdir}/car_nobump.stl", kept)
kc = kept["v"].mean(1); kin = np.all((kc > lo - 100) & (kc < hi + 100), 1)
Tk = cKDTree(kc[kin])
rc = brem["v"].mean(1)
sel = np.all((rc > lo) & (rc < hi), 1) & (rc[:, 2] < a.zmax)
dk = Tk.query(rc[sel], distance_upper_bound=60)[0]; db = Tb.query(rc[sel], distance_upper_bound=60)[0]
ok = (dk > a.fill) & (db > a.cut)
idx = np.where(sel)[0][ok]
print("fill tris", len(idx))
W(f"{a.outdir}/front_fill.stl", brem[idx])
