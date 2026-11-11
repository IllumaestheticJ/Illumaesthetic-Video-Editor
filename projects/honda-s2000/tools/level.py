"""Level the S2000 full-car scan (Artec frame is tilted arbitrarily and has no scanned ground):
PCA -> long axis = Y, height = Z; then a plane through the lowest point of each tyre (4 quadrants) -> Z=0 ground,
yaw re-fit; front direction chosen with --front-sign (+1: nose at -Y after levelling, house convention).
Writes one rigid transform {R, t} (mm -> mm, levelled frame, origin = footprint centre on the ground).
    level.py fit car_4mm.stl level.json [--flip]
    level.py apply level.json in.stl out.stl   (streams)"""
import json, struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def fit(path, out, flip=False, up_flip=False):
    c = np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    mu = c.mean(0)
    w, V = np.linalg.eigh(np.cov((c - mu).T))
    # eigh ascending: V[:,0] smallest (height), V[:,2] largest (length)
    R = np.stack([np.cross(V[:, 2], V[:, 0]), V[:, 2], V[:, 0]])  # rows: x(width), y(length), z(up)
    q = (c - mu) @ R.T
    # up sign: the roof (top) is narrower than the floor/sills -> width of top 15 % slab < bottom 15 % slab
    top = q[q[:, 2] > np.percentile(q[:, 2], 85)]; bot = q[q[:, 2] < np.percentile(q[:, 2], 15)]
    if np.ptp(top[:, 0]) > np.ptp(bot[:, 0]):
        R = np.diag([-1, 1, -1.0]) @ R
    if up_flip:
        R = np.diag([-1, 1, -1.0]) @ R
    for it in range(3):
        q = (c - mu) @ R.T
        # tyre bottoms: lowest point per quadrant
        pts = []
        for sx in (-1, 1):
            for sy in (-1, 1):
                Q = q[(np.sign(q[:, 0]) == sx) & (np.sign(q[:, 1]) == sy) & (np.abs(q[:, 1]) > 600)]
                k = Q[np.argsort(Q[:, 2])[:200]]
                pts.append(k.mean(0))
        P = np.array(pts)
        A = np.c_[P[:, 0], P[:, 1], np.ones(4)]
        a, b, _ = np.linalg.lstsq(A, P[:, 2], rcond=None)[0]
        n = np.array([-a, -b, 1.0]); n /= np.linalg.norm(n)
        z = np.array([0, 0, 1.0]); v = np.cross(n, z); s = np.linalg.norm(v)
        if s > 1e-9:
            vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            R = (np.eye(3) + vx + vx @ vx * ((1 - n @ z) / s ** 2)) @ R
        q = (c - mu) @ R.T
        body = q[q[:, 2] > np.percentile(q[:, 2], 40)]
        xy = body[:, :2] - body[:, :2].mean(0)
        e = np.linalg.eigh(np.cov(xy.T))[1][:, -1]
        ang = np.arctan2(e[0], e[1])
        Rz = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
        R = Rz @ R
        print("iter", it, "tyre pts z", np.round(P[:, 2], 1), "yaw corr deg", round(np.degrees(ang), 3))
    if flip:
        R = np.diag([-1, -1, 1.0]) @ R
    q = (c - mu) @ R.T
    lo, hi = q.min(0), q.max(0)
    ground = np.median(np.sort(q[:, 2])[:2000])
    t = -np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, ground]) - (R @ mu)
    q2 = c @ R.T + t
    print("levelled size mm", np.round(q2.max(0) - q2.min(0)), "zmin", q2[:, 2].min().round(1))
    json.dump({"R": R.tolist(), "t": t.tolist()}, open(out, "w"), indent=1)


def apply(tj, src, dst):
    T = json.load(open(tj)); R = np.array(T["R"]); t = np.array(T["t"])
    m = np.memmap(src, dtype=TRI, mode="r", offset=84)
    out = open(dst, "wb"); out.write(b"ive level s2k".ljust(80)); out.write(struct.pack("<I", len(m)))
    for i in range(0, len(m), 2_000_000):
        ch = np.array(m[i:i + 2_000_000])
        ch["v"] = (ch["v"].reshape(-1, 3).astype(np.float64) @ R.T + t).reshape(-1, 3, 3).astype(np.float32)
        ch["n"] = (ch["n"].astype(np.float64) @ R.T).astype(np.float32)
        ch.tofile(out)
    out.close(); print(dst, len(m))


if __name__ == "__main__":
    if sys.argv[1] == "fit": fit(sys.argv[2], sys.argv[3], "--flip" in sys.argv, "--up-flip" in sys.argv)
    else: apply(sys.argv[2], sys.argv[3], sys.argv[4])
