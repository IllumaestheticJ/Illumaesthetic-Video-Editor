"""Kick-anchored beat grid + per-beat accent table for a track (lessons: anchor on the 40-120 Hz kick peak, cut on accents).
    python music_grid.py track.mp3 [--bpm 152]"""
import sys, numpy as np, librosa
path = sys.argv[1]; bpm = float(sys.argv[sys.argv.index("--bpm") + 1]) if "--bpm" in sys.argv else 152.0
y, sr = librosa.load(path, sr=22050, mono=True); hop = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop)); f = librosa.fft_frequencies(sr=sr, n_fft=2048)
low = S[(f > 40) & (f < 120)].sum(0); t = librosa.frames_to_time(np.arange(len(low)), sr=sr, hop_length=hop)
lf = np.maximum(0, np.diff(low, prepend=low[0])); lf /= lf.max()
pk = librosa.util.peak_pick(lf, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=0.08, wait=40)
kt = t[pk]; P = 60 / bpm
ph = np.angle(np.mean(np.exp(2j * np.pi * kt / P))); t0 = (ph / (2 * np.pi)) * P % P
n = np.round((kt - t0) / P); good = np.abs(kt - (t0 + n * P)) < 0.06
(Pf, t0f), *_ = np.linalg.lstsq(np.c_[n, np.ones_like(n)][good], kt[good], rcond=None)
print("kicks %d on-grid %d  period %.5f s (%.2f BPM)  t0 %.4f  resid %.1f ms" % (len(kt), good.sum(), Pf, 60 / Pf, t0f, 1000 * np.std(kt[good] - (t0f + n[good] * Pf))))
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
on = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
print(" beat     t   kick                  onset   rms(next beat)")
for k in range(int((t[-1] - t0f) / Pf) + 1):
    tb = t0f + k * Pf; i = np.searchsorted(t, tb); w = slice(max(0, i - 3), i + 4); j = np.searchsorted(t, tb + Pf)
    print(f"{k:4d} {tb:7.3f} {'#' * int(lf[w].max() * 20):20s} {on[w].max():6.1f} {rms[i:j].mean() * 100:6.1f}")
