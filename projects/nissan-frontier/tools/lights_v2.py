"""v10 grille lights (user on v9: "the grille lights aren't aligned correctly"). The 1:1 onion showed the real lights as thin strips framed
by the brow openings; v8/v9 laid the 55 mm lens ON the brow, so it read as a big pad. Now each scanned light sits UNDER its opening:
  1. per pocket frame: L = long axis (nose tangent in plan), n = brow-slope normal (58 deg up from forward), w = n x L
  2. depth raster of Upper_Grille_V1 along n -> the through-opening (no hit / > 15 mm deeper than the skin) = the visible window
  3. lens face 2 mm under the skin, centred on the window, long axis along the window
  4. any light triangle that would show OUTSIDE the grille (outside the CAD skin seen along n, forward or up, except through the
     window) is dropped - the housing stays hidden inside the brow.
    python lights_v2.py  -> lights/lt2_grille_{lens,body}.stl, ../lights_v2.json
"""
import json, os
import numpy as np
from scipy import ndimage
from lights import TRI, M, A, load, save, canon

CAD = load(f"{M}/ronin_lev/Upper_Grille_V1.stl")
CP = np.concatenate([CAD.reshape(-1, 3), CAD.mean(1), (CAD[:, 0] + CAD[:, 1]) / 2, (CAD[:, 1] + CAD[:, 2]) / 2, (CAD[:, 0] + CAD[:, 2]) / 2])
OLD = json.load(open(os.path.join(os.path.dirname(__file__), "..", "lights.json")))["grille"]
TILT, SINK, S = 58.0, 2.0, 2.0


def frame(s):
    L = np.array(s["long"], float); L /= np.linalg.norm(L)
    F = np.array([L[1], -L[0], 0.0]); F /= np.linalg.norm(F)
    if F[1] > 0: F = -F
    t = np.radians(TILT); n = F * np.cos(t) + np.array([0, 0, 1.0]) * np.sin(t); w = np.cross(n, L)
    return np.array(s["centre"], float), L, w, n, F


def depth(P, c, a, b, d, ra=200, rb=80):
    """outermost CAD depth along d over the (a, b) plane through c, 0.5 mm cells"""
    q = P - c; u, v, z = q @ a, q @ b, q @ d; m = (np.abs(u) < ra) & (np.abs(v) < rb)
    W, H = int(2 * ra * S), int(2 * rb * S); zb = np.full((H, W), -1e9)
    np.maximum.at(zb, (((v[m] + rb) * S).astype(int), ((u[m] + ra) * S).astype(int)), z[m])
    return zb, ra, rb


def look(zb, ra, rb, P, c, a, b, d):
    q = P - c; u, v, z = q @ a, q @ b, q @ d
    i = np.clip(((v + rb) * S).astype(int), 0, zb.shape[0] - 1); j = np.clip(((u + ra) * S).astype(int), 0, zb.shape[1] - 1)
    inside = (np.abs(u) < ra) & (np.abs(v) < rb)
    return z, zb[i, j], inside, i, j


def main():
    v = load(A + "Grille Fogs.stl"); c = v.mean(1); mu = c.mean(0); w_, V = np.linalg.eigh(np.cov((c - mu).T)); q = (c - mu) @ V[:, -1]
    lens_all, body_all, info = [], [], []
    for (a0, b0), s in zip([(-1e9, -150), (-150, 150), (150, 1e9)], OLD):
        c0, L, w, n, F = frame(s)
        zb, ra, rb = depth(CP, c0, L, w, n)
        has = zb > -1e8
        for it in range(2):                                    # refit the slope normal to the skin around the window
            cols = np.abs(np.arange(zb.shape[1]) / S - ra)
            band = has & ((cols > 118) & (cols < 150))[None, :] & (np.abs(np.arange(zb.shape[0]) / S - rb) < 25)[:, None]
            rr, cc = np.nonzero(band); sk3 = c0 + L * (cc / S - ra)[:, None] * 0 + 0
            pts = c0 + np.outer(cc / S - ra, L) + np.outer(rr / S - rb, w) + np.outer(zb[rr, cc], n)
            pts = pts[zb[rr, cc] > np.percentile(zb[rr, cc], 40)]
            mu_ = pts.mean(0); ev, EV = np.linalg.eigh(np.cov((pts - mu_).T)); n2 = EV[:, 0] * np.sign(EV[:, 0] @ n)
            n = n2 - L * (n2 @ L); n /= np.linalg.norm(n); w = np.cross(n, L)
            zb, ra, rb = depth(CP, c0, L, w, n); has = zb > -1e8
        cols = np.abs(np.arange(zb.shape[1]) / S - ra)
        ringc = has & ((cols > 118) & (cols < 150))[None, :]
        surf = np.array([np.median(zb[r][ringc[r]]) if ringc[r].sum() > 5 else np.nan for r in range(zb.shape[0])])
        hole = ((~has) | (zb < surf[:, None] - 10)) & ~np.isnan(surf)[:, None]
        hole[:, :int((ra - 125) * S)] = False; hole[:, int((ra + 125) * S):] = False
        hole[:int((rb - 35) * S)] = False; hole[int((rb + 35) * S):] = False
        hole = ndimage.binary_opening(hole, iterations=1)
        lab, k = ndimage.label(hole); cnt = np.bincount(lab.ravel()); cnt[0] = 0; win = lab == cnt.argmax()
        rr, cc = np.nonzero(win); uu, ww = cc / S - ra, rr / S - rb
        uc, wc = (uu.min() + uu.max()) / 2, (ww.min() + ww.max()) / 2
        tilt_deg = float(np.degrees(np.arcsin(np.clip(n[2], -1, 1))))
        sk = np.nanmedian(surf[max(0, int((wc + rb) * S) - 4):int((wc + rb) * S) + 4])
        P, lm = canon(v[(q > a0) & (q < b0)], half_w=40, half_d=30)
        R = np.stack([L, w, n], 1)
        Wd = P @ R.T + c0 + L * uc + w * wc + n * (sk - SINK)
        # drop anything that would show outside the grille skin (3 directions), except lens seen through the window along n
        keep = np.ones(len(Wd), bool)
        for d_, a_, b_ in ((n, L, w), (F, L, np.cross(F, L)), (np.array([0, 0, 1.0]), L, np.cross(np.array([0, 0, 1.0]), L))):
            zb2, ra2, rb2 = depth(CP, c0, a_, b_, d_, 220, 120)
            z, zs, ins, i, j = look(zb2, ra2, rb2, Wd.reshape(-1, 3), c0, a_, b_, d_)
            out = ins & ((zs < -1e8) | (z > zs + 0.5))
            if d_ is n:
                z1, _, _, i1, j1 = look(zb, ra, rb, Wd.reshape(-1, 3), c0, L, w, n)
                inwin = win[np.clip(i1, 0, win.shape[0] - 1), np.clip(j1, 0, win.shape[1] - 1)]
                out &= ~inwin
            else:
                out &= ~np.repeat(lm, 3)                      # lens is judged along n only
            keep &= ~out.reshape(-1, 3).any(1)
        lens_all.append(Wd[lm & keep]); body_all.append(Wd[~lm & keep])
        info.append({"x": float(c0[0]), "window_len": float(np.ptp(uu)), "window_wid": float(np.ptp(ww)), "u_c": float(uc), "w_c": float(wc),
                     "skin": float(sk), "tilt": tilt_deg, "dropped": int((~keep).sum()), "of": int(len(keep))})
        print(info[-1])
    save(f"{M}/lights/lt2_grille_lens.stl", np.concatenate(lens_all)); save(f"{M}/lights/lt2_grille_body.stl", np.concatenate(body_all))
    json.dump(info, open(os.path.join(os.path.dirname(__file__), "..", "lights_v2.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
