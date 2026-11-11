"""Hood panel from the full car via a filled top-view mask (the difference-based extract leaves holes where the
Hood Open scan had geometry near the closed-hood plane). Mask = extracted hood (tools/extract.py) on a 20 mm grid,
closed + hole-filled + largest component; panel = car tris in the mask, z > 700 mm, within 45 mm of the column top.
  hood_mask.py car.stl hood_extract.stl out.stl"""
import struct, sys
import numpy as np
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84); c = car["v"].mean(1)
h = np.fromfile(sys.argv[2], dtype=TRI, offset=84)["v"].mean(1)
g = 20.0; lo = np.array([-1100, -2400])
ij = lambda p: ((p[:, :2] - lo) / g).astype(int)
M = np.zeros((120, 110), bool); k = ij(h); M[k[:, 0], k[:, 1]] = True
M = ndimage.binary_closing(M, iterations=3); M = ndimage.binary_fill_holes(M); M = ndimage.binary_opening(M, iterations=2)
lab, n = ndimage.label(M); M = lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)
kc = ij(c); ok = (kc[:, 0] >= 0) & (kc[:, 0] < 120) & (kc[:, 1] >= 0) & (kc[:, 1] < 110)
inm = np.zeros(len(c), bool); inm[ok] = M[kc[ok, 0], kc[ok, 1]]
key = kc[:, 0] * 1000 + kc[:, 1]
top = {}
for kk, z in zip(key[inm], c[inm, 2]): top[kk] = max(top.get(kk, -1e9), z)
tz = np.array([top.get(kk, 1e9) for kk in key])
sel = inm & (c[:, 2] > 700) & (c[:, 2] > tz - 45)
print("mask cells", M.sum(), "panel tris", sel.sum())
with open(sys.argv[3], "wb") as f:
    f.write(b"gr86 hood".ljust(80)); f.write(struct.pack("<I", sel.sum())); car[sel].tofile(f)
