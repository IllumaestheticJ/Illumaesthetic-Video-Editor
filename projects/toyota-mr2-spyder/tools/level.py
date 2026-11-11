"""Level the MR2 scan frame (the 2023 Full Car export has no ground plane, so huracan-evo/tools/level.py's RANSAC
ground fit has nothing to lock to). Ground = plane through the lowest tyre points of the four wheel quadrants;
long axis -> +/-Y via PCA above wheel-hub height; nose direction chosen with --nose (+y or -y after yaw).
Writes {R, origin} in mm compatible with projects/huracan-evo/tools/level.py `apply`.
  level.py fit full.stl transform.json [--flip]"""
import json, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])

def rot_to(n, z=np.array([0, 0, 1.0])):
    v = np.cross(n, z); s = np.linalg.norm(v); c = n @ z
    if s < 1e-9: return np.eye(3)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * ((1 - c) / s ** 2)

def fit(path, out, flip=False):
    c = np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    cen = np.median(c, 0)
    R = np.eye(3)
    for it in range(3):
        q = (c - cen) @ R.T
        zlo = np.percentile(q[:, 2], 0.2)
        body = q[q[:, 2] > zlo + 350]
        xy = body[:, :2] - body[:, :2].mean(0)
        e = np.linalg.eigh(np.cov(xy.T))[1][:, -1]
        ang = np.arctan2(e[0], e[1])
        Rz = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
        R = Rz @ R
        q = (c - cen) @ R.T
        # four quadrants: lowest 300 pts each = tyre contact patches
        mx, my = np.median(q[:, 0]), np.median(q[:, 1])
        P = []
        for sx in (-1, 1):
            for sy in (-1, 1):
                m = ((q[:, 0] - mx) * sx > 300) & ((q[:, 1] - my) * sy > 600)
                qq = q[m]; P.append(qq[np.argsort(qq[:, 2])[:300]].mean(0))
        P = np.array(P); pc = P.mean(0)
        n = np.linalg.svd(P - pc)[2][2]
        if n[2] < 0: n = -n
        print("iter", it, "ground normal", n.round(4), "contact z spread", np.ptp(P[:, 2]).round(1))
        R = rot_to(n) @ R
    q = (c - cen) @ R.T
    if flip:
        R = np.diag([-1, -1, 1.0]) @ R; q = (c - cen) @ R.T
    z0 = np.mean(sorted(q[:, 2])[:2000])
    origin = cen + R.T @ np.array([0, 0, z0])
    q = (c - origin) @ R.T
    body = q[q[:, 2] > 300]
    print("extent x", np.ptp(body[:, 0]).round(), "y", np.ptp(body[:, 1]).round(), "z", q[:, 2].max().round())
    json.dump({"R": R.tolist(), "origin": origin.tolist()}, open(out, "w"), indent=1)

if __name__ == "__main__":
    fit(sys.argv[2], sys.argv[3], "--flip" in sys.argv)
