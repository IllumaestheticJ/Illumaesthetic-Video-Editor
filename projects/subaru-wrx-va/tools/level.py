"""Level the WRX VA scan frame (adapted from projects/huracan-evo/tools/level.py, nose = +X here so the
A90 shot renderer's az convention applies: az 0 = at the nose, 90 = car's left side).

  level.py fit full.stl level.json        RANSAC ground plane -> +Z, long axis -> X, nose -> +X (the STI wing is at
                                           the rear: the end whose top 5 % sits higher is the tail)
  level.py apply level.json in.stl out.stl [T.json]   streams (works on 1.25 GB raw STLs); optional extra 4x4 (mm,
                                           raw part -> raw car frame) applied first for scans from other sessions
Output stays in mm, origin = ground plane under the body centre.
"""
import json
import struct
import sys

import numpy as np

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def fit(path, out):
    c = np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    rng = np.random.default_rng(0)
    low = c[c[:, 2] < np.percentile(c[:, 2], 30)]
    best, bn, bd = 0, None, None
    for _ in range(4000):
        p = low[rng.choice(len(low), 3, replace=False)]
        n = np.cross(p[1] - p[0], p[2] - p[0]); L = np.linalg.norm(n)
        if L < 1e-6:
            continue
        n /= L
        if abs(n[2]) < 0.8:
            continue
        d = -n @ p[0]
        inl = np.abs(low @ n + d) < 6
        if inl.sum() > best:
            best, bn, bd = inl.sum(), n, d
    inl = np.abs(low @ bn + bd) < 6
    P = low[inl]; cen = P.mean(0)
    n = np.linalg.svd(P - cen, full_matrices=False)[2][2]
    if n[2] < 0:
        n = -n
    z = np.array([0, 0, 1.0]); v = np.cross(n, z); s = np.linalg.norm(v); cth = n @ z
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R1 = np.eye(3) + vx + vx @ vx * ((1 - cth) / s ** 2)
    q = (c - cen) @ R1.T
    body = q[q[:, 2] > 300]
    xy = body[:, :2] - body[:, :2].mean(0)
    e = np.linalg.eigh(np.cov(xy.T))[1][:, -1]
    ang = -np.arctan2(e[1], e[0])  # long axis -> +X
    Rz = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
    R = Rz @ R1
    q = (c - cen) @ R.T
    body = q[q[:, 2] > 300]
    mid = np.median(body[:, :2], 0)
    xs = body[:, 0] - mid[0]
    L = np.ptp(xs)
    top_f = np.percentile(body[xs > 0.3 * L / 2, 2], 99)
    top_r = np.percentile(body[xs < -0.3 * L / 2, 2], 99)
    if top_f > top_r:  # wing end must be -X
        R = np.diag([-1, -1, 1.0]) @ R
    q = (c - cen) @ R.T
    body = q[q[:, 2] > 300]
    off = np.array([*np.median(body[:, :2], 0), 0.0])  # centre the body in XY
    o = cen + R.T @ off
    print("extent x", np.ptp(body[:, 0]).round(), "y", np.ptp(body[:, 1]).round(), "z", body[:, 2].max().round(),
          "tops f/r", round(top_f), round(top_r))
    json.dump({"R": R.tolist(), "origin": o.tolist(), "ground_inliers": int(best), "ground_normal": n.tolist()},
              open(out, "w"), indent=1)
    print(out, "ground inliers", best)


def apply(tj, src, dst, extra=None):
    T = json.load(open(tj)); R = np.array(T["R"]); o = np.array(T["origin"])
    X = np.array(json.load(open(extra))["T_part_to_car_mm"]) if extra else np.eye(4)
    m = np.memmap(src, dtype=TRI, mode="r", offset=84)
    out = open(dst, "wb"); out.write(b"ive level".ljust(80)); out.write(struct.pack("<I", len(m)))
    for i in range(0, len(m), 2_000_000):
        ch = np.array(m[i:i + 2_000_000])
        v = ch["v"].reshape(-1, 3).astype(np.float64) @ X[:3, :3].T + X[:3, 3]
        v = (v - o) @ R.T
        ch["v"] = v.reshape(-1, 3, 3).astype(np.float32)
        ch["n"] = (ch["n"].astype(np.float64) @ (R @ X[:3, :3]).T).astype(np.float32)
        ch.tofile(out)
    out.close(); print(dst, len(m))


if __name__ == "__main__":
    if sys.argv[1] == "fit":
        fit(sys.argv[2], sys.argv[3])
    else:
        apply(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
