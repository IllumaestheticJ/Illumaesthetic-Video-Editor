"""Bumper top-edge line (user on v4: "the front end scan is missing a huge chunk of the car").
The bumper scan's top edge, per 20 mm column across the car (98th percentile of z, robust to stray shards), splits the
nose: car faces ABOVE the line (+margin) are headlights / hood / fender and always stay on the car; bumper-scan faces
above it are shards of the headlight surround and are trimmed off the moving part.
    bumperline.py car_cut.stl car.stl bumper.stl car_out.stl bumper_out.stl --margin 8 --corner-x 450 --corner-z 40
At the corners the bumper scan is below z ~30 mm for 90 % of its faces; the rest are headlight-surround shards.
car_cut = the car with the bumper zone removed (frontcut.py); faces of the ORIGINAL car above the line that the cut
removed are put back."""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car_cut"); ap.add_argument("car"); ap.add_argument("bumper"); ap.add_argument("car_out"); ap.add_argument("bumper_out")
ap.add_argument("--margin", type=float, default=8); ap.add_argument("--corner-x", type=float, default=450); ap.add_argument("--corner-z", type=float, default=40); ap.add_argument("--bin", type=float, default=20)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=DT, offset=84)
def save(p, m):
    with open(p, "wb") as f: f.write(b"grc bumperline".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
bu = L(a.bumper); bc = bu["v"].mean(1)
edges = np.arange(bc[:, 0].min() - a.bin, bc[:, 0].max() + a.bin, a.bin); k = np.digitize(bc[:, 0], edges)
top = np.full(len(edges) + 1, np.inf)
for i in np.unique(k): top[i] = np.percentile(bc[k == i, 2], 98)
xc = 0.5 * (bc[:, 0].min() + bc[:, 0].max())
def line(x):  # at the corners (|x - centre| > corner-x) the cover never reaches the headlights: cap the line there
    t = top[np.digitize(x, edges)]
    return np.where(np.abs(x - xc) > a.corner_x, np.minimum(t, a.corner_z - a.margin), t)
car, cut = L(a.car), L(a.car_cut); cc, ct = car["v"].mean(1), cut["v"].mean(1)
d, _ = cKDTree(ct).query(cc, distance_upper_bound=0.5, workers=-1); gone = np.isinf(d)
back = gone & (cc[:, 2] > line(cc[:, 0]) + a.margin)
print("restored above the bumper line:", int(back.sum()), "of", int(gone.sum()), "removed")
save(a.car_out, np.concatenate([cut, car[back]]))
shard = bc[:, 2] > line(bc[:, 0]) + a.margin
print("bumper shards trimmed:", int(shard.sum()), "of", len(bu)); save(a.bumper_out, bu[~shard])
