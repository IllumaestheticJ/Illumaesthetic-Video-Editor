"""Factory spoiler side covers (user on v11: "the small side pieces on the trunk need to come off" before the Epsilon
Aero WRC wing goes on; the Epsilon install guide: "Remove factory wing/factory side covers"). Each cover is the narrow
triangle between the hatch shut line, the spoiler's lower edge and the rear-glass edge, traced on a near-orthographic
render along the cover's outward normal (8 m, focal 200 mm; wing/cover_{L,R}_basis.npy = loc, forward, up, right, K).
Cover = faces inside the outline on the visible surface (within --skin mm of the nearest face along the view).
    sidecover.py in.stl basisL.npy basisR.npy coverL.stl coverR.stl rest.stl [--skin 15]"""
import argparse, struct
import numpy as np
from PIL import Image, ImageDraw
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
OUT_L = [(304, 966), (340, 955), (380, 943), (420, 925), (452, 909), (445, 930), (442, 975), (445, 1015), (460, 1050),
         (485, 1085), (510, 1120), (540, 1150), (570, 1180), (600, 1215), (628, 1248), (600, 1238), (548, 1200),
         (498, 1155), (448, 1110), (398, 1062), (348, 1012), (310, 975)]
OUT_R = [(716, 966), (690, 950), (650, 935), (610, 920), (570, 908), (582, 950), (580, 1000), (565, 1040), (540, 1075),
         (510, 1110), (480, 1145), (450, 1175), (420, 1200), (395, 1245), (420, 1222), (470, 1186), (520, 1150),
         (570, 1105), (620, 1060), (670, 1015)]
ap = argparse.ArgumentParser()
for n in ("src", "basisL", "basisR", "outL", "outR", "rest"): ap.add_argument(n)
ap.add_argument("--skin", type=float, default=15)
a = ap.parse_args()
car = np.fromfile(a.src, dtype=DT, offset=84); raw = car["v"].mean(1).astype(float)
def select(basis, outline):
    loc, f, u, r, kk = np.load(basis); K = kk[0]
    P = raw / 1000 + ROOT - loc; dep = P @ f
    pu = 540 + K * (P @ r) / dep; pv = 960 - K * (P @ u) / dep
    mask = Image.new("L", (1080, 1920), 0); ImageDraw.Draw(mask).polygon(outline, fill=1); mask = np.array(mask, bool)
    ok = (pu >= 0) & (pu < 1080) & (pv >= 0) & (pv < 1920) & (dep > 0)
    iu, iv = np.clip(np.round(pu).astype(int), 0, 1079), np.clip(np.round(pv).astype(int), 0, 1919)
    inside = ok & mask[iv, iu]
    key = iv * 4000 + iu; order = np.argsort(dep); ks, first = np.unique(key[order], return_index=True)
    near = np.full(1920 * 4000, np.inf); near[ks] = dep[order[first]]
    return inside & ((dep - near[key]) * 1000 < a.skin)
L, R = select(a.basisL, OUT_L), select(a.basisR, OUT_R)
print("faces", len(car), "| cover L", int(L.sum()), "| cover R", int(R.sum()))
for p, m in ((a.outL, car[L]), (a.outR, car[R]), (a.rest, car[~(L | R)])):
    with open(p, "wb") as fh: fh.write(b"grc sidecover".ljust(80)); fh.write(struct.pack("<I", len(m))); m.tofile(fh)
