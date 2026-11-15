"""v10 (user on v9: "bumper trimmed works great - but once the bumper is on the car, revert back to the full car scan - since the bumper is
warped on the edges and stick out"). The bumper as it is on the truck = FULL-CAR scan (lev/front_2mm.stl, 2 mm nose crop of
'Full Car.stl') triangles in the bumper zone that are not already body (> 4 mm from c3_body) and not hood, then grille-clipped like
the body (tools/grille_clip.py). Also the scanned badge, centred on the CAD badge ring and scaled to it (the real Ronin badge fills
the ring - 1:1 onion; the accessory scan is the smaller stock badge).
    python fullbumper.py"""
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = "/home/user/media/nissan-frontier"


def load(p): return np.fromfile(p, dtype=TRI, offset=84)


def save(p, d):
    with open(p, "wb") as f: f.write(b"\0" * 80); f.write(np.uint32(len(d)).tobytes()); d.tofile(f)


full = load(f"{M}/lev/front_2mm.stl"); c = full["v"].mean(1)
cut = load(f"{M}/parts/bumper_cut.stl")["v"].reshape(-1, 3)
lo, hi = cut.min(0) - 15, cut.max(0) + 15
zone = np.all((c > lo) & (c < hi), 1)
body = load(f"{M}/parts/c3_body.stl")["v"].mean(1); hood = load(f"{M}/parts/hood.stl")["v"].mean(1)
tb = cKDTree(body[np.all((body > lo - 50) & (body < hi + 50), 1)]); th = cKDTree(hood)
db, _ = tb.query(c[zone], distance_upper_bound=50); dh, _ = th.query(c[zone], distance_upper_bound=50)
near_bumper = cKDTree(cut[::3]).query(c[zone], distance_upper_bound=60)[0] < 60     # the bumper's own neighbourhood (not wheels/frame)
keep = np.zeros(len(c), bool); keep[np.nonzero(zone)[0]] = (db > 4) & (dh > 4) & near_bumper
save(f"{M}/parts/fullbumper.stl", full[keep]); print("full-scan bumper tris", int(keep.sum()), "of zone", int(zone.sum()))
# badge onto the ring
b = load(f"{M}/lights/badge_clean.stl"); v = b["v"].astype(np.float64)
circ = np.array([(v[..., 0].min() + v[..., 0].max()) / 2, 0, (v[..., 2].min() + v[..., 2].max()) / 2])
RING_X, RING_Z, SC, FRONT_Y = 18.0, 965.0, 1.06, -3482.0   # v11: user "badge still too low" - 1:1 frame: real badge top matched, bottom 14 px lower = render too big; real badge about 148 mm
v = (v - circ) * SC; v[..., 0] += RING_X; v[..., 2] += RING_Z; v[..., 1] += FRONT_Y - v[..., 1].min()
b["v"] = v.astype(np.float32); save(f"{M}/lights/badge_ring.stl", b)
print("badge now", v.reshape(-1, 3).min(0).round(1), v.reshape(-1, 3).max(0).round(1))
