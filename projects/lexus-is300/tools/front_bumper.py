"""Derive the front bumper cover from the data: the full car minus the registered 'front end bumper removed'
state scan. (There is no separate front-bumper part scan for the IS300.)
Bumper = car triangles in the nose zone (y < --ymax, levelled mm) that are > --far mm from the state scan and
below the state scan's own top surface in the same 30 mm (x,y) cell (+ --zpad) - the state has no hood, so the
hood stays on the car. Largest connected pieces only (by 15 mm voxel adjacency).
  python front_bumper.py car_lv.stl state_lv.stl out_bumper.stl
"""
import struct, sys
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car_p, st_p, out = sys.argv[1:4]
YMAX, FAR, ZPAD, CELL = -1880.0, 10.0, 25.0, 30.0
ZHL, FAR_HL = -150.0, 45.0
ZTOP = float(sys.argv[4]) if len(sys.argv) > 4 else -60.0
ZLAMP = float(sys.argv[5]) if len(sys.argv) > 5 else -250.0
XLAMP = 330.0
car = np.fromfile(car_p, dtype=TRI, offset=84); cc = car["v"].mean(1)
st = np.fromfile(st_p, dtype=TRI, offset=84)["v"].mean(1)
lo = np.minimum(cc.min(0), st.min(0))
key = lambda p: (np.floor((p[:, 0] - lo[0]) / CELL).astype(int), np.floor((p[:, 1] - lo[1]) / CELL).astype(int))
nx, ny = 200, 200
zmax = np.full((nx, ny), -1e9)
i, j = key(st); ok = (i < nx) & (j < ny)
np.maximum.at(zmax, (i[ok], j[ok]), st[ok, 2])
zmax = ndimage.grey_dilation(zmax, size=(9, 9))
d, _ = cKDTree(st).query(cc, distance_upper_bound=FAR_HL * 2)
i, j = key(cc); i = np.clip(i, 0, nx - 1); j = np.clip(j, 0, ny - 1)
far = np.where(cc[:, 2] > ZHL, FAR_HL, FAR)  # headlight lenses sit ~10-40 mm proud of the state's lamp bodies
sel = (cc[:, 1] < YMAX) & (d > far) & (cc[:, 2] < zmax[i, j] + ZPAD) & (cc[:, 2] < np.where(np.abs(cc[:, 0]) > XLAMP, ZLAMP, ZTOP))  # above: hood nose + lamp bezels stay on the car
# connected components on a 15 mm voxel grid
v = np.floor((cc[sel] - lo) / 15).astype(int)
g = np.zeros(v.max(0) + 2, bool); g[tuple(v.T)] = True
lab, n = ndimage.label(g, structure=np.ones((3, 3, 3)))
sizes = ndimage.sum(g, lab, range(1, n + 1))
keep_lab = set((np.argsort(sizes)[::-1][:3] + 1).tolist())
keep_lab = {l for l in keep_lab if sizes[l - 1] > 0.05 * sizes.max()}
kk = np.isin(lab[tuple(v.T)], list(keep_lab))
idx = np.where(sel)[0][kk]
print("bumper tris", len(idx), "components kept", sorted(sizes[[l - 1 for l in keep_lab]].astype(int)))
m = car[idx]
with open(out, "wb") as f:
    f.write(b"is300 front bumper (car - state)".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print("bbox", m["v"].reshape(-1, 3).min(0).round(), m["v"].reshape(-1, 3).max(0).round())
