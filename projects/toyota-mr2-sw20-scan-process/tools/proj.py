"""Quick orthographic splat views of STL scans (numpy only) - registration checks without Blender.
usage: proj.py out.png base.stl [part.stl ...]  (base grey, parts coloured) [--R R.npy]"""
import sys, numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)
args = [a for a in sys.argv[1:]]
R = None
if "--R" in args:
    i = args.index("--R"); R = np.load(args[i + 1]); del args[i:i + 2]
out, files = args[0], args[1:]
pts = [load(f) for f in files]
if R is not None: pts = [p @ R.T for p in pts]
allp = np.concatenate(pts); lo = np.percentile(allp, 0.1, 0); hi = np.percentile(allp, 99.9, 0)
cols = [(150, 150, 150), (255, 60, 60), (60, 200, 255), (80, 255, 80), (255, 200, 40), (255, 80, 255)]
S = float(__import__("os").environ.get("S", "4"))
views = [(0, 1), (0, 2), (1, 2)]
panels = []
for a, b in views:
    W = int((hi[a] - lo[a]) / S) + 10; H = int((hi[b] - lo[b]) / S) + 10
    img = np.zeros((H, W, 3), np.uint8)
    for k, p in enumerate(pts):
        x = ((p[:, a] - lo[a]) / S).astype(int) + 5; y = H - 1 - (((p[:, b] - lo[b]) / S).astype(int) + 5)
        m = (x >= 0) & (x < W) & (y >= 0) & (y < H)
        img[y[m], x[m]] = cols[k % len(cols)] if k else (110, 110, 110)
    panels.append(Image.fromarray(img))
Wt = sum(p.width for p in panels) + 20; Ht = max(p.height for p in panels)
canvas = Image.new("RGB", (Wt, Ht)); x = 0
for p in panels: canvas.paste(p, (x, 0)); x += p.width + 10
canvas.save(out); print(out, canvas.size)
