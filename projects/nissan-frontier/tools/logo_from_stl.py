"""Flat logo PNG (white on transparent) from a 3D logo STL: orthographic fill of every triangle onto the logo's face plane.
Used for the MotoIQ wordmark ('Nismo QX80 motoiq logo.stl', engineering drive) - the .ai in the user's own Drive is not readable here.
    python logo_from_stl.py in.stl out.png [width_px]"""
import sys
import numpy as np
from PIL import Image, ImageDraw
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
v = np.fromfile(sys.argv[1], dtype=TRI, offset=84)["v"].astype(np.float64); W = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
c = v.reshape(-1, 3); mu = c.mean(0); w, V = np.linalg.eigh(np.cov((c - mu).T)); V = V[:, ::-1]
q = (v - mu) @ V
n = np.cross(q[:, 1] - q[:, 0], q[:, 2] - q[:, 0]); front = n[:, 2] > 0
if front.sum() < (~front).sum(): q[..., 0] *= -1                 # look at the face that reads left-to-right
lo = q[..., :2].reshape(-1, 2).min(0); hi = q[..., :2].reshape(-1, 2).max(0); S = 2 * W / (hi[0] - lo[0])
H = int((hi[1] - lo[1]) * S) + 4; im = Image.new("L", (2 * W + 4, H), 0); d = ImageDraw.Draw(im)
for t in q:
    d.polygon([((p[0] - lo[0]) * S + 2, H - 2 - (p[1] - lo[1]) * S) for p in t], fill=255)
im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
out = Image.new("RGBA", im.size, (255, 255, 255, 0)); out.putalpha(im); out.save(sys.argv[2]); print(out.size)
