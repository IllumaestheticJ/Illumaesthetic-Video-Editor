"""Kick-peak beat grid + per-second energy (numpy only). usage: python kicks.py <audio> [--grid]"""
import subprocess, sys
import numpy as np
sr, hop, win = 22050, 128, 2048
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
fr = np.lib.stride_tricks.sliding_window_view(x, win)[::hop] * np.hanning(win)
S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(win, 1 / sr)
t = (np.arange(len(S)) * hop + win / 2) / sr
low = S[:, (f > 40) & (f < 120)].sum(1); hi = S[:, f > 2500].sum(1); full = S.sum(1)
print("sec   low    hi   full")
for s in range(0, int(t[-1]) + 1):
    m = (t >= s) & (t < s + 1)
    print(f"{s:3d} {low[m].mean():7.1f} {hi[m].mean():6.1f} {full[m].mean():7.1f}")
# kick peaks: local maxima of low band over +-0.12 s above 35% of the running max
w = int(0.12 * sr / hop); lo = low / low.max()
pk = [i for i in range(w, len(lo) - w) if lo[i] == lo[i - w:i + w + 1].max() and lo[i] > 0.35]
print("kicks:", " ".join(f"{t[i]:.3f}({lo[i]:.2f})" for i in pk))
if "--grid" in sys.argv:
    # least-squares grid through the kick peaks, then per-beat accent = spectral flux (all bands) in +-50 ms
    kt = np.array([t[i] for i in pk]); n = np.round((kt - kt[0]) / np.median(np.diff(kt)))
    A = np.vstack([n, np.ones_like(n)]).T; per, t0 = np.linalg.lstsq(A, kt, rcond=None)[0]
    print(f"grid: t0={t0:.4f} period={per:.5f} bpm={60/per:.2f} resid_ms={1000*np.abs(A@[per,t0]-kt).max():.1f}")
    flux = np.r_[0, np.maximum(0, np.diff(np.log1p(S), axis=0)).sum(1)]
    fh = np.r_[0, np.maximum(0, np.diff(np.log1p(S[:, f > 1500]), axis=0)).sum(1)]
    k = 0
    rows = []
    while t0 + k * per < 30:
        b = t0 + k * per; m = np.abs(t - b) < 0.05
        mo = np.abs(t - (b + per / 2)) < 0.05
        rows.append((k, b, flux[m].max(), fh[m].max(), fh[mo].max()))
        k += 1
    fm = np.median([r[2] for r in rows])
    for r in rows:
        print(f"beat {r[0]:2d} {r[1]:7.3f}  flux {r[2]/fm:4.2f}  hiflux {r[3]:6.1f}  offbeat_hi {r[4]:6.1f}")
