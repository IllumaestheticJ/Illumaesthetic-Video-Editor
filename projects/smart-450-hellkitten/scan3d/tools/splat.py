"""Orthographic depth splats of an STL (3 views: along each axis). splat.py in.stl out.png [mm_per_px]"""
import sys, numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
d = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
c = d["v"].mean(1); n = d["n"]
s = float(sys.argv[3]) if len(sys.argv) > 3 else 6
lo, hi = c.min(0), c.max(0)
ims = []
for ax, (u, v) in [(2, (0, 1)), (1, (0, 2)), (0, (1, 2))]:
    W = int((hi[u]-lo[u])/s)+1; H = int((hi[v]-lo[v])/s)+1
    iu = ((c[:, u]-lo[u])/s).astype(int); iv = (H-1-((c[:, v]-lo[v])/s)).astype(int)
    z = c[:, ax]
    img = np.full((H, W), -1e9)
    np.maximum.at(img, (iv, iu), z)
    sh = np.zeros((H, W)); 
    m = img > -1e9
    zz = (img - lo[ax])/(hi[ax]-lo[ax]+1e-9)
    out = np.where(m, 40+215*zz, 0).astype(np.uint8)
    ims.append(Image.fromarray(out).convert("RGB"))
Wt = sum(i.width for i in ims)+20; Ht = max(i.height for i in ims)
canvas = Image.new("RGB", (Wt, Ht), (60, 0, 0)); x = 0
for i in ims: canvas.paste(i, (x, 0)); x += i.width + 10
canvas.save(sys.argv[2]); print(sys.argv[2], canvas.size, "bbox", lo.round(), hi.round(), "tris", len(d))
