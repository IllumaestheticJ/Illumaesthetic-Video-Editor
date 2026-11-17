"""v1: split a GLB-frame scan into panel zones by FOOTPRINT (replaces the v0 3D-radius cut, which left ragged margins).

A scan triangle belongs to a zone when its centroid projects onto the zone's reference surface: nearest surface sample
within `depth` mm along that sample's normal and within `lat` mm sideways, so the cut edge follows the panel's own outline
(the lookbook's stock piece = the shut line) instead of a blurred radius. Zones never take wheel/tyre triangles.

    python cutparts.py scan.stl keep.stl wheels.stl[,..] zone_out.stl:depth:lat:a.stl,b.stl[:ymax] ...
"""
import sys

import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl, write_stl  # noqa: E402

STEP = 0.003


def samples(paths):
    P, N = [], []
    rng = np.random.default_rng(0)
    for p in paths:
        T = read_stl(p)
        n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); a = np.linalg.norm(n, axis=1); ok = a > 1e-12
        T, n, a = T[ok], n[ok] / a[ok, None], a[ok] / 2
        k = np.maximum(1, np.ceil(a / (STEP * STEP)).astype(int)); k = np.minimum(k, 4000)
        idx = np.repeat(np.arange(len(T)), k)
        r = rng.random((len(idx), 2)); m = r.sum(1) > 1; r[m] = 1 - r[m]
        P.append(T[idx, 0] + r[:, :1] * (T[idx, 1] - T[idx, 0]) + r[:, 1:] * (T[idx, 2] - T[idx, 0])); N.append(n[idx])
        P.append(T.reshape(-1, 3)); N.append(np.repeat(n, 3, 0))
    return np.concatenate(P), np.concatenate(N)


def main():
    scan, keep_p, wheels = sys.argv[1], sys.argv[2], sys.argv[3]
    T = read_stl(scan); C = T.mean(1)
    wheel = np.zeros(len(T), bool)           # wheel = a cylinder round each lookbook wheel (scan wheels differ in design)
    for w in wheels.split(","):
        W = read_stl(w).reshape(-1, 3); lo, hi = W.min(0), W.max(0)
        cy, cz, rad = (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2, (hi[2] - lo[2]) / 2 + 0.02
        wheel |= (C[:, 0] > lo[0] - 0.04) & (C[:, 0] < hi[0] + 0.04) & (np.hypot(C[:, 1] - cy, C[:, 2] - cz) < rad)
    taken = np.zeros(len(T), bool)
    for z in sys.argv[4:]:
        f = z.split(":")
        if f[1] == "idx":                       # zone precomputed from a removed-state scan (triangle indices of this scan)
            sel = np.load(f[2]); sel = sel[~taken[sel] & ~wheel[sel]]; taken[sel] = True
            write_stl(f[0], T[sel]); print(f[0].rsplit("/", 1)[1], len(sel), "tris (state)"); continue
        out, lat, srcs = f[0], float(f[2]) / 1000, f[3].split(",")
        dd = [float(x) / 1000 for x in f[1].split("/")]; depth = max(dd); d_in, d_out = (dd[0], dd[-1])   # "25" or "in/out" (signed by the normal)
        P, N = samples(srcs)
        lo, hi = P.min(0) - lat, P.max(0) + lat
        cand = np.where(((C >= lo - depth) & (C <= hi + depth)).all(1) & ~taken & ~wheel)[0]
        tree = cKDTree(P)
        d, j = tree.query(C[cand], k=8, distance_upper_bound=depth + lat)
        m = np.zeros(len(cand), bool)
        for kk in range(8):
            ok = np.isfinite(d[:, kk]); jj = np.where(ok, j[:, kk], 0)
            v = C[cand] - P[jj]; sn = (v * N[jj]).sum(1); dl = np.sqrt(np.maximum((v * v).sum(1) - sn * sn, 0))
            m |= ok & (sn >= -d_in) & (sn <= d_out) & (dl <= lat)
        sel = cand[m]
        # a triangle whose 3 vertices all project is inside; boundary triangles follow their centroid (already tested)
        taken[sel] = True
        write_stl(out, T[sel]); print(out.rsplit("/", 1)[1], len(sel), "tris")
    write_stl(keep_p, T[~taken]); print(keep_p.rsplit("/", 1)[1], int((~taken).sum()), "tris")


main()
