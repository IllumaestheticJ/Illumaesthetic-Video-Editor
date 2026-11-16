"""Fins for the Jackson Racing intercooler CAD (core_7.6.23.stp, user-supplied; its core is a smooth shell - user on v9:
"add fins in"). Like icfins.py, but the core faces are not axis-aligned: each is the plane y = a + B*x (yaw ~0.7 deg)
and its z edges rise R mm per mm of x (roll ~0.4 deg) - measured from jr_core_raw.stl (fit residual < 0.01 mm).
The core is stepped: a lower block (z -380..-234 at x -542) and a thinner upper block (-234..-127).
    icfins2.py jr_core_raw.stl out.stl"""
import argparse, struct
import numpy as np
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
B, R, XREF = -0.01228, 0.0066, -541.9
# (a, outward sign along y, z0, z1 at x = XREF)
FACES = [(-2989.30, -1, -379.8, -234.2), (-2960.18, -1, -234.2, -126.6),
         (-2912.76, 1, -234.2, -126.6), (-2889.76, 1, -379.8, -234.2)]
X0, X1 = -537.0, 78.0          # between the end tanks
ap = argparse.ArgumentParser(); ap.add_argument("ic"); ap.add_argument("out")
ap.add_argument("--pitch", type=float, default=11); ap.add_argument("--tube", type=float, default=4)
ap.add_argument("--proud", type=float, default=2.5); ap.add_argument("--fin", type=float, default=3.5); ap.add_argument("--depth", type=float, default=1.6)
a = ap.parse_args()
tris = []
def quad(p0, p1, p2, p3): tris.extend([(p0, p1, p2), (p0, p2, p3)])
def P(fa, s, x, z, off):        # point on face at x, local height z (at XREF), `off` mm proud
    return (x, fa + B * x + s * off, z + R * (x - XREF))
for fa, s, z0, z1 in FACES:
    z0, z1 = z0 + 2, z1 - 2
    zt = np.arange(z0 + a.pitch / 2, z1, a.pitch)
    for zc in zt:
        lo, hi = zc - a.tube / 2, zc + a.tube / 2
        quad(P(fa, s, X0, lo, a.proud), P(fa, s, X1, lo, a.proud), P(fa, s, X1, hi, a.proud), P(fa, s, X0, hi, a.proud))
        quad(P(fa, s, X0, hi, 0), P(fa, s, X1, hi, 0), P(fa, s, X1, hi, a.proud), P(fa, s, X0, hi, a.proud))
        quad(P(fa, s, X0, lo, 0), P(fa, s, X0, lo, a.proud), P(fa, s, X1, lo, a.proud), P(fa, s, X1, lo, 0))
    edges = np.r_[z0, np.ravel([[zc - a.tube / 2, zc + a.tube / 2] for zc in zt]), z1]
    xs = np.arange(X0, X1 + 1e-6, a.fin / 2)
    dd = np.where(np.arange(len(xs)) % 2 == 0, 0.2, a.depth)
    for g0, g1 in zip(edges[0::2], edges[1::2]):
        if g1 - g0 < 1: continue
        for i in range(len(xs) - 1):
            quad(P(fa, s, xs[i], g0, dd[i]), P(fa, s, xs[i + 1], g0, dd[i + 1]),
                 P(fa, s, xs[i + 1], g1, dd[i + 1]), P(fa, s, xs[i], g1, dd[i]))
t = np.array(tris, np.float32); m = np.zeros(len(t), DT); m["v"] = t
nn = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]); m["n"] = nn / np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-9)
base = np.fromfile(a.ic, dtype=DT, offset=84); out = np.concatenate([base, m])
with open(a.out, "wb") as f: f.write(b"JR IC + modelled fins".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
print("fin/tube triangles", len(m), "| total", len(out))
