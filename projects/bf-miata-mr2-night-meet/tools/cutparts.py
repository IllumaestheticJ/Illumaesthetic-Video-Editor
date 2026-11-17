"""v0: split a GLB-frame scan into the piece that comes off (scan within R of a lookbook stock/part surface) and the rest.
Several zones can be cut from one scan; each gets its own cut file, and keep = scan minus all zones.

    python cutparts.py scan_glbframe.stl keep.stl R_mm zone_out.stl:a.stl,b.stl [zone2_out.stl:c.stl ...]
"""
import sys

import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl, write_stl  # noqa: E402


def surf_points(paths, step=0.006):
    pts = []
    for p in paths:
        T = read_stl(p)
        pts.append(T.reshape(-1, 3)); pts.append(T.mean(1))
        # extra samples on big triangles
        e = np.linalg.norm(T[:, 1] - T[:, 0], axis=1) + np.linalg.norm(T[:, 2] - T[:, 0], axis=1)
        big = T[e > 2 * step]
        if len(big):
            r = np.random.default_rng(0).random((len(big), 8, 2)); m = r.sum(2) > 1; r[m] = 1 - r[m]
            pts.append((big[:, None, 0] + r[..., :1] * (big[:, None, 1] - big[:, None, 0]) + r[..., 1:] * (big[:, None, 2] - big[:, None, 0])).reshape(-1, 3))
    return np.concatenate(pts)


def main():
    scan, keep_p, R = sys.argv[1], sys.argv[2], float(sys.argv[3]) / 1000
    T = read_stl(scan); C = T.mean(1)
    taken = np.zeros(len(T), bool)
    for z in sys.argv[4:]:
        out, srcs = z.split(":")
        P = surf_points(srcs.split(","))
        d, _ = cKDTree(P).query(C, distance_upper_bound=R)
        m = np.isfinite(d) & ~taken
        taken |= m
        write_stl(out, T[m]); print(out, int(m.sum()), "tris")
    write_stl(keep_p, T[~taken]); print(keep_p, int((~taken).sum()), "tris")


main()
