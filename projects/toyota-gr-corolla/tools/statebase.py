"""Seat a state scan inside the full car (skill rule: show the state as captured, car carved around it).
Drops car faces within --d mm of the state (no double skins) and every car face inside the --box zones (the panel
that moved, e.g. the closed door when the state has it open); drops state faces below --floor (turntable/ground) and above --ceil (strays over the roof).
    statebase.py car.stl state.stl out.stl --d 15 --box x0,x1,y0,y1,z0,z1 [--box ...] --floor -572   (raw mm)"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--d", type=float, default=15); ap.add_argument("--box", action="append", default=[]); ap.add_argument("--szone", help="keep only STATE faces inside this zone (x0,x1,y0,y1,z0,z1): the car stays intact elsewhere, no seams where the state scan thins out"); ap.add_argument("--sbox", action="append", default=[], help="drop STATE faces in this zone (keep the car there, e.g. a wheel the state scanned only partly)"); ap.add_argument("--floor", type=float, default=-1e9); ap.add_argument("--ceil", type=float, default=1e9)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=DT, offset=84)
car, st = L(a.car), L(a.state); cc, sc = car["v"].mean(1), st["v"].mean(1)
ok = (sc[:, 2] > a.floor) & (sc[:, 2] < a.ceil)
if a.szone:
    q = [float(x) for x in a.szone.split(",")]
    ok &= (sc[:, 0] > q[0]) & (sc[:, 0] < q[1]) & (sc[:, 1] > q[2]) & (sc[:, 1] < q[3]) & (sc[:, 2] > q[4]) & (sc[:, 2] < q[5])
for b in a.sbox:
    q = [float(x) for x in b.split(",")]
    ok &= ~((sc[:, 0] > q[0]) & (sc[:, 0] < q[1]) & (sc[:, 1] > q[2]) & (sc[:, 1] < q[3]) & (sc[:, 2] > q[4]) & (sc[:, 2] < q[5]))
st, sc = st[ok], sc[ok]
lo, hi = sc.min(0) - a.d, sc.max(0) + a.d; idx = np.where(np.all((cc > lo) & (cc < hi), 1))[0]
d, _ = cKDTree(sc[::2]).query(cc[idx], distance_upper_bound=a.d, workers=-1)
keep = np.ones(len(car), bool); keep[idx[np.isfinite(d)]] = False
for b in a.box:
    q = [float(x) for x in b.split(",")]
    keep &= ~((cc[:, 0] > q[0]) & (cc[:, 0] < q[1]) & (cc[:, 1] > q[2]) & (cc[:, 1] < q[3]) & (cc[:, 2] > q[4]) & (cc[:, 2] < q[5]))
print("car", len(car), "-> kept", int(keep.sum()), "| state faces", len(st))
out = np.concatenate([car[keep], st])
with open(a.out, "wb") as f:
    f.write(b"grc statebase".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
