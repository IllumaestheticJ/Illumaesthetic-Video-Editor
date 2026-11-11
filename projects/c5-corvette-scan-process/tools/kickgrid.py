"""Kick-peak beat grid (lessons: anchor on 40-120 Hz kick peaks, not spectral onsets).
Prints the fitted grid, per-beat low/full-band strength, RMS envelope per bar."""
import sys, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=256))
f = librosa.fft_frequencies(sr=sr, n_fft=2048)
low = S[(f >= 40) & (f <= 120)].sum(0)
lowflux = np.maximum(0, np.diff(low, prepend=low[0]))
lowflux /= lowflux.max()
full = librosa.onset.onset_strength(y=y, sr=sr, hop_length=256); full /= full.max()
t = librosa.frames_to_time(np.arange(len(low)), sr=sr, hop_length=256)
pk = librosa.util.peak_pick(lowflux, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=0.08, wait=10)
kt = t[pk]
P = 60 / float(sys.argv[2]) if len(sys.argv) > 2 else 0.557
# fit t0 + P*n by least squares on kicks near the grid
best = None
for t0 in np.arange(0, P, 0.002):
    n = np.round((kt - t0) / P); err = kt - (t0 + n * P)
    sc = np.sum(np.abs(err) < 0.03)
    if best is None or sc > best[0]: best = (sc, t0)
t0 = best[1]
n = np.round((kt - t0) / P); m = np.abs(kt - (t0 + n * P)) < 0.04
A = np.vstack([np.ones(m.sum()), n[m]]).T
(t0, P), *_ = np.linalg.lstsq(A, kt[m], rcond=None)
res = kt[m] - (t0 + n[m] * P)
print(f"grid t0={t0:.4f} P={P:.5f} bpm={60/P:.2f} kicks={m.sum()}/{len(kt)} rms={1000*np.sqrt((res**2).mean()):.1f}ms")
rms = librosa.feature.rms(y=y, hop_length=256)[0]
for i in range(int((len(y)/sr - t0) / P) + 1):
    bt = t0 + i * P
    j = np.searchsorted(t, bt); w = slice(max(0, j-3), j+4)
    near = kt[np.abs(kt - bt) < 0.04]
    print(f"{i:3d} {bt:7.3f}  low={lowflux[w].max():.2f} full={full[w].max():.2f} rms={rms[j:j+int(P*sr/256)].mean():.3f} {'K' if len(near) else ''}")
