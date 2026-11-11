"""Kick-peak beat grid (numpy only): 40-120 Hz energy envelope, local-max peaks, least-squares fit to period P.
usage: kickgrid.py audio [period_s]   -> prints grid t0/period and per-beat kick/broadband strength"""
import sys, subprocess, numpy as np
f = sys.argv[1]; P0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
sr = 22050
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
hop, n = 256, 2048; win = np.hanning(n)
fr = np.lib.stride_tricks.sliding_window_view(y, n)[::hop] * win
S = np.abs(np.fft.rfft(fr, axis=1)); fq = np.fft.rfftfreq(n, 1 / sr); t = (np.arange(len(S)) * hop + n / 2) / sr
kick = S[:, (fq >= 40) & (fq <= 120)].sum(1); kick /= kick.max()
flux = np.maximum(0, np.diff(np.log1p(S), axis=0)).sum(1); flux = np.r_[0, flux]; flux /= flux.max()
rms = np.sqrt((fr ** 2).mean(1))
pk = [i for i in range(8, len(kick) - 8) if kick[i] == kick[i - 8:i + 9].max() and kick[i] > 0.25]
pt = t[pk]
n_ = np.round((pt - pt[0]) / P0); A = np.c_[np.ones_like(n_), n_]; c = np.linalg.lstsq(A, pt, rcond=None)[0]; r = pt - A @ c
print("kick peaks %d  grid t0 %.4f period %.5f  rms %.1f ms" % (len(pt), c[0], c[1], 1000 * np.sqrt((r ** 2).mean())))
k = 0
while c[0] + c[1] * (k - 1) > 0: k -= 1
b = c[0] + c[1] * k
while b < t[-1]:
    i = np.argmin(abs(t - b)); w = slice(max(0, i - 4), i + 5)
    print("%7.3f kick %.2f flux %.2f rms %.3f %s" % (b, kick[w].max(), flux[w].max(), rms[i], "#" * int(kick[w].max() * 20)))
    k += 1; b = c[0] + c[1] * k
