"""Kick-peak beat grid + per-beat accent strength + where the music ends (numpy only; no librosa on the box).
  accents.py track.mp3 [--period 0.604]
Lesson (FG2): anchor the grid on the kick peak (40-120 Hz energy), not the first spectral-flux onset."""
import argparse, subprocess
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("track"); ap.add_argument("--period", type=float, default=0.604)
a = ap.parse_args()
sr = 22050
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.track, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
y = np.frombuffer(raw, np.float32)
hop, n = 256, 2048
fr = np.lib.stride_tricks.sliding_window_view(np.pad(y, (n // 2, n // 2)), n)[::hop] * np.hanning(n)
S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(n, 1 / sr); t = np.arange(len(S)) * hop / sr
low = S[:, (f >= 40) & (f <= 120)].sum(1); low /= low.max()
flux = np.maximum(0, np.diff(np.log1p(S), axis=0)).sum(1); flux = np.r_[0, flux]; flux /= np.percentile(flux, 99)
db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
# kick peaks: local max of low within +-60 ms, above 0.25
w = 5
pk = [i for i in range(w, len(low) - w) if low[i] == low[i - w:i + w + 1].max() and low[i] > 0.25]
kt = t[pk]; ka = low[pk]
print("kicks:", " ".join(f"{x:.3f}" for x in kt))
P = a.period
k = np.round((kt - kt[0]) / P); A = np.vstack([k, np.ones_like(k)]).T
sol = np.linalg.lstsq(A, kt, rcond=None)[0]
for _ in range(3):
    res = kt - (A @ sol); ok = np.abs(res) < 0.06; sol = np.linalg.lstsq(A[ok], kt[ok], rcond=None)[0]
P, ph = sol; ph = ph - np.floor(ph / P) * P
print(f"grid period {P:.4f} s ({60 / P:.2f} BPM) phase {ph:.4f}; residual median {np.median(np.abs(kt[ok] - A[ok] @ sol)) * 1000:.1f} ms")
print("level dB per 0.5 s from 30 s:", " ".join(f"{s:.1f}:{db[(t >= s) & (t < s + .5)].mean():.0f}" for s in np.arange(30, t[-1], 0.5)))
for b in range(int((t[-1] - ph) / P) + 1):
    tb = ph + b * P; i = int(round(tb * sr / hop)); j = slice(max(0, i - 3), i + 4)
    print(f"b{b:02d} {tb:6.3f}  low {low[j].max():.2f}  flux {flux[j].max():4.2f}  rms {db[j].mean():6.1f}  " + "#" * int(low[j].max() * 20))
