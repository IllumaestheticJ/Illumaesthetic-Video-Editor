"""v7b brake section ON THE CAR SCAN: per-part meshes for one corner + the other three corners assembled.
Same placement as brake_on_car.py (hub frame from brake_assemble.py; hubs.json from export_wheels.py).
  python brake_corner.py hubs.json hub_lo_dir out_dir FOCUS_HUB
Writes (design frame, mm): c_ring, c_hat, c_adapter, c_caliper (FOCUS_HUB) and o3_iron, o3_caliper (other hubs).
FOCUS_HUB for the camera side (-x prepped, outboard -x): Brembo_GTS_disc_001.002 = front-left, hub (-0.86, 1.661, 0.412) m."""
import json, sys, struct, numpy as np
H, src, out, focus = sys.argv[1:5]
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
hubs = json.load(open(H)); CL = np.mean([h['centre'][0] for h in hubs.values()]); th = np.radians(5)


def place(name, part):
    c = np.array(hubs[name]['centre']); inb = np.sign(CL - c[0])
    sd = -1 if c[1] > 0 else 1                                                    # v7c: fronts trail, rears lead
    X = np.array([inb, 0, 0]); Y = -np.array([0, sd * np.cos(th), np.sin(th)]); Z = np.cross(X, Y); R = np.stack([X, Y, Z], 1)
    a = np.fromfile(f'{src}/{part}.stl', dtype=TRI, offset=84).copy(); v = a['v'].reshape(-1, 3).astype(np.float64)
    a['v'] = (v @ R.T + c - 25.3 * X).reshape(-1, 3, 3).astype(np.float32); a['n'] = 0; return a


def save(path, A):
    with open(path, 'wb') as fh:
        fh.write(b'qx80 gt-r brake corner'.ljust(80)); fh.write(struct.pack('<I', len(A))); A.tofile(fh)


for nm, part in (('c_ring', 'ring_scan'), ('c_hat', 'hat_cad'), ('c_adapter', 'adapter_cad'), ('c_caliper', 'caliper_scan')):
    save(f'{out}/{nm}.stl', place(focus, part))
others = [h for h in hubs if h != focus]
save(f'{out}/o3_iron.stl', np.concatenate([place(h, p) for h in others for p in ('ring_scan', 'hat_cad', 'adapter_cad')]))
save(f'{out}/o3_caliper.stl', np.concatenate([place(h, 'caliper_scan') for h in others]))
print('ok', focus, others)
