"""v7c: front-left wheel well from the real scan (Drive Scans/Suspension (MCS)/Infiniti QX80 Left Side Compressed.stl, raw
Artec frame - regcheck 5.05 mm median on the 19.7 % that overlaps the body). Crop around the FL arch in the levelled frame,
remove the stock rotor + caliper (the GT-R brake replaces them) and the jack stand under the hub.
Hub measured on the scan (prepped m): wheel face x -0.860, centre y 1.6537 z 0.3177 (suspension compressed: 94 mm lower than
the designer's wheel). Stock rotor faces x -0.82..-0.795.
  python wheelwell.py fl_well_lev.stl out.stl"""
import json, sys, struct, numpy as np
M = '/home/user/media/infiniti-qx80'
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
root = np.array(json.load(open(M + '/blend/car6.json'))['root_location'])
HUB = np.array(json.load(open(M + '/wheelwell/fl_hub.json'))['hub'])
a = np.fromfile(sys.argv[1], dtype=TRI, offset=84); c = a['v'].mean(1) / 1000 + root
r = np.hypot(c[:, 1] - HUB[1], c[:, 2] - HUB[2])
keep = (r < 0.62) & (c[:, 2] > 0.02)
keep &= ~((r > 0.07) & (r < 0.245) & (c[:, 0] < -0.735))                  # stock rotor + caliper (outboard of the knuckle)
keep &= ~((c[:, 2] < HUB[2] - 0.17) & (np.abs(c[:, 1] - HUB[1]) < 0.16))  # jack stand under the hub
A = a[keep]
with open(sys.argv[2], 'wb') as fh:
    fh.write(b'qx80 FL wheel well (scan) lev mm'.ljust(80)); fh.write(struct.pack('<I', len(A))); A.tofile(fh)
print('kept', len(A), 'of', len(a))
