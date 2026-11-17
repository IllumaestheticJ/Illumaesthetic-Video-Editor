"""v1.5b: NC fender zone by the part's SIDE OUTLINE (clean edge). The fender-cut panel faces +-x, so per side the part is
rasterised in (y, z) at 2 mm, closed (fill holes) and dilated 2 mm; the zone = scan triangles on that side whose (y, z)
falls inside the outline and that sit on the outer skin (|x| >= outermost scan |x| at that (y, z) - 80 mm).
    python nc_fender_outline.py"""
import sys, numpy as np
from scipy import ndimage
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl
M = "/home/user/media/bf-miata-mr2-night-meet"; D = f"{M}/dec"; K = f"{M}/kit_nc"; G = 0.002
S = read_stl(f"{D}/nc_glbframe.stl"); C = S.mean(1)
P = read_stl(f"{K}/part_fender_cuts.stl")
sel = []
for side in (1, -1):
    T = P[(np.sign(P.mean(1)[:, 0]) == side)]
    V = T.reshape(-1, 3); y0, z0 = V[:, 1].min() - 0.02, V[:, 2].min() - 0.02
    ny, nz = int((V[:, 1].max() + 0.02 - y0) / G) + 1, int((V[:, 2].max() + 0.02 - z0) / G) + 1
    img = np.zeros((ny, nz), bool)
    # rasterise triangles by dense barycentric sampling
    r = np.random.default_rng(0).random((60, 2)); m = r.sum(1) > 1; r[m] = 1 - r[m]
    pts = (T[:, None, 0] + r[None, :, :1] * (T[:, None, 1] - T[:, None, 0]) + r[None, :, 1:] * (T[:, None, 2] - T[:, None, 0])).reshape(-1, 3)
    pts = np.concatenate([pts, V])
    iy = ((pts[:, 1] - y0) / G).astype(int); iz = ((pts[:, 2] - z0) / G).astype(int); img[iy, iz] = True
    img = ndimage.binary_closing(img, iterations=3); img = ndimage.binary_fill_holes(img); img = ndimage.binary_dilation(img, iterations=1)
    on = np.where(np.sign(C[:, 0]) == side)[0]
    iy = ((C[on, 1] - y0) / G).astype(int); iz = ((C[on, 2] - z0) / G).astype(int)
    ok = (iy >= 0) & (iy < ny) & (iz >= 0) & (iz < nz); inside = np.zeros(len(on), bool); inside[ok] = img[iy[ok], iz[ok]]
    cand = on[inside]
    # outer skin: keep triangles within 80 mm of the outermost |x| in their 1 cm (y, z) cell
    key = (np.round(C[cand, 1] / 0.01).astype(int) * 100000 + np.round(C[cand, 2] / 0.01).astype(int))
    ax = np.abs(C[cand, 0]); order = np.argsort(key); ks, idx0 = np.unique(key[order], return_index=True)
    mx = np.maximum.reduceat(ax[order], idx0); lookup = dict(zip(ks, mx))
    outer = np.array([a >= lookup[k] - 0.08 for k, a in zip(key, ax)])
    sel.append(cand[outer]); print("side", side, "outline px", int(img.sum()), "zone tris", int(outer.sum()))
np.save(f"{D}/nc_fender_idx.npy", np.concatenate(sel))
