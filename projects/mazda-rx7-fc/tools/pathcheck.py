"""Do moving parts pass through the body or through each other? (lamborghini-revuelto lesson, rewritten for this
project's shot.py specs). For every keyed part, sample its pose each frame exactly as shot.py does (eased loc offset +
XYZ euler about its pivot), and report the worst fraction of its points within TOL of the base or of any other part
(at their own poses) while it is more than 10 cm from home.
    pathcheck.py spec.json [spec.json ...]"""
import json, math, os, sys
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot
TOL, HOME = 0.008, 0.10
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def ease(t, kind):
    t = min(1.0, max(0.0, t))
    return {"in": t ** 3, "out": 1 - (1 - t) ** 3, "lin": t, "in2": t * t, "out2": 1 - (1 - t) ** 2}.get(kind, t * t * (3 - 2 * t))


def sample(keys, t, f):
    if t <= keys[0]["t"]:
        return np.array(keys[0][f], float)
    for a, b in zip(keys, keys[1:]):
        if t <= b["t"]:
            k = ease((t - a["t"]) / max(1e-9, b["t"] - a["t"]), b.get("ease", "inout"))
            return np.array(a[f], float) + (np.array(b[f], float) - np.array(a[f], float)) * k
    return np.array(keys[-1][f], float)


def pts(blend, n):
    j = json.load(open(blend[:-6] + ".json"))
    c = np.fromfile(j["sources"][0], dtype=TRI, offset=84)["v"].mean(1).astype(float) * j["unit_scale"] + j["root_location"]
    return c[np.random.default_rng(0).choice(len(c), min(n, len(c)), replace=False)]


for f in sys.argv[1:]:
    d = json.load(open(f)); fps = d.get("fps", 15); nf = int(round(d["seconds"] * fps))
    base = np.concatenate([pts(b, 500000) for b in d["base"]]); TB = cKDTree(base)
    parts = []
    for p in d["parts"]:
        P = pts(p["blend"], 40000)
        piv = np.array(p["pivot"]) if p.get("pivot") else (P.min(0) + P.max(0)) / 2
        parts.append((os.path.basename(p["blend"])[:-6], P, piv, p.get("keys") or [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}]))
    def pose(P, piv, keys, t):
        R = Rot.from_euler("xyz", sample(keys, t, "rot"), degrees=True).as_matrix()
        return (P - piv) @ R.T + piv + sample(keys, t, "loc")
    worst = {}
    for fr in range(0, nf + 1):
        t = fr / fps
        posed = [(n, pose(P, piv, k, t)) for n, P, piv, k in parts]
        trees = {n: cKDTree(Q) for n, Q in posed}
        for (n, P, piv, k), (_, Q) in zip(parts, posed):
            if len(k) < 2:
                continue
            away = np.linalg.norm(Q - P, axis=1) > HOME
            if away.sum() < 50:
                continue
            hits = {"base": (TB.query(Q[away], distance_upper_bound=TOL)[0] < TOL).mean()}
            for m, T in trees.items():
                if m != n:
                    hits[m] = (T.query(Q[away], distance_upper_bound=TOL)[0] < TOL).mean()
            for m, v in hits.items():
                if v > worst.get((n, m), (0, 0))[0]:
                    worst[(n, m)] = (v, round(t, 2))
    print(f"== {os.path.basename(f)}")
    bad = {k: v for k, v in worst.items() if v[0] > 0.002}
    for (n, m), (v, t) in sorted(bad.items(), key=lambda x: -x[1][0]):
        print(f"  {n:14s} through {m:14s} {100 * v:5.1f} % of its points at t={t}")
    if not bad:
        print("  clean (no part > 0.2 % within 8 mm of anything while away from home)")
