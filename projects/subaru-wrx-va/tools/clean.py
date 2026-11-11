"""Ground removal in the levelled frame (ground plane = z 0, nose +X). `ive crop` assumes the long axis is Y,
so it would cut the tyres' sidewalls (widest low geometry) as "past the overhang" here.
  clean.py in.stl out.stl [--footprint car_lvl_4mm.stl] [--zcut 14]
- drop everything below --zcut mm (scanned ground is within +-6 mm of z 0; tyre contact patch is never visible)
- drop up-facing faces (n.z > 0.85) below 70 mm (ground scraps; the underside faces down)
- drop triangles outside the body XY footprint (geometry above 300 mm, 0.1/99.9 pct, +40 mm)
"""
import argparse
import struct

import numpy as np

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--footprint"); ap.add_argument("--zcut", type=float, default=14.0)
a = ap.parse_args()
m = np.fromfile(a.src, dtype=TRI, offset=84)
c = m["v"].mean(1)
ref = np.fromfile(a.footprint, dtype=TRI, offset=84)["v"].mean(1) if a.footprint else c
body = ref[ref[:, 2] > 300]
lo = np.percentile(body[:, :2], 0.1, 0) - 40
hi = np.percentile(body[:, :2], 99.9, 0) + 40
n = m["n"].astype(np.float64)
nn = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
keep = (c[:, 2] > a.zcut) & ~((nn[:, 2] > 0.85) & (c[:, 2] < 70)) & np.all((c[:, :2] >= lo) & (c[:, :2] <= hi), 1)
k = m[keep]
with open(a.dst, "wb") as f:
    f.write(b"wrx clean".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print(a.dst, len(m), "->", len(k), "footprint", lo.round(), hi.round())
