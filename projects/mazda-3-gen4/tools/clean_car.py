"""Remove the scissor jack / lift fragments under the Mazda 3 (levelled frame, mm; nose -Y).
The car sat on jacks ~15 cm up: sills bottom out at z~280-300 mm, tyres hang to z~125 mm.
Delete every triangle below --z (250 mm) outside the two wheel zones (front y -1300..-400, rear 1450..2350), and anything below 60 mm (scanned floor; tyres end ~100 mm).
    python projects/mazda-3-gen4/tools/clean_car.py in.stl out.stl"""
import struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
Z, FLOOR, WHEELS = 250.0, 60.0, [(-1300, -400), (1450, 2350)]
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
c = m["v"].mean(1)
inwheel = np.zeros(len(m), bool)
for a, b in WHEELS:
    inwheel |= (c[:, 1] > a) & (c[:, 1] < b)
drop = ((c[:, 2] < Z) & ~inwheel) | (c[:, 2] < FLOOR)
print("dropped", int(drop.sum()), "of", len(m))
m = m[~drop]
with open(sys.argv[2], "wb") as f:
    f.write(b"mazda3 clean".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
