"""Orient a wheel scan for tools/wheel_build.py: hub-centred, axle on X, face +X, metres; split into rim and tyre by radius.

    python wheel_prep.py <decimated scan.stl> <out dir> [split radius m, default 0.236]
Writes rim_part.stl and, when the scan includes a tyre (anything beyond the split radius), tyre_part.stl.
The axle is the scan's smallest principal axis; the face is the side the spokes sit toward.
"""
import sys
import numpy as np

dt = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
d = np.fromfile(sys.argv[1], dtype=dt, offset=84); out = sys.argv[2]; SPLIT = float(sys.argv[3]) if len(sys.argv) > 3 else 0.236
v = d["v"].astype(np.float64); pts = v.reshape(-1, 3)
c = pts.mean(0); w, U = np.linalg.eigh(np.cov((pts[::10] - c).T)); ax = U[:, 0]
h = (pts - c) @ ax; rad = (pts - c) - np.outer(h, ax); r = np.linalg.norm(rad, axis=1)
c = c + rad[r > np.percentile(r, 80)].mean(0)                       # centre on the outer band
h = (pts - c) @ ax; rad = (pts - c) - np.outer(h, ax); r = np.linalg.norm(rad, axis=1)
sp = (r > 90) & (r < 180)
if h[sp].mean() < (h.min() + h.max()) / 2:
    ax = -ax; h = -h
mid = (h.min() + h.max()) / 2
e1 = np.cross(ax, [0, 0, 1.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(ax, e1)
q = (v - c) @ np.stack([ax, e1, e2], 0).T; q[..., 0] -= mid; q /= 1000.0
rc = np.linalg.norm(q.mean(1)[:, 1:], axis=1)


def write(name, tri):
    o = np.zeros(len(tri), dt); o["v"] = tri.astype(np.float32)
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); o["n"] = (n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)).astype(np.float32)
    with open(name, "wb") as f:
        f.write(b"\0" * 80); f.write(np.uint32(len(tri)).tobytes()); o.tofile(f)


write(out + "/rim_part.stl", q[rc < SPLIT])
if (rc >= SPLIT).sum() > 1000:
    write(out + "/tyre_part.stl", q[rc >= SPLIT])
print("radius", round(float(np.linalg.norm(q.reshape(-1, 3)[:, 1:], axis=1).max()), 4), "width", round(float(np.ptp(q[..., 0])), 4), "rim", int((rc < SPLIT).sum()), "tyre", int((rc >= SPLIT).sum()))
