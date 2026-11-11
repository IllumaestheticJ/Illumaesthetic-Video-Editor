"""align_check.py aligned_mm.stl glb.npz out.png : side/top/front point overlays (scan grey, model red)."""
import sys, numpy as np
from PIL import Image
f = open(sys.argv[1], 'rb'); f.seek(80); n = np.frombuffer(f.read(4), np.uint32)[0]
S = np.fromfile(f, np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]), count=n)['v'].reshape(-1, 3) / 1000
G = np.load(sys.argv[2])['v']; rng = np.random.default_rng(0)
S = S[rng.choice(len(S), min(400000, len(S)), replace=False)]; G = G[rng.choice(len(G), min(300000, len(G)), replace=False)]
views = [(1, 2), (1, 0), (0, 2)]; px = 150; tiles = []
for a, b in views:
    lo = np.minimum(S[:, [a, b]].min(0), G[:, [a, b]].min(0)); hi = np.maximum(np.percentile(S[:, [a, b]], 99.9, 0), G[:, [a, b]].max(0))
    W, H = (np.ceil((hi - lo) * px) + 4).astype(int); im = np.zeros((H, W, 3), np.uint8)
    for P, col in [(S, (170, 170, 170)), (G, (255, 40, 40))]:
        u = ((P[:, a] - lo[0]) * px).astype(int); v = (H - 3 - (P[:, b] - lo[1]) * px).astype(int); ok = (u >= 0) & (u < W) & (v >= 0) & (v < H)
        im[v[ok], u[ok]] = col
    tiles.append(Image.fromarray(im))
Wt = max(t.width for t in tiles); out = Image.new('RGB', (Wt, sum(t.height for t in tiles) + 20)); y = 0
for t in tiles: out.paste(t, (0, y)); y += t.height + 10
out.thumbnail((1400, 1400)); out.save(sys.argv[3])
