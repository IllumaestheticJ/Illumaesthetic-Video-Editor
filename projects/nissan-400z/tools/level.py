"""Level the 400Z Artec frame (no scanned ground: the full car was exported clean).
fit: yaw the long axis (PCA of the body above the hubs) onto Y with the nose (Bumper Only scan) at -Y,
     then tilt so the plane through the 4 tyre contact patches is horizontal. One rigid transform (R, origin in mm).
apply: streams any STL in the same Artec frame through it (all 400Z state scans share the frame: regcheck).
  level.py fit full.stl bumper_only.stl level.json
  level.py apply level.json in.stl out.stl"""
import json, struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def cent(p):
    return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)


def rot_to(a, b):
    a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
    v = np.cross(a, b); s = np.linalg.norm(v); c = a @ b
    if s < 1e-12:
        return np.eye(3)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * ((1 - c) / s ** 2)


def fit(car_p, bumper_p, out):
    c = cent(car_p)
    o = c[c[:, 2] > np.percentile(c[:, 2], 30)].mean(0)
    body = c[c[:, 2] > -600] - o
    e = np.linalg.eigh(np.cov(body[:, :2].T))[1][:, -1]
    ang = np.arctan2(e[0], e[1])
    Rz = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
    if ((cent(bumper_p) - o) @ Rz.T)[:, 1].mean() > 0:  # nose to -Y
        Rz = np.diag([-1, -1, 1.0]) @ Rz
    q = (c - o) @ Rz.T
    pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            m = (np.sign(q[:, 0]) == sx) & (np.sign(q[:, 1]) == sy) & (np.abs(q[:, 1]) > 800)
            z = q[m, 2]
            pts.append(q[m][z < np.percentile(z, 0.05)].mean(0))
    P = np.array(pts)
    A = np.c_[P[:, 0], P[:, 1], np.ones(4)]
    a, b, _ = np.linalg.lstsq(A, P[:, 2], rcond=None)[0]
    n = np.array([-a, -b, 1.0])
    R = rot_to(n, np.array([0, 0, 1.0])) @ Rz
    q = (c - o) @ R.T
    print("tyre contacts (mm)", P.round(), "tilt corr deg", np.degrees(np.arccos(n[2] / np.linalg.norm(n))).round(2))
    print("levelled extents", np.ptp(q, 0).round())
    json.dump({"R": R.tolist(), "origin": o.tolist(), "tyre_contacts": P.tolist()}, open(out, "w"), indent=1)


def apply(tj, src, dst):
    T = json.load(open(tj)); R = np.array(T["R"]); o = np.array(T["origin"])
    m = np.memmap(src, dtype=TRI, mode="r", offset=84)
    out = open(dst, "wb"); out.write(b"ive level 400z".ljust(80)); out.write(struct.pack("<I", len(m)))
    for i in range(0, len(m), 2_000_000):
        ch = np.array(m[i:i + 2_000_000])
        ch["v"] = ((ch["v"].reshape(-1, 3).astype(np.float64) - o) @ R.T).reshape(-1, 3, 3).astype(np.float32)
        ch["n"] = (ch["n"].astype(np.float64) @ R.T).astype(np.float32)
        ch.tofile(out)
    out.close(); print(dst)


if __name__ == "__main__":
    if sys.argv[1] == "fit":
        fit(*sys.argv[2:5])
    else:
        apply(*sys.argv[2:5])
