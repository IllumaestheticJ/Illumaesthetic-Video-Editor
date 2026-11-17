"""v0: put a raw Artec full-car scan (mm, arbitrary frame, may include ground) into the lookbook GLB frame
(metres, nose -Y, floor z=0) so GLB kit parts sit on it.

1. RANSAC the ground plane -> up axis; drop ground points.
2. PCA in the ground plane -> length axis; try both nose directions.
3. Trimmed ICP (rigid, then similarity) of the scan onto the GLB painted body above the sills; keep the better yaw.
4. Write the scan in the GLB frame with ground triangles removed, plus scan_to_glb.json.

    python scan_to_glb.py scan_dec.stl glb_body.stl out.stl
"""
import json
import os
import sys

import numpy as np
from scipy.spatial import cKDTree


def read_stl(p):
    with open(p, "rb") as f:
        f.seek(80)
        n = int(np.frombuffer(f.read(4), np.uint32)[0])
        d = np.frombuffer(f.read(n * 50), np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    return d["v"].astype(np.float64)


def write_stl(p, tri):
    tri = tri.astype(np.float32)
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    d = np.zeros(len(tri), np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    d["n"], d["v"] = n, tri
    with open(p, "wb") as f:
        f.write(b"\0" * 80); f.write(np.uint32(len(tri)).tobytes()); f.write(d.tobytes())


def umeyama(A, B, scale):
    ma, mb = A.mean(0), B.mean(0); A0, B0 = A - ma, B - mb
    U, D, Vt = np.linalg.svd(B0.T @ A0 / len(A)); S = np.eye(3); S[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ S @ Vt; s = (D * np.diag(S)).sum() / A0.var(0).sum() if scale else 1.0
    return s, R, mb - s * R @ ma


def main(scan_p, body_p, out_p):
    rng = np.random.default_rng(0)
    T = read_stl(scan_p)                       # (n,3,3) mm
    C = T.mean(1)
    P = C[rng.choice(len(C), min(250000, len(C)), replace=False)]
    # 1-2. PCA: length = largest axis, up = smallest axis (both signs tried below). Raw scans carry little ground.
    ctr = P.mean(0); w, V = np.linalg.eigh(np.cov((P - ctr).T))
    z = V[:, 0]; ax = V[:, 2]
    a0 = ctr; ground_frac = 0.0
    car = P
    B = read_stl(body_p).reshape(-1, 3); B = np.unique(B.round(4), axis=0); B = B[B[:, 2] > 0.35]
    Bt = cKDTree(B)
    results = []
    for zs, sgn in ([tuple(int(v) for v in os.environ['ONLY'].split(','))] if os.environ.get('ONLY') else ((1, 1), (1, -1), (-1, 1), (-1, -1))):
        zz = z * zs; y = ax * sgn; x = np.cross(y, zz)
        R0 = np.stack([x, y, zz])               # rows: scan -> frame
        def to(p): return ((p - a0) @ R0.T) * 0.001
        S = to(car)
        S = S[rng.choice(len(S), min(80000, len(S)), replace=False)]
        cen = np.array([(S[:, 0].min() + S[:, 0].max()) / 2, (S[:, 1].min() + S[:, 1].max()) / 2, np.percentile(S[:, 2], 99.5)])
        bc = np.array([(B[:, 0].min() + B[:, 0].max()) / 2, (B[:, 1].min() + B[:, 1].max()) / 2, B[:, 2].max()])
        s, R, t = 1.0, np.eye(3), bc - cen
        for scale, keep, it in ((False, 0.5, 30), (False, 0.6, 30), (True, 0.7, 30)):
            for _ in range(it):
                Pp = s * S @ R.T + t; d, j = Bt.query(Pp)
                m = (d <= np.quantile(d, keep)) & (Pp[:, 2] > 0.35)
                s, R, t = umeyama(S[m], B[j[m]], scale)
        Pp = s * S @ R.T + t; d, _ = Bt.query(Pp); dd = d[Pp[:, 2] > 0.35]
        results.append((np.median(dd), (zs, sgn), s, R, t, R0))
        print(f"up {zs} yaw {sgn}: median {np.median(dd)*1000:.1f} mm p75 {np.percentile(dd,75)*1000:.1f} scale {s:.4f}")
    med, sgn, s, R, t, R0 = min(results, key=lambda r: r[0])
    # full transform: frame = s*R*(0.001*R0*(p - a0)) + t
    def full(p): return s * (((p - a0) @ R0.T) * 0.001) @ R.T + t
    V = full(T.reshape(-1, 3)).reshape(-1, 3, 3)
    keep = (V[:, :, 2].min(1) > 0.012) & (np.abs(V[:, :, 0]).max(1) < 1.3) & (np.abs(V[:, :, 1]).max(1) < 2.6)
    write_stl(out_p, V[keep])
    json.dump({"median_mm": med * 1000, "ground_frac": ground_frac, "a0": a0.tolist(), "R0": R0.tolist(),
               "s": s, "R": R.tolist(), "t": t.tolist(), "kept_tris": int(keep.sum())},
              open(out_p.replace(".stl", ".json"), "w"), indent=1)
    print("best median", round(med * 1000, 1), "mm; kept", int(keep.sum()), "of", len(V), "tris; ground frac", round(ground_frac, 3))


if __name__ == "__main__":
    main(*sys.argv[1:4])
