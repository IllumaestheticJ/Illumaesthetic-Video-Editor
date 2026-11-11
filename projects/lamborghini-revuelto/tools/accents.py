"""Music map for cutting: RMS per 0.5 s, low-band (40-120 Hz kick/taiko) peaks, beat grid fitted to those peaks,
and per-beat accent strength (spectral flux + low-band energy). Lesson: anchor the grid on kick peaks, not the
first flux onset.   accents.py track.mp3 [bpm]"""
import sys, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
hop = 256; t = lambda f: f * hop / sr
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
print("duration %.3f" % (len(y) / sr))
print("RMS dBFS per 0.5 s:")
step = int(0.5 * sr / hop)
print(" ".join("%.1f:%d" % (t(i), 20 * np.log10(rms[i:i + step].mean() + 1e-9)) for i in range(0, len(rms), step)))
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop)); f = librosa.fft_frequencies(sr=sr, n_fft=2048)
low = S[(f >= 40) & (f <= 120)].sum(0); low = low / low.max()
flux = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop); flux = flux / flux.max()
pk = librosa.util.peak_pick(low, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=0.08, wait=20)
print("low-band peaks (t, strength):", [(round(t(p), 3), round(float(low[p]), 2)) for p in pk])
bpm = float(sys.argv[2]) if len(sys.argv) > 2 else float(librosa.beat.tempo(onset_envelope=flux, sr=sr, hop_length=hop)[0])
P = 60 / bpm
# fit phase of the grid to the strong low peaks (least squares on the nearest-beat residuals)
strong = np.array([t(p) for p in pk if low[p] > 0.3])
best = min(np.linspace(0, P, 200, endpoint=False), key=lambda ph: np.sum(np.minimum(((strong - ph + P / 2) % P - P / 2) ** 2, 0.01)))
res = (strong - best + P / 2) % P - P / 2
ph = best + np.mean(res[np.abs(res) < 0.06]) if np.any(np.abs(res) < 0.06) else best
print("bpm %.2f period %.4f phase %.4f (resid ms med %.1f)" % (bpm, P, ph, 1000 * np.median(np.abs(res))))
grid = np.arange(ph, len(y) / sr, P)
print("beat  t      low   flux  rms_dB")
for i, g in enumerate(grid):
    fr = int(round(g * sr / hop)); w = slice(max(0, fr - 3), fr + 4)
    print("%3d %7.3f  %.2f  %.2f  %d" % (i, g, low[w].max(), flux[w].max(), 20 * np.log10(rms[w].mean() + 1e-9)))
