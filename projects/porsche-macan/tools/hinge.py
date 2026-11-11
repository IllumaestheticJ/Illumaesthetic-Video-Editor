"""Fit a panel hinge from two Artec state scans (adapted from huracan-evo/tools/hinge.py).

    python projects/porsche-macan/tools/hinge.py out.json --closed closed.stl --open open.stl \
        [--part part.stl] --zone "x0,x1,y0,y1,z0,z1" --like car4.json [--sep 25]

All STLs in the same levelled mm frame. The panel that moved = points of --closed (or --part) inside --zone that are
> --sep mm from the --open scan; the panel in its open pose = points of --open inside the zone (expanded up/back)
that are > --sep mm from --closed. Fits an axis ~parallel to X (small tilt) through (y_h, z_h) and an angle that
maps closed -> open (mean nearest distance, capped). Writes pivot/axis in the PREPPED frame (m) + open angle, and
saves the moved-panel points mask as <out>.panel.npy (levelled mm) for composites.
"""
import argparse, json
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
load = lambda p: np.unique(np.round(np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(float), 1), axis=0)  # dedupe: clustered meshes repeat centroids


def inbox(c, z):
    return (c[:, 0] > z[0]) & (c[:, 0] < z[1]) & (c[:, 1] > z[2]) & (c[:, 1] < z[3]) & (c[:, 2] > z[4]) & (c[:, 2] < z[5])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--closed", required=True); ap.add_argument("--open", required=True)
    ap.add_argument("--part"); ap.add_argument("--zone", required=True); ap.add_argument("--open-zone")
    ap.add_argument("--like", required=True); ap.add_argument("--sep", type=float, default=25)
    ap.add_argument("--above", type=float, help="open panel must be this many mm above the closed surface")
    a = ap.parse_args()
    z = [float(v) for v in a.zone.split(",")]
    oz = [float(v) for v in (a.open_zone or a.zone).split(",")]
    closed, opn = load(a.closed), load(a.open)
    src = load(a.part) if a.part else closed
    src = src[inbox(src, z)]
    o = opn[inbox(opn, oz)]
    d, _ = cKDTree(o).query(src, distance_upper_bound=a.sep * 2); panel = src[d > a.sep] if not a.part else src
    cz = closed[inbox(closed, oz)]
    d, _ = cKDTree(cz).query(o, distance_upper_bound=a.sep * 2); openp = o[d > a.sep]
    if a.above is not None:  # open panel = above the closed car's top surface (40 mm cells), not the bay under it
        cell = 40.0
        k = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
        u, inv = np.unique(k(cz[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cz[:, 2])
        ko = k(openp[:, :2]); i = np.clip(np.searchsorted(u, ko), 0, len(u) - 1); roof = np.where(u[i] == ko, top[i], -1e9)
        openp = openp[openp[:, 2] > roof + a.above]
    print("panel pts", len(panel), "open pts", len(openp), flush=True); np.save(a.out + ".open.npy", openp)
    if len(panel) > 200000: panel = panel[np.random.default_rng(1).choice(len(panel), 200000, replace=False)]
    rng = np.random.default_rng(0)
    H = panel[rng.choice(len(panel), min(3000, len(panel)), replace=False)]
    T = cKDTree(openp)

    def xf(p, P):
        yh, zh, ang, tz, ty = p
        ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
        R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
        return (P - c) @ R.T + c

    cost = lambda p: np.mean(np.minimum(T.query(xf(p, H), distance_upper_bound=60)[0], 60))
    # hinge candidates near the panel's ends (front or rear edge, top)
    ys = [H[:, 1].min(), H[:, 1].max()]
    grid = []
    for y0 in ys:
        z0 = H[np.abs(H[:, 1] - y0) < 80][:, 2].mean()
        for ang in range(-100, 101, 5):
            for dy in (-150, 0, 150):
                for dz in (-100, 0, 100):
                    grid.append((cost([y0 + dy, z0 + dz, ang, 0, 0]), [y0 + dy, z0 + dz, ang, 0, 0]))
    grid.sort(key=lambda g: g[0]); print("grid best", round(grid[0][0], 1), np.round(grid[0][1], 1))
    best = None
    for c0, x0 in grid[:4]:
        r = minimize(cost, x0, method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.5, "fatol": 0.02})
        if best is None or r.fun < best.fun: best = r
    p = best.x; d, _ = T.query(xf(p, H), distance_upper_bound=200)
    like = json.load(open(a.like)); s, rl = like["unit_scale"], np.array(like["root_location"])
    ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
    out = {"pivot": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]),
           "fit_mean_mm": float(best.fun), "fit_median_mm": float(np.median(d)), "panel_pts": int(len(panel)),
           "open_pts": int(len(openp))}
    json.dump(out, open(a.out, "w"), indent=1); np.save(a.out + ".panel.npy", panel); np.save(a.out + ".open.npy", openp)
    print(out)


if __name__ == "__main__":
    main()
