"""Ground / lift-pad removal for the Frontier scans (levelled frame, mm, ground at z=0).
`ive crop` clipped the mirrors (its footprint is measured on the body, |x|<991 mm; mirrors reach 1084 mm),
so this keeps everything above --zmin (truck sits on lift pads, no wheels; the pads + lift arms + ground are all
below ~200 mm while the lowest real geometry, frame rails/control arms, starts at ~200-250 mm) inside |x|<1200.
  clean.py in.stl out.stl [--zmin 200]"""
import argparse, struct
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--zmin", type=float, default=200); ap.add_argument("--xmax", type=float, default=1200)
a = ap.parse_args()
m = np.fromfile(a.inp, dtype=TRI, offset=84)
v = m["v"]
keep = (v[:, :, 2].min(1) >= a.zmin) & (np.abs(v[:, :, 0]).max(1) <= a.xmax)
r = m[keep]
with open(a.out, "wb") as f:
    f.write(b"ive frontier clean".ljust(80)); f.write(struct.pack("<I", len(r))); r.tofile(f)
print(a.out, len(m), "->", len(r))
