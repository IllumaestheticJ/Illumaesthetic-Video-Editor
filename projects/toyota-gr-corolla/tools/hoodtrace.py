"""Hood cut from its traced shut lines (user on v7: "the hood is cut wrong" - the seam cut took the cowl/wipers and
left the hood's front strip on the car). Traced on a near-orthographic render along the hood normal (chk5/hood_ortho:
camera = hood centre + 26 m * normal, focal 200 mm; basis saved in hood_cam_basis.npy = loc, forward, up, right, K).
Outline: cowl seam (rear), fender shut lines (sides), front crease above the headlights/grille surround.
Hood = car faces inside the outline that are on the visible surface (within --skin mm of the nearest face along the view).
    hoodtrace.py car.stl basis.npy hood_out.stl car_out.stl --skin 30"""
import argparse, struct
import numpy as np
from PIL import Image, ImageDraw
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
OUTLINE = [(240, 842), (300, 868), (400, 880), (500, 884), (600, 884), (700, 868), (760, 850), (820, 832),
           (825, 880), (830, 940), (832, 1000), (828, 1060), (822, 1100), (810, 1140), (790, 1170), (770, 1195),
           (740, 1215), (680, 1238), (600, 1246), (520, 1246), (400, 1240), (330, 1222), (290, 1200), (255, 1165),
           (235, 1130), (228, 1100), (222, 1060), (217, 1020), (215, 980), (218, 940), (222, 900), (232, 880)]
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("basis"); ap.add_argument("hood_out"); ap.add_argument("car_out")
ap.add_argument("--skin", type=float, default=30)
a = ap.parse_args()
loc, f, u, r, kk = np.load(a.basis); K = kk[0]
car = np.fromfile(a.car, dtype=DT, offset=84); raw = car["v"].mean(1).astype(float); P = raw / 1000 + ROOT - loc
dep = P @ f; pu = 540 + K * (P @ r) / dep; pv = 960 - K * (P @ u) / dep
mask = Image.new("L", (1080, 1920), 0); ImageDraw.Draw(mask).polygon(OUTLINE, fill=1); mask = np.array(mask, bool)
iu, iv = np.clip(np.round(pu).astype(int), 0, 1079), np.clip(np.round(pv).astype(int), 0, 1919)
inside = mask[iv, iu]
key = iv * 4000 + iu; order = np.argsort(dep); ks, first = np.unique(key[order], return_index=True)
near_d = dict(zip(ks, dep[order[first]]))
skin = (dep - np.array([near_d[k] for k in key])) * 1000 < a.skin
hood = inside & skin
print("car", len(car), "-> hood", int(hood.sum()))
for p, m in ((a.hood_out, car[hood]), (a.car_out, car[~hood])):
    with open(p, "wb") as fh: fh.write(b"grc hoodtrace".ljust(80)); fh.write(struct.pack("<I", len(m))); m.tofile(fh)
