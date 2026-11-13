"""Place Ecky's Nismo QX80 kit STLs (design frame, mm) on the QX80 scan's levelled frame.
Ecky's review blend holds the full-car scan as an object whose local coords are the raw Artec frame in metres
(checked: local*1000 vs our raw car = 1.6 mm median, 99 % < 5 mm). Its matrix_world M maps raw(m) -> design(m),
so raw_mm = R^T (part_mm - 1000 t). Then the same level.json as every scan -> prep --like car6.json.
  kit2lev.py scanM.json level.json out_dir part1.stl part2.stl ..."""
import json, os, struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = np.array(json.load(open(sys.argv[1]))["Infiniti QX80 QX80 Full Car.008"]["M"]); R, t = M[:3, :3], M[:3, 3] * 1000
L = json.load(open(sys.argv[2])); RL = np.array(L["R"]); oL = np.array(L["origin"])
out = sys.argv[3]; os.makedirs(out, exist_ok=True)
for p in sys.argv[4:]:
    a = np.fromfile(p, dtype=TRI, offset=84)
    v = a["v"].reshape(-1, 3).astype(np.float64)
    raw = (v - t) @ R            # R^T (v - t), rows
    lev = (raw - oL) @ RL.T
    a["v"] = lev.reshape(-1, 3, 3).astype(np.float32)
    n = np.cross(a["v"][:, 1] - a["v"][:, 0], a["v"][:, 2] - a["v"][:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    a["n"] = n.astype(np.float32)
    dst = os.path.join(out, os.path.basename(p))
    with open(dst, "wb") as f:
        f.write(b"ive qx80 kit -> level".ljust(80)); f.write(struct.pack("<I", len(a))); a.tofile(f)
    print(dst, len(a), lev.min(0).round(), lev.max(0).round())
