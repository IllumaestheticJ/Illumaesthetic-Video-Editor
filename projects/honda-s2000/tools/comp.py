"""Composite a 'panels off / open' base in the levelled frame (mm): a car-minus-panels STL + only the NEW geometry of
state scans (triangles > --new mm from the base) inside a zone box, minus exclusion boxes (e.g. the one scanned wheel,
the propped-open lid). Later fills only add what earlier ones lack.
    python projects/honda-s2000/tools/comp.py out.stl --base car_nolid.stl --fill trunk.stl:x0,x1,y0,y1,z0,z1 \
        [--exclude x0,x1,y0,y1,z0,z1 ...] [--new 7]"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
box = lambda s: [float(v) for v in s.split(",")]
inb = lambda c, b: (c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--base", required=True)
ap.add_argument("--fill", nargs="*", default=[]); ap.add_argument("--exclude", action="append", default=[], help="repeat as --exclude=x0,...")
ap.add_argument("--new", type=float, default=7.0)
a = ap.parse_args()
base = np.fromfile(a.base, dtype=TRI, offset=84); acc = base["v"].mean(1).astype(float)
pieces = [base]
for f in a.fill:
    path, z = f.rsplit(":", 1)
    m = np.fromfile(path, dtype=TRI, offset=84); c = m["v"].mean(1).astype(float)
    sel = inb(c, box(z))
    for e in a.exclude: sel &= ~inb(c, box(e))
    d, _ = cKDTree(acc).query(c[sel], distance_upper_bound=a.new * 2)
    idx = np.where(sel)[0]; sel[idx[d <= a.new]] = False
    print(path.split("/")[-1], "+", int(sel.sum())); pieces.append(m[sel]); acc = np.concatenate([acc, c[sel]])
allm = np.concatenate(pieces)
with open(a.out, "wb") as fh:
    fh.write(b"ive comp s2k".ljust(80)); fh.write(struct.pack("<I", len(allm))); allm.tofile(fh)
print(a.out, len(allm))
