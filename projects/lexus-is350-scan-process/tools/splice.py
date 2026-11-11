"""Swap a removed part out of the full car by surface distance (not a box - a box exposed coverage holes).
  python splice.py full.stl state.stl part.stl tol_mm out.stl
Drops full-car faces within tol of the part scan's surface (= the part itself), then adds state-scan faces near the
part (bbox + 30 mm) that are farther than tol from the remaining full car (= the pocket the part leaves)."""
import sys, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from align import load
full, state, part, tol, out = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
hdr, F = load(full); _, S = load(state); _, P = load(part)
fc, sc, pc = F['v'].mean(1), S['v'].mean(1), P['v'].reshape(-1, 3)
lo, hi = pc.min(0) - 30, pc.max(0) + 30
near = lambda c: np.all((c > lo) & (c < hi), axis=1)
fz = near(fc); d, _ = cKDTree(pc).query(fc[fz]); drop = np.zeros(len(F), bool); drop[np.where(fz)[0][d < tol]] = True
keep = F[~drop]
sz = near(sc); d2, _ = cKDTree(keep['v'].mean(1)[near(keep['v'].mean(1))]).query(sc[sz]); add = S[np.where(sz)[0][d2 > tol]]
print("drop full", drop.sum(), "add state", len(add))
e = np.concatenate([keep, add])
with open(out, 'wb') as f:
    f.write(hdr); f.write(np.uint32(len(e)).tobytes()); f.write(e.tobytes())
