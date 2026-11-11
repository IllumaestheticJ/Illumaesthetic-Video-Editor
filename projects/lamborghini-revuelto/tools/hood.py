"""Cut the closed front hood (frunk lid) out of the full-car scan: car triangles in the hood zone that the
'Hood Open' state scan no longer has (> GAP mm from it) = the panel that moved. Also writes the open hood as
captured (Hood Open points above the car's roofline) for the hinge fit.
  hood.py car.stl st_hood_open.stl hood_closed.stl hood_open_pts.npy"""
import struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
GAP = 10.0
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84); st = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
cc = car["v"].mean(1); sc = st["v"].mean(1)
# top surface of the nose only (within 40 mm of the highest car point per 30 mm XY cell)
kc = np.floor(cc[:, 0] / 30).astype(np.int64) * 100000 + np.floor(cc[:, 1] / 30).astype(np.int64)
uu, ii = np.unique(kc, return_inverse=True); tp = np.full(len(uu), -1e9); np.maximum.at(tp, ii, cc[:, 2])
zone = (cc[:, 1] > -2400) & (cc[:, 1] < -1100) & (np.abs(cc[:, 0]) < 950) & (cc[:, 2] > 250) & (cc[:, 2] > tp[ii] - 40)
d, _ = cKDTree(sc).query(cc[zone], distance_upper_bound=GAP + 1)
idx = np.where(zone)[0][d > GAP]
idx = idx[cc[idx, 1] < -1220]  # stray cowl-edge slivers behind the lid
# the lid is one surface: keep the cells that are well populated (drops stray far points like glass edges)
cell = 50.0
k = np.floor(cc[idx, 0] / cell) * 1000 + np.floor(cc[idx, 1] / cell)
u, inv, cnt = np.unique(k, return_inverse=True, return_counts=True)
idx = idx[cnt[inv] >= 20]
# close pinholes: grow the lid into zone triangles within 8 mm of it (twice) - lid triangles that happened to sit
# near something in the Hood Open scan were missed and showed as black dots once the base was trimmed
zidx = np.where(zone & (cc[:, 1] < -1220))[0]
ztree = cKDTree(cc[zidx])
for _ in range(2):
    near = ztree.query_ball_point(cc[idx], r=8.0)
    idx = np.unique(np.concatenate([idx, zidx[np.unique(np.concatenate(near)).astype(int)]]))
hood = car[idx]
with open(sys.argv[3], "wb") as f:
    f.write(b"ive revuelto hood".ljust(80)); f.write(struct.pack("<I", len(hood))); hood.tofile(f)
print("hood tris", len(hood), "x", cc[idx, 0].min().round(), cc[idx, 0].max().round(), "y", cc[idx, 1].min().round(),
      cc[idx, 1].max().round(), "z", cc[idx, 2].min().round(), cc[idx, 2].max().round())
# open hood in the state scan: above the full car's own top surface (per 40 mm cell) in the front half
cell = 40.0
key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
ks = key(sc[:, :2]); i = np.clip(np.searchsorted(u, ks), 0, len(u) - 1); roof = np.where(u[i] == ks, top[i], -1e9)
op = sc[(sc[:, 2] > roof + 30) & (sc[:, 1] < -900)]
np.save(sys.argv[4], op); print("open hood pts", len(op), "z", op[:, 2].min().round(), op[:, 2].max().round())
