"""Move the licence plate (left on the base by composite.py: it is in the full car but not in the bumper part scan)
from a base STL into its own part that rides with the front bumper. Raw mm: plate = tris in front of y < --y.
    python projects/subaru-wrx-vb/tools/split_plate.py base.stl base_out.stl plate_out.stl [--y -2345]"""
import struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
y = float(sys.argv[sys.argv.index("--y") + 1]) if "--y" in sys.argv else -2345.0
b = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
c = b["v"].mean(1)
sel = (c[:, 1] < y) & (np.abs(c[:, 0] + 50) < 350) & (c[:, 2] > 150) & (c[:, 2] < 700)
for p, m in ((sys.argv[2], b[~sel]), (sys.argv[3], b[sel])):
    with open(p, "wb") as f:
        f.write(b"wrx split".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
    print(p, len(m))
