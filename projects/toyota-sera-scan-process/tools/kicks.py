"""Kick-anchored beat grid + per-beat accent strength (lessons: anchor on 40-120 Hz kick peaks,
cut on accents). Prints the least-squares grid, per-beat low/full energy and the RMS envelope
per bar so the drop and the music end can be located.

    python tools/kicks.py track.mp3
"""
import subprocess
import sys

import numpy as np

sr, hop = 22050, 128
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
win = 2048
fr = np.lib.stride_tricks.sliding_window_view(x, win)[::hop] * np.hanning(win)
S = np.abs(np.fft.rfft(fr, axis=1))
f = np.fft.rfftfreq(win, 1 / sr)
low = S[:, (f >= 40) & (f <= 120)].sum(1)
full = S.sum(1)
t = np.arange(len(low)) * hop / sr + win / 2 / sr
lf = np.maximum(0, np.diff(np.log1p(low), prepend=0))
# kick peaks
thr = lf.mean() + 1.5 * lf.std()
pk = [i for i in range(2, len(lf) - 2) if lf[i] > thr and lf[i] == lf[i - 2:i + 3].max()]
pt = t[pk]
period = 60 / 99.4
# least squares fit of grid to peaks near integer beats
ph = np.angle(np.exp(2j * np.pi * pt / period).sum()) / (2 * np.pi) * period
for _ in range(3):
    n = np.round((pt - ph) / period)
    ok = np.abs(pt - ph - n * period) < 0.06
    A = np.vstack([np.ones(ok.sum()), n[ok]]).T
    ph, period = np.linalg.lstsq(A, pt[ok], rcond=None)[0]
print(f"grid: t0={ph:.4f} period={period:.4f} bpm={60 / period:.2f} kicks_used={ok.sum()}/{len(pt)}")
dur = len(x) / sr
k0 = int(np.ceil(-ph / period))
rms = lambda a, b: float(np.sqrt(np.mean(x[int(a * sr):int(b * sr)] ** 2)) + 1e-9)
print("beat  time   lowE  fullRMS  kick?")
for k in range(k0, int((dur - ph) / period) + 1):
    tb = ph + k * period
    if tb < 0 or tb > dur:
        continue
    i = np.searchsorted(t, tb)
    s = slice(max(0, i - 3), i + 6)
    lo = float(lf[s].max())
    near = np.min(np.abs(pt - tb)) if len(pt) else 9
    print(f"{k:4d} {tb:6.3f} {lo:6.2f} {rms(tb, tb + period):7.4f} {'K' if near < 0.04 else ''}")
