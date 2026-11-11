"""Measure the Miata track: kick peaks (40-120 Hz), beat grid fitted to them (least squares), per-beat kick/RMS/onset,
and where the music ends. Lessons: anchor the grid on the kick peak, cut on accents, measure the real end.
  music_scan.py track.mp3"""
import sys, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
hop = 128
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop)); f = librosa.fft_frequencies(sr=sr, n_fft=2048)
low = S[(f > 40) & (f < 120)].sum(0); low /= low.max()
hi = S[f > 2000].sum(0); hi /= hi.max()
rms = librosa.feature.rms(y=y, hop_length=hop)[0]; db = 20 * np.log10(rms + 1e-6)
on = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop); on /= on.max()
t = librosa.frames_to_time(np.arange(len(low)), sr=sr, hop_length=hop)
pk = librosa.util.peak_pick(low, pre_max=10, post_max=10, pre_avg=40, post_avg=40, delta=0.05, wait=60)
kt, kv = t[pk], low[pk]
strong = kt[kv > 0.35]
print("strong kicks:", len(strong), np.round(strong, 3).tolist())
# grid fit: period + phase by least squares on strong kicks
P = np.median(np.diff(strong)); t0 = strong[0]
for _ in range(5):  # iterate: index kicks on the current grid, refit period + phase
    n = np.round((strong - t0) / P)
    A = np.c_[n, np.ones_like(n)]; (P, t0), *_ = np.linalg.lstsq(A, strong, rcond=None)
res = strong - (t0 + n * P)
print(f"grid: beat {P:.5f} s ({60/P:.2f} BPM), anchor {t0:.3f}, residual p50 {np.median(np.abs(res))*1000:.1f} ms max {np.abs(res).max()*1000:.1f} ms")
k0 = int(np.floor(-t0 / P))
print(" beat   t     kick  rms_dB onset hihat")
for k in range(k0, int((t[-1] - t0) / P) + 1):
    bt = t0 + k * P
    if bt < 0: continue
    m = (t > bt - 0.06) & (t < bt + 0.08)
    w = (t > bt) & (t < bt + P)
    if not m.any(): continue
    print(f"{k:4d} {bt:6.3f}  {low[m].max():.2f}  {db[w].mean():6.1f}  {on[m].max():.2f}  {hi[m].max():.2f}")
# end of music
for thr in (-30, -40, -50):
    loud = t[db > db.max() + thr]
    print(f"last frame within {thr} dB of peak: {loud.max():.2f} s")
