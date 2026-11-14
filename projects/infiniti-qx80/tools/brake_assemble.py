"""GT-R front brake, assembled for the v7 brake shot (bench, not on the car).

Sources (engineering Drive 'Infiniti QX80'):
  Scans/Infiniti QX80 Front Rotor Ring.stl + Rotor Hat Front.stl  - GT-R ring + its flat hat, scanned together (one frame)
  Scans/Infiniti QX80 Front Caliper.stl                            - GT-R monoblock caliper, bench scan (own frame)
  Brake/Nismo QX80 Front Rotor Hat8288.stl                         - our CAD hat (QX80 lug pattern), CAD hub frame
  Brake/Nismo QX80 Front Caliper Adapter Left.stl                  - our CAD caliper adapter, same CAD hub frame

Frame out: mm, hub centre = origin, hub axis = +X (inboard), CAD adapter on -Y.
- CAD hat: centre (-1295.4, 1378.0, -972.0) of the CAD frame -> origin (bbox centre in YZ, mean X).
- Ring: axis by PCA (thin axis), in-plane centre by bbox; scanned with its flat hat on one face: hat plate axial 17.5..26.8,
  ring -21.9..16.4 -> ring midplane 25.3 mm from the hat midplane, on the side away from the hat. Placed at X = +25.3
  (inboard, the side the CAD adapter is on: adapter X +49..+78).
- Caliper (bench frame: x radial with +x toward the hub - its ends curve to +x; y tangential; z axial, +z = smooth outboard
  face): x -> +Y radial (outer bridge at r = R_out 210 + 28 mm clearance), y -> Z (tangential, centred on the adapter),
  z -> +X (ears inboard), axial centre on the ring midplane.
Placement of ring and caliper is by geometry, not a measured assembly: it is a bench exploded/assembled view.
"""
import sys, struct, numpy as np

B = '/home/user/media/infiniti-qx80/brake'
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = lambda f: np.fromfile(f, dtype=TRI, offset=84)


def save(path, a):
    with open(path, 'wb') as fh:
        fh.write(b'qx80 gt-r brake'.ljust(80)); fh.write(struct.pack('<I', len(a))); a.tofile(fh)


def xf(a, fn):
    v = a['v'].reshape(-1, 3).astype(np.float64); a = a.copy(); a['v'] = fn(v).reshape(-1, 3, 3).astype(np.float32); a['n'] = 0; return a


hat = L(f'{B}/raw/Nismo QX80 Front Rotor Hat8288.stl'); hv = hat['v'].reshape(-1, 3)
C = np.array([hv[:, 0].mean(), (hv[:, 1].min() + hv[:, 1].max()) / 2, (hv[:, 2].min() + hv[:, 2].max()) / 2])
save(f'{B}/hub/hat_cad.stl', xf(hat, lambda v: v - C))
save(f'{B}/hub/adapter_cad.stl', xf(L(f'{B}/raw/Nismo QX80 Front Caliper Adapter Left.stl'), lambda v: v - C))

ring = L(f'{B}/d/front_rotor_ring.stl'); rv = ring['v'].reshape(-1, 3).astype(np.float64)
c = rv.mean(0); w, U = np.linalg.eigh(np.cov((rv - c)[::10].T)); ax = U[:, 0]
shat = L(f'{B}/d/rotor_hat_front.stl')['v'].reshape(-1, 3)
if ((shat - c) @ ax).mean() < 0: ax = -ax          # +ax points from the ring toward its scanned hat
e1 = np.cross(ax, [1, 0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(ax, e1)
p = np.stack([(rv - c) @ e1, (rv - c) @ e2], 1); cen = (p.max(0) + p.min(0)) / 2
c = c + cen[0] * e1 + cen[1] * e2
a_ring = (rv - c) @ ax; mid = (np.percentile(a_ring, 0.5) + np.percentile(a_ring, 99.5)) / 2
r_out = np.percentile(np.hypot((rv - c) @ e1, (rv - c) @ e2), 99.8)
# hat side (+ax) -> outboard (-X): X = -(a - mid) + 25.3
save(f'{B}/hub/ring_scan.stl', xf(ring, lambda v: np.stack([-((v - c) @ ax - mid) + 25.3, (v - c) @ e1, (v - c) @ e2], 1)))

cal = L(f'{B}/d/front_caliper.stl'); cv = cal['v'].reshape(-1, 3)
lo, hi = cv.min(0), cv.max(0); cc = (lo + hi) / 2
R_BRIDGE = r_out + 28.0
def cal_fn(v):
    # v7c fix (reviewer: "the GTR brakes are backwards"): the caliper's +z face is the smooth outboard (logo) face and -z
    # carries the brake-line fitting / mounting bosses (inboard) - checked on shaded views of both faces. v7/v7b had it
    # inside-out. Now +z -> outboard (-X); tangential flipped too so it is a rotation (180 deg about the radial axis), not a mirror.
    X = -(v[:, 2] - cc[2]) + 25.3                     # axial: smooth face outboard
    Y = -R_BRIDGE + (v[:, 0] - lo[0])                 # radial: outer bridge (x min) at -R_BRIDGE on -Y
    Z = -(v[:, 1] - cc[1])                            # tangential
    return np.stack([X, Y, Z], 1)                     # [[0,0,-1],[1,0,0],[0,-1,0]]: det +1
save(f'{B}/hub/caliper_scan.stl', xf(cal, cal_fn))
print('r_out', round(float(r_out), 1), 'ring mid', round(float(mid), 1), 'hub C', C.round(1))
