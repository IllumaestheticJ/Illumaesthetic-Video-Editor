"""Level the IS300 Artec frame (arbitrary orientation: the car lies diagonally in raw x/y/z).
fit:   long axis (PCA) -> Y with the nose at -Y (nose = end nearer the 'front end bumper removed' scan),
       up = smallest PCA axis, sign chosen so the car is narrower at the top (greenhouse),
       then refine the tilt with a plane through the lowest points of the four tyre patches -> +Z.
       Right-handed (det +1): no mirroring.  Car's right side ends up at -X.
apply: one rigid transform (R, t mm) for the car and every registered part, so all states stay together.
  level.py fit car_4mm.stl front_part.stl level.json
  level.py apply level.json in.stl out.stl [--pre T.json]   (--pre: part->car registration applied first)
"""
import json, struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def cent(p):
    return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)


def fit(car, front, out):
    c = cent(car); m = c.mean(0)
    e, V = np.linalg.eigh(np.cov((c - m).T))
    up, side, lng = V[:, 0], V[:, 1], V[:, 2]
    fc = cent(front).mean(0)
    if (fc - m) @ lng > 0:
        lng = -lng          # +lng now points to the rear
    q = c - m
    h = q @ up
    w = np.abs(q @ side)
    top, bot = w[h > np.percentile(h, 85)].mean(), w[h < np.percentile(h, 30)].mean()
    if top > bot:
        up = -up
    Y = lng  # rear = +Y, nose at -Y
    Z = up - (up @ Y) * Y; Z /= np.linalg.norm(Z)
    X = np.cross(Y, Z)
    R = np.stack([X, Y, Z])  # rows: new axes
    q = (c - m) @ R.T
    # tyre patches: lowest points in each quadrant
    pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            sel = (np.sign(q[:, 0]) == sx) & (np.sign(q[:, 1]) == sy) & (np.abs(q[:, 1]) > 800) & (np.abs(q[:, 1]) < 1800)
            s = q[sel]; s = s[s[:, 2] < np.percentile(s[:, 2], 0.5)]
            pts.append(s.mean(0))
    P = np.array(pts)
    A = np.c_[P[:, 0], P[:, 1], np.ones(4)]
    a, b, _ = np.linalg.lstsq(A, P[:, 2], rcond=None)[0]
    n = np.array([-a, -b, 1.0]); n /= np.linalg.norm(n)
    z = np.array([0, 0, 1.0]); v = np.cross(n, z); s = np.linalg.norm(v); ct = n @ z
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R2 = np.eye(3) + vx + vx @ vx * ((1 - ct) / max(s, 1e-12) ** 2) if s > 1e-9 else np.eye(3)
    R = R2 @ R
    t = -R @ m
    q = c @ R.T + t
    print("tyre patches (pre-refine):", np.round(P, 0).tolist())
    print("tilt refine deg:", round(float(np.degrees(np.arcsin(min(1, s)))), 2), "det", round(float(np.linalg.det(R)), 4))
    print("extent mm:", np.round(q.max(0) - q.min(0)))
    json.dump({"R": R.tolist(), "t_mm": t.tolist()}, open(out, "w"), indent=1)


def apply(js, src, dst, pre=None):
    L = json.load(open(js)); R = np.array(L["R"]); t = np.array(L["t_mm"])
    if pre:
        M = np.array(json.load(open(pre))["T_part_to_car_mm"])
        t = R @ M[:3, 3] + t; R = R @ M[:3, :3]
    m = np.fromfile(src, dtype=TRI, offset=84)
    m["v"] = (m["v"].astype(np.float64) @ R.T + t).astype(np.float32)
    m["n"] = (m["n"].astype(np.float64) @ R.T).astype(np.float32)
    with open(dst, "wb") as f:
        f.write(b"is300 levelled".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
    print("wrote", dst, len(m))


if __name__ == "__main__":
    if sys.argv[1] == "fit":
        fit(*sys.argv[2:5])
    else:
        args = sys.argv[2:]
        pre = None
        if "--pre" in args:
            i = args.index("--pre"); pre = args[i + 1]; args = args[:i] + args[i + 2:]
        apply(*args, pre=pre)
