"""Cut the CAPTURED open hood out of the Hood Up state scan, so the hood that lifts off in s9_hoodoff is real
open-hood data, not the closed skin swung on a hinge (user v2 addendum D: never fake an opening).
  - hood_v2 (closed skin cut from the full car) is swung onto the open pose with the fitted hinge (hinge.json,
    exact axis + angle), and hup triangles within --dist mm of it are kept (= the scanned open panel).
  - The kept panel is rotated back to the CLOSED pose with the same exact hinge, so shot.py keys keep the
    hood.blend convention (rot X 44.42 = open). Output in levelled mm, prep it with --like car4.json.
    hoodup.py hinge.json car4.json hood_v2.stl hup_clean.stl out.stl [--dist 8]"""
import json, struct, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
hj, cj, hood_f, hup_f, out = sys.argv[1:6]
dist = float(sys.argv[sys.argv.index("--dist") + 1]) if "--dist" in sys.argv else 8.0
h = json.load(open(hj)); root = np.array(json.load(open(cj))["root_location"]) * 1000.0
p = np.array(h["p"]) * 1000.0 - root                     # hinge point in levelled mm
R = Rot.from_rotvec(np.radians(h["open_deg"]) * np.array(h["axis"]) / np.linalg.norm(h["axis"])).as_matrix()
hood = np.fromfile(hood_f, dtype=TRI, offset=84)["v"].reshape(-1, 3).astype(float)
hood_open = (hood - p) @ R.T + p
hup = np.fromfile(hup_f, dtype=TRI, offset=84)
c = hup["v"].mean(1).astype(float)
d, _ = cKDTree(hood_open[::3]).query(c, distance_upper_bound=dist)
keep = np.isfinite(d)
print(f"hood verts {len(hood)}  hup tris {len(hup)}  kept {keep.sum()} (within {dist} mm)")
panel = hup[keep].copy()
v = panel["v"].reshape(-1, 3).astype(float)
v = (v - p) @ R + p                                       # inverse rotation (R orthonormal): back to closed pose
panel["v"] = v.reshape(-1, 3, 3).astype(np.float32)
with open(out, "wb") as f:
    f.write(b"rx7 hood_up panel (captured, closed pose)".ljust(80)); f.write(struct.pack("<I", len(panel))); panel.tofile(f)
# report how well the captured panel, closed again, sits on the closed skin
dd, _ = cKDTree(hood[::3]).query(v[::5])
print(f"closed-back panel vs hood_v2: median {np.median(dd):.2f} mm, 95% {np.percentile(dd, 95):.2f} mm -> {out}")
