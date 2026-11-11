"""Extra ground cleanup for the IS350 full-car scan (after align + ive crop).

  python clean.py in.stl out.stl [--report]
Drops faces below `low` mm (above floor) that lie outside the body footprint measured above `body` mm
(+ margin), and faces within `floor_band` mm of the floor except inside the four tyre contact zones.
"""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from align import load, DT

src, dst = sys.argv[1], sys.argv[2]
hdr, d = load(src)
c = d['v'].mean(1)
floor = np.percentile(c[:, 2], 0.5)
z = c[:, 2] - floor
body = c[z > 300]
lo, hi = np.percentile(body[:, :2], [0.2, 99.8], axis=0)
mx, my = 30, 60
outside = (c[:, 0] < lo[0] - mx) | (c[:, 0] > hi[0] + mx) | (c[:, 1] < lo[1] - my) | (c[:, 1] > hi[1] + my)
drop = outside & (z < 300)
# tyre contact zones: dense columns of points reaching z>350 at |x| extremes near wheel centres
# approximate wheel y centres from the lowest 60 mm points' y histogram
low = c[z < 60]
hist, edges = np.histogram(low[:, 1], bins=60, range=(lo[1], hi[1]))
keep_floor = np.zeros(len(c), bool)
for i in np.argsort(hist)[-6:]:
    y0 = (edges[i] + edges[i + 1]) / 2
    keep_floor |= np.abs(c[:, 1] - y0) < 220
drop |= (z < 40) & ~keep_floor
up = d['n'][:, 2] > 0.85
drop |= up & (z < 120) & outside
print(f"floor {floor:.0f}  footprint x {lo[0]:.0f}..{hi[0]:.0f} y {lo[1]:.0f}..{hi[1]:.0f}  len {hi[1]-lo[1]:.0f} wid {hi[0]-lo[0]:.0f}  drop {drop.sum()} / {len(c)}")
e = d[~drop]
with open(dst, 'wb') as f:
    f.write(hdr); f.write(np.uint32(len(e)).tobytes()); f.write(e.tobytes())
