"""Remove every scanned triangle that clips the Ronin CAD grille (v9, user: "do a careful look at the front grille and remove any
section that clips with the new grille").
Levelled mm frame, nose -Y. Depth maps of the CAD grille (upper + lower) over an x-z grid: front face yf, back face yb. The silhouette
is closed/filled; inside its openings yb comes from the nearest CAD cell (bar backs), so a part seen THROUGH an opening survives only if
it is behind the grille. A scan triangle is removed when any of its vertices is inside the (slightly grown) silhouette and in front of
yb + MARGIN - i.e. inside or in front of the grille. Writes <part>_gc.stl + the removed triangles (<part>_gcx.stl) for the check render.
    python grille_clip.py bumper_cut c3_body c7_body_w hood c3_flarefill
"""
import sys
import numpy as np
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = "/home/user/media/nissan-frontier"; CELL, MARGIN, GROW = 3.0, 8.0, 2


def maps():
    v = np.concatenate([np.fromfile(f"{M}/ronin_lev/{n}_Grille_V1.stl", dtype=TRI, offset=84)["v"] for n in ("Upper", "Lower")])
    p = np.concatenate([v.reshape(-1, 3), v.mean(1), (v[:, 0] + v[:, 1]) / 2, (v[:, 1] + v[:, 2]) / 2, (v[:, 0] + v[:, 2]) / 2])
    lo = np.array([p[:, 0].min() - 30, p[:, 2].min() - 30]); ij = ((p[:, [0, 2]] - lo) / CELL).astype(int); sh = ij.max(0) + 12
    yb = np.full(sh, -1e9, np.float32); np.maximum.at(yb, (ij[:, 0], ij[:, 1]), p[:, 1])
    has = yb > -1e8
    sil = ndimage.binary_fill_holes(ndimage.binary_closing(has, iterations=4))
    idx = ndimage.distance_transform_edt(~has, return_distances=False, return_indices=True)
    ybf = yb[idx[0], idx[1]]                            # openings / grown rim: back depth of the nearest CAD cell
    ybf = ndimage.maximum_filter(ybf, size=3)
    sil = ndimage.binary_dilation(sil, iterations=GROW)
    return lo, sil, ybf


def main():
    lo, sil, ybf = maps(); print("silhouette cells", int(sil.sum()))
    for name in sys.argv[1:]:
        d = np.fromfile(f"{M}/parts/{name}.stl", dtype=TRI, offset=84); v = d["v"]
        ij = ((v[..., [0, 2]] - lo) / CELL).astype(int)
        ok = (ij[..., 0] >= 0) & (ij[..., 0] < sil.shape[0]) & (ij[..., 1] >= 0) & (ij[..., 1] < sil.shape[1])
        i0 = np.clip(ij[..., 0], 0, sil.shape[0] - 1); i1 = np.clip(ij[..., 1], 0, sil.shape[1] - 1)
        hit = (ok & sil[i0, i1] & (v[..., 1] < ybf[i0, i1] + MARGIN)).any(1)
        for suf, s in (("_gc", d[~hit]), ("_gcx", d[hit])):
            with open(f"{M}/parts/{name}{suf}.stl", "wb") as f:
                f.write(b"\0" * 80); f.write(np.uint32(len(s)).tobytes()); s.tofile(f)
        c = v[hit].reshape(-1, 3)
        print(name, "tris", len(d), "removed", int(hit.sum()), "bbox of removed", (c.min(0).round(0).tolist(), c.max(0).round(0).tolist()) if len(c) else None)


main()
