"""Merge the track pieces into one car-relative camera per capture frame 1653..1972, smooth it, write
poses.json (every frame) and cams_30.json (every 2nd frame, ive camera schema, for render_car.py --cam-anim).
    python poses.py <work>/track"""
import sys, json, numpy as np, cv2
sys.path.insert(0, __import__("os").path.dirname(__file__))
import sil
d = sys.argv[1]
L = lambda n: {int(k): np.array(v["pose"]) for k, v in json.load(open(f"{d}/{n}.json"))["frames"].items()}
a, b, c = L("in2"), L("in_f1600"), L("out_f1600")
F = 1600.0
IN0, SWITCH, HOLD0, HOLD1, OUT1 = 1653, 1698, 1746, 1838, 1972
GAP = (1692, 1697)      # close sweep: both runs drift here (the silhouette says little when the car fills the frame); bridged
P = {}
for i in range(IN0, OUT1 + 1):
    if i < SWITCH: P[i] = a[i]
    elif i <= HOLD0: P[i] = b[i]
    elif i < HOLD1: P[i] = None
    else: P[i] = c[i]
hold = np.median([b[i] for i in range(1742, 1747)] + [c[i] for i in range(1837, 1840)], 0)
print("junction diff", np.round(a[SWITCH - 1] - b[SWITCH - 1], 3), "hold", np.round(hold, 4), "hold ends", np.round(b[1746] - hold, 3), np.round(c[1838] - hold, 3))
for i in range(HOLD0 + 1, HOLD1): P[i] = hold
idx = np.arange(IN0, OUT1 + 1); M = np.array([P[i] for i in idx])
def to_rc(p):
    R, _ = cv2.Rodrigues(p[:3]); return R, -R.T @ p[3:6]
def from_rc(R, C):
    return np.concatenate([cv2.Rodrigues(R)[0].ravel(), -R @ C])
k0, k1 = GAP[0] - 1 - IN0, GAP[1] + 1 - IN0
R0, C0 = to_rc(M[k0]); R1, C1 = to_rc(M[k1]); rel = cv2.Rodrigues(R1 @ R0.T)[0].ravel()
for k in range(k0 + 1, k1):
    t = (k - k0) / (k1 - k0)
    M[k] = from_rc(cv2.Rodrigues(rel * t)[0] @ R0, C0 * (1 - t) + C1 * t)
# rotation vectors: keep them continuous (same rotation, |r| vs 2pi-|r| branch)
for k in range(1, len(M)):
    r = M[k, :3]; n = np.linalg.norm(r)
    alt = r * (1 - 2 * np.pi / n)
    if np.linalg.norm(alt - M[k - 1, :3]) < np.linalg.norm(r - M[k - 1, :3]): M[k, :3] = alt
# v2 smoothing (user: "the car shakes oddly when entering the screen"). The fit measures where the car is on screen
# well, and its distance and heading poorly, so the three are smoothed separately: screen position of the car's
# centre lightly, distance and rotation heavily (Savitzky-Golay), then the pose is rebuilt from them.
from scipy.signal import savgol_filter
X0 = np.array([0.0, 0.0, 0.5])
def split(p):
    R, _ = cv2.Rodrigues(p[:3]); pc = R @ X0 + p[3:6]
    return p[:3].copy(), F * pc[0] / pc[2], F * pc[1] / pc[2], np.linalg.norm(pc)
def join(r, u, v, d):
    R, _ = cv2.Rodrigues(r); ray = np.array([u / F, v / F, 1.0]); pc = ray / np.linalg.norm(ray) * d
    return np.concatenate([r, pc - R @ X0])
S = M.copy()
for lo, hi in ((0, HOLD0 - IN0 + 1), (HOLD1 - IN0, len(M))):
    seg = [split(p) for p in M[lo:hi]]
    r = np.array([q[0] for q in seg]); u = np.array([q[1] for q in seg]); v = np.array([q[2] for q in seg]); dd = np.array([q[3] for q in seg])
    n = hi - lo
    w_rot = min(21, n // 2 * 2 - 1); w_uv = 9
    r = savgol_filter(r, w_rot, 3, axis=0); ld = savgol_filter(np.log(dd), w_rot, 3)
    u = savgol_filter(u, w_uv, 3); v = savgol_filter(v, w_uv, 3)
    for k in range(n):
        S[lo + k] = join(r[k], u[k], v[k], float(np.exp(ld[k])))
# v3: a game camera does not roll and does not bob. The free fit let the roll wander to -3 deg and the camera height
# between 0.81 and 1.17 m during the drive-in, which read as the car shaking. The drive-in and the hold are rebuilt
# from: view azimuth, camera height, distance (all heavily smoothed), zero roll, and the car's measured screen position.
from scipy.optimize import least_squares
def params(p):
    R, _ = cv2.Rodrigues(p[:3]); c = -R.T @ p[3:6]; pc = R @ X0 + p[3:6]
    return np.degrees(np.arctan2(c[0], -c[1])), c[2], np.linalg.norm(c - X0), F * pc[0] / pc[2], F * pc[1] / pc[2]
def build(az, cz, dist, u, v):
    h = cz - X0[2]; rho = np.sqrt(max(dist ** 2 - h ** 2, 1e-6)); a = np.radians(az)
    c = np.array([np.sin(a) * rho, -np.cos(a) * rho, cz])
    def Rof(q):                                   # zero-roll camera: yaw about world Z, then pitch
        yaw, pit = q
        fwd = np.array([np.cos(pit) * np.sin(yaw), np.cos(pit) * np.cos(yaw), np.sin(pit)])
        right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right); down = np.cross(fwd, right)
        return np.stack([right, down, fwd])
    def res(q):
        pc = Rof(q) @ (X0 - c); return [F * pc[0] / pc[2] - u, F * pc[1] / pc[2] - v]
    w = (X0 - c) / np.linalg.norm(X0 - c)
    q = least_squares(res, [np.arctan2(w[0], w[1]), np.arcsin(w[2])]).x
    R = Rof(q); return np.concatenate([cv2.Rodrigues(R)[0].ravel(), -R @ c])
hp = params(hold); hold = build(*hp)
def sm(Q):
    Q[:, 0] = savgol_filter(Q[:, 0], 21, 3); Q[:, 1] = savgol_filter(Q[:, 1], 41, 2); Q[:, 2] = np.exp(savgol_filter(np.log(Q[:, 2]), 21, 3))
    Q[:, 3] = savgol_filter(Q[:, 3], 13, 3); Q[:, 4] = savgol_filter(Q[:, 4], 13, 3)
    return Q
PAD = np.repeat(np.array([hp]), 30, 0)                         # pad with the hold so the filters settle on it
lo, hi = 0, HOLD0 - IN0 + 1
Q = np.array([params(p) for p in S[lo:hi]]); Q[:, 0] = np.unwrap(np.radians(Q[:, 0])) * 180 / np.pi
Q = sm(np.vstack([Q, PAD + [Q[-1, 0] - hp[0] - ((Q[-1, 0] - hp[0] + 180) % 360 - 180), 0, 0, 0, 0]]))
for k in range(hi):
    S[lo + k] = build(*Q[k])
lo, hi = HOLD1 - IN0, len(M)
Q = np.array([params(p) for p in S[lo:hi]]); Q[:, 0] = np.unwrap(np.radians(Q[:, 0])) * 180 / np.pi
Q = sm(np.vstack([PAD + [Q[0, 0] - hp[0] - ((Q[0, 0] - hp[0] + 180) % 360 - 180), 0, 0, 0, 0], Q]))[30:]
for k in range(hi - lo):
    S[lo + k] = build(*Q[k])
for k, i in enumerate(idx):
    if HOLD0 < i < HOLD1: S[k] = hold
# ease into / out of the hold pose over 6 frames so the car does not tick when the hold starts
for k, i in enumerate(idx):
    if HOLD0 - 10 <= i <= HOLD0: t = ((HOLD0 - i) / 10) ** 2 * (3 - 2 * (HOLD0 - i) / 10); S[k] = hold * (1 - t) + S[k] * t
    if HOLD1 <= i <= HOLD1 + 10: t = ((i - HOLD1) / 10) ** 2 * (3 - 2 * (i - HOLD1) / 10); S[k] = hold * (1 - t) + S[k] * t
print("max smoothing shift (rad, m):", np.abs(S - M)[:, :3].max().round(4), np.abs(S - M)[:, 3:].max().round(4))
json.dump({"focal_px": F, "hold": hold.tolist(), "frames": {int(i): S[k].tolist() for k, i in enumerate(idx)}}, open(f"{d}/poses.json", "w"))
cams = {int(i): sil.cam_json(S[k], F) for k, i in enumerate(idx)}
json.dump(cams, open(f"{d}/cams_all.json", "w"))
