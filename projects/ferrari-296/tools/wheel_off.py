"""Front-right wheel off: split the wheel out of a composite and fill the arch from the wheel-off state scan.

    python projects/ferrari-296/tools/wheel_off.py comp_explode.stl brake_disk__2mm.stl comp_v5.stl x_wheel.stl

The "Brake Disk" scan is both front arches captured with the wheels OFF (carbon-ceramic disc, caliper, hub, upright,
arch liner). Raw-mm Artec frame: car's right = -X, front = -Y. Axle = least-squares intersection of the tread
normals (every tread triangle's normal passes through the axle): y -1472.1, z -388.3, tread r 338 +-4 mm (245/35 R20
~340); the radial histogram is empty at 345-355 mm (tyre | arch liner). A hub-face circle fit was 100 mm off - don't.
  wheel  = composite triangles with r < R and x < X_IN, minus the brake seen through the spokes (r < R_BRAKE behind
           the spoke face X_SPOKE) which stays on the car
  bottom = the car scan was cut at the ground (raw z -695): the tyre's lowest ~31 mm are missing. The 296 wheel has 5
           double spokes, so the wheel rotated 144 deg about the axle fills that sector spoke-for-spoke.
  fill   = right-half wheel-off triangles > NEW mm from the remaining car (brake, hub, liner the car never saw)
"""
import struct
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
AXIS_Y, AXIS_Z, R, X_IN, NEW = -1472.1, -388.3, 350.0, -700.0, 7.0
R_BRAKE, X_SPOKE, Z_CUT, ROT = 238.0, -895.0, -680.0, 144.0


def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"ferrari-296 wheel_off".ljust(80))
        f.write(struct.pack("<I", len(m)))
        m.tofile(f)


def largest_component(m):
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    _, inv = np.unique(np.round(m["v"].reshape(-1, 3) * 2).astype(np.int64), axis=0, return_inverse=True)
    inv = inv.reshape(-1, 3)
    g = coo_matrix((np.ones(inv.size), (np.repeat(np.arange(len(m)), 3), inv.ravel())), shape=(len(m), inv.max() + 1)).tocsr()
    _, lab = connected_components(g @ g.T, directed=False)
    return m[lab == np.argmax(np.bincount(lab))]


def complete_bottom(w):
    th = np.radians(ROT)
    c, s = np.cos(th), np.sin(th)
    r = w.copy()
    v = r["v"].copy()
    y, z = v[..., 1] - AXIS_Y, v[..., 2] - AXIS_Z
    v[..., 1], v[..., 2] = AXIS_Y + c * y - s * z, AXIS_Z + s * y + c * z
    r["v"] = v
    n = r["n"].copy()
    ny, nz = n[:, 1].copy(), n[:, 2].copy()
    n[:, 1], n[:, 2] = c * ny - s * nz, s * ny + c * nz
    r["n"] = n
    return np.concatenate([w[w["v"].mean(1)[:, 2] >= Z_CUT], r[r["v"].mean(1)[:, 2] < Z_CUT]])


def main(comp, state, out_comp, out_wheel):
    c = load(comp)
    ctr = c["v"].mean(1)
    r = np.hypot(ctr[:, 1] - AXIS_Y, ctr[:, 2] - AXIS_Z)
    brake = (r < R_BRAKE) & (ctr[:, 0] > X_SPOKE)
    wheel = (r < R) & (ctr[:, 0] < X_IN) & ~brake
    rest = c[~wheel]
    w = largest_component(c[wheel])
    w = complete_bottom(w)
    s = load(state)
    sc = s["v"].mean(1)
    s = s[sc[:, 0] < 0]  # right arch only (the left wheel stays on)
    d, _ = cKDTree(rest["v"].reshape(-1, 3)[::2]).query(s["v"].mean(1), k=1)
    fill = s[d > NEW]
    save(out_comp, np.concatenate([rest, fill]))
    save(out_wheel, w)
    print(f"wheel {wheel.sum()} tris, body {len(rest)}, fill {len(fill)} of {len(s)} right-arch tris")


if __name__ == "__main__":
    main(*sys.argv[1:5])
