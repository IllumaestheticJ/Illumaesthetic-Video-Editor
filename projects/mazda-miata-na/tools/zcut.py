"""Drop triangles below a height (levelled frame, mm) or outside a Y range: scanned ground remnants and debris.
    python zcut.py in.stl out.stl --zmin 8 [--upflat 60 --ymin -2100 --ymax 1800]"""
import argparse, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("i"); ap.add_argument("o")
ap.add_argument("--zmin", type=float, default=8); ap.add_argument("--ymin", type=float, default=-1e9); ap.add_argument("--ymax", type=float, default=1e9)
ap.add_argument("--upflat", type=float, default=0, help="also drop up-facing (n.z>0.9) faces below this height (ground strips under the car)")
ap.add_argument("--low-keep-wheels", default="")
a = ap.parse_args()
m = np.fromfile(a.i, dtype=TRI, offset=84); c = m["v"].mean(1)
k = (m["v"][:, :, 2].min(1) > a.zmin) & (c[:, 1] > a.ymin) & (c[:, 1] < a.ymax)
if a.upflat:
    v = m["v"].astype(np.float64); n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    k &= ~((np.abs(n[:, 2]) > 0.9) & (c[:, 2] < a.upflat))
if a.low_keep_wheels:  # below this height keep only the tyre contact zones (boxes "x0,x1,y0,y1;...")
    zl, boxes = a.low_keep_wheels.split("@")
    low = c[:, 2] < float(zl); inb = np.zeros(len(c), bool)
    for b in boxes.split(";"):
        x0, x1, y0, y1 = map(float, b.split(","))
        inb |= (c[:, 0] > x0) & (c[:, 0] < x1) & (c[:, 1] > y0) & (c[:, 1] < y1)
    k &= ~(low & ~inb)
with open(a.o, "wb") as f:
    f.write(b"ive zcut".ljust(80)); f.write(struct.pack("<I", int(k.sum()))); m[k].tofile(f)
print(a.o, len(m), "->", int(k.sum()))
