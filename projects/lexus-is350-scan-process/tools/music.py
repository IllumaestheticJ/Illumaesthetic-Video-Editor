"""Build the reel's music: start on kick 26 (drop = kick 32 lands at 3.000 s), repeat the 16 beats
kick 40..56 once (8.0 s) so the scan section has room, then let the track end naturally.
Kick-peak grid (40-120 Hz, least squares, 3.0 ms rms): t_k = 0.0545 + 0.50004 k."""
import numpy as np, soundfile as sf, librosa, sys
src, out = sys.argv[1], sys.argv[2]
y, sr = librosa.load(src, sr=44100, mono=False)
t = lambda k: 0.0545 + 0.50004 * k
pre = 0.015; xf = int(0.012 * sr)
s = lambda sec: int(round(sec * sr))
a = y[:, s(t(26)):s(t(56) - pre) + xf]          # +xf tail: crossfades overlap, grid stays continuous
b = y[:, s(t(40) - pre):s(t(56) - pre) + xf]
c = y[:, s(t(56) - pre):]
def join(p, q):
    r = np.linspace(0, 1, xf)
    mid = p[:, -xf:] * (1 - r) + q[:, :xf] * r
    return np.concatenate([p[:, :-xf], mid, q[:, xf:]], axis=1)
o = join(join(a, b), c)
sf.write(out, o.T, sr, subtype='PCM_24')
print("duration", o.shape[1] / sr, "drop at", t(32) - t(26), "last kick at", t(64) - t(26) + 0.50004 * 16)
