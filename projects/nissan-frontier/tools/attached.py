"""Drop detached islands from a state-scan fill: keep only fill triangles whose 15 mm voxel is connected (26-neighbour)
to the truck body it sits on. Scan debris floating under the nose (lift/floor speckle) is not attached to anything.
  attached.py fill.stl body.stl out.stl [--vox 15]"""
import argparse, struct
import numpy as np
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("fill"); ap.add_argument("body"); ap.add_argument("out"); ap.add_argument("--vox", type=float, default=15)
a = ap.parse_args()
f = np.fromfile(a.fill, dtype=TRI, offset=84); fc = f["v"].mean(1)
b = np.fromfile(a.body, dtype=TRI, offset=84)["v"].mean(1)
lo = fc.min(0) - 60; hi = fc.max(0) + 60
b = b[np.all((b >= lo) & (b <= hi), axis=1)]
shape = np.ceil((hi - lo) / a.vox).astype(int) + 1
g = np.zeros(shape, bool)
fi = ((fc - lo) / a.vox).astype(int); bi = ((b - lo) / a.vox).astype(int)
g[tuple(fi.T)] = True; g[tuple(bi.T)] = True
lab, n = ndimage.label(g, structure=np.ones((3, 3, 3)))
body_labels = np.unique(lab[tuple(bi.T)])
sizes = np.bincount(lab.ravel()); main = body_labels[np.argmax(sizes[body_labels])]
keep = lab[tuple(fi.T)] == main
r = f[keep]
with open(a.out, "wb") as o:
    o.write(b"ive frontier attached".ljust(80)); o.write(struct.pack("<I", len(r))); r.tofile(o)
print(a.out, len(f), "->", len(r), "dropped", int((~keep).sum()))
