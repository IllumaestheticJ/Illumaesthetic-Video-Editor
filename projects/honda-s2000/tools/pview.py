"""Fast orthographic point views of binary STLs (triangle centroids), for identifying scans and eyeballing
registration without Blender. Each file gets a colour; 3 panels: XY (top), XZ, YZ.
    python projects/honda-s2000/tools/pview.py out.png a.stl [b.stl ...] [--n 400000] [--T b:T.json]"""
import sys, json, numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
COL = [(200, 200, 200), (255, 40, 30), (40, 220, 255), (60, 255, 60), (255, 220, 0), (255, 0, 220)]
args = sys.argv[1:]; out = args.pop(0); n = 400000; Ts = {}
if "--n" in args: i = args.index("--n"); n = int(args[i + 1]); del args[i:i + 2]
while "--T" in args:
    i = args.index("--T"); k, p = args[i + 1].split(":", 1); Ts[int(k)] = np.array(json.load(open(p))["T_part_to_car_mm"]); del args[i:i + 2]
pts = []
for j, p in enumerate(args):
    m = np.memmap(p, dtype=TRI, offset=84, mode="r")
    idx = np.sort(np.random.default_rng(0).choice(len(m), min(n, len(m)), replace=False))
    c = np.asarray(m["v"][idx]).mean(1).astype(np.float64)
    if j in Ts: c = c @ Ts[j][:3, :3].T + Ts[j][:3, 3]
    pts.append(c)
allp = np.concatenate(pts); lo, hi = allp.min(0), allp.max(0); S = 500 / (hi - lo).max()
panels = []
for ax in [(0, 1), (0, 2), (1, 2)]:
    w = int((hi[ax[0]] - lo[ax[0]]) * S) + 4; h = int((hi[ax[1]] - lo[ax[1]]) * S) + 4
    img = np.zeros((h, w, 3), np.uint8)
    for j, c in enumerate(pts):
        u = ((c[:, ax[0]] - lo[ax[0]]) * S).astype(int) + 2; v = h - 3 - ((c[:, ax[1]] - lo[ax[1]]) * S).astype(int)
        img[v, u] = COL[j % len(COL)]
    panels.append(Image.fromarray(img))
W = sum(p.width for p in panels) + 20; H = max(p.height for p in panels)
sheet = Image.new("RGB", (W, H), (30, 30, 40)); x = 0
for p in panels: sheet.paste(p, (x, 0)); x += p.width + 10
sheet.save(out); print(out, "lo", lo.round(), "hi", hi.round())
