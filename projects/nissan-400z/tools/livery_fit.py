"""Fit the PSD side view (livery/tex/mask.png = L2 silhouette of the kitted car, driver side) to the kitted car in the render
frame: rasterise the (y, z) silhouette of car + kit points and grid-search scale/offset for the best IoU with the mask.
Writes projects/nissan-400z/livery_map.json: y = Y0 + u*LEN (u = image x / width), z = Z0 + (1 - v)*HGT (v = image y / height)."""
import glob, json
import numpy as np
from PIL import Image
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
pj = json.load(open("/home/user/media/work/z400/blend/car.json")); root = np.array(pj["root_location"])
def pts(p, step): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)[::step].astype(np.float64) * 0.001 + root
P = np.concatenate([pts("/home/user/media/nissan-400z/lev/Full_Car_3mm.stl", 4)] +
                   [pts(f, 4) for f in glob.glob("/home/user/media/nissan-400z/kit/lev/*.stl") if "mirror" not in f])
P = P[P[:, 2] > 0.02]
m = np.asarray(Image.open("/home/user/media/nissan-400z/livery/tex/mask.png"))[..., 3] > 128
Hh, Ww = m.shape
best = None
for sc in np.linspace(0.96, 1.06, 11):          # image px per (m) relative to the bbox fit
    for dy in np.linspace(-0.08, 0.08, 9):
        for dz in np.linspace(-0.06, 0.06, 7):
            LEN = 4.464 / sc; Y0 = -2.21 + dy; HGT = LEN * Hh / Ww; Z0 = 0.13 + dz
            u = ((P[:, 1] - Y0) / LEN * Ww).astype(int); v = ((1 - (P[:, 2] - Z0) / HGT) * Hh).astype(int)
            k = (u >= 0) & (u < Ww) & (v >= 0) & (v < Hh)
            r = np.zeros_like(m); r[v[k], u[k]] = True
            r = ndimage.binary_closing(r, np.ones((5, 5)), iterations=2)
            iou = (r & m).sum() / (r | m).sum()
            if best is None or iou > best[0]: best = (iou, Y0, LEN, Z0, HGT)
iou, Y0, LEN, Z0, HGT = best
print("IoU %.3f Y0 %.3f LEN %.3f Z0 %.3f HGT %.3f" % best)
json.dump({"Y0": Y0, "LEN": LEN, "Z0": Z0, "HGT": HGT, "iou": iou}, open("projects/nissan-400z/livery_map.json", "w"), indent=1)
u = ((P[:, 1] - Y0) / LEN * Ww).astype(int); v = ((1 - (P[:, 2] - Z0) / HGT) * Hh).astype(int); k = (u >= 0) & (u < Ww) & (v >= 0) & (v < Hh)
o = np.zeros((Hh, Ww, 3), np.uint8); o[m] = (90, 90, 90); o[v[k], u[k]] = (255, 60, 60)
Image.fromarray(o).save("/tmp/claude-0/-home-user-Illumaesthetic-Video-Editor/7fb2e21b-fa3b-5a1c-abba-9b3f48ec7a09/scratchpad/livfit.png")
