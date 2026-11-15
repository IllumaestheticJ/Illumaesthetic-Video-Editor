"""Split 'Liners Trimmed Fused (1.1m)' (the underbody plastics: 4 arch liners + undertrays, one fused mesh, car raw mm) into the
pieces that come off separately. Arch liners: within 560 mm (x-z) of an arch centre and |y| > 380. Undertrays: the rest, split at
x = 800 (front), x = -1100 (rear) and y = 0 (left / right floor). Specks < 300 tris dropped.
    python projects/a90-supra/tools/split_plastics.py  -> /home/user/media/work/a90/v3/pl_<piece>.stl + plastics.json (centres)"""
import json, os, struct, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from build_v3 import TRI, islands
O = "/home/user/media/work/a90/v3/"
m = np.fromfile("/home/user/media/a90-supra/scans/Liners Trimmed Fused (1.1m).stl", dtype=TRI, offset=84)
c = m["v"].mean(1)
arch = {"FR": (1229, -1), "FL": (1231, 1), "RR": (-1238, -1), "RL": (-1239, 1)}
lab = np.full(len(m), "", dtype=object)
for k, (ax, s) in arch.items():
    r = np.hypot(c[:, 0] - ax, c[:, 2] - 190); lab[(r < 560) & (s * c[:, 1] > 380) & (lab == "")] = "liner_" + k
u = lab == ""
lab[u & (c[:, 0] > 800)] = "tray_front"; lab[u & (c[:, 0] < -1100)] = "tray_rear"
mid = u & (c[:, 0] <= 800) & (c[:, 0] >= -1100)
lab[mid & (c[:, 1] >= 0)] = "tray_floor_L"; lab[mid & (c[:, 1] < 0)] = "tray_floor_R"
info = {}
for k in sorted(set(lab)):
    p = m[lab == k]; il = islands(p); p = p[np.bincount(il)[il] >= 300]
    with open(O + f"pl_{k}.stl", "wb") as f:
        f.write(b"ive plastics".ljust(80)); f.write(struct.pack("<I", len(p))); p.tofile(f)
    pc = p["v"].mean(1); info[k] = dict(tris=int(len(p)), lo=pc.min(0).round().tolist(), hi=pc.max(0).round().tolist())
    print(k, info[k])
json.dump(info, open(O + "plastics.json", "w"), indent=1)
