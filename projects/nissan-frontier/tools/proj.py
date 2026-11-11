"""Quick orthographic point projections of an STL (no Blender): side (Y-Z), top (Y-X), front (X-Z).
  proj.py in.stl out.png [stl2 ...]   (extra STLs drawn in red over the first, for registration checks)"""
import sys
import numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
S = 0.12  # px per mm


def pts(p):
    return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)


def main():
    out = sys.argv[2]
    sets = [pts(sys.argv[1])] + [pts(p) for p in sys.argv[3:]]
    lo = sets[0].min(0); hi = sets[0].max(0)
    views = [(1, 2), (1, 0), (0, 2)]
    tiles = []
    for a, b in views:
        W = int((hi[a] - lo[a]) * S) + 10; H = int((hi[b] - lo[b]) * S) + 10
        img = np.zeros((H, W, 3), np.float32)
        for k, c in enumerate(sets):
            x = ((c[:, a] - lo[a]) * S).astype(int) + 5; y = H - 1 - (((c[:, b] - lo[b]) * S).astype(int) + 5)
            ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
            col = np.array([1, 1, 1]) if k == 0 else np.array([1, 0.1, 0.05])
            acc = np.zeros((H, W)); np.add.at(acc, (y[ok], x[ok]), 1)
            v = np.clip(acc / (np.percentile(acc[acc > 0], 90) + 1e-6), 0, 1)[..., None]
            img = img * (1 - v * (k > 0)) + v * col * (0.7 if k == 0 else 1)
        tiles.append((np.clip(img, 0, 1) * 255).astype(np.uint8))
    W = max(t.shape[1] for t in tiles)
    canvas = np.zeros((sum(t.shape[0] for t in tiles) + 20, W, 3), np.uint8); y = 0
    for t in tiles:
        canvas[y:y + t.shape[0], :t.shape[1]] = t; y += t.shape[0] + 10
    Image.fromarray(canvas).save(out); print(out, canvas.shape)


main()
