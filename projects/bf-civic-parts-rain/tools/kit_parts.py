"""v0: everything in RON'S design frame (m, level, front -Y, car's left +X): his production parts as they are, and our FE1 scan
moved in with the inverse of kit/ron_to_scan.json (1.1 mm median), cropped to his scan bbox + 25 mm.
Writes kit/parts/{car,front_lip,rear_lip,skirt_L,skirt_R,wing}.stl in METRES (Ron frame). Camera.006 (render 7) works as-is.
    python kit_parts.py
"""
import glob, json, sys, numpy as np
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/projects/honda-civic-11/tools")
from stlio import read, write, DT
M = "/home/user/media/bf-civic-parts-rain"; O = f"{M}/kit/parts"
import os; os.makedirs(O, exist_ok=True)
T = json.load(open(f"{M}/kit/ron_to_scan.json")); R = np.array(T["R"]); t = np.array(T["t"])
def save(name, tri):  # tri: (n,3,3) metres
    a = np.zeros(len(tri), DT); a["v"] = tri.astype(np.float32)
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    a["n"] = n.astype(np.float32); write(f"{O}/{name}.stl", a)
    v = tri.reshape(-1, 3); print(name, len(tri), v.min(0).round(3), v.max(0).round(3))
def ron(tri_m): return tri_m
save("front_lip", ron(read(f"{M}/ron/EP-HC11KK-FLV1-PU.stl")["v"].astype(np.float64) * 0.001))
save("rear_lip", ron(read(f"{M}/ron/EP-HC11SD-RLV1-PU.stl")["v"].astype(np.float64) * 0.001))
for f in glob.glob(f"{M}/ron/Side Skirt *.stl"):
    save("skirt_L" if "LH" in f else "skirt_R", ron(read(f)["v"].astype(np.float64) * 0.001))
save("wing", ron(np.load(f"{M}/kit/ron_wing002.npy").astype(np.float64)))
# car: prepped frame, cropped to Ron's (clean) scan bbox + 25 mm
j = json.load(open(f"{M}/prep/car.json")); root = np.array(j["root_location"])
c = read(f"{M}/dec/fe1_4mm_fill_0.95.stl")["v"].astype(np.float64) * 0.001 + root
c = (c - t) @ R  # prepped -> Ron frame
Q = np.load(f"{M}/kit/ron_fe1fl_pts.npy").astype(np.float64)
lo, hi = Q.min(0) - 0.025, Q.max(0) + 0.025
cen = c.mean(1); keep = np.all((cen > lo) & (cen < hi), 1) & (cen[:, 2] > 0.02)
print("car keep", keep.sum(), "of", len(c)); save("car", c[keep])
