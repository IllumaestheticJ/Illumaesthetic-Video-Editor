"""v6 bases (user 2026-11-14: Bomex front goes OVER the stock bumper; add Bomex mirrors + deep-dish wheels).
  kit/lev/bomex_mirror_{driver,pass}.stl : Mirror/V1 Shell + Glass Backing, kit_T applied (lev mm)
  parts/kb6_wing.stl / kb6_nowing.stl    : full car (stock bumper ON) minus stock mirrors (+ Side Mirrors Removed fill)
                                           [nowing: minus stock wing + Rear Wing Removed fill], stock wheels cut out
  parts/stock_wheels.stl                 : the cut wheels (cylinder about each axle, projects/nissan-400z/wheels_v6.json)"""
import json, struct, subprocess, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
N = "/home/user/media/nissan-400z"; L = f"{N}/lev"; P = f"{N}/parts"; K = f"{N}/kit"
def save(p, m, h=b"400z v6"):
    with open(p, "wb") as f: f.write(h.ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
T = json.load(open("projects/nissan-400z/kit_T.json")); R = np.array(T["R"]); t = np.array(T["t"])
for side, pre in (("driver", "Driver"), ("pass", "Pass")):
    m = np.concatenate([np.fromfile(f"{K}/STL/Mirror/V1/{pre}_{x}_V1.stl", dtype=TRI, offset=84) for x in ("Shell", "Glass_Backing")])
    m["v"] = (m["v"].reshape(-1, 3).astype(np.float64) @ R.T + t).reshape(-1, 3, 3).astype(np.float32)
    m["n"] = (m["n"].astype(np.float64) @ R.T).astype(np.float32)
    save(f"{K}/lev/bomex_mirror_{side}.stl", m); v = m["v"].reshape(-1, 3); print("bomex_mirror", side, len(m), v.min(0).round(), v.max(0).round())
C = "projects/ferrari-296/tools/composite.py"
subprocess.run([sys.executable, C, f"{P}/_kb6_wing.stl", "--car", f"{L}/Full_Car_3mm.stl", "--remove", f"{P}/mirror_r.stl", f"{P}/mirror_l.stl",
                "--fill", f"{L}/Side_Mirrors_Removed_3mm.stl", "--cut", "6", "--new", "6", "--zone-pad", "30"], check=True)
subprocess.run([sys.executable, C, f"{P}/_kb6_nowing.stl", "--car", f"{L}/Full_Car_3mm.stl", "--remove", f"{P}/mirror_r.stl", f"{P}/mirror_l.stl", f"{P}/wing.stl",
                "--fill", f"{L}/Side_Mirrors_Removed_3mm.stl", f"{L}/Rear_Wing_Removed_3mm.stl", "--cut", "6", "--new", "6", "--zone-pad", "30"], check=True)
root = np.array(json.load(open("/home/user/media/work/z400/blend/car.json"))["root_location"])
W = json.load(open("projects/nissan-400z/wheels_v6.json"))
def wheel_mask(c):  # c: lev mm centroids
    p = c * 0.001 + root; msk = np.zeros(len(p), bool)
    for w in W["stock"].values():
        x0, x1 = sorted((w["x_outer"], w["x_outer"] - np.sign(w["x_outer"] - W["xc"]) * 0.34))
        msk |= (np.hypot(p[:, 1] - w["y"], p[:, 2] - w["z"]) < W["r"] + 0.012) & (p[:, 0] > x0 - 0.01) & (p[:, 0] < x1 + 0.01)
    return msk
for nm in ("kb6_wing", "kb6_nowing"):
    m = np.fromfile(f"{P}/_{nm}.stl", dtype=TRI, offset=84); k = wheel_mask(m["v"].mean(1).astype(np.float64))
    save(f"{P}/{nm}.stl", m[~k]); print(nm, len(m), "- wheels", int(k.sum()))
    if nm == "kb6_wing": save(f"{P}/stock_wheels.stl", m[k])
