"""Measure the QX80 track: loudness envelope, end of music, beat-grid phase, and per-beat accent strength.
  python music.py track.mp3
Beat grid: period from `ive beats` (0.650 s); phase fitted to the low-band (40-150 Hz) + full-band flux peaks.
Accent = onset flux in a +-50 ms window at each grid beat (normalised), plus low-band hit and RMS."""
import subprocess, sys, numpy as np
SR = 22050
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)
y = load(sys.argv[1]); period = float(sys.argv[2]) if len(sys.argv) > 2 else 0.650
hop, n = 256, 2048
fr = np.lib.stride_tricks.sliding_window_view(np.pad(y, (n // 2, n // 2)), n)[::hop] * np.hanning(n)
S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(n, 1 / SR); t = np.arange(len(S)) * hop / SR
L = np.log1p(S * 10)
flux = np.maximum(0, np.diff(L, axis=0, prepend=L[:1])).sum(1)
lowflux = np.maximum(0, np.diff(L[:, (f > 40) & (f < 150)], axis=0, prepend=L[:1, (f > 40) & (f < 150)])).sum(1)
rms = np.sqrt((fr ** 2).mean(1)); db = 20 * np.log10(rms + 1e-9)
print("dB/s:", " ".join(f"{s}:{db[(t >= s) & (t < s + 1)].mean():.0f}" for s in range(int(t[-1]) + 1)))
peak = db.max(); loud = np.where(db > peak - 30)[0]
print(f"last frame within 30 dB of peak: {t[loud[-1]]:.2f} s; within 20 dB: {t[np.where(db > peak - 20)[0][-1]]:.2f} s")
# phase: maximise summed flux on the grid
env = flux / flux.max() + lowflux / lowflux.max()
ph = np.arange(0, period, 0.002)
score = [np.interp(np.arange(p, t[-1], period), t, env).sum() for p in ph]
p0 = ph[int(np.argmax(score))]
print(f"grid phase {p0:.3f} s, period {period:.3f}")
g = np.arange(p0, t[-1], period)
def win(sig, x): i = np.searchsorted(t, x); return sig[max(0, i - 4):i + 5].max()
A = np.array([win(flux, b) for b in g]); A /= A.max(); Lo = np.array([win(lowflux, b) for b in g]); Lo /= Lo.max()
for i, b in enumerate(g):
    print(f"beat {i:3d} {b:6.3f}  flux {A[i]:.2f}  low {Lo[i]:.2f}  dB {win(db, b):5.1f} {'#' * int(A[i] * 30)}")
