"""Level the GR86 scan frame (raw Artec mm): RANSAC the scanned ground plane with no up-axis assumption
(the raw frame is arbitrary), make its normal +Z (car side up), yaw the long axis onto Y with the nose at -Y
(house convention, same as huracan-evo/ferrari-296), ground at z=0. One rigid transform for every state scan.
  level.py fit full.stl transform.json [--flip]     (--flip: turn 180 deg about Z if the nose ends up at +Y)
  level.py apply transform.json in.stl out.stl      (streams GB files)"""
import json, struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def fit(path, out, flip=False):
    c = np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    rng = np.random.default_rng(0)
    s = c[rng.choice(len(c), min(400000, len(c)), replace=False)]
    best, bn, bd = 0, None, None
    for _ in range(4000):
        p = s[rng.choice(len(s), 3, replace=False)]
        n = np.cross(p[1] - p[0], p[2] - p[0]); L = np.linalg.norm(n)
        if L < 1e-6: continue
        n /= L; d = -n @ p[0]
        inl = (np.abs(s @ n + d) < 6).sum()
        if inl > best: best, bn, bd = inl, n, d
    inl = np.abs(s @ bn + bd) < 6
    P = s[inl]; cen = P.mean(0)
    n = np.linalg.svd(P - cen, full_matrices=False)[2][2]
    # car side up: most off-plane points on the positive side
    h = (s - cen) @ n
    if (h > 50).sum() < (h < -50).sum(): n = -n
    z = np.array([0, 0, 1.0]); v = np.cross(n, z); sv = np.linalg.norm(v); cth = n @ z
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R1 = np.eye(3) + vx + vx @ vx * ((1 - cth) / max(sv, 1e-12) ** 2)
    q = (c - cen) @ R1.T
    body = q[q[:, 2] > 250]
    xy = body[:, :2] - body[:, :2].mean(0)
    e = np.linalg.eigh(np.cov(xy.T))[1][:, -1]
    ang = np.arctan2(e[0], e[1])
    Rz = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
    R = Rz @ R1
    if flip: R = np.diag([-1, -1, 1.0]) @ R
    q = (c - cen) @ R.T
    body = q[q[:, 2] > 250]
    o = cen.copy()
    print("inliers", best, "normal", n.round(4), "body x", body[:, 0].min().round(), body[:, 0].max().round(),
          "y", body[:, 1].min().round(), body[:, 1].max().round(), "z max", body[:, 2].max().round())
    json.dump({"R": R.tolist(), "origin": o.tolist(), "ground_inliers": int(best), "ground_normal": n.tolist()},
              open(out, "w"), indent=1)


def apply(tj, src, dst):
    T = json.load(open(tj)); R = np.array(T["R"]); o = np.array(T["origin"])
    m = np.memmap(src, dtype=TRI, mode="r", offset=84)
    out = open(dst, "wb"); out.write(b"ive level gr86".ljust(80)); out.write(struct.pack("<I", len(m)))
    for i in range(0, len(m), 2_000_000):
        ch = np.array(m[i:i + 2_000_000])
        ch["v"] = ((ch["v"].reshape(-1, 3).astype(np.float64) - o) @ R.T).reshape(-1, 3, 3).astype(np.float32)
        ch["n"] = (ch["n"].astype(np.float64) @ R.T).astype(np.float32)
        ch.tofile(out)
    out.close(); print(dst)


if __name__ == "__main__":
    if sys.argv[1] == "fit": fit(sys.argv[2], sys.argv[3], "--flip" in sys.argv)
    else: apply(sys.argv[2], sys.argv[3], sys.argv[4])
