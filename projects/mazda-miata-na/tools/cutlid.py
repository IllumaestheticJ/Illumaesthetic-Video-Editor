"""Cut a lid (hood / trunk lid) out of the full-car scan along its panel gaps (levelled frame, mm).
Outlines were read off a 2 mm top-down seam map (height minus grey closing) of the 2 mm car scan.
    cutlid.py hood|trunk car.stl lid_out.stl rest_out.stl"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
which, src, lo, ro = sys.argv[1:5]
m = np.fromfile(src, dtype=TRI, offset=84)
v = m["v"].astype(np.float64); c = v.mean(1)
n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
x, y, z = c.T
if which == "hood":
    u = ((x + 80) / 640) ** 2
    k = (x > -706) & (x < 562) & (y > -1962 + 50 * u) & (y < -924 + 125 * u) & (z > 640)
    k &= ~((x < -445) & (y < -1652)) & ~((x > 287) & (y < -1648))   # pop-up headlamp doors stay on the car
    k &= np.abs(n[:, 2]) > 0.25          # skin (up/down facing), not fender walls through the gap
else:
    u = ((x + 110) / 525) ** 2
    k = (x > -632) & (x < 412) & (y > 1106 - 72 * u) & (z > 742) & (y < 1800)
    k &= (np.abs(n[:, 2]) > 0.25) | (n[:, 1] > 0.35)   # top skin + the rear face that wraps down to the plate recess
def save(p, sel):
    with open(p, "wb") as f:
        f.write(b"ive cutlid".ljust(80)); f.write(struct.pack("<I", int(sel.sum()))); m[sel].tofile(f)
save(lo, k); save(ro, ~k); print(which, "lid", int(k.sum()), "rest", int((~k).sum()))
