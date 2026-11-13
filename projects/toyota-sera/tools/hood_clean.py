"""Clean hood cut-out (user v4: "there are artifacts of the hood that aren't cleanly cut out").

    python3 hood_clean.py            -> rewrites clean/hood_panel.stl + hood_masks.npz (old ones kept as *_v3.*)

hinge_fit.py decided the hood per triangle (does the hinge land it on the 'Hood open' capture?), so the cut was ragged:
holes in the skin and a nose strip left on the car, wiper/cowl strips riding up with the hood, and inner-frame pieces
from the open capture that sit outside the hood (no XY limit). Here the hood is a REGION instead:
  F   hood outline on a 4 mm top-view grid: the landed-skin mask closed, hole-filled, opened, largest blob; its rear edge
      (the cowl side, where the wipers lie) replaced by a smooth curve fitted to the OPEN hood's rear edge swung closed
      ('Hood open' sees that edge unoccluded; on the closed car the wipers cover it).
  zs  smooth hood surface (robust 2D polynomial fitted to the skin's top heights inside F).
  panel outer = car tris with XY in F within LIP mm of the local top surface (the skin; the polynomial zs
                is only a fit-quality report - it can't follow the nose roll-off)
  panel inner = the open capture's inner frame (hinge_fit's swung-back tris) with XY inside F shrunk by 8 mm
  fills: 'Hood open' may only add triangles under the hood (XY in F grown by 40 mm) - stray scraps elsewhere in that
         capture (e.g. a card left on the fender) no longer reach the bases.
explode_base.py / hinge_fit.py base read the same masks, so rebuild the bases after this.
"""
import json
import os
import shutil
import struct

import numpy as np
from scipy.ndimage import maximum_filter, binary_closing, binary_dilation, binary_erosion, binary_fill_holes, binary_opening, label
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
C = "/home/user/media/toyota-sera/clean/"
X0, X1, Y0, Y1, S = -1050, 650, -1800, -150, 4.0
LIP = 25.0  # mm below the local top surface still counted as hood: the skin only - 70 mm reached the bumper top under the nose
NX, NY = int((X1 - X0) / S), int((Y1 - Y0) / S)


def load(n):
    return np.fromfile(C + n, dtype=TRI, offset=84)


def save(p, m, tag):
    with open(p, "wb") as f:
        f.write(tag.ljust(80)[:80]); f.write(struct.pack("<I", len(m))); m.tofile(f)


def cells(c):
    ix = np.floor((c[:, 0] - X0) / S).astype(int); iy = np.floor((c[:, 1] - Y0) / S).astype(int)
    ok = (ix >= 0) & (ix < NX) & (iy >= 0) & (iy < NY)
    return ix, iy, ok


def inside(c, F):
    ix, iy, ok = cells(c)
    r = np.zeros(len(c), bool); r[ok] = F[iy[ok], ix[ok]]
    return r


def poly2(x, y, deg=4):
    return np.stack([x ** i * y ** j for i in range(deg + 1) for j in range(deg + 1 - i)], 1)


def main():
    for n in ("hood_panel.stl", "hood_masks.npz"):
        b = C + n.replace(".", "_v3.")
        if not os.path.exists(b):
            shutil.copy(C + n, b)
    car = load("car3.stl"); cc = car["v"].mean(1).astype(float)
    mk = dict(np.load(C + "hood_masks_v3.npz"))
    outer0 = mk["outer"]
    # --- region F
    ix, iy, ok = cells(cc[outer0])
    m = np.zeros((NY, NX), bool); m[iy[ok], ix[ok]] = True
    m = binary_fill_holes(binary_closing(m, iterations=4)); m = binary_opening(m, iterations=3)
    lab, _ = label(m); sz = np.bincount(lab.ravel()); sz[0] = 0; m = lab == sz.argmax()
    cols = np.where(m.any(0))[0]
    # rear edge (cowl side): from the OPEN hood's skin swung closed through the fitted hinge - in 'Hood open' the hood's
    # rear edge is unoccluded, while on the closed car the wipers lie over it (the landed mask wandered into them)
    hg = json.load(open(C + "hood_hinge.json")); lk = json.load(open("/home/user/media/toyota-sera/prep/car4.json"))
    piv = (np.array(hg["pivot"]) - np.array(lk["root_location"])) / lk["unit_scale"]
    Rb = Rot.from_rotvec(np.radians(-hg["open_deg"]) * np.array(hg["axis"])).as_matrix()
    st0 = load(str(mk["state"]))
    sk = (st0["v"].mean(1).astype(float)[mk["drop"]] - piv) @ Rb.T + piv
    bx, by, bok = cells(sk)
    g = np.zeros((NY, NX), int); np.add.at(g, (by[bok], bx[bok]), 1)
    rear = np.array([np.where(g[:, c] > 2)[0].max() if (g[:, c] > 2).any() else np.where(m[:, c])[0].max()
                     for c in cols], float)
    core = (cols > cols.min() + 0.15 * len(cols)) & (cols < cols.max() - 0.15 * len(cols))
    w = core.copy()
    for _ in range(4):  # robust quadratic fit of the rear edge on the central 70 %
        p = np.polyfit(cols[w], rear[w], 2); res = rear - np.polyval(p, cols)
        w = core & (np.abs(res) < max(2.0, 2.5 * np.std(res[w])))
    fit = np.polyval(p, cols)  # last hood row per column
    for k, c in enumerate(cols):
        m[int(np.floor(fit[k])) + 1:, c] = False
    F = m
    # --- smooth surface zs over F (top skin heights)
    top = np.full((NY, NX), -1e9); ix, iy, ok = cells(cc)
    np.maximum.at(top, (iy[ok], ix[ok]), cc[ok, 2])
    yy, xx = np.where(binary_erosion(F, iterations=3) & (top > -1e8))
    xs, ys, zs = (xx + 0.5) * S + X0, (yy + 0.5) * S + Y0, top[yy, xx]
    nx, ny = (xs - xs.mean()) / 1000, (ys - ys.mean()) / 1000
    A = poly2(nx, ny); w = np.ones(len(zs), bool)
    for _ in range(5):
        coef, *_ = np.linalg.lstsq(A[w], zs[w], rcond=None); r = zs - A @ coef
        w = np.abs(r) < max(3.0, 2.5 * np.std(r[w]))
    print("hood surface fit: rms %.1f mm on %d cells (%.1f %% kept)" % (np.std(r[w]), w.sum(), 100 * w.mean()))

    def zsurf(c):
        return poly2((c[:, 0] - xs.mean()) / 1000, (c[:, 1] - ys.mean()) / 1000) @ coef

    # skin = within LIP mm of the local top surface (max over a 12 mm neighbourhood): follows the nose roll-off, which a
    # global polynomial can't; F's rear edge already stops short of the wipers, so nothing sits above the skin in F
    inF = inside(cc, F)
    topn = maximum_filter(top, size=3)
    ix, iy, ok = cells(cc)
    tl = np.full(len(cc), -1e9); tl[ok] = topn[iy[ok], ix[ok]]
    outer = inF & (cc[:, 2] > tl - LIP)
    print("outer tris: v3 %d -> %d (added %d, removed %d)" % (outer0.sum(), outer.sum(), (outer & ~outer0).sum(),
                                                            (outer0 & ~outer).sum()))
    # --- inner frame: hinge_fit's swung-back tris, limited to F shrunk by 8 mm
    pan = load("hood_panel_v3.stl"); back = pan[int(outer0.sum()):]
    Fi = binary_erosion(F, iterations=2)
    keep_in = inside(back["v"].mean(1).astype(float), Fi)
    print("inner tris: v3 %d -> %d" % (len(back), keep_in.sum()))
    save(C + "hood_panel.stl", np.concatenate([car[outer], back[keep_in]]), b"toyota-sera hood_clean")
    # --- fills: 'Hood open' only under the hood
    st = load(str(mk["state"]))
    under = inside(st["v"].mean(1).astype(float), binary_dilation(F, iterations=10))
    drop = mk["drop"] | ~under
    print("'Hood open' fill limited to under the hood: %d -> %d candidate tris" % ((~mk["drop"]).sum(), (~drop).sum()))
    mk.update(outer=outer, drop=drop)
    np.savez_compressed(C + "hood_masks.npz", **mk)
    np.save(C + "hood_region.npy", F)
    json.dump({"grid": [X0, X1, Y0, Y1, S], "rear_fit": p.tolist(), "outer": int(outer.sum()), "inner": int(keep_in.sum())},
              open(C + "hood_clean.json", "w"), indent=1)


if __name__ == "__main__":
    main()
