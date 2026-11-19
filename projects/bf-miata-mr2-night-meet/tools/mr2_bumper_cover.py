"""v2.0 (user: "the front bumper swap removes too much material on the MR2 Spyder").
The stock-bumper footprint cut also took a strip ABOVE the Epsilon bumper (under the hood nose / headlights and at the fender),
which left a black gap once the part was on. Keep on the car every cut triangle the new part does not cover:
covered = inside the part's front silhouette (x,z; holes filled) or, at the corners (|x| > 0.6), inside its side silhouette (y,z).
Run after cutparts.py:   python mr2_bumper_cover.py   (rewrites dec/mr2_cut_bumper.stl and appends the rest to dec/mr2_keep.stl)"""
import sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl, write_stl
M = "/home/user/media/bf-miata-mr2-night-meet"; PX = 0.004


def samples(T, step=0.002):
    rng = np.random.default_rng(0); a = np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1) / 2
    k = np.minimum(np.maximum(1, np.ceil(a / step ** 2)).astype(int), 20000); idx = np.repeat(np.arange(len(T)), k)
    r = rng.random((len(idx), 2)); m = r.sum(1) > 1; r[m] = 1 - r[m]
    return np.concatenate([T[idx, 0] + r[:, :1] * (T[idx, 1] - T[idx, 0]) + r[:, 1:] * (T[idx, 2] - T[idx, 0]), T.reshape(-1, 3)])


def raster(u, v, lo, shape):
    img = np.zeros(shape, bool); i = ((u - lo[0]) / PX).astype(int); j = ((v - lo[1]) / PX).astype(int)
    ok = (i >= 0) & (i < shape[0]) & (j >= 0) & (j < shape[1]); img[i[ok], j[ok]] = True
    return ndimage.binary_fill_holes(ndimage.binary_closing(img, iterations=2))


def inside(img, u, v, lo):
    i = ((u - lo[0]) / PX).astype(int); j = ((v - lo[1]) / PX).astype(int)
    ok = (i >= 0) & (i < img.shape[0]) & (j >= 0) & (j < img.shape[1]); out = np.zeros(len(u), bool); out[ok] = img[i[ok], j[ok]]
    return out


P = samples(read_stl(f"{M}/kit_mr2/part_front_bumper.stl"))
C = read_stl(f"{M}/dec/mr2_cut_bumper.stl"); c = C.mean(1)
lo = np.array([-1.0, -2.4, 0.0]); n = lambda a, b: int((b - a) / PX) + 1
front = raster(P[:, 0], P[:, 2], (lo[0], lo[2]), (n(-1, 1), n(0, 1)))
cov = inside(front, c[:, 0], c[:, 2], (lo[0], lo[2]))
for sgn in (-1, 1):
    S = P[P[:, 0] * sgn > 0.55]; side = raster(S[:, 1], S[:, 2], (lo[1], lo[2]), (n(-2.4, -0.4), n(0, 1)))
    cov |= (c[:, 0] * sgn > 0.6) & inside(side, c[:, 1], c[:, 2], (lo[1], lo[2]))
# a triangle must be covered at all 3 vertices' level too: drop boundary slivers by eroding with the centroid test only
keep = read_stl(f"{M}/dec/mr2_keep.stl")
write_stl(f"{M}/dec/mr2_cut_bumper.stl", C[cov]); write_stl(f"{M}/dec/mr2_keep.stl", np.concatenate([keep, C[~cov]]))
print(f"bumper cut {len(C)} -> {cov.sum()} tris; {(~cov).sum()} stay on the car")
