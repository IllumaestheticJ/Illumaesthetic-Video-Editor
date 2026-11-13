"""v7 (user on v6: "the BRZ and GR86 bumper are clipping into each other. have them come off and then split apart"):
the moving bumpers v4-v6 were ONE part = the BRZ full car's own bumper skin + the GR86 Bomex bumper scan's inner face
(two different bumpers in one mesh). Split them so they can leave together and then separate:
  fb_brz  = front_bumper_v5 tris that ARE car4 tris (BRZ skin, markers out) + its Side Markers Removed recess fill
  fb_gr86 = clean/front_bumper.stl (Bomex GR86 Front Bumper Only, whole scan)
  rb_brz  = rear_bumper_v4 tris that ARE car4 tris (BRZ skin; light skin already cut)
  rb_gr86 = comp/rb_nolights.stl (Bomex GR86 Rear Bumper minus the two light scans)
  split_v7.py"""
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


car_tree = cKDTree(L("clean/car4.stl")["v"].mean(1))
smr_tree = cKDTree(L("clean/smr.stl")["v"].mean(1))
fb = L("parts/front_bumper_v5.stl"); fc = fb["v"].mean(1)
d_car, _ = car_tree.query(fc, distance_upper_bound=0.05, workers=-1); d_smr, _ = smr_tree.query(fc, distance_upper_bound=0.05, workers=-1)
save("parts/fb_brz.stl", fb[(d_car < 0.05) | (d_smr < 0.05)], "front bumper BRZ skin")
save("parts/fb_gr86.stl", L("clean/front_bumper.stl"), "front bumper GR86 Bomex scan")
rb = L("parts/rear_bumper_v4.stl"); rc = rb["v"].mean(1)
d_car, _ = car_tree.query(rc, distance_upper_bound=0.05, workers=-1)
save("parts/rb_brz.stl", rb[d_car < 0.05], "rear bumper BRZ skin")
save("parts/rb_gr86.stl", L("comp/rb_nolights.stl"), "rear bumper GR86 Bomex scan (lights out)")
