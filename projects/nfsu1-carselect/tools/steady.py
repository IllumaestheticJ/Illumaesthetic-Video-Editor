"""Take the residual wobble out of the car's screen path without re-rendering.
The camera fit (poses.json) still carries the game car's small sideways and vertical wander (it rocks on its suspension as it
brakes, and the fit is noisy when the car is small). On a rigid kit car that reads as shaking while it drives straight.
This writes track/shift.json: per capture frame, the 2D shift (px at 2144 wide) that moves the rendered car from the fitted
screen position of its centre onto a steadied one. composite.py applies it to the render only; the game-car mask keeps the
original fit.   python steady.py <work>/track"""
import sys, json, numpy as np, cv2
from scipy.signal import savgol_filter
d = sys.argv[1]
P = json.load(open(f"{d}/poses.json")); F = P["focal_px"]; X0 = np.array([0, 0, 0.5])
def uv(p):
    p = np.array(p); R, _ = cv2.Rodrigues(p[:3]); pc = R @ X0 + p[3:6]; return F * pc[0] / pc[2], F * pc[1] / pc[2]
idx = sorted(int(k) for k in P["frames"]); U = np.array([uv(P["frames"][str(i)]) for i in idx]); h = np.array(uv(P["hold"]))
IN0, HOLD0, HOLD1, OUT1 = 1653, 1746, 1838, 1972
SW0, SW1 = 1672, 1712          # the close sweep past the lens: fast and real, left alone
TAIL = 1884                    # from here the car only drives away: one cubic
N = U.copy()
def ss(t): t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)
# drive-in: heavy smoothing outside the sweep, settling on the hold
a = np.array([i - IN0 for i in range(IN0, HOLD0 + 1)]); seg = np.vstack([U[a], np.repeat([h], 40, 0)])
heavy = savgol_filter(seg, 41, 2, axis=0)[:len(a)]
fr = np.arange(IN0, HOLD0 + 1)
w = np.maximum(ss((SW0 - fr) / 8.0), ss((fr - SW1) / 8.0))[:, None]       # 1 in the straights, 0 in the sweep
heavy += (h - heavy[-1]) * ss((fr - (HOLD0 - 24)) / 24.0)[:, None]      # land exactly on the hold
N[a] = U[a] * (1 - w) + heavy * w
# settling after the sweep: one Hermite ease from the measured position and speed at SET0 onto the hold (no dip and return)
SET0 = 1718; k0 = SET0 - IN0; T = HOLD0 - SET0
p0 = N[k0]; v0 = (N[k0] - N[k0 - 4]) / 4.0 * T
for i in range(SET0, HOLD0 + 1):
    t = (i - SET0) / T
    N[i - IN0] = (2 * t**3 - 3 * t**2 + 1) * p0 + (t**3 - 2 * t**2 + t) * v0 + (-2 * t**3 + 3 * t**2) * h
# drive-away: heavy smoothing through the swing, then a cubic for the straight
b = np.array([i - IN0 for i in range(HOLD1, OUT1 + 1)]); seg = np.vstack([np.repeat([h], 40, 0), U[b]])
heavy = savgol_filter(seg, 41, 2, axis=0)[40:]
fr = np.arange(HOLD1, OUT1 + 1); t = fr >= TAIL - 12
heavy += (h - heavy[0]) * ss((HOLD1 + 24 - fr) / 24.0)[:, None]           # leave exactly from the hold
cub = np.stack([np.polyval(np.polyfit(fr[t], heavy[t, k], 3), fr) for k in (0, 1)], 1)
w = ss((fr - (TAIL - 12)) / 24.0)[:, None]
N[b] = heavy * (1 - w) + cub * w
S = N - U
for k, i in enumerate(idx):
    if HOLD0 < i < HOLD1: S[k] = 0
print("max shift px", np.abs(S).max(0).round(1))
for i in list(range(1653, 1747, 6)) + list(range(1838, 1973, 6)):
    print(i, U[i - IN0].round(1), N[i - IN0].round(1))
json.dump({str(i): S[k].tolist() for k, i in enumerate(idx)}, open(f"{d}/shift.json", "w"))
