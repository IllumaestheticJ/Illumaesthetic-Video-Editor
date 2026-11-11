"""Trim the hood panel at the real hood/cowl gap (user v2 feedback: "hood opened scan cuts too much of the windshield out").
hood_mask.py's top-view mask came from car tris missing in 'Hood Open' - the open hood hid the lower windshield in that
scan, so the mask (and the hood part) ran 100-230 mm up the glass. Per 25 mm x-slice of the full car's top profile
(levelled mm), walk +y from the hood nose: the cowl gap is the first 20 mm dip below the running max of the top surface.
Hood tris behind gap_y(x) - 4 mm are dropped (median-filtered over x so one noisy slice can't bite a notch).
  hood_trim.py car.stl hood.stl out.stl [--check out.png]"""
import argparse, struct
import numpy as np
from scipy.ndimage import median_filter
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("hood"); ap.add_argument("out"); ap.add_argument("--check")
a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84)["v"].mean(1)
hood = np.fromfile(a.hood, dtype=TRI, offset=84); hc = hood["v"].mean(1)
XB, YB = 25.0, 10.0
xs = np.arange(np.floor(hc[:, 0].min() / XB) * XB, hc[:, 0].max() + XB, XB)
ys = np.arange(-1400, -700, YB)
sel = (car[:, 1] > ys[0]) & (car[:, 1] < ys[-1] + YB) & (car[:, 2] > 650)
C = car[sel]
ix = np.clip(((C[:, 0] - xs[0]) / XB).astype(int), 0, len(xs) - 1); iy = np.clip(((C[:, 1] - ys[0]) / YB).astype(int), 0, len(ys) - 1)
top = np.full((len(xs), len(ys)), -np.inf); np.maximum.at(top, (ix, iy), C[:, 2])
gap = np.full(len(xs), np.nan)
for i in range(len(xs)):
    t = top[i]; run = -np.inf; started = False
    for j in range(len(ys)):
        if not np.isfinite(t[j]):
            continue
        hj = (np.abs(hc[:, 0] - xs[i] - XB / 2) < XB / 2) & (np.abs(hc[:, 1] - ys[j] - YB / 2) < YB / 2)
        started |= bool(hj.any())
        if started and run - t[j] > 20:
            gap[i] = ys[j]; break
        run = max(run, t[j])
ok = np.isfinite(gap)
gap_f = np.interp(np.arange(len(xs)), np.where(ok)[0], gap[ok]) if ok.any() else np.full(len(xs), 1e9)
gap_f = median_filter(gap_f, size=5, mode="nearest")
hi = np.clip(((hc[:, 0] - xs[0]) / XB).astype(int), 0, len(xs) - 1)
keep = hc[:, 1] < gap_f[hi] - 4
print(f"slices {len(xs)} gap found {ok.sum()}  gap y {np.nanmin(gap):.0f}..{np.nanmax(gap):.0f} mm  hood {len(hood)} -> {keep.sum()} tris "
      f"(dropped {(~keep).sum()}, max y {hc[keep, 1].max():.0f} mm)")
with open(a.out, "wb") as f:
    f.write(b"gr86 hood trimmed at cowl gap".ljust(80)); f.write(struct.pack("<I", int(keep.sum()))); hood[keep].tofile(f)
if a.check:
    from PIL import Image
    R = 4; W = int(2000 / R); H = int(1600 / R); img = np.zeros((H, W, 3), np.uint8)   # top view: x across, y down
    cs = car[(car[:, 1] > -2200) & (car[:, 1] < -600) & (car[:, 2] > 650)]
    def put(p, col):
        img[np.clip(((p[:, 1] + 2200) / R).astype(int), 0, H - 1), np.clip(((p[:, 0] + 1000) / R).astype(int), 0, W - 1)] = col
    put(cs, (110, 110, 110)); put(hc[keep], (0, 200, 255)); put(hc[~keep], (255, 40, 30))
    Image.fromarray(img).save(a.check)
