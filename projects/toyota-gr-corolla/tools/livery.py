"""Castrol livery on the scan (user v13: "add the castrol livery to the car" - "the website glb has it"):
the website model eps-toyota-gr-corolla-v23.glb (Drive: Website Files/Epsilon-final-GLBs-2026-10-15.zip) carries the
livery as a 4096 px texture on its UV-mapped 'body'. Its body is ICP'd onto our car (similarity, body above the wheels:
scale 0.998, 6.9 mm rmse; wing/web_to_ours.npy). Every scan face takes the colour of the nearest point on that textured
body when it is within --maxd mm (else -1 = keep silver: glass, grille, wheel wells...).
Also drops the old wheels (inside each wheel cylinder) so the Motegi set can replace them in a 1:1 swap.
    livery.py car9.stl webbody.npz web_to_ours.npy livery_castrol.png out.stl out_colors.npy [--maxd 30]"""
import argparse, struct
import numpy as np, open3d as o3d
from PIL import Image
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
XC, RAD = 0.0055, 0.335
CENTRES = {"FL": (1, -1.22, 0.21), "FR": (-1, -1.22, 0.21), "RL": (1, 1.3445, 0.2105), "RR": (-1, 1.3805, 0.204)}
ap = argparse.ArgumentParser()
for n in ("car", "body", "xf", "tex", "out", "colors"): ap.add_argument(n)
ap.add_argument("--maxd", type=float, default=30)
a = ap.parse_args()
m = np.fromfile(a.car, dtype=DT, offset=84); c = m["v"].mean(1).astype(float) / 1000 + ROOT
wheel = np.zeros(len(m), bool)
for side, y, z in CENTRES.values():
    dx = side * (c[:, 0] - XC)
    wheel |= (dx > 0.55) & (dx < 1.0) & (np.hypot(c[:, 1] - y, c[:, 2] - z) < RAD)
m, c = m[~wheel], c[~wheel]
d = np.load(a.body); X = np.load(a.xf)
V = d["V"] @ X[:3, :3].T + X[:3, 3]
sc = o3d.t.geometry.RaycastingScene(); sc.add_triangles(o3d.core.Tensor(V.astype(np.float32)), o3d.core.Tensor(d["T"].astype(np.uint32)))
q = sc.compute_closest_points(o3d.core.Tensor(c.astype(np.float32)))
pid = q["primitive_ids"].numpy(); bu = q["primitive_uvs"].numpy(); pts = q["points"].numpy()
dist = np.linalg.norm(pts - c, axis=1) * 1000
UV = d["UV"][pid]; uv = UV[:, 0] * (1 - bu[:, :1] - bu[:, 1:]) + UV[:, 1] * bu[:, :1] + UV[:, 2] * bu[:, 1:]
img = np.asarray(Image.open(a.tex).convert("RGB")); H, W = img.shape[:2]
px = np.clip((uv[:, 0] % 1) * W, 0, W - 1).astype(int); py = np.clip((1 - uv[:, 1] % 1) * H, 0, H - 1).astype(int)
col = img[py, px].astype(np.int16); col[dist > a.maxd] = -1
np.save(a.colors, col)
with open(a.out, "wb") as f: f.write(b"car9 minus old wheels (livery.py)".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print("faces", len(m), "| old wheel faces dropped", int(wheel.sum()), "| liveried", int((dist <= a.maxd).sum()), f"({(dist <= a.maxd).mean():.1%})")
