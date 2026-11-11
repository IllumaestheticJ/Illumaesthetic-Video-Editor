"""Part-state composite (lessons: use the state scan as captured over the full car trimmed back).
Works on binary STLs in the raw Artec frame (mm). Car-local forward axis u = x*fx + y*fy
(the Sera sits ~15 deg yawed in the scan frame: forward = (0.258, 0.966)).

    python tools/composite.py full.stl state.stl out.stl --keep-below U [--side front|rear] [--fwd 0.258,0.966]

front: keep full-car triangles with u < U, add every state triangle.
rear:  keep full-car triangles with u > U, add every state triangle."""
import argparse, numpy as np
T = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("full"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--cut", type=float, required=True); ap.add_argument("--side", default="front")
ap.add_argument("--fwd", default="0.258,0.966")
ap.add_argument("--state-beyond", type=float, default=None, help="only take state triangles beyond this u (front: u > v, rear: u < v)")
a = ap.parse_args()
fx, fy = (float(v) for v in a.fwd.split(","))
F = np.fromfile(a.full, dtype=T, offset=84); S = np.fromfile(a.state, dtype=T, offset=84)
c = F["v"].mean(1); u = c[:, 0] * fx + c[:, 1] * fy
keep = F[u < a.cut] if a.side == "front" else F[u > a.cut]
if a.state_beyond is not None:
    cs = S["v"].mean(1); us = cs[:, 0] * fx + cs[:, 1] * fy
    S = S[us > a.state_beyond] if a.side == "front" else S[us < a.state_beyond]
out = np.concatenate([keep, S])
with open(a.out, "wb") as f:
    f.write(b"tools/composite.py".ljust(80)); f.write(np.uint32(len(out)).tobytes()); out.tofile(f)
print({"full_kept": int(len(keep)), "state": int(len(S)), "out": int(len(out))})
