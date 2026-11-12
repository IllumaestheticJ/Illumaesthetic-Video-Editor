"""Apply the exhaust registration (exhaust_reg.json: standalone EVO exhaust scan -> car frame, fitted by orientation search + ICP
against 'Rear End (No Bumper)' at 8 mm: median 4.7 mm, 65 % within 10 mm) to a levelled exhaust STL.  exhaust_place.py reg.json in.stl out.stl"""
import json, struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
j = json.load(open(sys.argv[1])); R = np.array(j["R"]); t = np.array(j["t"]); c = np.array(j["center"])
a = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
v = a["v"].reshape(-1, 3).astype(np.float64); v = (v - c) @ R.T + t
a["v"] = v.reshape(-1, 3, 3).astype(np.float32); a["n"] = (a["n"].astype(np.float64) @ R.T).astype(np.float32)
with open(sys.argv[3], "wb") as f:
    f.write(b"ive exhaust placed".ljust(80)); f.write(struct.pack("<I", len(a))); a.tofile(f)
print(sys.argv[3], len(a))
