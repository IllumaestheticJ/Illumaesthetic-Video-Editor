"""v7 (user on v6: "there are still bits of the rear trunk left behind"): two kinds of bits stayed on the base -
(1) the lid's front lip: the zone started at a FITTED arc (1480 - 0.00034 x^2) that sat ~40 mm behind the real shut-line gap;
    now the gap is traced from car4 itself (per 20 mm x slice, the widest y-gap in the deck surface between the glass and the lid);
(2) right-side gutter/wing strips the open captures lack but the mirrored lid excluded: everything in the zone the captures lack
    and that is not lid now goes into a DROP mask (removed from the base, not moved): parts/<out>_drop.npy.
v6 notes: Trunk lid cut on the REAL opening (user v5 note: "Rear trunk area is not cut correctly based on real trunk opening").
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
# shut-line gap traced from car4: per 20 mm x slice, deck points (z > 850) with y in 1330..1600, widest gap along y
from scipy.ndimage import median_filter
deck = cc[(cc[:, 1] > 1330) & (cc[:, 1] < 1600) & (cc[:, 2] > 850)]
xs = np.arange(-620, 641, 20.0); gy = np.full(len(xs), np.nan)
for i, x0 in enumerate(xs):
    yy = np.sort(deck[np.abs(deck[:, 0] - x0) < 10, 1])
    if len(yy) > 20:
        dg = np.diff(yy); j = int(np.argmax(dg))
        if dg[j] > 5: gy[i] = (yy[j] + yy[j + 1]) / 2
ok = np.isfinite(gy); gy = np.interp(xs, xs[ok], gy[ok]); gy = median_filter(gy, 5, mode="nearest")
print("shut-line gap y: centre %.0f, x=+-400: %.0f / %.0f mm (fitted v6 arc: 1480 / 1426)" % (np.interp(0, xs, gy), np.interp(-400, xs, gy), np.interp(400, xs, gy)))
arc = np.interp(cc[:, 0], xs, gy)
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
# everything else in the zone the open captures lack (smoothed raw label, before mirroring): drop from the base
rs = raw.copy()
for _ in range(2):
    rs = (np.array([rs[n].mean() for n in nb]) > 0.5).astype(float)
drop = np.zeros(len(car), bool); drop[zi[rs > 0.5]] = True; drop &= ~mask
np.save(M + a.out.replace(".stl", "_drop.npy"), drop); print("drop from base (not lid):", int(drop.sum()))
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
