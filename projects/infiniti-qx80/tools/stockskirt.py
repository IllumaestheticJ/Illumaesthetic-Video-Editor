"""v7f: split the STOCK side skirts (rocker cover / step under the doors) out of the car scan, so they can come off before
the kit skirts go on (reviewer: "the SUV needs the stock side skirts removed before the new ones go on").
Levelled frame, mm (car centreline x -60.9). Measured on a y=0 slice of car4: the stock skirt is the step at z 245-380,
x 808-970 (right) - exactly where the kit skirt sits (z 205-378, x 782-982). Region kept between the wheel arches
(y -690..1550; axles at lev y -1.12 / +1.98 m, wheel r 0.43).
  python stockskirt.py car_lev.stl out_base.stl out_skirt_l.stl out_skirt_r.stl"""
import sys, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
src, ob, ol, orr = sys.argv[1:5]
a = np.fromfile(src, dtype=TRI, offset=84); c = a['v'].mean(1)
band = (c[:, 1] > -690) & (c[:, 1] < 1550) & (c[:, 2] > 185) & (c[:, 2] < 380)
R = band & (c[:, 0] > 760); Lm = band & (c[:, 0] < -882)


def save(p, A):
    with open(p, 'wb') as fh:
        fh.write(b'qx80 stock skirt split'.ljust(80)); fh.write(struct.pack('<I', len(A))); A.tofile(fh)


save(ob, a[~(R | Lm)]); save(ol, a[Lm]); save(orr, a[R])
for n, m in (('left', Lm), ('right', R)):
    v = a[m]['v'].reshape(-1, 3); print(n, int(m.sum()), v.min(0).round(), v.max(0).round())
