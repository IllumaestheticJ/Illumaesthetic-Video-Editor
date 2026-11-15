"""Hatch cut from its traced shut line (user on v6: "rear trunk isn't cut out correctly").
The shut line was traced on a near-orthographic rear render of car2w (camera at prepped (xc, 26, 1.0) looking -y,
focal 220 mm, sensor 20.25 mm, 1080 px wide; chk5/rear_ortho, hz_left_1 / hz_right_1). A face is HATCH when its
projection is inside that outline and it is (a) on the visible rear surface (within --skin mm of the nearest face
along the view ray) or (b) one of the old seam-cut hatch faces (hidden spoiler underside, inner panel); faces forward
of the hatch's top edge (roof, antenna) never are. Everything else stays on the car.
    hatchtrace.py car.stl old_hatch.stl hatch_out.stl car_out.stl --skin 40"""
import argparse, struct
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import cKDTree
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
XC, CY, CZ, K = -0.201 + 0.2036, 26.0, 1.0, 220 / 20.25 * 1080
OUTLINE = [(310, 766), (760, 766), (775, 800), (790, 850), (815, 868), (820, 900), (818, 930), (815, 948), (822, 960),
           (827, 990), (832, 1010), (830, 1030), (823, 1050), (818, 1060), (818, 1075), (812, 1100), (800, 1120),
           (780, 1135), (740, 1150), (330, 1152), (280, 1140), (255, 1120), (240, 1100), (232, 1075), (230, 1055),
           (222, 1035), (220, 1015), (222, 1000), (230, 970), (240, 945), (236, 920), (234, 900), (236, 880),
           (240, 862), (290, 800)]
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("old_hatch"); ap.add_argument("hatch_out"); ap.add_argument("car_out")
ap.add_argument("--skin", type=float, default=40); ap.add_argument("--ymin", type=float, default=320)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=DT, offset=84)
def save(p, m):
    with open(p, "wb") as f: f.write(b"grc hatchtrace".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
car = L(a.car); raw = car["v"].mean(1).astype(float); P = raw / 1000 + ROOT
dist = CY - P[:, 1]; u = 540 - K * (P[:, 0] - XC) / dist; v = 960 - K * (P[:, 2] - CZ) / dist
mask = Image.new("L", (1080, 1920), 0); ImageDraw.Draw(mask).polygon(OUTLINE, fill=1); mask = np.array(mask, bool)
iu0, iv0 = np.clip(np.round(u).astype(int), 0, 1079), np.clip(np.round(v).astype(int), 0, 1919)
inside = mask[iv0, iu0] & (raw[:, 1] > a.ymin)
# z-buffer: nearest (max y) face per 1-px cell
iu, iv = np.round(u).astype(int), np.round(v).astype(int); key = iv * 4000 + iu
zb = {}
order = np.argsort(-raw[:, 1]); seen = np.unique(key[order], return_index=True)
front = dict(zip(seen[0], raw[order[seen[1]], 1]))
near = np.array([front[k] for k in key]) - raw[:, 1] < a.skin
old = L(a.old_hatch); d, _ = cKDTree(old["v"].mean(1)).query(raw, distance_upper_bound=1.0, workers=-1)
hatch = inside & (near | np.isfinite(d))
print("car", len(car), "-> hatch", int(hatch.sum()), "| old cut", len(old), "| old faces now kept on the car", int((np.isfinite(d) & ~hatch).sum()),
      "| new faces the old cut missed", int((hatch & ~np.isfinite(d)).sum()))
save(a.hatch_out, car[hatch]); save(a.car_out, car[~hatch])
