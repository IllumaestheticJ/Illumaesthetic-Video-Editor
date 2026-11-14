"""Clean + quadric-simplify a scan STL (no grid decimation: grid clustering leaves stair-step contours, A90 lesson).
meshprep.py in.stl out.stl [--M M.json] [--zmin -24] [--box x0,x1,y0,y1,z0,z1] [--target 5000000] [--island 3000] [--weld 0.02]
Coordinates: --M maps raw -> design mm first; all limits are in the design frame (mm)."""
import argparse, json, numpy as np
import fast_simplification
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--M"); ap.add_argument("--zmin", type=float); ap.add_argument("--box")
ap.add_argument("--target", type=int, default=0); ap.add_argument("--island", type=int, default=0); ap.add_argument("--weld", type=float, default=0.02)
a = ap.parse_args()
v = np.fromfile(a.src, dtype=TRI, offset=84)["v"]
print("in", len(v))
if a.M:
    M = np.array(json.load(open(a.M))["M"]); v = (v.reshape(-1, 3) @ M[:3, :3].T.astype(np.float32) + M[:3, 3].astype(np.float32)).reshape(-1, 3, 3)
c = v.mean(1); keep = np.ones(len(v), bool)
if a.zmin is not None: keep &= v[:, :, 2].min(1) > a.zmin
if a.box:
    b = [float(x) for x in a.box.split(",")]
    keep &= (c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])
v = v[keep]; del c; print("after crop", len(v))
q = np.round(v.reshape(-1, 3) / a.weld).astype(np.int64)
q -= q.min(0)
key = (q[:, 0] << 42) | (q[:, 1] << 21) | q[:, 2]
del q
uk, first, inv = np.unique(key, return_index=True, return_inverse=True)
pts = v.reshape(-1, 3)[first].astype(np.float64); F = inv.reshape(-1, 3).astype(np.int64)
del key, uk, first, inv, v
F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
print("welded verts", len(pts), "faces", len(F))
def islands(pts, F, minf):
    n = len(pts); e = np.concatenate([F[:, [0, 1]], F[:, [1, 2]]])
    g = coo_matrix((np.ones(len(e), np.int8), (e[:, 0], e[:, 1])), shape=(n, n))
    k, lab = connected_components(g, directed=False)
    fl = lab[F[:, 0]]; cnt = np.bincount(fl, minlength=k)
    keepf = cnt[fl] >= minf
    print("islands", k, "kept faces", keepf.sum(), "/", len(F))
    return F[keepf]
if a.island: F = islands(pts, F, a.island)
if a.target and len(F) > a.target:
    used = np.unique(F); remap = -np.ones(len(pts), np.int64); remap[used] = np.arange(len(used))
    pts = pts[used]; F = remap[F]
    pts, F = fast_simplification.simplify(pts.astype(np.float32), F.astype(np.int32), 1 - a.target / len(F))
    print("simplified", len(F))
T = pts[F].astype(np.float32)
n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
out = np.zeros(len(T), TRI); out["v"] = T; out["n"] = n
with open(a.dst, "wb") as f:
    f.write(b"\0" * 80); f.write(np.uint32(len(out)).tobytes()); out.tofile(f)
print("out", a.dst, len(out))
