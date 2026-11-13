"""Independent check of the strut-top spread from the engine-bay scans (as exported, shared frame).
For each jacked state: local trimmed ICP of the strut-top patch (state -> control) at each tower; the change in
tower-to-tower distance is the relative shift of the two patches along the tower-to-tower line.
usage: towerspread.py <bay_dir>   (control.stl jacked.stl fender.stl strut.stl both.stl)"""
import sys, json, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.mesh import TRI
D = sys.argv[1]; A0 = np.array([1085., 368.]); B0 = np.array([856., -577.])     # stud centres picked on the control height map (XY, mm)
def load(k): return np.fromfile(f'{D}/{k}.stl', dtype=TRI, offset=84)['v'].reshape(-1, 3).astype(np.float64)
def patch(P, c, r, zc=None, dz=60):
    k = (np.abs(P[:, 0]-c[0]) < r) & (np.abs(P[:, 1]-c[1]) < r); Q = P[k]; Q = Q[np.hypot(Q[:, 0]-c[0], Q[:, 1]-c[1]) < r]
    if zc is None: zc = np.quantile(Q[Q[:, 2] < -330, 2], .98)          # top of the strut hat (below hood level)
    return Q[(Q[:, 2] < zc + 8) & (Q[:, 2] > zc - dz)], zc
def kabsch(X, Y):
    cx, cy = X.mean(0), Y.mean(0); U, S, Vt = np.linalg.svd((X-cx).T @ (Y-cy)); d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1, 1, d]) @ U.T; return R, cy - R @ cx
def local(S, C, trim=.7):
    tree = cKDTree(C); R, t = np.eye(3), np.zeros(3)
    for _ in range(60):
        X = S @ R.T + t; d, j = tree.query(X); k = d <= np.quantile(d, trim); R2, t2 = kabsch(X[k], C[j[k]]); R, t = R2 @ R, R2 @ t + t2
    X = S @ R.T + t; d, _ = tree.query(X); return R, t, float(np.median(d))
C = load('control'); out = {}
for r in (35, 45, 60):
    CA, zA = patch(C, A0, r + 6); CB, zB = patch(C, B0, r + 6); a3 = np.array([*A0, zA]); b3 = np.array([*B0, zB]); L = np.linalg.norm(b3 - a3); u = (b3 - a3) / L
    print(f'radius {r} mm: control tower-to-tower (stud tops) {L:.1f} mm, patch pts {len(CA)} / {len(CB)}')
    for k in ('jacked', 'fender', 'strut', 'both'):
        S = load(k); SA, _ = patch(S, A0, r, zA); SB, _ = patch(S, B0, r, zB)
        RA, tA, mA = local(SA, CA); RB, tB, mB = local(SB, CB)
        pa = np.linalg.solve(RA, a3 - tA); pb = np.linalg.solve(RB, b3 - tB)       # where the control's stud tops sit in the state scan
        dl = np.linalg.norm(pb - pa) - L; out.setdefault(k, []).append(round(float(dl), 3))
        print(f'  {k:7s} spread change {dl:+.3f} mm   (patch shift A {np.linalg.norm(pa-a3):.2f} B {np.linalg.norm(pb-b3):.2f} mm; fit residual {mA:.2f}/{mB:.2f})')
json.dump(out, open(f'{D}/towerspread.json', 'w'), indent=1); print(out)
