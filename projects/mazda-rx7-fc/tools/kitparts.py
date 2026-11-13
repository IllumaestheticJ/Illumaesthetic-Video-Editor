"""Export the HertLife TA kit (FC3_TA.obj components, see ta_parts.npz) as one STL per panel group, in the S5 levelled
frame (mm) via kit_xform.json. The KeyShot file's low-poly stand-in body (doors, roof, pillars, quarter bits) is left out.
    kitparts.py ta_parts.npz kit_xform.json out_dir"""
import sys, json, struct, numpy as np
NPZ, XF, OUT = sys.argv[1:4]
GROUPS = {   # connected-component ids (objparts.py listing) -> panel
    "k_fbumper":   [84],
    "k_lights":    [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83],
    "k_splitter":  [85, 86, 87],
    "k_canards":   [88, 89],
    "k_hood":      [20],
    "k_side_l":    [16],                # widebody side skins (front fender -> rear fender), +X side
    "k_side_r":    [17],
    "k_sidesplit": [23, 24, 90, 91],
    "k_rbumper":   [55],
    "k_diffuser":  [56, 57, 58, 59, 60, 92, 93],
    "k_wing":      [61, 62, 63, 21, 22, 64, 65],
    "k_exhaust":   [18, 19],
}
d = np.load(NPZ); V, F, part = d["V"], d["F"], d["part"]
M = np.array(json.load(open(XF))["M"])
W = V @ M[:3, :3].T + M[:3, 3]
for name, ids in GROUPS.items():
    f = F[np.isin(part, ids)]; tri = W[f].astype(np.float32)
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    rec = np.zeros(len(tri), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]); rec["n"] = n; rec["v"] = tri
    with open(f"{OUT}/{name}.stl", "wb") as fh:
        fh.write(f"HertLife FC3S TA kit {name}".encode().ljust(80)); fh.write(struct.pack("<I", len(rec))); rec.tofile(fh)
    lo, hi = tri.reshape(-1, 3).min(0), tri.reshape(-1, 3).max(0)
    print(f"{name:12s} tris {len(rec):6d}  x[{lo[0]:6.0f},{hi[0]:6.0f}] y[{lo[1]:6.0f},{hi[1]:6.0f}] z[{lo[2]:5.0f},{hi[2]:5.0f}]")
