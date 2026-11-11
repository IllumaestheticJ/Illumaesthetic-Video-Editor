"""Level the Huracan scan frame: fit the scanned ground plane (RANSAC) on the full car, make its normal +Z,
yaw the car's long axis onto +Y (front = +Y), and write one rigid transform (R, t in mm) that every
part scan gets too (same frame, so parts stay registered). 
  level.py fit full.stl transform.json
  level.py apply transform.json in.stl out.stl     (streams; works on the 1.25 GB raw STL)"""
import json, struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])

def fit(path, out):
    c = np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    rng = np.random.default_rng(0)
    # candidate ground: lowest 30 % along the rough up axis (+Z here)
    low = c[c[:, 2] < np.percentile(c[:, 2], 30)]
    best, bn, bd = 0, None, None
    for _ in range(3000):
        p = low[rng.choice(len(low), 3, replace=False)]
        n = np.cross(p[1] - p[0], p[2] - p[0]); L = np.linalg.norm(n)
        if L < 1e-6: continue
        n /= L
        if abs(n[2]) < 0.8: continue
        d = -n @ p[0]
        inl = np.abs(low @ n + d) < 6
        if inl.sum() > best: best, bn, bd = inl.sum(), n, d
    inl = np.abs(low @ bn + bd) < 6
    P = low[inl]; cen = P.mean(0)
    n = np.linalg.svd(P - cen, full_matrices=False)[2][2]
    if n[2] < 0: n = -n
    # rotation taking n -> +Z
    z = np.array([0, 0, 1.0]); v = np.cross(n, z); s = np.linalg.norm(v); cth = n @ z
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R1 = np.eye(3) + vx + vx @ vx * ((1 - cth) / s ** 2)
    q = (c - cen) @ R1.T
    body = q[(q[:, 2] > 250)]  # above wheel hubs: car only, no ground
    xy = body[:, :2] - body[:, :2].mean(0)
    e = np.linalg.eigh(np.cov(xy.T))[1][:, -1]  # long axis
    ang = np.arctan2(e[0], e[1])
    Rz = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
    R = Rz @ R1
    q = (c - cen) @ R.T
    body = q[q[:, 2] > 250]
    print("long-axis check: y-extent", np.ptp(body[:, 1]).round(), "x-extent", np.ptp(body[:, 0]).round())
    json.dump({"R": R.tolist(), "origin": cen.tolist(), "ground_inliers": int(best), "ground_normal": n.tolist()}, open(out, "w"), indent=1)
    print(out, "ground inliers", best, "normal", n.round(4))

def apply(tj, src, dst, flip=False):
    T = json.load(open(tj)); R = np.array(T["R"]); o = np.array(T["origin"])
    if T.get("flip_y"): R = np.diag([-1, -1, 1.0]) @ R
    m = np.memmap(src, dtype=TRI, mode="r", offset=84)
    out = open(dst, "wb"); out.write(b"ive level".ljust(80)); out.write(struct.pack("<I", len(m)))
    for i in range(0, len(m), 2_000_000):
        ch = np.array(m[i:i + 2_000_000])
        v = (ch["v"].reshape(-1, 3).astype(np.float64) - o) @ R.T
        ch["v"] = v.reshape(-1, 3, 3).astype(np.float32)
        ch["n"] = (ch["n"].astype(np.float64) @ R.T).astype(np.float32)
        ch.tofile(out)
    out.close(); print(dst)

if __name__ == "__main__":
    if sys.argv[1] == "fit": fit(sys.argv[2], sys.argv[3])
    else: apply(sys.argv[2], sys.argv[3], sys.argv[4])
