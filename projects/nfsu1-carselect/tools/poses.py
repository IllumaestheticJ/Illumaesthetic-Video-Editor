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
S = M.copy()
dist = np.linalg.norm(M[:, 3:6], axis=1)
for k in range(len(M)):
    if HOLD0 - 2 <= idx[k] <= HOLD1 + 2: continue
    h = 2 if dist[k] < 9 else (4 if dist[k] < 16 else 7)      # far away the fit jitters in depth: average longer
    lo, hi = max(0, k - h), min(len(M), k + h + 1)
    if idx[k] >= HOLD1: lo = max(lo, HOLD1 - IN0)
    else: hi = min(hi, HOLD0 - IN0 + 1)
    ww = np.array([h + 1 - abs(j - k) for j in range(lo, hi)], float); ww /= ww.sum()
    S[k] = (M[lo:hi] * ww[:, None]).sum(0)
# ease into / out of the hold pose over 6 frames so the car does not tick when the hold starts
for k, i in enumerate(idx):
    if HOLD0 - 6 <= i <= HOLD0: t = (HOLD0 - i) / 6; S[k] = hold * (1 - t) + S[k] * t
    if HOLD1 <= i <= HOLD1 + 6: t = (i - HOLD1) / 6; S[k] = hold * (1 - t) + S[k] * t
print("max smoothing shift (rad, m):", np.abs(S - M)[:, :3].max().round(4), np.abs(S - M)[:, 3:].max().round(4))
json.dump({"focal_px": F, "hold": hold.tolist(), "frames": {int(i): S[k].tolist() for k, i in enumerate(idx)}}, open(f"{d}/poses.json", "w"))
cams = {int(i): sil.cam_json(S[k], F) for k, i in enumerate(idx)}
json.dump(cams, open(f"{d}/cams_all.json", "w"))
