"""Remove scanned-ground scraps from the C5 car scan (reviewer 2026-11-11: "delete/hide the artifacts").
Drops near-horizontal facets (|n_z| > NZ) below ZMAX mm (ground caught around the tyres / under the sills; the cameras never
look under the car) and then every connected component smaller than MIN tris (fringes left hanging).
  carclean.py in.stl out.stl [--zmax 100 --nz 0.7 --min 3000] [--wheels -1495,1160]"""
import argparse, struct, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from composite2 import components, L
ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--zmax", type=float, default=100); ap.add_argument("--nz", type=float, default=0.7); ap.add_argument("--min", type=int, default=3000)
ap.add_argument("--wheels", default="", help="y centres (mm) of the axles, e.g. -1495,1160: below --zmax keep only tris inside a tyre circle")
ap.add_argument("--r", type=float, default=345); ap.add_argument("--xin", type=float, default=560); ap.add_argument("--xout", type=float, default=985)
a = ap.parse_args()
t = L(a.inp); v = t["v"].astype(np.float64)
n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
c = v.mean(1)
keep = ~((c[:, 2] < a.zmax) & (np.abs(n[:, 2]) > a.nz))
if a.wheels:
    low = c[:, 2] < a.zmax
    tyre = np.zeros(len(c), bool)
    for yc in [float(v) for v in a.wheels.split(",")]:
        tyre |= ((c[:, 1] - yc) ** 2 + (c[:, 2] - a.r) ** 2 < (a.r + 25) ** 2) & (np.abs(c[:, 0]) > a.xin) & (np.abs(c[:, 0]) < a.xout)
    keep &= ~(low & ~tyre)
k = t[keep]; lab = components(k); cnt = np.bincount(lab); k = k[cnt[lab] >= a.min]
print(f"{len(t)} -> {int(keep.sum())} (low flat dropped) -> {len(k)} (islands < {a.min} dropped)")
with open(a.out, "wb") as f:
    f.write(b"ive c5 carclean".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
