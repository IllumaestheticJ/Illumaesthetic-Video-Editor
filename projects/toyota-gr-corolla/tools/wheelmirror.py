"""Right-rear AND front-left wheels for the full 360 (user on v11: "a full 360 of the car"): the full-car scan only caught fragments of
it. Mirror the complete left-rear wheel (tyre + rim + brake, inside a 330 mm cylinder) across the car's centre plane,
drop the right-rear fragments inside the same cylinder, and seat the mirrored wheel on the right wheel's own centre.
The front-left wheel was missing too (only rim/brake): mirror the complete front-right wheel straight across (same axle,
no shift; centre from wing/fwheel_grid.png). Centres read from near-orthographic side views (wing/wheel_{L,R}_grid.png, 2.25 mm/px), prepped metres.
    wheelmirror.py in.stl out.stl"""
import struct, sys
import numpy as np
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
XC = 0.0055                                   # car centre plane (raw x -198.1)
CL, CR, RAD = np.array([1.3445, 0.2105]), np.array([1.3805, 0.204]), 0.330
X_IN, X_OUT = 0.60, 0.97                      # |x - XC| span of the wheel
m = np.fromfile(sys.argv[1], dtype=DT, offset=84)
P = m["v"].astype(float) / 1000 + ROOT; c = P.mean(1); dx = c[:, 0] - XC
def in_wheel(centre, side):
    return (side * dx > X_IN) & (side * dx < X_OUT) & (np.linalg.norm(c[:, 1:3] - centre, axis=1) < RAD)
CF = np.array([-1.22, 0.21])                  # front axle (right wheel hub)
L, R = in_wheel(CL, 1), in_wheel(CR, -1)
FR, FL = in_wheel(CF, -1), in_wheel(CF, 1)
def mirrored(sel, shift):
    w = P[sel].copy(); w[..., 0] = 2 * XC - w[..., 0]; w[..., 1:3] += shift; w = w[:, ::-1]   # mirror, keep winding
    n = np.zeros(len(w), DT); n["v"] = ((w - ROOT) * 1000).astype(np.float32); return n
out = np.concatenate([m[~(R | FL)], mirrored(L, CR - CL), mirrored(FR, 0)])
print("front-right wheel", int(FR.sum()), "| front-left fragments dropped", int(FL.sum()))
nn = np.cross(out["v"][:, 1] - out["v"][:, 0], out["v"][:, 2] - out["v"][:, 0]); out["n"] = nn / np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-9)
with open(sys.argv[2], "wb") as f: f.write(b"grc + mirrored right-rear wheel".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
print("left wheel", int(L.sum()), "| right fragments dropped", int(R.sum()), "| total", len(out))
