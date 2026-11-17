"""Castrol livery + game-model surface classes on the scan (user v13: "add the window/light texture/etc that the video
game model have"). Website model eps-toyota-gr-corolla-v23.glb: 'body' (UV livery texture), 'glass', 'trim' (lights,
chrome, grille, plastics, mirror glass, underbody), ICP'd onto our car (wing/web_to_ours.npy). Each scan face takes the
class of the nearest website surface within --maxd mm (class 0 = none -> house silver); body faces also take the
livery texture colour. Drops the old wheels with the corrected hub centres (wheelplace.py) and a 0.345 m radius.
    livery2.py car9.stl web_parts.npz webbody.npz web_to_ours.npy livery_castrol.png out.stl out_prefix [--maxd 30]
Writes out_prefix_colors.npy (rgb uint8) and out_prefix_class.npy (0 = silver, 1 + website material index)."""
import argparse, struct
import numpy as np, open3d as o3d
from PIL import Image
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
XC, RAD = 0.0055, 0.345
CENTRES = {"FL": (1, -1.225, 0.287), "FR": (-1, -1.225, 0.287), "RL": (1, 1.34, 0.286), "RR": (-1, 1.376, 0.280)}
ap = argparse.ArgumentParser()
for n in ("car", "parts", "body", "xf", "tex", "out", "prefix"): ap.add_argument(n)
ap.add_argument("--maxd", type=float, default=30)
a = ap.parse_args()
m = np.fromfile(a.car, dtype=DT, offset=84); c = m["v"].mean(1).astype(float) / 1000 + ROOT
wheel = np.zeros(len(m), bool)
for side, y, z in CENTRES.values():
    dx = side * (c[:, 0] - XC)
    wheel |= (dx > 0.55) & (dx < 1.05) & (np.hypot(c[:, 1] - y, c[:, 2] - z) < RAD)
m, c = m[~wheel], c[~wheel]
X = np.load(a.xf); P = np.load(a.parts); B = np.load(a.body)
tris = P["tris"].reshape(-1, 3) @ X[:3, :3].T + X[:3, 3]
nb = len(B["T"]); assert (P["obj"][:nb] == 0).all() and len(P["obj"]) > nb
sc = o3d.t.geometry.RaycastingScene()
sc.add_triangles(o3d.core.Tensor(tris.astype(np.float32)), o3d.core.Tensor(np.arange(len(tris), dtype=np.uint32).reshape(-1, 3)))
q = sc.compute_closest_points(o3d.core.Tensor(c.astype(np.float32)))
pid = q["primitive_ids"].numpy(); bu = q["primitive_uvs"].numpy(); dist = np.linalg.norm(q["points"].numpy() - c, axis=1) * 1000
cls = (P["mat"][pid] + 1).astype(np.int16); cls[dist > a.maxd] = 0
col = np.full((len(m), 3), 255, np.uint8)
isb = (pid < nb) & (cls > 0)
UV = B["UV"][pid[isb]]; w = bu[isb]
uv = UV[:, 0] * (1 - w[:, :1] - w[:, 1:]) + UV[:, 1] * w[:, :1] + UV[:, 2] * w[:, 1:]
img = np.asarray(Image.open(a.tex).convert("RGB")); H, W = img.shape[:2]
col[isb] = img[np.clip((1 - uv[:, 1] % 1) * H, 0, H - 1).astype(int), np.clip((uv[:, 0] % 1) * W, 0, W - 1).astype(int)]
np.save(a.prefix + "_colors.npy", col); np.save(a.prefix + "_class.npy", cls)
with open(a.out, "wb") as f: f.write(b"car9 minus old wheels (livery2.py)".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
names = ["silver"] + list(P["matnames"])
print("faces", len(m), "| old wheel faces dropped", int(wheel.sum()))
for i, n in enumerate(names): print(f"  {n}: {int((cls == i).sum())}")
