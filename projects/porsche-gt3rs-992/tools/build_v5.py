"""v5 geometry (levelled mm frame, underbody session registered with regT_underbody_session.json):
  wheel_fl.stl        front-left wheel from "Underbody Wheels" (the part that comes off)
  comp_v5.stl         comp_v3 minus everything inside the FL wheel cylinder, plus the NEW geometry of
                      "Underbody front and rear wheel house" in the FL arch (state scan as captured, wheels off)
  underbody_new.stl   "Underbody underbody" triangles the car scan does not have (> 6 mm from the car)
    python projects/porsche-gt3rs-992/tools/build_v5.py"""
import struct
import numpy as np
from scipy.spatial import cKDTree
W = "/home/user/media/porsche-gt3rs-992"
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
load = lambda p: np.fromfile(p, dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"gt3 v5".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
    print(p.split("/")[-1], len(m))


wheels = load(f"{W}/xp/underbody_wheels.stl"); wc = wheels["v"].mean(1)
fl = wheels[wc[:, 1] < 0]; save(f"{W}/xp/wheel_fl.stl", fl)
v = fl["v"].reshape(-1, 3)
cy, cz = (v[:, 1].min() + v[:, 1].max()) / 2, (v[:, 2].min() + v[:, 2].max()) / 2
rad = max(np.ptp(v[:, 1]), np.ptp(v[:, 2])) / 2
x_in, x_out = v[:, 0].min(), v[:, 0].max()
print("FL wheel centre y %.0f z %.0f radius %.0f  x %.0f..%.0f" % (cy, cz, rad, x_in, x_out))

car = load(f"{W}/dec/comp_v3.stl"); cc = car["v"].mean(1)
r = np.hypot(cc[:, 1] - cy, cc[:, 2] - cz)
incyl = (r < rad + 12) & (cc[:, 0] > x_in - 25) & (cc[:, 0] < x_out + 30)
kept = car[~incyl]
print("car tris inside the wheel cylinder removed:", int(incyl.sum()))
wh = load(f"{W}/xp/underbody_front_and_rear_wheel_house.stl"); hc = wh["v"].mean(1)
zone = (hc[:, 0] > 250) & (np.abs(hc[:, 1] - cy) < rad + 260) & (hc[:, 2] > -20) & (hc[:, 2] < cz + rad + 260)
d, _ = cKDTree(kept["v"].mean(1)[::2]).query(hc[zone], distance_upper_bound=14)
sel = np.zeros(len(wh), bool); sel[np.where(zone)[0][d > 7]] = True
print("wheel-house fill tris:", int(sel.sum()), "of", int(zone.sum()), "in the FL arch zone")
save(f"{W}/dec/comp_v5.stl", np.concatenate([kept, wh[sel]]))

ub = load(f"{W}/xp/underbody_underbody.stl"); uc = ub["v"].mean(1)
d, _ = cKDTree(load(f"{W}/dec/carL_4mm_crop.stl")["v"].mean(1)[::2]).query(uc, distance_upper_bound=12)
new = (d > 6) & (uc[:, 2] < 520)
save(f"{W}/xp/underbody_new.stl", ub[new])
