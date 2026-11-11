"""Trunk lid = parts/trunk.stl (car tris missing from 'Trunk Open', tools/extract.py) minus the rear glass.
Trunk Open does not capture anything high, so the extract also took the rear window. Per 25 mm x-slice of the car's top
profile, walk +y from the roof: the glass ends where the top surface's slope over 40 mm flattens past --slope
(glass ~-0.35, deck lid ~-0.1). Lid tris in front of glass_end(x) + 6 mm are dropped (median over x).
  lid_trim.py car.stl trunk.stl out.stl [--slope -0.2] [--check top.png]"""
import argparse, struct
import numpy as np
from scipy.ndimage import median_filter
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("lid"); ap.add_argument("out")
ap.add_argument("--slope", type=float, default=-0.2); ap.add_argument("--check"); a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84)["v"].mean(1)
lid = np.fromfile(a.lid, dtype=TRI, offset=84); lc = lid["v"].mean(1)
XB, YB = 25.0, 10.0
xs = np.arange(np.floor(lc[:, 0].min() / XB) * XB, lc[:, 0].max() + XB, XB); ys = np.arange(1000, 2000, YB)
C = car[(car[:, 1] > ys[0]) & (car[:, 2] > 700)]
ix = np.clip(((C[:, 0] - xs[0]) / XB).astype(int), 0, len(xs) - 1); iy = np.clip(((C[:, 1] - ys[0]) / YB).astype(int), 0, len(ys) - 1)
top = np.full((len(xs), len(ys)), np.nan); tmp = np.full((len(xs), len(ys)), -np.inf); np.maximum.at(tmp, (ix, iy), C[:, 2]); top[np.isfinite(tmp)] = tmp[np.isfinite(tmp)]
end = np.full(len(xs), np.nan)
for i in range(len(xs)):
    t = top[i]
    for j in range(len(ys) - 4):
        if np.isfinite(t[j]) and np.isfinite(t[j + 4]) and t[j] > 900:
            if (t[j + 4] - t[j]) / (4 * YB) > a.slope and ys[j] > 1250:
                end[i] = ys[j]; break
ok = np.isfinite(end)
e = np.interp(np.arange(len(xs)), np.where(ok)[0], end[ok]); e = median_filter(e, size=7, mode="nearest")
hi = np.clip(((lc[:, 0] - xs[0]) / XB).astype(int), 0, len(xs) - 1)
keep = lc[:, 1] > e[hi] + 6
print(f"slices {len(xs)} found {ok.sum()}  glass end y {np.nanmin(end):.0f}..{np.nanmax(end):.0f} mm  lid {len(lid)} -> {keep.sum()} tris")
with open(a.out, "wb") as f:
    f.write(b"gr86 trunk lid (no glass)".ljust(80)); f.write(struct.pack("<I", int(keep.sum()))); lid[keep].tofile(f)
if a.check:
    from PIL import Image
    R = 4; img = np.zeros((int(1100 / R), int(2000 / R), 3), np.uint8)
    put = lambda p, col: img.__setitem__((np.clip(((p[:, 1] - 1000) / R).astype(int), 0, img.shape[0] - 1), np.clip(((p[:, 0] + 1000) / R).astype(int), 0, img.shape[1] - 1)), col)
    put(C, (110, 110, 110)); put(lc[keep], (0, 200, 255)); put(lc[~keep], (255, 40, 30)); Image.fromarray(img).save(a.check)
