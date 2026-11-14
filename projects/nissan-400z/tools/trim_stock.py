"""Trim the stock car where it pokes through the seated Bomex kit (user 2026-11-14: "the bumper needs to be trimmed to not
clip with the new pieces"). Ray test (thin CAD shells defeat a nearest-normal sign test): a stock triangle near the kit
(< --near mm) is removed if a ray from its centroid INTO the car (along -its normal) hits the kit within --depth mm, i.e. the
stock skin sits outside, or inside the thickness of, a kit shell. Stock surface under a kit part (ray goes into the car,
never meets the kit) is kept.
  python trim_cand.py base.stl cand.npy --parts ... ; blender -b -P trim_stock.py -- base.stl out.stl --cand cand.npy --parts front_bumper canard_driver ... [--near 80] [--depth 90]"""
import argparse, struct, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
argv = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser(); ap.add_argument("base"); ap.add_argument("out"); ap.add_argument("--parts", nargs="+", required=True)
ap.add_argument("--near", type=float, default=80.0); ap.add_argument("--depth", type=float, default=90.0); ap.add_argument("--removed", default=None); ap.add_argument("--cand", required=True)  # .npy of candidate tri indices (trim_cand.py)
a = ap.parse_args(argv)
K = "/home/user/media/nissan-400z/kit/lev"
m = np.fromfile(a.base, dtype=TRI, offset=84); v = m["v"].astype(np.float64)
c = v.mean(1); n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); L = np.linalg.norm(n, axis=1); n = n / np.maximum(L, 1e-12)[:, None]
kv = np.concatenate([np.fromfile(f"{K}/{p}.stl", dtype=TRI, offset=84)["v"] for p in a.parts]).astype(np.float64)
verts = kv.reshape(-1, 3); polys = np.arange(len(verts)).reshape(-1, 3)
bvh = BVHTree.FromPolygons([Vector(p) for p in verts], polys.tolist(), all_triangles=True)
cand = np.load(a.cand)
print("candidates", len(cand), flush=True)
rm = np.zeros(len(c), bool)
for k, j in enumerate(cand):
    o = Vector(c[j]); dirn = Vector(-n[j])
    hit = bvh.ray_cast(o, dirn, a.depth)
    if hit[0] is not None:
        rm[j] = True
    if k % 500000 == 0: print(k, flush=True)
print(a.base.split("/")[-1], "->", a.out.split("/")[-1], "removed", int(rm.sum()), "of", len(m), flush=True)
for path, sel in ((a.out, ~rm), (a.removed, rm)):
    if not path: continue
    with open(path, "wb") as f:
        k = m[sel]; f.write(b"400z stock trimmed to kit".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
