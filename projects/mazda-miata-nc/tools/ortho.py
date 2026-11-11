"""Orthographic point plots (top XY / side XZ / front YZ) of binary STLs in their raw frame, overlaid.
    python projects/mazda-miata-nc/tools/ortho.py out.png a.stl [b.stl ...]
First file grey, the rest red/cyan/lime/orange/magenta. 1 px = 5 mm. Used to check frames and
registration cheaply before Blender."""
import sys
import numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
out, files = sys.argv[1], sys.argv[2:]
cols = [(150, 150, 150), (255, 40, 30), (0, 220, 255), (60, 255, 60), (255, 160, 0), (255, 0, 220)]
pts = []
for f in files:
    m = np.memmap(f, dtype=TRI, offset=84, mode="r")
    pts.append(np.asarray(m["v"][:: max(1, len(m) // 400000)].mean(1)))
allp = np.concatenate(pts); lo, hi = allp.min(0) - 50, allp.max(0) + 50
S = 5.0
panels = []
for i, j in [(0, 1), (0, 2), (1, 2)]:
    W, H = int((hi[i] - lo[i]) / S) + 1, int((hi[j] - lo[j]) / S) + 1
    im = np.zeros((H, W, 3), np.uint8)
    for k, c in enumerate(pts):
        x = ((c[:, i] - lo[i]) / S).astype(int); y = H - 1 - ((c[:, j] - lo[j]) / S).astype(int)
        im[y, x] = cols[k % 6]
    panels.append(Image.fromarray(im))
Wt = sum(p.width for p in panels) + 40; Ht = max(p.height for p in panels)
sheet = Image.new("RGB", (Wt, Ht)); x = 0
for p in panels:
    sheet.paste(p, (x, 0)); x += p.width + 20
sheet.save(out); print(out, "lo", lo.round(), "hi", hi.round())
