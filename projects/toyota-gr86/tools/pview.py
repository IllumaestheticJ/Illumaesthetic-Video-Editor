"""Quick orthographic point views of STLs (no Blender): side (Y-Z), top (Y-X), front (X-Z), stacked.
  pview.py out.png a.stl [b.stl ...]   first file grey, others coloured red/cyan/green/yellow on top."""
import sys
import numpy as np
from PIL import Image, ImageDraw
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
COL = [(150, 150, 150), (255, 40, 30), (0, 200, 255), (40, 255, 40), (255, 220, 0)]
files = sys.argv[2:]
pts = [np.fromfile(f, dtype=TRI, offset=84)["v"].mean(1) for f in files]
allp = np.concatenate([p[::20] for p in pts])
lo, hi = np.percentile(allp, 0.1, axis=0) - 50, np.percentile(allp, 99.9, axis=0) + 50
sc = 0.18  # px per mm
views = [(1, 2), (1, 0), (0, 2)]
W = int((hi[1] - lo[1]) * sc) + 1
Hs = [int((hi[j] - lo[j]) * sc) + 1 for _, j in views]
img = Image.new("RGB", (max(W, int((hi[0] - lo[0]) * sc) + 1), sum(Hs) + 20), (0, 0, 0))
y0 = 0
for (i, j), H in zip(views, Hs):
    for k, p in enumerate(pts):
        p = p[:: max(1, len(p) // 400000)]
        u = ((p[:, i] - lo[i]) * sc).astype(int); v = (H - 1 - (p[:, j] - lo[j]) * sc).astype(int)
        ok = (u >= 0) & (u < img.width) & (v >= 0) & (v < H)
        a = np.array(img)
        a[v[ok] + y0, u[ok]] = COL[min(k, len(COL) - 1)]
        img = Image.fromarray(a)
    ImageDraw.Draw(img).line([(0, y0 + H + 5), (img.width, y0 + H + 5)], fill=(60, 60, 60))
    y0 += H + 10
img.save(sys.argv[1]); print(sys.argv[1], lo.round(), hi.round())
