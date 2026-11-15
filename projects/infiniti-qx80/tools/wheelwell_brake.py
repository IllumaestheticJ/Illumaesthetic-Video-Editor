"""v7c: the GT-R front brake (brake_assemble.py hub frame, mm) on the SCANNED front-left hub of the wheel-well scan.
Hub (prepped m, wheelwell/fl_hub.json): wheel face x -0.860, centre y 1.6537, z 0.3177; outboard = -x.
The CAD hat's outboard face (hub-frame X -5) sits on the wheel face. Caliper behind the hub (front corner), 5 deg up.
Writes levelled-frame mm STLs (for prep --like car6.json): w_ring, w_hat, w_adapter, w_caliper.
  python wheelwell_brake.py hub_lo_dir out_dir"""
import json, sys, struct, numpy as np
M = '/home/user/media/infiniti-qx80'
src, out = sys.argv[1], sys.argv[2]
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
root = np.array(json.load(open(M + '/blend/car6.json'))['root_location'])
H = np.array(json.load(open(M + '/wheelwell/fl_hub.json'))['hub'])
th = np.radians(5)
X = np.array([1.0, 0, 0]); Y = -np.array([0, -np.cos(th), np.sin(th)]); Z = np.cross(X, Y); R = np.stack([X, Y, Z], 1)
o = H + np.array([0.0054, 0, 0])                       # hat outboard face (X -5.4 mm) on the wheel face
for nm, part in (('w_ring', 'ring_scan'), ('w_hat', 'hat_cad'), ('w_adapter', 'adapter_cad'), ('w_caliper', 'caliper_scan')):
    a = np.fromfile(f'{src}/{part}.stl', dtype=TRI, offset=84).copy(); v = a['v'].reshape(-1, 3).astype(np.float64) / 1000
    p = v @ R.T + o                                     # prepped metres
    a['v'] = ((p - root) * 1000).reshape(-1, 3, 3).astype(np.float32); a['n'] = 0
    with open(f'{out}/{nm}.stl', 'wb') as fh:
        fh.write(b'qx80 gt-r brake on scanned FL hub'.ljust(80)); fh.write(struct.pack('<I', len(a))); a.tofile(fh)
    print(nm, p.min(0).round(3), p.max(0).round(3))
