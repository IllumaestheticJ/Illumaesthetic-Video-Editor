"""Motegi MF TL6 + AR1 wheels (game model 'Render Wheels', per-face materials) placed in the car's real stance
(user on v13: "fix wheel stance"). v13 had the hubs 70 mm too low (centres misread). Centres now = mean of (a) circle
fits to the scanned tyres' outer edge, (b) engineering's game-model stock wheels moved into our frame, (c) a measured
orthographic side render (wing/ortho_L_circles.jpg); right rear keeps its mirror offset. Outer face flush with the
scanned tyre.
    wheelplace.py car9.stl gm_wheels.npz out_wheels.npz"""
import sys
import numpy as np
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
XC = 0.0055
CEN = {"FL": (1, -1.225, 0.287), "FR": (-1, -1.225, 0.287), "RL": (1, 1.34, 0.286), "RR": (-1, 1.376, 0.280)}
car, wpath, out = sys.argv[1:4]
m = np.fromfile(car, dtype=DT, offset=84); cc = m["v"].mean(1).astype(float) / 1000 + ROOT
d = np.load(wpath); T = d["tris"]; mat = d["mat"]; names = list(d["matnames"]); tyre_id = names.index("Tire_sidewall.001")
tc = T.mean(1)
outT, outM = [], []
for name, (side, y, z) in CEN.items():
    dx = side * (cc[:, 0] - XC)
    near = (dx > 0.55) & (dx < 1.05) & (np.hypot(cc[:, 1] - y, cc[:, 2] - z) < 0.36)
    old = cc[near]
    sel = (np.sign(tc[:, 0]) == side) & (np.sign(tc[:, 1]) == np.sign(y))
    P = T[sel].copy(); pm = mat[sel]; pc = P.reshape(-1, 3)
    cy = (np.percentile(pc[:, 1], .5) + np.percentile(pc[:, 1], 99.5)) / 2; cz = (np.percentile(pc[:, 2], .5) + np.percentile(pc[:, 2], 99.5)) / 2
    outer_old = np.percentile(dx[near & (np.hypot(cc[:, 1] - y, cc[:, 2] - z) < 0.335)], 99.5)
    outer_new = np.percentile(side * (pc[:, 0] - XC), 99.5)
    sh = np.array([side * (outer_old - outer_new), y - cy, z - cz])
    print(name, "centre", (y, z), "shift mm", (sh * 1000).round(1))
    outT.append(P + sh); outM.append(pm)
np.savez(out, tris=np.concatenate(outT), mat=np.concatenate(outM), matnames=d["matnames"])
