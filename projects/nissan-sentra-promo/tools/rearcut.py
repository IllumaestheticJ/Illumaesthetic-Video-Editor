"""v2 cuts (reviewer: new wheels not on, old diffuser not removed). From car_nobump.stl / front_fill.stl:
- stock wheels+tyres: tris outboard of the hub face (|x| > xin) within rup (above the axle) / rlow (below) of the new wheel centre
  -> stock_wheels.stl; removed from the car.
- stock rear valance under the new diffuser: tris within dmax of Uncut_Rear_Diffuser, behind the rear axle, below the
  diffuser's top edge (+10) -> stock_diffuser.stl; removed from the car.
Writes car_v2.stl, fill_v2.stl, stock_wheels.stl, stock_diffuser.stl (design frame, mm).
rearcut.py car_nobump.stl front_fill.stl Uncut_Rear_Diffuser.stl outdir [--dmax 45] [--rup 360] [--rlow 410] [--xin 630]"""
import argparse, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); [ap.add_argument(x) for x in ("car", "fill", "diff", "outdir")]
ap.add_argument("--dmax", type=float, default=45); ap.add_argument("--rup", type=float, default=360); ap.add_argument("--rlow", type=float, default=410); ap.add_argument("--xin", type=float, default=630)
a = ap.parse_args()
def L(p): return np.fromfile(p, dtype=TRI, offset=84)
def W(p, d):
    with open(p, "wb") as f: f.write(b"\0" * 80); f.write(np.uint32(len(d)).tobytes()); d.tofile(f)
# centred on the NEW wheels (Sentra Review 2.blend FL/FR/RL/RR bbox centres, y z mm): above the axle only out to
# rup (keeps the wheel-well liner), below it out to rlow (stock tyre bulge; nothing else lives there)
NEW = [(+1, -1075, 350), (-1, -1077, 345), (+1, 1634, 344), (-1, 1631, 347)]
def wheel_mask(c):
    m = np.zeros(len(c), bool)
    for s, y, z in NEW:
        r = np.hypot(c[:, 1] - y, c[:, 2] - z)
        m |= (s * c[:, 0] > a.xin) & (r < np.where(c[:, 2] > z, a.rup, a.rlow))
    return m
car, fill = L(a.car), L(a.fill)
dv = L(a.diff)["v"].reshape(-1, 3); T = cKDTree(dv[::2])
cc = car["v"].mean(1)
wm = wheel_mask(cc)
# diffuser region: top edge per 20 mm x-column
xb = np.arange(-900, 901, 20); ztop = np.full(len(xb), -1e9)
ix = np.clip(((dv[:, 0] + 900) // 20).astype(int), 0, len(xb) - 1); np.maximum.at(ztop, ix, dv[:, 2])
ci = np.clip(((cc[:, 0] + 900) // 20).astype(int), 0, len(xb) - 1)
cand = (cc[:, 1] > 2100) & (cc[:, 2] < ztop[ci] + 10) & ~wm
d = np.full(len(cc), np.inf); d[cand] = T.query(cc[cand], distance_upper_bound=a.dmax + 5)[0]
dm = cand & (d <= a.dmax)
print("stock wheel tris", wm.sum(), "stock diffuser tris", dm.sum())
W(f"{a.outdir}/stock_wheels.stl", np.concatenate([car[wm], fill[wheel_mask(fill["v"].mean(1))]]))
W(f"{a.outdir}/stock_diffuser.stl", car[dm])
W(f"{a.outdir}/car_v2.stl", car[~(wm | dm)])
fm = wheel_mask(fill["v"].mean(1)); print("fill wheel tris", fm.sum())
W(f"{a.outdir}/fill_v2.stl", fill[~fm])
