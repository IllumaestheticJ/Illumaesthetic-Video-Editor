"""Thin cross-section overlay (numpy): car grey, part red, in a slab |x-x0|<w (side section) and |y-y0|<w (front section)
and top view. Shows registration errors far better than a full silhouette splat.
  sect.py out.png car.stl part.stl --x 400 --y -1500 [--w 15] [--S 4]"""
import argparse, numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("car"); ap.add_argument("parts", nargs="+")
ap.add_argument("--x", type=float, default=0); ap.add_argument("--y", type=float, default=0); ap.add_argument("--z", type=float, default=600)
ap.add_argument("--w", type=float, default=12); ap.add_argument("--S", type=float, default=4)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)
pts = [L(a.car)] + [L(p) for p in a.parts]
cols = [(150, 150, 150), (255, 50, 50), (60, 200, 255), (80, 255, 80)]
lo = np.array([-1000, -2100, -50.0]); hi = np.array([1000, 2100, 1400.0])
panels = []
for ax, (u, v), val in [(0, (1, 2), a.x), (1, (0, 2), a.y), (2, (0, 1), a.z)]:
    W = int((hi[u] - lo[u]) / a.S); H = int((hi[v] - lo[v]) / a.S)
    img = np.zeros((H, W, 3), np.uint8)
    for k, p in enumerate(pts):
        q = p[np.abs(p[:, ax] - val) < a.w] if ax < 2 else p[p[:, 2] > val]
        x = ((q[:, u] - lo[u]) / a.S).astype(int); y = H - 1 - ((q[:, v] - lo[v]) / a.S).astype(int)
        m = (x >= 0) & (x < W) & (y >= 0) & (y < H)
        img[y[m], x[m]] = cols[k]
    panels.append(Image.fromarray(img))
Wt = sum(p.width for p in panels) + 20; c = Image.new("RGB", (Wt, max(p.height for p in panels))); x = 0
for p in panels: c.paste(p, (x, 0)); x += p.width + 10
c.save(a.out); print(a.out, c.size)
