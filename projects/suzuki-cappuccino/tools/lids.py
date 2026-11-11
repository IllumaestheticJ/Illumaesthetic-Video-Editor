"""Cut the closed hood and trunk lid out of the levelled full car (mm frame): car triangles in the lid zone that the
open-state scan does NOT have (>D mm from it, the lid moved away), above the shut-line height, upward-facing-ish.
  lids.py car.stl fboho.stl reto.stl outdir"""
import sys, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
def save(p, r): open(p, "wb").write(b"lid".ljust(80) + struct.pack("<I", len(r)) + r.tobytes()); print(p, len(r))
if sys.argv[1] != "--clip":
  car = load(sys.argv[1]); cc = car["v"].mean(1)
  for name, st, ysel, zmin in (("hood", sys.argv[2], lambda y: (y > -1330) & (y < -300), 560),
                               ("trunk", sys.argv[3], lambda y: (y > 1240) & (y < 1880), 640)):
      s = load(st)["v"].mean(1)
      zone = ysel(cc[:, 1]) & (cc[:, 2] > zmin) & (car["n"][:, 2] > 0.2)
      d, _ = cKDTree(s).query(cc[zone], distance_upper_bound=12)
      idx = np.where(zone)[0][d > 10]
      save(f"{sys.argv[4]}/{name}_raw.stl", car[idx])

# --- second pass (run: lids.py --clip car.stl outdir): clip each raw lid to the shut lines seen in top-down renders:
# hood edges ~85 mm inside the body edge, trunk lid ~110 mm inside, lid front edge at the hardtop (y > TRUNK_Y0)
def clip(car_p, outdir, margins=dict(hood=85, trunk=110), TRUNK_Y0=1420):
    car = load(car_p); cc = car["v"].mean(1); body = cc[cc[:, 2] > 450]
    for name in margins:
        t = load(f"{outdir}/{name}_raw.stl"); c = t["v"].mean(1)
        keep = np.zeros(len(t), bool)
        for y0 in np.arange(c[:, 1].min(), c[:, 1].max() + 20, 20):
            band = body[np.abs(body[:, 1] - y0 - 10) < 15]
            if len(band) < 50: continue
            lo, hi = np.percentile(band[:, 0], [0.5, 99.5])
            m = (c[:, 1] >= y0) & (c[:, 1] < y0 + 20)
            keep |= m & (c[:, 0] > lo + margins[name]) & (c[:, 0] < hi - margins[name])
        if name == "trunk": keep &= c[:, 1] > TRUNK_Y0
        save(f"{outdir}/{name}.stl", t[keep])
if __name__ == "__main__" and sys.argv[1] == "--clip": clip(sys.argv[2], sys.argv[3])
