"""Cut a lid/panel out of the full car where an "open"/"removed" state scan has no surface.
    python lid.py car.stl state.stl out.stl --box x0 x1 y0 y1 z0 z1 [--gap 8]
Keeps car triangles inside the box (levelled mm frame) that are > --gap mm from the state scan: the panel that
was open/off during the state capture. Then composite.py --remove out.stl --fill state.stl builds the base."""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--box", nargs=6, type=float, required=True); ap.add_argument("--gap", type=float, default=8)
ap.add_argument("--min-island", type=int, default=0)
a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84); c = car["v"].mean(1)
b = a.box; inb = (c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])
st = np.fromfile(a.state, dtype=TRI, offset=84)["v"].mean(1)
d, _ = cKDTree(st).query(c[inb], distance_upper_bound=a.gap * 2)
sel = np.zeros(len(car), bool); sel[np.where(inb)[0][d > a.gap]] = True
m = car[sel]
with open(a.out, "wb") as f:
    f.write(b"gt3 lid".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
v = m["v"].reshape(-1, 3); print(a.out, len(m), "bbox", v.min(0).round(), v.max(0).round())
