"""Level the NC Miata frame (no ground in the scan): yaw the car's long axis (XY PCA) onto Y with the nose
at -Y (house frame, car's right = -X), then tilt so the four tyre contact points sit on one plane z = const.
Writes one rigid 4x4 (mm) that every scan gets, optionally pre-multiplied per scan (e.g. a global-registration
transform for the 2023 trunk scans).
  level.py fit car.stl level.json
  level.py apply level.json in.stl out.stl [--pre T.json]     (streams in chunks; fine on 750 MB raw STLs)"""
import json, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def fit(path, out):
    c = np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    xy = c[:, :2] - c[:, :2].mean(0)
    ev, evec = np.linalg.eigh(np.cov(xy.T))
    ax = evec[:, np.argmax(ev)]                 # long axis in XY
    # nose = the end where the front-state scans sit: +X in the raw frame
    if ax[0] < 0: ax = -ax
    # rotate so ax -> -Y
    ang = np.arctan2(-1, 0) - np.arctan2(ax[1], ax[0])
    ca, sa = np.cos(ang), np.sin(ang)
    Rz = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1.0]])
    p = c @ Rz.T
    # tyre contact points: lowest point in each quadrant (wheels are the lowest geometry; no ground scanned)
    cx, cy = np.median(p[:, 0]), np.median(p[:, 1])
    pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            q = p[(np.sign(p[:, 0] - cx) == sx) & (np.sign(p[:, 1] - cy) == sy)]
            q = q[q[:, 2] < np.percentile(q[:, 2], 0.2)]
            pts.append(q[np.argsort(q[:, 2])[: max(5, len(q) // 10)]].mean(0))
    pts = np.array(pts)
    A = np.c_[pts[:, 0], pts[:, 1], np.ones(4)]
    a, b, _ = np.linalg.lstsq(A, pts[:, 2], rcond=None)[0]
    n = np.array([-a, -b, 1.0]); n /= np.linalg.norm(n)
    z = np.array([0, 0, 1.0]); v = np.cross(n, z); s = np.linalg.norm(v); cth = n @ z
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    Rt = np.eye(3) + K + K @ K * ((1 - cth) / s ** 2) if s > 1e-9 else np.eye(3)
    R = Rt @ Rz
    T = np.eye(4); T[:3, :3] = R
    tilt = np.degrees(np.arccos(cth))
    json.dump({"T_mm": T.tolist(), "yaw_deg": float(np.degrees(ang)), "tilt_deg": float(tilt),
               "contacts_mm": pts.tolist()}, open(out, "w"), indent=1)
    print("yaw", np.degrees(ang).round(2), "tilt", tilt.round(3), "contacts z", pts[:, 2].round(1))


def apply(tj, src, dst, pre=None):
    T = np.array(json.load(open(tj))["T_mm"])
    if pre:
        j = json.load(open(pre))
        P = np.array(j.get("T_part_to_car_mm") or j["T_mm"])
        T = T @ P
    R, t = T[:3, :3].astype(np.float32), T[:3, 3].astype(np.float32)
    m = np.memmap(src, dtype=TRI, offset=84, mode="r")
    with open(dst, "wb") as f:
        f.write(b"mazda-miata-nc levelled".ljust(80)); f.write(np.uint32(len(m)).tobytes())
        for i in range(0, len(m), 2_000_000):
            ch = np.array(m[i:i + 2_000_000])
            ch["v"] = ch["v"] @ R.T + t
            ch["n"] = ch["n"] @ R.T
            ch.tofile(f)
    print(dst, len(m))


if __name__ == "__main__":
    if sys.argv[1] == "fit":
        fit(sys.argv[2], sys.argv[3])
    else:
        pre = sys.argv[sys.argv.index("--pre") + 1] if "--pre" in sys.argv else None
        apply(sys.argv[2], sys.argv[3], sys.argv[4], pre)
