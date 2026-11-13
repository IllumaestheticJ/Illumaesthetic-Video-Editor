"""faceview.py in.stl out.png side(+1 rear/-1 front) ymin_abs : local-depth image of the car's end face, 3 mm/px, with 100 mm grid labels"""
import sys, numpy as np
from PIL import Image, ImageDraw
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
c = np.fromfile(sys.argv[1], dtype=TRI, offset=84)["v"].mean(1)
side = float(sys.argv[3]); lim = float(sys.argv[4])
c = c[c[:, 1] * side > lim]
s = 3.0
x0, x1, z0, z1 = c[:, 0].min(), c[:, 0].max(), 0, c[:, 2].max()
W, H = int((x1 - x0) / s) + 1, int((z1 - z0) / s) + 1
ix = ((c[:, 0] - x0) / s).astype(int); iz = (H - 1 - ((c[:, 2] - z0) / s)).astype(int)
ok = (iz >= 0) & (iz < H)
d = np.full((H, W), -1e9); np.maximum.at(d, (iz[ok], ix[ok]), c[ok, 1] * side)
m = d > -1e9
from scipy.ndimage import uniform_filter
dd = np.where(m, d, np.nan); fill = np.where(m, d, np.nanmedian(dd))
loc = fill - uniform_filter(fill, 15)
img = np.clip(128 + loc * 12, 0, 255).astype(np.uint8); img[~m] = 0
im = Image.fromarray(img).convert("RGB"); dr = ImageDraw.Draw(im)
for x in range(int(x0 // 100 + 1) * 100, int(x1), 100):
    X = (x - x0) / s; dr.line([(X, 0), (X, H)], fill=(0, 120, 255)); dr.text((X + 2, 2), str(x), fill=(255, 255, 0))
for z in range(100, int(z1), 100):
    Y = H - 1 - z / s; dr.line([(0, Y), (W, Y)], fill=(0, 120, 255)); dr.text((2, Y + 2), str(z), fill=(255, 255, 0))
im.save(sys.argv[2]); print(im.size)
