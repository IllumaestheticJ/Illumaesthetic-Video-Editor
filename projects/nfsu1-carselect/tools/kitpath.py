"""Final path of the kit car (v8). steady.py smoothed only where the car's centre sits on screen (a 2D shift of the render);
the car's heading still wandered a few degrees while it drove away, twitched ~1 deg just before it stopped, and the centre
went left-right-left through the swing out. Here the whole view (azimuth, camera height, distance, screen position) is made
smooth and baked into the pose, so the render itself is steady and no 2D shift is needed:
  settle (1718..hold): one Hermite ease of all five parameters onto the hold
  drive-away: screen position = hold + s^2 * cubic(s) (leaves the hold at rest, one turn); azimuth/height/distance of the
              straight (from 1884) = low-order fits
Writes track/poses_kit.json (composite.py uses it for the kit car and then ignores shift.json) and cams_30_<car>.json.
    python kitpath.py <work>/track"""
import sys, json, os, numpy as np, cv2
from scipy.optimize import least_squares
sys.path.insert(0, os.path.dirname(__file__))
import sil
from composite import WHEELS
d = sys.argv[1]
P = json.load(open(f"{d}/poses.json")); SH = json.load(open(f"{d}/shift.json")); F = P["focal_px"]; X0 = np.array([0, 0, 0.5])
IN0, HOLD0, HOLD1, OUT1, SET0, TAIL = 1653, 1746, 1838, 1972, 1718, 1884
def params(p):
    p = np.array(p); R, _ = cv2.Rodrigues(p[:3]); c = -R.T @ p[3:6]; pc = R @ X0 + p[3:6]
    return np.degrees(np.arctan2(c[0], -c[1])), c[2], np.linalg.norm(c - X0), F * pc[0] / pc[2], F * pc[1] / pc[2]
def build(az, cz, dist, u, v):
    h = cz - X0[2]; rho = np.sqrt(max(dist ** 2 - h ** 2, 1e-6)); a = np.radians(az)
    c = np.array([np.sin(a) * rho, -np.cos(a) * rho, cz])
    def Rof(q):
        yaw, pit = q
        fwd = np.array([np.cos(pit) * np.sin(yaw), np.cos(pit) * np.cos(yaw), np.sin(pit)])
        right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right); down = np.cross(fwd, right)
        return np.stack([right, down, fwd])
    res = lambda q: (lambda pc: [F * pc[0] / pc[2] - u, F * pc[1] / pc[2] - v])(Rof(q) @ (X0 - c))
    w = (X0 - c) / np.linalg.norm(X0 - c)
    q = least_squares(res, [np.arctan2(w[0], w[1]), np.arcsin(w[2])]).x
    R = Rof(q); return np.concatenate([cv2.Rodrigues(R)[0].ravel(), -R @ c])
idx = np.arange(IN0, OUT1 + 1)
Q = np.array([params(P["frames"][str(i)]) for i in idx]); Q[:, 0] = np.degrees(np.unwrap(np.radians(Q[:, 0])))
Q[:, 3:5] += np.array([SH.get(str(i), (0, 0)) for i in idx])          # start from the steadied screen path
Q[:, 2] = np.log(Q[:, 2]); Q0 = Q.copy()
hq = Q[HOLD0 - IN0].copy()
ss = lambda t: (lambda t: t * t * (3 - 2 * t))(np.clip(t, 0, 1))
# settle
k0 = SET0 - IN0; T = HOLD0 - SET0; p0 = Q[k0].copy(); v0 = (Q[k0] - Q[k0 - 4]) / 4.0 * T
for i in range(SET0, HOLD0 + 1):
    t = (i - SET0) / T
    Q[i - IN0] = (2 * t**3 - 3 * t**2 + 1) * p0 + (t**3 - 2 * t**2 + t) * v0 + (-2 * t**3 + 3 * t**2) * hq
# drive-away
b = np.arange(HOLD1 - IN0, len(idx)); s = (idx[b] - HOLD1) / (OUT1 - HOLD1)
for k in (3, 4):                                                       # u, v: hold + s^2 * cubic
    M = np.stack([s**2, s**3, s**4, s**5], 1); co = np.linalg.lstsq(M, Q0[b, k] - hq[k], rcond=None)[0]; Q[b, k] = hq[k] + M @ co
t = idx[b] >= TAIL
for k, deg in ((0, 2), (1, 3), (2, 3)):                                # az, height, log distance on the straight
    fit = np.polyval(np.polyfit(idx[b][t], Q0[b, k][t], deg), idx[b]); w = ss((idx[b] - TAIL) / 16.0)
    Q[b, k] = Q0[b, k] * (1 - w) + fit * w
for k, i in enumerate(idx):
    if HOLD0 <= i <= HOLD1: Q[k] = hq
print("max change  az %.2f deg  height %.2f m  log-dist %.3f  u %.1f px  v %.1f px" % tuple(np.abs(Q - Q0).max(0)))
for i in list(range(1714, 1747, 4)) + list(range(1838, 1973, 6)):
    print(i, np.round(Q0[i - IN0], 2), "->", np.round(Q[i - IN0], 2))
Q[:, 2] = np.exp(Q[:, 2])
poses = {int(i): (P["frames"][str(i)] if i < SET0 and abs(SH.get(str(i), (0, 0))[0]) + abs(SH.get(str(i), (0, 0))[1]) < 1e-6 else build(*Q[k]).tolist()) for k, i in enumerate(idx)}
for i in range(HOLD0, HOLD1 + 1): poses[i] = P["frames"][str(i)]
json.dump({"focal_px": F, "hold": P["hold"], "frames": poses}, open(f"{d}/poses_kit.json", "w"))
for car, (_, _, (sx, sy)) in WHEELS.items():
    old = json.load(open(f"{d}/cams_30_{car}.json")); out = []
    for c in old:
        n = sil.cam_json(poses[c["src"]], F); n["blender"]["location"][0] += sx; n["blender"]["location"][1] += sy
        n["src"] = c["src"]; n["steer"] = c.get("steer", 0.0); out.append(n)
    json.dump(out, open(f"{d}/cams_30_{car}.json", "w"))
