"""Kick-anchored beat grid + per-beat strength for the reel's track (lesson: anchor on the kick peak, not flux).
    python projects/porsche-gt3rs-992/tools/music_grid.py track.mp3"""
import sys
import librosa
import numpy as np
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
hop = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
f = librosa.fft_frequencies(sr=sr, n_fft=2048)
kick = S[(f > 40) & (f < 120)].sum(0); kick /= kick.max()
t = librosa.frames_to_time(np.arange(len(kick)), sr=sr, hop_length=hop)
pk = librosa.util.peak_pick(kick, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=0.08, wait=20)
kt = t[pk[kick[pk] > 0.25]]
p, o = 0.464, kt[0]
for _ in range(4):
    k = np.round((kt - o) / p); r = kt - (p * k + o); m = np.abs(r) < 0.06
    p, o = np.polyfit(k[m], kt[m], 1)
k = np.round((kt - o) / p); r = kt - (p * k + o)
print(f"kicks {len(kt)}  period {p:.5f}  bpm {60/p:.2f}  grid offset {o:.4f}  |res| median {np.median(np.abs(r))*1000:.1f} ms")
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
hi = S[f > 2000].sum(0); hi /= hi.max()
b0 = -int(o // p)
for b in range(b0, int((len(y) / sr - o) / p) + 1):
    tb = o + b * p; i0 = int(tb * sr / hop); i1 = int((tb + p) * sr / hop)
    print(f"{b:3d} {tb:7.3f} kick={kick[max(0,i0-3):i0+4].max():.2f} hi={hi[max(0,i0-3):i0+4].max():.2f} rms={20*np.log10(rms[i0:i1].mean()+1e-9):6.1f}dB")
