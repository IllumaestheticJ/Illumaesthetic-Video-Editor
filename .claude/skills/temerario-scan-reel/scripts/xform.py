"""Apply a rigid correction (regcheck.py's <part>.icp.json: R, t in levelled mm) to STLs.
  xform.py corr.icp.json in.stl out.stl [in2.stl out2.stl ...]
Used for the exhaust-session scans (Engine Bay / Catback / Cats / Exhaust Tip Assembly): they share one small offset
to the car frame, solved once on 'Engine Bay Exhaust On' (most overlap with the bumper-off state)."""
import json, struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
T = json.load(open(sys.argv[1])); R = np.array(T["R"]); t = np.array(T["t"])
for i, o in zip(sys.argv[2::2], sys.argv[3::2]):
    d = np.fromfile(i, dtype=TRI, offset=84)
    d["v"] = (d["v"].reshape(-1, 3).astype(np.float64) @ R.T + t).reshape(-1, 3, 3).astype(np.float32)
    d["n"] = (d["n"].astype(np.float64) @ R.T).astype(np.float32)
    with open(o, "wb") as f:
        f.write(b"ive xform".ljust(80)); f.write(struct.pack("<I", len(d))); d.tofile(f)
    print(o, len(d))
