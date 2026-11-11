"""Cargo-area fill for the hatch-open shot from the 'trunk open (removed)' state scan (same frame, 2.0 mm).

    python projects/toyota-gr-corolla/tools/cargofill.py base.stl "trunk open (removed).stl" out.stl

Keeps state-scan triangles under the hatch (raw mm: y > 100, z < 620, |x - xc| < 640), dropping the
propped-open hatch it also captured (everything above z 620), and only where they are > 8 mm from the base.
"""
import struct
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
base = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
st = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
c = st["v"].mean(1)
zone = (c[:, 1] > 100) & (c[:, 2] < 620) & (c[:, 2] > -300) & (np.abs(c[:, 0] + 198) < 640)
d, _ = cKDTree(base["v"].mean(1)).query(c[zone], distance_upper_bound=16)
sel = np.where(zone)[0][d > 8]
with open(sys.argv[3], "wb") as f:
    f.write(b"gr-corolla cargo fill".ljust(80))
    f.write(struct.pack("<I", len(sel)))
    st[sel].tofile(f)
print("cargo fill", len(sel))
