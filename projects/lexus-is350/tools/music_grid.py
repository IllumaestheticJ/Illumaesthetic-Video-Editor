"""Beat grid + accents for the reel track: kick-peak grid (40-120 Hz energy, peak_pick, least-squares fit of
t = t0 + k*period), per-beat kick strength / broadband flux, 1 s RMS envelope (where the music really ends).
    music_grid.py track.mp3 [period_guess]"""
import sys, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
P0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
hop = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
f = librosa.fft_frequencies(sr=sr, n_fft=2048)
kick = S[(f >= 40) & (f <= 120)].sum(0); kick /= kick.max()
t = librosa.frames_to_time(np.arange(len(kick)), sr=sr, hop_length=hop)
pk = librosa.util.peak_pick(kick, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=0.05, wait=int(0.3 * sr / hop))
pt = t[pk]; strong = pt[kick[pk] > 0.25]
k = np.round((strong - strong[0]) / P0)
A = np.c_[np.ones(len(k)), k]; t0, per = np.linalg.lstsq(A, strong, rcond=None)[0]
res = strong - (t0 + per * k)
print(f"kick grid: t0={t0:.3f} period={per:.4f} ({60/per:.2f} BPM) from {len(strong)} kicks, |res| median {np.median(abs(res))*1000:.0f} ms")
flux = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
dur = len(y) / sr
print("beat   t      kick  flux  rms(dB)")
n = int((dur - t0) / per) + 1
for b in range(-int(t0 / per), n):
    tb = t0 + b * per
    i = np.searchsorted(t, tb); w = slice(max(0, i - 4), i + 6)
    kv = kick[w].max() if i < len(kick) else 0; fv = flux[w].max() if i < len(flux) else 0
    rv = 20 * np.log10(rms[w].mean() + 1e-9) if i < len(rms) else -99
    bar = "|" if b % 4 == 0 else " "
    print(f"{bar}{b:3d} {tb:6.3f}  {kv:4.2f}  {fv:5.1f}  {rv:6.1f}  " + "#" * int(kv * 20))
