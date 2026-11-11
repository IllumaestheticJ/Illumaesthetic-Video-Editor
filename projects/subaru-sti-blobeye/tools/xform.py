"""Apply a rigid 4x4 (mm) to a binary STL, streamed in chunks (works on the 1.15 GB raw car).
    python xform.py in.stl T.json out.stl      # T.json: {"T": 4x4} or {"T_part_to_car_mm": 4x4}; several T.json -> applied left to right
"""
import json, struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
src, *tjs, out = sys.argv[1:]
T = np.eye(4)
for tj in tjs:
    j = json.load(open(tj)); T = np.array(j.get("T", j.get("T_part_to_car_mm"))) @ T
m = np.memmap(src, dtype=TRI, mode="r", offset=84)
with open(out, "wb") as f:
    f.write(b"sti xform".ljust(80)); f.write(struct.pack("<I", len(m)))
    for i in range(0, len(m), 2_000_000):
        ch = np.array(m[i:i + 2_000_000])
        ch["v"] = (ch["v"].reshape(-1, 3).astype(np.float64) @ T[:3, :3].T + T[:3, 3]).reshape(-1, 3, 3).astype(np.float32)
        ch["n"] = (ch["n"].astype(np.float64) @ T[:3, :3].T).astype(np.float32)
        ch.tofile(f)
print(out, len(m))
