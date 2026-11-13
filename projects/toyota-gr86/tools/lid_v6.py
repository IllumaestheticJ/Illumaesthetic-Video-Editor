"""Trunk lid cut on the REAL opening (user v5 note: "Rear trunk area is not cut correctly based on real trunk opening").
v4's lid_v4 was a smoothed top/rear SILHOUETTE: its outline was not the scan's opening, so the base kept car-skin strips
and saw-tooth edges between the lid's outline and the Trunk Open capture (deck edge at the glass, lamp tops, a stray
panel in the cargo opening).
Here the lid is exactly the car4 triangles the open-trunk captures do NOT have: inside the trunk zone, a car4 tri is lid when
neither Trunk Open nor Trunk Open Bumper Off (which fills Trunk Open's missing lamp tops) has surface within --gap mm.
The per-triangle label is then smoothed on the surface (majority of car tris within --r mm, a few passes) so the edge
follows the real gap instead of triangle speckle, made symmetric (a coverage hole on one side is not lid), and only the main\nbody (25 mm voxel connectivity) is kept.
The base around it (tools/build_v6.py) then shows Trunk Open as captured, so lid outline == opening outline.
  lid_v6.py out.stl [--gap 8 --r 20 --passes 4] [--check prefix]"""
import argparse, struct
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = "/home/user/media/work/gr86/"
ap = argparse.ArgumentParser(); ap.add_argument("out")
ap.add_argument("--gap", type=float, default=8.0); ap.add_argument("--r", type=float, default=20.0)
ap.add_argument("--passes", type=int, default=4); ap.add_argument("--check")
a = ap.parse_args()
L = lambda f: np.fromfile(M + f, dtype=TRI, offset=84)
car = L("clean/car4.stl"); cc = car["v"].mean(1).astype(float)
# trunk zone: behind the rear-glass shut-line gap (the black arc in the scan), above the bumper, inside the body
arc = 1480 - 0.00034 * cc[:, 0] ** 2
zone = (cc[:, 1] > arc) & (cc[:, 1] < 2010) & (cc[:, 2] > 600) & (np.abs(cc[:, 0] - 9) < 760)
zi = np.where(zone)[0]; zc = cc[zi]
d = np.full(len(zi), np.inf)
for s in ("clean/Trunk_Open.stl", "clean/Trunk_Open_Bumper_Off.stl"):
    dd, _ = cKDTree(L(s)["v"].mean(1)).query(zc, distance_upper_bound=60, workers=-1); d = np.minimum(d, dd)
lab = (d > a.gap).astype(float)
raw = lab.copy()
nb = cKDTree(zc).query_ball_point(zc, a.r, workers=-1)
for _ in range(a.passes):
    lab = np.array([lab[n].mean() for n in nb]) > 0.5
    lab = lab.astype(float)
lab = lab > 0.5
# symmetric: the right side's open-trunk captures have a coverage hole at the C-pillar base / right lamp top, which read as
# "lid" (a wedge forward along the pillar). The lid is symmetric about the centreline (x = +9 mm, car4 bbox centre), so a tri
# on the right half takes the label at its mirror point on the left (nearest zone tri, within 40 mm).
mir = zc.copy(); mir[:, 0] = 18.0 - mir[:, 0]
dm, jm = cKDTree(zc).query(mir, distance_upper_bound=40, workers=-1)   # 15 mm left notches: the car is not exactly symmetric
ok = np.isfinite(dm); jm[~ok] = 0
lab = np.where(zc[:, 0] < 9.0, lab, ok & lab[jm])   # right half = mirror of the clean left half (AND of both sides
# was too strict: each side has small holes in different places, it shrank the rear face to +-300 mm vs the real +-500 mm)
# main body only
vox = np.floor(zc[lab] / 25).astype(int); o = vox.min(0) - 1
g = np.zeros(tuple(vox.max(0) - o + 2), bool); g[tuple((vox - o).T)] = True
cl, n = ndimage.label(g, np.ones((3, 3, 3))); sizes = ndimage.sum(g, cl, range(1, n + 1))
main = cl[tuple((vox - o).T)] == 1 + int(np.argmax(sizes))
idx = zi[np.where(lab)[0][main]]
mask = np.zeros(len(car), bool); mask[idx] = True
c = cc[mask]
print(f"zone {len(zi)} tris: raw lid {int(raw.sum())} -> smoothed {int(lab.sum())} -> main body {int(mask.sum())}"
      f"  bbox {c.min(0).round()} .. {c.max(0).round()}")
with open(M + a.out, "wb") as f:
    f.write(b"gr86 lid_v6 (complement of the Trunk Open captures)".ljust(80)); f.write(struct.pack("<I", int(mask.sum()))); car[mask].tofile(f)
np.save(M + a.out.replace(".stl", "_mask.npy"), mask)
if a.check:
    from PIL import Image
    to = np.concatenate([L(s)["v"].mean(1) for s in ("clean/Trunk_Open.stl",)])
    R = 2.5
    for name, (U, V, D, v0, v1) in {"top": (lambda P: P[:, 0], lambda P: P[:, 1], lambda P: P[:, 2], 1100, 2100),
                                    "rear": (lambda P: -P[:, 0], lambda P: -P[:, 2], lambda P: P[:, 1], -1150, -450)}.items():
        W = int(2000 / R); H = int((v1 - v0) / R); img = np.zeros((H, W, 3), np.uint8); zb = np.full((H, W), -1e9)
        sel = lambda P: P[(P[:, 1] > 1100) & (P[:, 2] > 450)]
        for P, col in ((sel(cc[~mask]), (95, 95, 95)), (c, (255, 60, 40))):
            u, v, dd = U(P), V(P), D(P); iu = ((u + 1000) / R).astype(int); iv = ((v - v0) / R).astype(int)
            ok = (iu >= 0) & (iu < W) & (iv >= 0) & (iv < H); oo = np.where(ok)[0][np.argsort(dd[ok])]
            for k in (0, 1):
                yy = np.clip(iv[oo] + k, 0, H - 1); upd = dd[oo] >= zb[yy, iu[oo]]; zb[yy[upd], iu[oo][upd]] = dd[oo][upd]; img[yy[upd], iu[oo][upd]] = col
        Image.fromarray(img).save(f"{a.check}_{name}.png")
