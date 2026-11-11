"""Top-down |n.z| map of the RAW full-car scan (levelled), highest surface wins, 2 mm/px - panel seams show as
thin dark lines. px -> mm: x = X0 + 2 px, y = Y0 + 2 (H-1-py).
    seammap.py raw.stl level.json out.png X0 X1 Y0 Y1"""
import json, sys
import numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
raw, lj, out = sys.argv[1:4]; X0, X1, Y0, Y1 = (float(v) for v in sys.argv[4:8])
R = np.array(json.load(open(lj))["T_mm"])[:3, :3]
m = np.memmap(raw, dtype=TRI, offset=84, mode="r")
S = 2.0; W, H = int((X1 - X0) / S), int((Y1 - Y0) / S)
zb = np.full(H * W, -1e9); nb = np.zeros(H * W)
for i in range(0, len(m), 3_000_000):
    v = np.array(m[i:i + 3_000_000])["v"] @ R.T
    c = v.mean(1); n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    ok = (c[:, 0] > X0) & (c[:, 0] < X1) & (c[:, 1] > Y0) & (c[:, 1] < Y1)
    c, n = c[ok], n[ok]
    k = (H - 1 - ((c[:, 1] - Y0) / S).astype(int)) * W + ((c[:, 0] - X0) / S).astype(int)
    o = np.argsort(c[:, 2]); k, z, nz = k[o], c[o, 2], np.abs(n[o, 2])
    better = z > zb[k]
    zb[k[better]] = z[better]; nb[k[better]] = nz[better]
Image.fromarray((np.clip(nb, 0, 1) ** 3 * 255).reshape(H, W).astype(np.uint8)).save(out)
print(out, W, H)
