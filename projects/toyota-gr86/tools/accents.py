"""Kick-anchored beat grid + per-beat accent strength + where the music ends (lessons: anchor on kick peaks,
cut on accents, measure the real end of generated tracks).
  accents.py track.mp3"""
import sys
import numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
hop = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
f = librosa.fft_frequencies(sr=sr, n_fft=2048)
kick = S[(f > 40) & (f < 120)].sum(0); kick /= kick.max()
t = librosa.frames_to_time(np.arange(len(kick)), sr=sr, hop_length=hop)
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
flux = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop); flux /= flux.max()
pk = librosa.util.peak_pick(kick, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=0.08, wait=20)
period = 0.604
# least-squares grid on strong kicks
kt = t[pk][kick[pk] > 0.35]
ph = np.angle(np.mean(np.exp(2j * np.pi * kt / period))) / (2 * np.pi) * period
n = np.round((kt - ph) / period); A = np.c_[n, np.ones_like(n)]
(per, off), *_ = np.linalg.lstsq(A, kt, rcond=None)
print(f"grid: period {per:.4f}s ({60/per:.2f} BPM) offset {off:.3f}s; kick residual ms",
      np.round(1000 * np.median(np.abs(kt - (n * per + off))), 1))
db = 20 * np.log10(rms + 1e-9); thr = db.max() - 35
last = t[np.where(db > thr)[0][-1]]
print(f"duration {len(y)/sr:.2f}s, audible to {last:.2f}s (-35 dB), peak RMS dB {db.max():.1f}")
k0 = int(np.ceil(-off / per))
print(" beat   t      kick  flux  rmsdB")
for k in range(k0, int((len(y) / sr - off) / per) + 1):
    bt = off + k * per
    i = np.searchsorted(t, bt); w = slice(max(0, i - 3), i + 4)
    print(f"{k:4d} {bt:7.3f}  {kick[w].max():.2f}  {flux[w].max():.2f}  {db[i] if i < len(db) else -99:6.1f}" + ("  <-- strong" if kick[w].max() > 0.6 else ""))
