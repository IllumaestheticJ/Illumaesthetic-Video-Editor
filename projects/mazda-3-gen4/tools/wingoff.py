"""Wing-off base: car minus the rear-wing skin (car tris within --cut mm of the Rear Wing scan) plus the
"Wing Removed" state scan where it adds surface the trimmed car lacks (> --new mm from the KEPT car, inside the wing bbox + pad).
(ferrari composite.py compares fills against the uncut car; here the hatch under the wing is within a few mm of the wing's
underside, so that test rejects it.)   wingoff.py car.stl rwing.stl wingrm.stl out.stl"""
import struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)
car, wing, st = (L(p) for p in sys.argv[1:4])
CUT, NEW, PAD = 9.0, 1.5, 60.0
wv = wing["v"].reshape(-1, 3); lo, hi = wv.min(0) - PAD, wv.max(0) + PAD
cc = car["v"].mean(1); d, _ = cKDTree(wv[::2]).query(cc, distance_upper_bound=CUT)
kept = car[~(d < CUT)]; print("car", len(car), "wing skin removed", int((d < CUT).sum()))
sc = st["v"].mean(1); inz = np.all((sc >= lo) & (sc <= hi), axis=1)
d2, _ = cKDTree(kept["v"].mean(1)).query(sc[inz], distance_upper_bound=NEW * 2)
add = st[np.where(inz)[0][d2 > NEW]]; print("state fill +", len(add))
out = np.concatenate([kept, add])
with open(sys.argv[4], "wb") as f: f.write(b"wingoff".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
