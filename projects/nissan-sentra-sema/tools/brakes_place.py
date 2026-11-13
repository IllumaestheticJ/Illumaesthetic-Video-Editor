"""Seat the designer's GT-R brake set (calipers, rotors, Sentra adapters; right side only, mm, nose +Y) on Ron's wheels.
The brake file is in its own frame, so each corner is placed by the wheel it sits in: rotor centre -> wheel centre (y, z,
measured from the kit wheel meshes), rotor hat face 10 mm outboard of the wheel's centre plane (x). Left side = mirror.
Writes calipers.stl and rotors.stl in the levelled-scan mm frame, ready for `ive prep --like car.json`.
  brakes_place.py brakes_raw.npz car.json g_wheelsL_2mm.stl g_wheelsR_2mm.stl out_dir"""
import sys, json, os, numpy as np
T = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
B = np.load(sys.argv[1]); S = np.array(json.load(open(sys.argv[2]))['root_location']) * 1000.0
def wheels(p):                                   # per-axle wheel centre (mm, levelled-scan frame) and centre-plane x
    v = np.fromfile(p, dtype=T, offset=84)['v'].reshape(-1, 3).astype(np.float64)
    out = {}
    for ax, m in (('front', v[:, 1] + S[1] > 0), ('rear', v[:, 1] + S[1] < 0)):
        w = v[m]; lo, hi = w.min(0), w.max(0); r = (hi[1] - lo[1]) / 2
        out[ax] = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, hi[2] - r])
    return out
WL, WR = wheels(sys.argv[3]), wheels(sys.argv[4])
SETS = {'front': ('Senta_SR_Front_Rotor', ['Senta_SR_Front_Caliper'], ['Senta_SR_Front_Rotor', 'FrontV6.004']),
        'rear': ('Senta_SR_Rear_Rotor', ['Senta_SR_Rear_Caliper'], ['Senta_SR_Rear_Rotor', 'RearV3.003'])}
cal, rot = [], []
for ax, (rk, cals, rots) in SETS.items():
    r = B[rk].reshape(-1, 3); lo, hi = r.min(0), r.max(0)
    rc = np.array([hi[0], (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2])          # hat face x, rotor centre y z
    for side, W in (('R', WR[ax]), ('L', WL[ax])):
        tgt = np.array([W[0] + (10.0 if side == 'R' else -10.0), W[1], W[2]])
        for names, acc in ((cals, cal), (rots, rot)):
            for nm in names:
                v = B[nm].astype(np.float64) - rc                               # (n,3,3) relative to the hat-face centre
                if side == 'L': v[..., 0] *= -1; v = v[:, ::-1, :]             # mirror + flip winding
                acc.append(v + tgt)
        print(ax, side, 'rotor centre ->', tgt.round(1))
def wr(p, tris):
    a = np.zeros(len(tris), T); a['v'] = tris.astype(np.float32)
    e1, e2 = tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]; n = np.cross(e1, e2); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    a['n'] = n.astype(np.float32)
    with open(p, 'wb') as f: f.write(b'brakes_place'.ljust(80)); f.write(np.uint32(len(a)).tobytes()); a.tofile(f)
    print(os.path.basename(p), len(a))
wr(os.path.join(sys.argv[5], 'calipers.stl'), np.concatenate(cal)); wr(os.path.join(sys.argv[5], 'rotors.stl'), np.concatenate(rot))
