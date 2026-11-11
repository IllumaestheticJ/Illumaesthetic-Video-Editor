"""Fill small see-through holes in the upper body panels (hood, roof, deck lid) with an interpolated surface.

    python fill_top.py car.stl out.stl [--donor other_aligned.stl] --zmin -800 --cell 6

Height map of the topmost surface (max z per XY cell). A cell is a hole when it sits > --drop mm below the
median-filtered surface around it (you see the engine bay/cabin through the panel) or is empty but enclosed.
Components larger than --maxarea m^2 are left alone (glass, real openings). Holes are filled by Laplace
interpolation from the surrounding panel and triangulated 1 mm below it (no z-fighting with the real scan).
"""
import argparse, os, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read, write, tris  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("out")
ap.add_argument("--donor"); ap.add_argument("--zmin", type=float, default=-800)
ap.add_argument("--cell", type=float, default=6); ap.add_argument("--drop", type=float, default=35)
ap.add_argument("--maxarea", type=float, default=0.25)
ap.add_argument("--zone", type=float, nargs=4, action="append", help="xmin xmax ymin ymax raw mm; holes only searched here")
ap.add_argument("--dens", type=float, default=0.7)
ap.add_argument("--rim", type=float, default=20, help="mm the filled area extends past the detected hole (covers speckle)")
ap.add_argument("--win", type=float, default=60)
ap.add_argument("--mask-out", help="debug png of the hole mask")
a = ap.parse_args()
car = read(a.car)
pts = car["v"].reshape(-1, 3)
if a.donor:
    pts = np.concatenate([pts, read(a.donor)["v"].reshape(-1, 3)])
pts = pts[pts[:, 2] > a.zmin]
lo = pts[:, :2].min(0); C = a.cell
ij = ((pts[:, :2] - lo) / C).astype(int)
W, H = ij.max(0) + 1
hm = np.full((W, H), np.nan)
order = np.argsort(pts[:, 2])
hm[ij[order, 0], ij[order, 1]] = pts[order, 2]  # last write wins = max z
occ = ~np.isnan(hm)
body = ndimage.binary_closing(occ, iterations=6)
body = ndimage.binary_fill_holes(body)
f = np.where(occ, hm, np.nanmin(hm))
smooth = ndimage.median_filter(f, size=25)
inner = ndimage.binary_erosion(body, iterations=int(45 / C))
dens = ndimage.uniform_filter(occ.astype(float), size=int(a.win / C) | 1)
hole = inner & ((dens < a.dens) | (f < smooth - a.drop))
hole = ndimage.binary_opening(hole, iterations=int(12 / C))   # drops thin real gaps (cowl, panel seams)
lab, n = ndimage.label(hole)
keep = np.zeros_like(hole)
zm = np.zeros_like(hole)
gx = lo[0] + (np.arange(W) + 0.5) * C; gy = lo[1] + (np.arange(H) + 0.5) * C
for x0, x1, y0, y1 in a.zone or []:
    zm |= ((gx[:, None] > x0) & (gx[:, None] < x1)) & ((gy[None] > y0) & (gy[None] < y1))
for k in range(1, n + 1):
    m = lab == k
    area = m.sum() * (C / 1000) ** 2
    if area < a.maxarea and (m & zm).sum() > 0.8 * m.sum():
        keep |= m
# per component: robust quadratic fit z(x,y) to clean panel cells in a ring around the hole
zf = f.copy()
final = np.zeros_like(keep)
gx = lo[0] + (np.arange(W) + 0.5) * C; gy = lo[1] + (np.arange(H) + 0.5) * C
GX, GY = np.meshgrid(gx, gy, indexing="ij")
lab2, n2 = ndimage.label(keep)
for k in range(1, n2 + 1):
    m = ndimage.binary_dilation(lab2 == k, iterations=int(a.rim / C)) & body
    ring = ndimage.binary_dilation(m, iterations=int(100 / C)) & ~ndimage.binary_dilation(m, iterations=int(12 / C)) & occ & (dens > a.dens)
    X, Y, Z = GX[ring], GY[ring], f[ring]
    A = np.stack([np.ones_like(X), X, Y, X * X, X * Y, Y * Y], 1)
    sx, sy = X.mean(), Y.mean()
    A = np.stack([np.ones_like(X), X - sx, Y - sy, (X - sx) ** 2, (X - sx) * (Y - sy), (Y - sy) ** 2], 1)
    use = np.ones(len(Z), bool)
    for _ in range(6):
        coef, *_ = np.linalg.lstsq(A[use], Z[use], rcond=None)
        r = Z - A @ coef
        use = np.abs(r) < max(2.0, 2.5 * np.median(np.abs(r[use])))
    print("component %d: ring %d cells, fit residual p50 %.2f p90 %.2f mm" % (k, ring.sum(), np.median(np.abs(r[use])), np.percentile(np.abs(r[use]), 90)))
    Xm, Ym = GX - sx, GY - sy
    zfit = coef[0] + coef[1] * Xm + coef[2] * Ym + coef[3] * Xm ** 2 + coef[4] * Xm * Ym + coef[5] * Ym ** 2
    zf = np.where(m, zfit, zf)
    final |= m
keep = final
zf -= 1.0
# triangulate filled cells (two tris per cell using corner heights from neighbours)
I, J = np.nonzero(keep)
def P(i, j):
    i = np.clip(i, 0, W - 1); j = np.clip(j, 0, H - 1)
    return np.stack([lo[0] + i * C + C / 2, lo[1] + j * C + C / 2, zf[i, j]], -1)
a0, a1, a2, a3 = P(I, J), P(I + 1, J), P(I + 1, J + 1), P(I, J + 1)
v = np.concatenate([np.stack([a0, a1, a2], 1), np.stack([a0, a2, a3], 1)])
new = tris(v.astype(np.float32))
if a.mask_out:
    from PIL import Image
    img = np.zeros((W, H, 3), np.uint8); img[occ] = 90; img[keep] = (255, 40, 40)
    Image.fromarray(img.transpose(1, 0, 2)[::-1]).save(a.mask_out)
# drop the speckle inside filled cells (base triangles near the filled surface), keep everything below it
cc = car["v"].mean(1)
ci = ((cc[:, :2] - lo) / C).astype(int)
inb = (ci[:, 0] >= 0) & (ci[:, 0] < W) & (ci[:, 1] >= 0) & (ci[:, 1] < H)
drop = np.zeros(len(car), bool)
ii = np.nonzero(inb)[0]
drop[ii] = keep[ci[ii, 0], ci[ii, 1]] & (np.abs(cc[ii, 2] - zf[ci[ii, 0], ci[ii, 1]]) < 25)
print("speckle tris removed", int(drop.sum()))
write(a.out, np.concatenate([car[~drop], new]))
print("added", len(new))
