"""Clipping check: does any moving part pass through the car body? Samples every part's keyed path (same easing as
tools/shot.py) at 120 Hz and reports, per part, the worst fraction of its points within --tol m of the body while the part
is more than 3 cm from home.   python projects/porsche-gt3rs-992/tools/clipcheck.py spec.json [spec.json ...] [--tol 0.008]"""
import json, math, os, sys
import numpy as np
from scipy.spatial import cKDTree
W = "/home/user/media/porsche-gt3rs-992"
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array(json.load(open(f"{W}/prep/car4.json"))["root_location"])
SRC = {"comp_v2": f"{W}/dec/comp_v2.stl", "comp_v3": f"{W}/dec/comp_v3.stl", "comp_explode4": f"{W}/dec/comp_explode4.stl", "car4": f"{W}/dec/carL_4mm_crop.stl"}


def pts(stl, step=1):
    v = np.fromfile(stl, dtype=TRI, offset=84)["v"]
    return v.reshape(-1, 3)[::step].astype(np.float64) * 0.001 + ROOT


def ease(t, k):
    t = min(1.0, max(0.0, t))
    return {"in": t ** 3, "out": 1 - (1 - t) ** 3, "lin": t, "in2": t * t, "out2": 1 - (1 - t) ** 2}.get(k, t * t * (3 - 2 * t))


def sample(keys, t, f):
    if t <= keys[0]["t"]: return np.array(keys[0][f], float)
    for a, b in zip(keys, keys[1:]):
        if t <= b["t"]:
            u = ease((t - a["t"]) / max(1e-9, b["t"] - a["t"]), b.get("ease", "inout"))
            return np.array(a[f], float) + (np.array(b[f], float) - np.array(a[f], float)) * u
    return np.array(keys[-1][f], float)


def rot(deg):
    x, y, z = (math.radians(d) for d in deg)
    Rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    Rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


args = [a for a in sys.argv[1:] if not a.startswith("--")]
tol = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 0.008
args = [a for a in args if a != str(tol)]
bodies = {}
bad = 0
for sp in args:
    s = json.load(open(sp))
    base = os.path.basename(s["base"][0]).replace(".blend", "")
    if base not in bodies:
        bodies[base] = cKDTree(pts(SRC[base], 2))
    body = bodies[base]
    secs = s["seconds"]
    print(os.path.basename(sp))
    for p in s["parts"]:
        name = os.path.basename(p["blend"])[2:-6]
        P = pts(f"{W}/xp/{name}.stl", 1)
        P = P[np.random.default_rng(0).choice(len(P), min(len(P), 6000), replace=False)]
        piv = (P.min(0) + P.max(0)) / 2
        worst, wt = 0.0, None
        for t in np.arange(0, secs + 1e-6, 1 / 120):
            off = sample(p["keys"], t, "loc")
            if np.linalg.norm(off) < 0.03: continue
            Q = (P - piv) @ rot(sample(p["keys"], t, "rot")).T + piv + off
            d, _ = body.query(Q, distance_upper_bound=tol)
            frac = float(np.mean(np.isfinite(d)))
            if frac > worst: worst, wt = frac, t
        flag = "CLIP" if worst > 0.01 else "ok"
        bad += flag == "CLIP"
        print(f"  {name:28s} worst {worst*100:5.1f}% of points within {tol*1000:.0f} mm of the body" + (f" at t={wt:.2f}s" if wt is not None else "") + f"  {flag}")
print("CLIPPING PARTS:", bad)
