"""Trunk lid cut along its real shut lines (user v3 feedback: "the rear trunk needs to be cut correctly").
Neither 'Trunk Open' capture holds the propped lid, but both show the body around the opening, so the car4 triangles they
lack (> --gap mm from both) mark where the lid was. That mask is speckled (scan holes, the open lid's shadow) and v3's
blob version (lid_mask.py) spilled onto the tail lamps and the bumper. Here it only *votes* a silhouette:
  top view  (x, y), top-most surface per 10 mm cell   -> per-y-row interval [xl, xr]
  rear view (x, z), rear-most surface per 10 mm cell  -> per-z-row interval [xl, xr]
each row an interval median-smoothed over rows and made symmetric about the centreline, so the outline is one clean curve (no notches, no islands).
lid = car tris inside BOTH silhouettes, on the visible top or rear surface, behind the glass shut-line arc
(y > 1480 - 0.00034 x^2 + 4, the black gap in the scan), z > 600.
  lid_v4.py car4.stl Trunk_Open.stl Trunk_Open_Bumper_Off.stl out.stl [--check prefix]"""
import argparse, struct
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("s1"); ap.add_argument("s2"); ap.add_argument("out")
ap.add_argument("--gap", type=float, default=6.0); ap.add_argument("--cell", type=float, default=10.0)
ap.add_argument("--check")
a = ap.parse_args()
L = lambda f: np.fromfile(f, dtype=TRI, offset=84)
car = L(a.car); cc = car["v"].mean(1).astype(float)
reg = (cc[:, 1] > 1250) & (cc[:, 2] > 560)
d = np.full(len(cc), np.inf)
for s in (a.s1, a.s2):
    dd, _ = cKDTree(L(s)["v"].mean(1)).query(cc[reg], distance_upper_bound=60)
    d[reg] = np.where(np.isfinite(d[reg]), np.minimum(d[reg], dd), dd)
arc = 1480 - 0.00034 * cc[:, 0] ** 2 + 4
cand = reg & (d > a.gap) & (cc[:, 1] > arc)
G = a.cell


def silhouette(u, v, depth, name, v_lo, v_hi):
    """Cells over (u = x, v); surface = tris within 20 mm of the cell's max depth. Returns (in_mask per tri, surface per tri)."""
    u0 = -1000.0
    iu = ((u - u0) / G).astype(int); iv = ((v - v_lo) / G).astype(int)
    W = int(2000 / G); H = int((v_hi - v_lo) / G) + 1
    ok = reg & (iu >= 0) & (iu < W) & (iv >= 0) & (iv < H)
    key = iv * W + iu
    top = np.full(H * W, -np.inf); np.maximum.at(top, key[ok], depth[ok])
    surf = ok & (depth > top[np.clip(key, 0, H * W - 1)] - 20)
    n_all = np.bincount(key[surf], minlength=H * W); n_c = np.bincount(key[surf & cand], minlength=H * W)
    m = (n_c > 0.5 * np.maximum(n_all, 1)) & (n_all > 0)
    m = m.reshape(H, W)
    m = ndimage.binary_closing(m, np.ones((3, 3)), iterations=2)
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lab, range(1, n + 1)); m = lab == (1 + int(np.argmax(sizes)))
    # one interval per row, smoothed over rows
    xl = np.full(H, np.nan); xr = np.full(H, np.nan)
    for r in range(H):
        cols = np.where(m[r])[0]
        if len(cols) > 2:
            xl[r], xr[r] = cols.min(), cols.max()
    have = np.isfinite(xl)
    xl_s = xl.copy(); xr_s = xr.copy()
    if have.sum() > 5:
        xl_s[have] = ndimage.median_filter(xl[have], 7, mode="nearest"); xr_s[have] = ndimage.median_filter(xr[have], 7, mode="nearest")
    # the lid is symmetric: clamp each row to the narrower half-width about the centreline (x = +9 mm, car4 bbox centre),
    # so a scan hole on one side can't let the other side spill onto the C-pillar / lamp
    cx = (9.0 - u0) / G
    hw = np.minimum(xr_s - cx, cx - xl_s); xl_s, xr_s = cx - hw, cx + hw
    rows = np.clip(iv, 0, H - 1)
    inside = ok & have[rows] & (iu >= np.nan_to_num(xl_s[rows], nan=1e9)) & (iu <= np.nan_to_num(xr_s[rows], nan=-1e9))
    print(f"{name}: rows {int(have.sum())}, cells {int(m.sum())}")
    return inside, surf, (m, xl_s, xr_s, v_lo)


in_top, surf_top, T = silhouette(cc[:, 0], cc[:, 1], cc[:, 2], "top", 1250, 2100)
in_rear, surf_rear, Rr = silhouette(cc[:, 0], -cc[:, 2], cc[:, 1], "rear", -1100, -560)
lid = in_top & in_rear & (surf_top | surf_rear) & (cc[:, 1] > arc) & (cc[:, 2] > 600)
# drop stray islands: keep tris within 25 mm of the main lid body (connected through a coarse voxel grid)
vox = np.floor(cc[lid] / 25).astype(int); vk = {tuple(v) for v in vox}
grid = np.zeros(tuple(vox.max(0) - vox.min(0) + 3), bool); grid[tuple((vox - vox.min(0) + 1).T)] = True
lab, n = ndimage.label(grid, np.ones((3, 3, 3)))
sizes = ndimage.sum(grid, lab, range(1, n + 1)); big = 1 + int(np.argmax(sizes))
keep_l = lab[tuple((vox - vox.min(0) + 1).T)] == big
idx = np.where(lid)[0]; lid[idx[~keep_l]] = False
c = cc[lid]
print(f"lid tris {int(lid.sum())}  bbox {c.min(0).round()} .. {c.max(0).round()}  (islands dropped {int((~keep_l).sum())})")
with open(a.out, "wb") as f:
    f.write(b"gr86 lid_v4 (shut-line silhouettes)".ljust(80)); f.write(struct.pack("<I", int(lid.sum()))); car[lid].tofile(f)
np.save(a.out.replace(".stl", "_mask.npy"), lid)
if a.check:
    from PIL import Image
    for name, (U, V, D, v0, v1) in {"top": (cc[:, 0], cc[:, 1], cc[:, 2], 1150, 2100),
                                    "rear": (cc[:, 0], -cc[:, 2], cc[:, 1], -1100, -400)}.items():
        R = 2.0; W = int(2000 / R); H = int((v1 - v0) / R)
        sel = (cc[:, 1] > 1100) & (cc[:, 2] > 400)
        iu = ((U - -1000) / R).astype(int); iv = ((V - v0) / R).astype(int)
        ok = sel & (iu >= 0) & (iu < W) & (iv >= 0) & (iv < H)
        o = np.where(ok)[0][np.argsort(D[ok])]
        img = np.zeros((H, W, 3), np.uint8)
        colr = np.where(lid[o, None], np.array([[255, 60, 40]]), np.array([[130, 130, 130]]))
        img[iv[o], iu[o]] = colr
        if name == "rear": img = img[:, ::-1]   # as seen from behind
        Image.fromarray(img).save(f"{a.check}_{name}.png")
