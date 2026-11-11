"""Quick orthographic point projections (XY, XZ, YZ) of STLs overlaid in colours -> png. For frame/registration sanity.
    python ortho.py out.png a.stl[:color] b.stl[:color] ..."""
import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
out = sys.argv[1]; fig, ax = plt.subplots(1, 3, figsize=(24, 8))
cols = ["0.6", "r", "c", "g", "m", "y", "b"]
for k, a in enumerate(sys.argv[2:]):
    p, _, c = a.partition(":")
    v = np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)
    v = v[np.random.default_rng(0).choice(len(v), min(len(v), 150000), replace=False)]
    c = c or cols[k % len(cols)]
    for j, (i0, i1) in enumerate([(0, 1), (0, 2), (1, 2)]):
        ax[j].scatter(v[:, i0], v[:, i1], s=0.05, c=c, alpha=0.5)
for j, t in enumerate(["XY", "XZ", "YZ"]): ax[j].set_title(t); ax[j].set_aspect("equal")
plt.tight_layout(); plt.savefig(out, dpi=60)
