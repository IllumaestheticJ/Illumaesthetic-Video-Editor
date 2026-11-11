"""Measure the Mazda track: per-second loudness, kick (40-130 Hz) onsets, and per-beat accent strength on a fitted grid.
    python projects/mazda-3-gen4/tools/music_grid.py track.mp3 [--bpm 110]"""
import subprocess, sys, numpy as np
from scipy.signal import find_peaks
path = sys.argv[1]; bpm = float(sys.argv[sys.argv.index("--bpm") + 1]) if "--bpm" in sys.argv else 110.0
sr = 22050
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32)
hop, n = 256, 2048
fr = np.lib.stride_tricks.sliding_window_view(np.pad(y, (n // 2, n // 2)), n)[::hop] * np.hanning(n)
S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(n, 1 / sr); t = np.arange(len(S)) * hop / sr
low = S[:, (f > 40) & (f < 130)].sum(1); full = np.sqrt((fr ** 2).mean(1))
print("per-second RMS dB / low-band:")
for s in range(int(t[-1]) + 1):
    m = (t >= s) & (t < s + 1)
    print(f"  {s:2d}s {20*np.log10(full[m].mean()+1e-9):6.1f} dB  low {low[m].mean():7.1f}")
lf = np.maximum(0, np.diff(low, prepend=low[0]))
pk, _ = find_peaks(lf, height=lf.max() * 0.12, distance=int(0.2 * sr / hop))
kicks = t[pk]; print("kick onsets:", [round(float(k), 3) for k in kicks])
beat = 60 / bpm
# fit phase: least squares of kicks to nearest grid line
best = min(np.linspace(0, beat, 200, endpoint=False), key=lambda p: np.sum(np.minimum(((kicks - p) % beat), beat - ((kicks - p) % beat)) ** 2))
k = np.round((kicks - best) / beat); A = np.vstack([k, np.ones_like(k)]).T
per, ph = np.linalg.lstsq(A, kicks, rcond=None)[0]
print(f"grid: beat {per:.4f} s ({60/per:.2f} BPM), phase {ph:.3f}")
grid = ph + per * np.arange(-2, int(t[-1] / per) + 2); grid = grid[(grid >= 0) & (grid < t[-1])]
print("per-beat strength (low-band flux within 60 ms):")
for i, g in enumerate(grid):
    m = (t > g - 0.03) & (t < g + 0.06)
    v = lf[m].max() if m.any() else 0
    print(f"  b{i:02d} {g:7.3f}  {'#' * int(40 * v / lf.max())}")
