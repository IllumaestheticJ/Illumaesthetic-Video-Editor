"""Repeat the 8 beats [a, b) of the track once at b (12 ms crossfades) - lessons: extend on measured kick onsets.
   python extend_music.py in.mp3 out.wav a b"""
import sys, numpy as np, soundfile as sf, librosa
y, sr = librosa.load(sys.argv[1], sr=44100, mono=False)
a, b = float(sys.argv[3]), float(sys.argv[4])
y = np.atleast_2d(y); ia, ib = int(a * sr), int(b * sr); xf = int(0.012 * sr)
seg = y[:, ia:ib].copy(); tail = y[:, ib:]
ramp = np.linspace(0, 1, xf)
# seam 1: end of original [..b) -> start of repeat ; seam 2: end of repeat -> original b..
out1 = y[:, :ib].copy(); out1[:, -xf:] = out1[:, -xf:] * (1 - ramp) + seg[:, :xf] * ramp
rep = seg[:, xf:].copy(); rep[:, -xf:] = rep[:, -xf:] * (1 - ramp) + tail[:, :xf] * ramp
out = np.concatenate([out1, rep, tail[:, xf:]], axis=1)
sf.write(sys.argv[2], out.T, sr); print(sys.argv[2], out.shape[1] / sr)
