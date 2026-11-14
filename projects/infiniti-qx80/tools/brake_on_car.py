"""Put the assembled GT-R front brake (brake_assemble.py, hub frame) at the 4 wheels of the design frame (mm).
hubs.json (export_wheels.py) gives each Brembo_GTS_disc_001 centre = rotor midplane on the hub axis (design X).
Hub frame: +X inboard, ring midplane at X = +25.3, caliper on -Y. Design frame: nose +Y, car centreline x ~ -408.
Caliper placed at the trailing side, 20 deg above horizontal - where it shows behind the spokes in photos 1701 / 1702.
Same front brake on all four corners (front scans only; the rear caliper/rotor scans are not used).
Outputs: <out>/brake_iron.stl (ring scans + CAD hats + CAD adapters), <out>/brake_caliper.stl (caliper scans)."""
import json, sys, struct, numpy as np
H, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = lambda f: np.fromfile(f, dtype=TRI, offset=84)
hubs = json.load(open(H)); CL = np.mean([h['centre'][0] for h in hubs.values()])
groups = {'brake_iron': ['ring_scan', 'hat_cad', 'adapter_cad'], 'brake_caliper': ['caliper_scan']}
th = np.radians(20)
for g, parts in groups.items():
    acc = []
    for name, h in sorted(hubs.items()):
        c = np.array(h['centre']); inb = np.sign(CL - c[0])
        X = np.array([inb, 0, 0]); Ym = np.array([0, -np.cos(th), np.sin(th)])     # hub -Y -> rear, 20 deg up
        Y = -Ym; Z = np.cross(X, Y); R = np.stack([X, Y, Z], 1)                  # columns: hub axes in design frame
        o = c - 25.3 * X
        for p in parts:
            a = L(f'{src}/{p}.stl').copy(); v = a['v'].reshape(-1, 3).astype(np.float64)
            a['v'] = (v @ R.T + o).reshape(-1, 3, 3).astype(np.float32); a['n'] = 0; acc.append(a)
    A = np.concatenate(acc)
    with open(f'{out}/{g}.stl', 'wb') as fh:
        fh.write(b'qx80 gt-r brakes design frame'.ljust(80)); fh.write(struct.pack('<I', len(A))); A.tofile(fh)
    print(g, len(A))
