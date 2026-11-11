"""Fill openings left by carved panels with state scans *as captured*, each only inside its own box (frame-A mm).
Only fill triangles > --new mm from the trimmed car (and from earlier fills) are added (no double skins).
    python fill.py rest.stl out.stl --fill bumper_removed_r.stl:x0,x1,y0,y1,z0,z1 --fill engine_bay.stl:... [--new 7]
"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("rest"); ap.add_argument("out")
ap.add_argument("--fill", action="append", default=[]); ap.add_argument("--new", type=float, default=7)
a = ap.parse_args()
car = np.fromfile(a.rest, dtype=TRI, offset=84)
pieces = [car]; acc = car["v"].mean(1)[::2]
for spec in a.fill:
    path, box = spec.split(":"); b = np.array([float(v) for v in box.split(",")])
    m = np.fromfile(path, dtype=TRI, offset=84); c = m["v"].mean(1)
    inb = np.all((c >= b[0::2]) & (c <= b[1::2]), axis=1)
    d, _ = cKDTree(acc).query(c[inb], distance_upper_bound=a.new * 2)
    sel = np.where(inb)[0][d > a.new]
    print(f"{path.split('/')[-1]}: +{len(sel)} of {inb.sum()} in box")
    pieces.append(m[sel]); acc = np.concatenate([acc, c[sel]])
allm = np.concatenate(pieces)
with open(a.out, "wb") as f: f.write(b"sti fill".ljust(80)); f.write(struct.pack("<I", len(allm))); allm.tofile(f)
print(a.out, len(allm))
