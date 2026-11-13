"""Seat the SCANNED Ronin lights into the CAD (levelled mm frame) - v8, user: "for the grille lights we have 3D scans ... also the fender lights".

Drive 'Nissan Frontier Pro-4X/Scans':
  'Frontier Accessories Grille Fogs.stl'  = the THREE grille slot lights scanned side by side (each ~267 x 55 x 40 mm, trapezoid lens,
                                            two clip pairs + pigtail) -> the three pockets on the nose of Upper_Grille_V1
  'Frontier Accessories Sidemarker 1/2'   = fender lights (253 x 56 x 37 mm, raised lens bar, two tabs) -> the slot at the top of each
                                            of the four CAD fenders (both have two bosses behind the slot)
Each light: robust PCA (pigtail/wire outliers dropped), lens side = the side away from the clips/wires; the lens face is put on the
slot opening (slot centre, long axis and outward normal measured from the CAD), 1 mm proud. Lens and housing are written separately
(lens = emissive material in the renders).
    python lights.py   -> /home/user/media/nissan-frontier/lights/lt_{grille,fen_R,fen_L}_{lens,body}.stl + lights.json
"""
import json, os
import numpy as np
from scipy import ndimage

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = "/home/user/media/nissan-frontier"
A = f"{M}/scans_acc/Frontier Accessories "
OUT = f"{M}/lights"


def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)["v"].astype(np.float64)


def save(p, v):
    d = np.zeros(len(v), TRI); d["v"] = v
    n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); d["n"] = n / (np.linalg.norm(n, axis=1)[:, None] + 1e-12)
    with open(p, "wb") as f:
        f.write(b"\0" * 80); f.write(np.uint32(len(d)).tobytes()); d.tofile(f)


def canon(v, half_w=45, half_d=30):
    """-> (tris in the light's own frame: x long, y width, z outward through the lens; origin on the lens face centre), lens mask"""
    c = v.mean(1); m = np.ones(len(c), bool)
    for _ in range(5):
        mu = c[m].mean(0); w, V = np.linalg.eigh(np.cov((c[m] - mu).T)); V = V[:, ::-1]
        if np.linalg.det(V) < 0: V[:, 2] *= -1
        q = (c - mu) @ V
        m = (np.abs(q[:, 2] - np.median(q[m, 2])) < half_d) & (np.abs(q[:, 1] - np.median(q[m, 1])) < half_w)
    mw = np.abs(q[:, 1] - np.median(q[m, 1])) < half_w
    a, md, b = np.percentile(q[mw, 2], [0.3, 50, 99.7])
    if b - md > md - a:                                # clips/wires reach further from the body than the lens -> they are the BACK
        V[:, 2] *= -1; V[:, 1] *= -1; q = (c - mu) @ V
    P = (v - mu) @ V
    zt = np.percentile(q[m, 2], 99.5)
    top = m & (q[:, 2] > zt - 8)
    o = np.array([np.median(q[top, 0]), np.median(q[top, 1]), zt])
    P = P[m] - o; q = q[m] - o
    n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    lens = (q[:, 2] > -9) & (n[:, 2] > 0.25)
    return P, lens


def place(P, centre, long, normal, proud=1.0, flip=False):
    long = long / np.linalg.norm(long); normal = normal - long * (normal @ long); normal /= np.linalg.norm(normal)
    y = np.cross(normal, long)
    if flip: long, y = -long, -y
    R = np.stack([long, y, normal], 1)                  # columns = light x, y, z in the car frame
    return P @ R.T + centre + normal * proud


TILT, BACK, RISE, PROUD = 54.0, 22.0, 21.0, -1.0


def grille_slots():
    """Three pockets on the nose of the upper grille: centre on the opening, long axis = local nose tangent, normal = -Y in plan."""
    v = load(f"{M}/ronin_lev/Upper_Grille_V1.stl").reshape(-1, 3)
    cx = (v[:, 0].min() + v[:, 0].max()) / 2
    band = v[(v[:, 2] > 1058) & (v[:, 2] < 1088)]
    xs = np.arange(-480, 500, 10.0); nose = np.array([band[np.abs(band[:, 0] - x) < 6, 1].min() for x in xs])
    out = []
    for dx in (-303, 0, 303):
        x0 = cx + dx; s = np.abs(xs - x0) < 110
        a, b = np.polyfit(xs[s], nose[s], 1)             # nose line y = a x + b across the slot
        long = np.array([1, a, 0.0]); nrm = np.array([a, -1, 0.0]); nrm /= np.linalg.norm(nrm)
        # the pocket is a wedge notched into the sloped top face: nose (y, z 1073) -> back wall top (y + 33, z 1097). The lens
        # continues that slope (36 deg from horizontal), so its normal points forward and 54 deg up; centre = middle of the slope
        up = np.radians(TILT); nrm = nrm * np.cos(up) + np.array([0, 0, np.sin(up)])
        c0 = np.array([x0, a * x0 + b, 1073.0]) + np.array([-a, 1, 0.0]) / np.hypot(a, 1) * BACK + np.array([0, 0, RISE])
        out.append({"centre": c0.tolist(), "long": long.tolist(), "normal": nrm.tolist()})
    return out


def fender_slot(path):
    """Through-slot at the top of a CAD fender: enclosed hole in the side (Y-Z) projection."""
    t = load(path); v = np.concatenate([t.reshape(-1, 3), t.mean(1)])
    S = 0.5; lo = v[:, 1:].min(0) - 10
    ij = ((v[:, 1:] - lo) * S).astype(int); g = np.zeros(ij.max(0) + 6, bool); g[ij[:, 0], ij[:, 1]] = True
    g = ndimage.binary_closing(g, iterations=2)
    lab, n = ndimage.label(~g)
    border = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
    best = max((i for i in range(1, n + 1) if i not in border), key=lambda i: (lab == i).sum())
    hy, hz = np.nonzero(lab == best); hole = np.stack([hy, hz], 1) / S + lo
    c2 = hole.mean(0)
    w, V = np.linalg.eigh(np.cov((hole - c2).T)); d2 = V[:, -1]; L = np.ptp((hole - c2) @ d2)
    c = t.mean(1); n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]); ar = np.linalg.norm(n, axis=1); n /= ar[:, None] + 1e-12
    side = 1 if c[:, 0].mean() > 0 else -1
    near = (np.abs((c[:, 1:] - c2) @ d2) < L / 2 + 15) & (np.abs((c[:, 1:] - c2) @ np.array([-d2[1], d2[0]])) < 30)
    skin = near & (n[:, 0] * side > 0.2)                 # outer skin around the slot
    xo = np.percentile(c[skin, 0] * side, 70) * side
    rim = skin & (np.abs(c[:, 0] - xo) < 25)
    nrm = (n[rim] * ar[rim, None]).sum(0); nrm /= np.linalg.norm(nrm)
    centre = np.array([np.average(c[rim, 0], weights=ar[rim]), c2[0], c2[1]])
    long = np.array([0, d2[0], d2[1]]); long *= np.sign(long[1]) or 1
    return {"centre": centre.tolist(), "long": long.tolist(), "normal": nrm.tolist(), "len": float(L), "px": int(len(hole))}


def main():
    os.makedirs(OUT, exist_ok=True); info = {}
    # grille: split the three scanned lights along the scan's long axis
    v = load(A + "Grille Fogs.stl"); c = v.mean(1); mu = c.mean(0); w, V = np.linalg.eigh(np.cov((c - mu).T)); q = (c - mu) @ V[:, -1]
    slots = grille_slots(); lens, body = [], []
    for (a, b), s in zip([(-1e9, -150), (-150, 150), (150, 1e9)], slots):
        P, lm = canon(v[(q > a) & (q < b)], half_w=40, half_d=30)
        W = place(P, np.array(s["centre"]), np.array(s["long"]), np.array(s["normal"]), proud=PROUD)
        lens.append(W[lm]); body.append(W[~lm]); s["size"] = np.ptp(P.reshape(-1, 3), 0).round(1).tolist()
    save(f"{OUT}/lt_grille_lens.stl", np.concatenate(lens)); save(f"{OUT}/lt_grille_body.stl", np.concatenate(body)); info["grille"] = slots
    # fenders: Sidemarker 1 on the right pair, Sidemarker 2 on the left pair
    for side, scan in (("R", "Sidemarker 1"), ("L", "Sidemarker 2")):
        P, lm = canon(load(A + scan + ".stl"), half_w=45, half_d=26)
        lens, body = [], []
        for pos in ("Front", "Rear"):
            s = fender_slot(f"{M}/ronin_lev/Fender_{pos}{'Right' if side == 'R' else 'Left'}.stl")
            W = place(P, np.array(s["centre"]), np.array(s["long"]), np.array(s["normal"]), proud=1.0)
            lens.append(W[lm]); body.append(W[~lm]); info[f"fender_{pos}{side}"] = s
        save(f"{OUT}/lt_fen_{side}_lens.stl", np.concatenate(lens)); save(f"{OUT}/lt_fen_{side}_body.stl", np.concatenate(body))
    json.dump(info, open(os.path.join(os.path.dirname(__file__), "..", "lights.json"), "w"), indent=1)
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1: TILT, BACK, RISE, PROUD = map(float, sys.argv[1:5])
    main()
