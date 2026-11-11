"""Fit each caliper onto its (already placed) rotor: rotation search that makes the caliper straddle the disc
ring with the fewest points inside the disc, bridge 20 mm outside the disc edge, clocked 20 deg above rear.
    python projects/a90-supra/tools/fit_caliper.py /home/user/media/work/a90/corners
Overwrites <corner>_caliper.stl and records the fit in corners.json."""
import json, struct, sys
import numpy as np
from scipy.spatial.transform import Rotation

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
S = "/home/user/media/a90-supra/scans2/"
D = sys.argv[1]
J = json.load(open(f"{D}/corners.json"))
rng = np.random.default_rng(0)

for c in ("FR", "FL", "RR", "RL"):
    side = -1 if c[1] == "R" else 1
    hub = np.array(J[c]["wheel"]["hub_face"])
    rot = np.fromfile(f"{D}/{c}_rotor.stl", dtype=TRI, offset=84)["v"].reshape(-1, 3).astype(float)
    d = rot - hub; rr = np.hypot(d[:, 0], d[:, 2]); ra = d[:, 1] * side
    rmax = np.percentile(rr, 99.7); band = rr > rmax - 40
    a0, a1 = np.percentile(ra[band], [2, 98]); amid = (a0 + a1) / 2
    rin = rmax - 55                                   # friction ring inner radius (approx)
    src = S + ("fsusp/FR Caliper (118k).stl" if c[0] == "F" else "rsusp/Rear Caliper (144k).stl")
    C = np.fromfile(src, dtype=TRI, offset=84)
    P = C["v"].reshape(-1, 3).astype(float)
    if c[1] == "L":
        P[:, 1] *= -1
    P0 = P - P.mean(0)
    samp = P0[rng.choice(len(P0), 4000, replace=False)]
    ang = np.radians(20)
    u = np.array([-np.cos(ang), 0, np.sin(ang)])     # radial (rearward, 20 deg up)
    w = np.array([0, side, 0.0])                      # axial outboard
    v = np.cross(w, u)

    def place(Rm, pts):
        Q = pts @ Rm.T
        qu, qv, qw = Q @ u, Q @ v, Q @ w
        t = hub + u * (rmax + 20 - qu.max()) - v * qv.mean() + w * (amid - qw.mean())
        return t

    def score(Rm):
        t = place(Rm, samp); Q = samp @ Rm.T + t
        dd = Q - hub; r = np.hypot(dd[:, 0], dd[:, 2]); a = dd[:, 1] * side
        inside = ((r > rin) & (r < rmax) & (a > a0) & (a < a1)).mean()
        near = (r > rin - 10)
        both = min(((a > a1) & near).mean(), ((a < a0) & near).mean())
        return inside * 10 - both

    # constrained search: the caliper's axle-direction axis comes from its shape (front: piston pairs face each
    # other across the slot along local y; rear: piston bore along local z), then spin / sense / axial offset
    k = np.array([0, 1.0, 0]) if c[0] == "F" else np.array([0, 0, 1.0])
    if c[1] == "L":
        k = k * [1, -1, 1]
    best = (1e9, None)
    for sgn in (1, -1):
        base = Rotation.align_vectors([w], [sgn * k])[0].as_matrix()
        for th in np.radians(np.arange(0, 360, 4)):
            Rm = Rotation.from_rotvec(w * th).as_matrix() @ base
            for off in range(-40, 41, 5):
                t = place(Rm, samp) + w * off; Q = samp @ Rm.T + t
                dd = Q - hub; r = np.hypot(dd[:, 0], dd[:, 2]); a = dd[:, 1] * side
                inside = ((r > rin) & (r < rmax) & (a > a0) & (a < a1)).mean()
                near = r > rin - 10
                both = min(((a > a1) & near).mean(), ((a < a0) & near).mean())
                sc = inside * 10 - both
                if sc < best[0]:
                    best = (sc, Rm, off)
    _, Rb0, off0 = best
    best = [Rb0]
    Rb = best[0]; tb = place(Rb, P0) + w * off0
    V = (P0 @ Rb.T + tb).reshape(-1, 3, 3).astype(np.float32)
    if c[1] == "L":
        V = V[:, ::-1]
    m = C.copy(); m["v"] = V
    n = np.cross(V[:, 1] - V[:, 0], V[:, 2] - V[:, 0]); m["n"] = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
    with open(f"{D}/{c}_caliper.stl", "wb") as f:
        f.write(b"ive caliper".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
    dd = (P0 @ Rb.T + tb) - hub; r = np.hypot(dd[:, 0], dd[:, 2]); a = dd[:, 1] * side
    inside = int(((r > rin) & (r < rmax) & (a > a0 + 1) & (a < a1 - 1)).sum())
    J[c]["caliper"] = {"fit": "rotation search straddling the disc ring", "pts_inside_disc": inside, "of": len(P0),
                       "radial_mm": np.percentile(r, [2, 98]).round(0).tolist(), "axial_mm": np.percentile(a, [2, 98]).round(0).tolist(),
                       "disc_axial_mm": [round(a0), round(a1)], "disc_r": round(rmax)}
    print(c, J[c]["caliper"])
json.dump(J, open(f"{D}/corners.json", "w"), indent=1)
