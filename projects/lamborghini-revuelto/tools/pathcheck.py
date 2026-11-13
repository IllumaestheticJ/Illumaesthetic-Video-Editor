"""Do moving parts pass through the body or through each other? (user on v3: the rear bumper clipped the tail lights
and wing on its way off.) Samples every translated part's keyed path from a shot spec and reports the worst fraction
of its points within TOL of (a) the base and (b) every other part, while it is > 10 cm from home (closer than that it still touches its own seat).
  pathcheck.py shot.json [shot.json ...]      (translation keys only; hinge/spin parts are skipped as movers)"""
import json, os, sys, numpy as np
from scipy.spatial import cKDTree
C = "/home/user/media/lamborghini-revuelto/clean3/"; TOL = 0.008
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def pts(name, n=60000):
    c = np.fromfile(C + name + ".stl", dtype=TRI, offset=84)["v"].mean(1).astype(np.float64) * 0.001
    return c[np.random.default_rng(0).choice(len(c), min(n, len(c)), replace=False)]
def ease(u, k):
    u = min(1, max(0, u)); return {"in": u ** 3, "lin": u}.get(k, u * u * (3 - 2 * u))
def off(keys, t):
    if t <= keys[0]["t"]: return np.array(keys[0]["off"], float)
    for a, b in zip(keys, keys[1:]):
        if t <= b["t"]:
            u = ease((t - a["t"]) / max(1e-9, b["t"] - a["t"]), "in" if b.get("ease") == "in" else ("lin" if b.get("lin") else ""))
            return np.array(a["off"], float) + (np.array(b["off"], float) - np.array(a["off"], float)) * u
    return np.array(keys[-1]["off"], float)
for f in sys.argv[1:]:
    d = json.load(open(f)); names = {k: os.path.basename(v)[:-6] for k, v in d["objects"].items()}
    P = {k: pts(n, 400000 if k == "base" else 60000) for k, n in names.items() if k not in ("car",) and os.path.exists(C + n + ".stl")}
    T = {k: cKDTree(p) for k, p in P.items()}
    an = d.get("anims", {}); worst = {}
    for t in np.linspace(0, 1, 49):
        o = {k: (off(an[k], t) if k in an and "off" in an[k][0] else np.zeros(3)) for k in P}
        for k in P:
            if k == "base" or np.linalg.norm(o[k]) < 0.10: continue
            vis = d.get("visible", {})
            for j in P:
                if j == k or (j in vis and not (vis[j][0] <= t <= vis[j][1])) or (k in vis and not (vis[k][0] <= t <= vis[k][1])): continue
                dd, _ = T[j].query(P[k][::6] + o[k] - o[j], distance_upper_bound=TOL)
                fr = float(np.isfinite(dd).mean())
                if fr > worst.get((k, j), (0, 0))[0]: worst[(k, j)] = (fr, t)
    bad = {p: w for p, w in worst.items() if w[0] > 0.01}
    print(os.path.basename(f), "OK" if not bad else "", " ".join(f"{k}x{j}:{w[0]*100:.1f}%@{w[1]:.2f}" for (k, j), w in sorted(bad.items(), key=lambda x: -x[1][0])))
