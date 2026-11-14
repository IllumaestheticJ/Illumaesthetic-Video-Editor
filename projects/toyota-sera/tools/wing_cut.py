"""Rear wing part + wing-removed fill for the Sera (user v5: "include the rear wing ... data too").

    python3 wing_cut.py            -> clean/wing_panel.stl, clean/wing_masks.npz, clean/wing_region.npy

'Spoiler removed' is a patchy capture (no hatch glass, holes everywhere), so 'car minus state' is not the wing. The
wing is found geometrically instead (side sections: an airfoil on the hatch's rear edge, y ~1790-1965, z ~930-990):
  hatch  smooth surface z(x, y) fitted to the full car's top skin just ahead of the wing (y 1450-1760), extrapolated back
  wing   car tris in y 1680-2080 (the ends reach forward to ~1700, the centre back to ~2020) more than 10 mm and less than 160 mm above that surface, cleaned as a REGION on a 4 mm
         top-view grid (close, fill, open, largest blob - the hood_clean.py lesson), then every car tri more than 4 mm
         above the hatch inside the region (keeps the underside that runs close to the hatch)
  fill   'Spoiler removed' tris only inside the wing region grown by 30 mm and below the wing (the hatch skin the wing
         hid), more than 6 mm from the car minus wing - no other part of that capture reaches the base
"""
import struct

import numpy as np
from scipy.ndimage import binary_closing, binary_dilation, binary_fill_holes, binary_opening, label
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
C = "/home/user/media/toyota-sera/clean/"
X0, X1, Y0, Y1, S = -1150, 750, 1400, 2150, 4.0
NX, NY = int((X1 - X0) / S), int((Y1 - Y0) / S)


def load(n):
    return np.fromfile(C + n, dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"toyota-sera wing_cut".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)


def cells(c):
    ix = np.floor((c[:, 0] - X0) / S).astype(int); iy = np.floor((c[:, 1] - Y0) / S).astype(int)
    return ix, iy, (ix >= 0) & (ix < NX) & (iy >= 0) & (iy < NY)


def inside(c, F):
    ix, iy, ok = cells(c); r = np.zeros(len(c), bool); r[ok] = F[iy[ok], ix[ok]]; return r


def basis(x, y):
    x = x / 1000.0; y = (y - 1600) / 1000.0
    return np.stack([x ** i * y ** j for i in range(5) for j in range(3)], 1)


def main():
    car = load("car3.stl"); cc = car["v"].mean(1).astype(float)
    # hatch surface from the car's top skin ahead of the wing
    top = np.full((NY, NX), -1e9); ix, iy, ok = cells(cc); np.maximum.at(top, (iy[ok], ix[ok]), cc[ok, 2])
    yy, xx = np.where(top > 850)
    ys = (yy + 0.5) * S + Y0; xs = (xx + 0.5) * S + X0; zs = top[yy, xx]
    sel = (ys > 1450) & (ys < 1760)
    A = basis(xs[sel], ys[sel]); z = zs[sel]; w = np.ones(len(z), bool)
    for _ in range(6):
        coef, *_ = np.linalg.lstsq(A[w], z[w], rcond=None); r = z - A @ coef
        w = np.abs(r) < max(3.0, 2.5 * np.std(r[w]))
    print("hatch fit rms %.1f mm on %d cells" % (np.std(r[w]), w.sum()))
    hz = lambda c: basis(c[:, 0], c[:, 1]) @ coef
    band = (cc[:, 1] > 1680) & (cc[:, 1] < 2080) & (cc[:, 2] > 800)
    dz = np.full(len(cc), -1e9); dz[band] = cc[band, 2] - hz(cc[band])
    cand = band & (dz > 10) & (dz < 160)  # seeds the region; the part itself takes dz > 4 (underside)
    ix, iy, ok = cells(cc[cand])
    m = np.zeros((NY, NX), bool); m[iy[ok], ix[ok]] = True
    m = binary_fill_holes(binary_closing(m, iterations=3)); m = binary_opening(m, iterations=2)
    lab, n = label(m); sz = np.bincount(lab.ravel()); sz[0] = 0; F = lab == sz.argmax()
    print("wing region: %d cells, %d blobs before cleanup (largest %d)" % (F.sum(), n, sz.max()))
    Fg = F.copy()  # grow FORWARD only (-y, lower rows): the leading edge meets the hatch below the 10 mm seed (an isotropic
    for k in range(1, 7):  # grow also took the tail-panel corner behind the wing); dz > 4 still excludes the hatch skin
        Fg[:-k] |= F[k:]
    F = Fg
    wing = inside(cc, F) & band & (dz > 4)
    ys_, xs_ = np.where(F)
    print("wing: %d tris, x %.0f..%.0f, y %.0f..%.0f mm, z %.0f..%.0f" % (
        wing.sum(), cc[wing, 0].min(), cc[wing, 0].max(), cc[wing, 1].min(), cc[wing, 1].max(),
        cc[wing, 2].min(), cc[wing, 2].max()))
    save(C + "wing_panel.stl", car[wing])
    # fill: the spoiler-removed state's hatch skin under the wing only
    st = load("spoiler_removed_3mm.stl"); sc = st["v"].mean(1).astype(float)
    keep = inside(sc, binary_dilation(F, iterations=8))
    keep &= sc[:, 2] < np.where(keep, hz(sc) + 12, -1e9) if keep.any() else keep
    d, _ = cKDTree(cc[~wing]).query(sc[keep], distance_upper_bound=20)
    idx = np.where(keep)[0]; keep[:] = False; keep[idx[d > 6]] = True
    print("fill from 'Spoiler removed': %d tris (of %d in that scan)" % (keep.sum(), len(st)))
    np.savez_compressed(C + "wing_masks.npz", outer=wing, fill=keep, state="spoiler_removed_3mm.stl")
    np.save(C + "wing_region.npy", F)


if __name__ == "__main__":
    main()
