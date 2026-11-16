"""Fins for a CAD intercooler core (user: "add fins in" - the CSF STEP core is a smooth slab).
On each flat core face (plane y = y0, x/z extents, outward direction): flat horizontal tubes (--pitch, --tube tall,
--proud mm proud) and between them a corrugated fin row (vertical crests every --fin mm, 0.2..--depth mm proud).
    icfins.py ic.stl out.stl   (faces are listed in FACES below, raw car mm)"""
import argparse, struct
import numpy as np
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
# (y0, outward sign along y, x0, x1, z0, z1) - measured from csf_ic.stl (front plane y -2982; back planes -2852 / -2886)
FACES = [(-2982, -1, -552, 101, -403, -209), (-2852, 1, -550, 99, -353, -212), (-2886, 1, -594, 142, -400, -338)]
ap = argparse.ArgumentParser(); ap.add_argument("ic"); ap.add_argument("out")
ap.add_argument("--pitch", type=float, default=11); ap.add_argument("--tube", type=float, default=4)
ap.add_argument("--proud", type=float, default=2.5); ap.add_argument("--fin", type=float, default=3.5); ap.add_argument("--depth", type=float, default=1.6)
a = ap.parse_args()
tris = []
def quad(p0, p1, p2, p3): tris.extend([(p0, p1, p2), (p0, p2, p3)])
for y0, s, x0, x1, z0, z1 in FACES:
    x0, x1, z0, z1 = x0 + 3, x1 - 3, z0 + 2, z1 - 2
    zt = np.arange(z0 + a.pitch / 2, z1, a.pitch)
    yt = y0 + s * a.proud
    for zc in zt:                                   # tube: front face + top + bottom
        lo, hi = zc - a.tube / 2, zc + a.tube / 2
        quad((x0, yt, lo), (x1, yt, lo), (x1, yt, hi), (x0, yt, hi))
        quad((x0, y0, hi), (x1, y0, hi), (x1, yt, hi), (x0, yt, hi))
        quad((x0, y0, lo), (x0, yt, lo), (x1, yt, lo), (x1, y0, lo))
    edges = np.r_[z0, np.ravel([[zc - a.tube / 2, zc + a.tube / 2] for zc in zt]), z1]
    xs = np.arange(x0, x1 + 1e-6, a.fin / 2)
    yy = np.where(np.arange(len(xs)) % 2 == 0, y0 + s * 0.2, y0 + s * a.depth)
    for g0, g1 in zip(edges[0::2], edges[1::2]):     # fin rows in the gaps between tubes
        if g1 - g0 < 1: continue
        for i in range(len(xs) - 1):
            quad((xs[i], yy[i], g0), (xs[i + 1], yy[i + 1], g0), (xs[i + 1], yy[i + 1], g1), (xs[i], yy[i], g1))
t = np.array(tris, np.float32); m = np.zeros(len(t), DT); m["v"] = t
nn = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]); m["n"] = nn / np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-9)
base = np.fromfile(a.ic, dtype=DT, offset=84); out = np.concatenate([base, m])
with open(a.out, "wb") as f: f.write(b"CSF IC + modelled fins".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
print("fin/tube triangles", len(m), "| total", len(out))
