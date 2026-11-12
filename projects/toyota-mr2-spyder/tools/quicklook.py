"""Fast numpy look at levelled STLs (car frame, mm): orthographic depth-shaded views, no Blender.
    quicklook.py out.png view[,view..] a.stl [b.stl ...]     views: front rear top bottom left right
Each STL gets one row; shading = normal . light, nearest surface wins (4 mm pixels)."""
import sys, numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
out, views, files = sys.argv[1], sys.argv[2].split(","), sys.argv[3:]
AX = {"front": (0, 2, 1, +1, -1), "rear": (0, 2, 1, -1, +1), "top": (0, 1, 2, +1, +1), "bottom": (0, 1, 2, -1, -1),
      "left": (1, 2, 0, -1, +1), "right": (1, 2, 0, +1, -1)}   # (u axis, v axis, depth axis, depth sign toward viewer, u flip)
PX = 4.0; rows = []
for f in files:
    m = np.fromfile(f, dtype=TRI, offset=84); c = m["v"].mean(1)
    v = m["v"]; n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
    tiles = []
    for vw in views:
        ua, va, da, ds, uf = AX[vw]
        u = c[:, ua] * uf; w = c[:, va]; d = c[:, da] * ds
        W, H = (1000, 1100) if vw in ("top", "bottom") else ((1100, 420) if vw in ("left", "right") else (520, 420))
        x = ((u - (-W * PX / 2)) / PX).astype(int)
        y0 = -H * PX / 2 if vw in ("top", "bottom") else -100
        y = H - 1 - ((w - y0) / PX).astype(int)
        ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
        o = np.argsort(d[ok]); xi, yi = x[ok][o], y[ok][o]
        L = np.array([0.3, 0.4, 0.85]); view_dir = np.zeros(3); view_dir[da] = ds
        sh = np.abs(n[ok][o] @ (0.6 * view_dir + 0.4 * L / np.linalg.norm(L)))
        img = np.zeros((H, W), np.float32); img[yi, xi] = 0.15 + 0.85 * sh      # later (nearer) overwrite
        tiles.append(img)
    Hm = max(t.shape[0] for t in tiles)
    rows.append(np.hstack([np.pad(t, ((0, Hm - t.shape[0]), (0, 8))) for t in tiles]))
Wm = max(r.shape[1] for r in rows)
Image.fromarray((np.vstack([np.pad(r, ((0, 8), (0, Wm - r.shape[1]))) for r in rows]) * 255).astype(np.uint8)).save(out)
