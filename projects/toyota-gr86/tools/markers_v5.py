"""v5 (user: "make sure all parts are highlighted"): the front side markers - the one scanned part v1-v4 never showed.
Bomex Side Markers (two corner markers, own capture) placed with its ICP (dec/Side_Markers_lev_icp.npy -> parts/side_markers.stl,
median 3.5 mm to front_bumper_v4). Splits them into R (x > 0) / L parts and makes the front bumper without them:
front_bumper_v4 minus tris within 5 mm of a marker + the 'Side Markers Removed' state's tris (clean/smr.stl) inside each
marker box (+30 mm) that are > 4 mm from the bumper (the empty marker recess).
  markers_v5.py   (writes parts/side_marker_R.stl, side_marker_L.stl, front_bumper_v5.stl)"""
import struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = "/home/user/media/work/gr86/"
L = lambda f: np.fromfile(M + f, dtype=TRI, offset=84)


def save(f, m, tag):
    with open(M + f, "wb") as o:
        o.write(("gr86 " + tag).encode().ljust(80)); o.write(struct.pack("<I", len(m))); m.tofile(o)
    c = m["v"].mean(1); print(f, len(m), c.min(0).round(), c.max(0).round())


mk = L("parts/side_markers.stl"); mc = mk["v"].mean(1)
save("parts/side_marker_R.stl", mk[mc[:, 0] > 0], "side marker R"); save("parts/side_marker_L.stl", mk[mc[:, 0] <= 0], "side marker L")
fb = L("parts/front_bumper_v4.stl"); fc = fb["v"].mean(1)
d, _ = cKDTree(mc).query(fc, distance_upper_bound=10); keep = ~(d < 5)
smr = L("clean/smr.stl"); sc = smr["v"].mean(1)
add = np.zeros(len(smr), bool)
for side in (mc[:, 0] > 0, mc[:, 0] <= 0):
    lo, hi = mc[side].min(0) - 30, mc[side].max(0) + 30
    add |= np.all((sc > lo) & (sc < hi), 1)
d2, _ = cKDTree(fc[keep]).query(sc[add], distance_upper_bound=10); idx = np.where(add)[0][~(d2 < 4)]
print("bumper", len(fb), "-> minus markers", int((~keep).sum()), "+ recess fill", len(idx))
save("parts/front_bumper_v5.stl", np.concatenate([fb[keep], smr[idx]]), "front bumper v5 (markers out)")
