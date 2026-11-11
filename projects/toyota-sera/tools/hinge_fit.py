"""Fit a hinge (any axis direction) that swings a closed panel on the full car onto the same panel captured OPEN in a
state scan, then split out the panel and build the "panel open" base. Generalises projects/huracan-evo/tools/hinge.py
(axis ~X only) so it also handles the Sera's butterfly doors.

    hinge_fit.py <name> <state.stl> --closed "x0,x1,y0,y1,z0,z1" --open "x0,x1,y0,y1,z0,z1" [--far 15]

All inputs: levelled + cropped 3 mm STLs (mm) in /home/user/media/toyota-sera/clean. Writes, in that folder:
  <name>_panel.stl   closed panel: car triangles the fitted hinge lands on the open capture (outer skin) + the open
                     capture's other triangles (inner frame / trim) swung back through the inverse hinge
  <name>_masks.npz   outer-skin mask (car) and open-panel mask (state) for the base step
    hinge_fit.py base out.stl <name> [<name> ...]   car minus the named panels + what their state scans add
and <name>_hinge.json in the prepped Blender frame (m; prep/car4.json offset) for tools/shot.py:
  {"pivot": [...], "axis": [...], "open_deg": a, "fit_median_mm": ...}

Steps: closed candidates = car tris > --far mm from the state scan inside the --closed box; open panel = state tris
> --far mm from the car inside the --open box. Truncated-mean point-to-nearest cost, coarse grid over axis directions /
angles / pivots, then Nelder-Mead on (pivot xyz, axis theta/phi, angle)."""
import argparse, json, struct
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
C = "/home/user/media/toyota-sera/clean/"
LIKE = "/home/user/media/toyota-sera/prep/car4.json"


def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"toyota-sera hinge_fit".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)


def box(c, b):
    x0, x1, y0, y1, z0, z1 = b
    return (c[:, 0] > x0) & (c[:, 0] < x1) & (c[:, 1] > y0) & (c[:, 1] < y1) & (c[:, 2] > z0) & (c[:, 2] < z1)


def axis_of(th, ph):
    return np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])


def xf(P, piv, ax, ang):
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix()
    return (P - piv) @ R.T + piv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name"); ap.add_argument("state")
    ap.add_argument("--closed", required=True); ap.add_argument("--open", required=True)
    ap.add_argument("--far", type=float, default=15.0)
    ap.add_argument("--outside", action="store_true",
                    help="open panel pts must be >30 mm above the car's roofline (40 mm XY cells) or outside its footprint")
    ap.add_argument("--inner-below", action="store_true",
                    help="keep inner tris only if, swung closed, they sit >3 mm below the outer skin (hood frame); "
                         "else parts of the open capture's own outer skin poke through the closed panel")
    ap.add_argument("--land-loose", type=float, default=0.0,
                    help="mm: closed candidates (car tris the state lacks, inside --closed) count as panel if they land this close")
    ap.add_argument("--land", type=float, default=10.0, help="mm: car tri is panel if hinge lands it this close to the open capture")
    a = ap.parse_args()
    cb = [float(v) for v in a.closed.split(",")]; ob = [float(v) for v in a.open.split(",")]
    car = load(C + "car3.stl"); st = load(C + a.state)
    cc = car["v"].mean(1).astype(float); sc = st["v"].mean(1).astype(float)
    d_cs, _ = cKDTree(sc).query(cc, distance_upper_bound=a.far * 2)
    d_sc, _ = cKDTree(cc).query(sc, distance_upper_bound=a.far * 2)
    cand = cc[(d_cs > a.far) & box(cc, cb)]
    om = (d_sc > a.far) & box(sc, ob)
    if a.outside:
        cell = 40.0
        key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
        u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
        ks = key(sc[:, :2]); i = np.clip(np.searchsorted(u, ks), 0, len(u) - 1)
        roof = np.where(u[i] == ks, top[i], -1e9)
        om &= sc[:, 2] > roof + 30
    openp = sc[om]
    print("closed candidates", len(cand), "open panel pts", len(openp))
    rng = np.random.default_rng(0)
    H = cand[rng.choice(len(cand), min(2500, len(cand)), replace=False)]
    T = cKDTree(openp[rng.choice(len(openp), min(60000, len(openp)), replace=False)])  # fit tree (subsampled)
    TF = cKDTree(openp)  # full tree for landing the panel

    def cost(p):
        d, _ = T.query(xf(H, p[:3], axis_of(p[3], p[4]), p[5]))
        return np.mean(np.minimum(d, 60))

    lo, hi = cand.min(0), cand.max(0)
    pivs = [np.array([x, y, z]) for x in np.linspace(lo[0], hi[0], 3) for y in np.linspace(lo[1], hi[1], 3)
            for z in np.linspace(lo[2], hi[2], 2)]
    dirs = []  # hemisphere of axis directions (sign folded into the angle)
    for th in np.radians(np.arange(10, 171, 20)):
        for ph in np.radians(np.arange(0, 180, 20)):
            dirs.append((th, ph))
    dirs.append((0.0, 0.0))
    grid = []
    for th, ph in dirs:
        ax = axis_of(th, ph)
        for pv in pivs:
            for ang in range(-120, 121, 15):
                if ang == 0: continue
                d, _ = T.query(xf(H[::6], pv, ax, ang), distance_upper_bound=60)
                grid.append((np.mean(np.minimum(d, 60)), pv, th, ph, ang))
    grid.sort(key=lambda g: g[0])
    print("grid best", [(round(g[0], 1), np.degrees([g[2], g[3]]).round(), g[4]) for g in grid[:4]])
    best = None
    for g in grid[:6]:
        r = minimize(cost, [*g[1], g[2], g[3], g[4]], method="Nelder-Mead",
                     options={"maxiter": 3000, "xatol": 0.2, "fatol": 0.01})
        if best is None or r.fun < best.fun: best = r
    p = best.x; ax = axis_of(p[3], p[4]); ang = p[5]
    # make the pivot the point on the axis nearest the panel centroid (any point on the axis is equivalent)
    cen = cand.mean(0); piv = p[:3] + ax * ((cen - p[:3]) @ ax)
    # outer skin = car tris that land on the open capture
    land, _ = TF.query(xf(cc, piv, ax, ang), distance_upper_bound=a.land * 2)
    outer = (land < a.land) & (d_cs > a.far * 0.5)
    if a.land_loose:  # skin strips where the fit is weaker (hood nose) would otherwise stay behind on the base
        outer |= (land < a.land_loose) & (d_cs > a.far) & box(cc, cb)
    dmed, _ = TF.query(xf(cc[outer], piv, ax, ang)); fit_med = float(np.median(dmed))
    print("fit cost %.2f mm; outer tris %d; axis %s angle %.1f; landing median %.2f mm" % (best.fun, outer.sum(), ax.round(3), ang, fit_med))
    # inner skin = the state's open-panel tris that are not the outer skin (hood frame, door trim), swung back closed
    d_o, _ = cKDTree(xf(cc[outer], piv, ax, ang)).query(sc, distance_upper_bound=200)
    inner = om & (d_o > 6) & (d_o < 120)
    back = st[inner].copy()
    R = Rot.from_rotvec(np.radians(-ang) * ax).as_matrix()
    back["v"] = (((back["v"].reshape(-1, 3).astype(float) - piv) @ R.T) + piv).reshape(-1, 3, 3).astype(np.float32)
    back["n"] = (back["n"].astype(float) @ R.T).astype(np.float32)
    if a.inner_below:
        bc = back["v"].mean(1).astype(float); oc = cc[outer]
        _, j = cKDTree(oc[:, :2]).query(bc[:, :2])
        below = bc[:, 2] < oc[j, 2] - 3
        idx = np.where(inner)[0]; inner = np.zeros_like(inner); inner[idx[below]] = True; back = back[below]
    save(C + a.name + "_panel.stl", np.concatenate([car[outer], back]))
    print("panel = outer %d + inner %d (from the open capture)" % (outer.sum(), inner.sum()))
    np.savez_compressed(C + a.name + "_masks.npz", outer=outer, drop=om | (d_o < 25), state=a.state)
    like = json.load(open(LIKE)); s, rl = like["unit_scale"], np.array(like["root_location"])
    out = {"pivot": (piv * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(ang), "fit_median_mm": fit_med,
           "fit_cost_mm": float(best.fun), "outer_tris": int(outer.sum()), "inner_tris": int(inner.sum())}
    json.dump(out, open(C + a.name + "_hinge.json", "w"), indent=1)
    print(json.dumps(out))


def base(argv):
    """base out.stl name [name ...]: full car minus every named outer panel + each named state's tris that the trimmed
    car lacks (> 8 mm), with every named open panel (and the region around it) dropped."""
    out, names = argv[0], argv[1:]
    car = load(C + "car3.stl"); keep = np.ones(len(car), bool)
    states = {}
    for n in names:
        m = np.load(C + n + "_masks.npz")
        keep &= ~m["outer"]
        st = str(m["state"]); states.setdefault(st, np.zeros(len(m["drop"]), bool))
        states[st] |= m["drop"]
    kc = car[keep]; tk = cKDTree(kc["v"].mean(1)); pieces = [kc]
    for st, drop in states.items():
        m = load(C + st); d, _ = tk.query(m["v"].mean(1), distance_upper_bound=20)
        add = (d > 8) & ~drop; pieces.append(m[add]); print(st, "adds", int(add.sum()))
    save(out, np.concatenate(pieces)); print(out, "car kept", int(keep.sum()), "of", len(car))


if __name__ == "__main__":
    import sys
    if sys.argv[1] == "base":
        base(sys.argv[2:])
    else:
        main()
