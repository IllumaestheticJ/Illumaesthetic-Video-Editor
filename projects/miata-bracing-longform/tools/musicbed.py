"""Continuous, levelled music bed from the rough cut's own track (100.4 BPM from 3:04 to the end; the rough cut ducks it
20-30 dB under the graphic cards). usage: musicbed.py <rough_audio48.wav> <t0> <t1> <length_s> <out.wav>
Un-ducks with a slow gain envelope to a constant RMS, then repeats on a 16-beat grid with an equal-power crossfade."""
import sys, wave, numpy as np
src, t0, t1, need, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
BPM = 100.4; TARGET = -20.0; MAXG = 34.0
w = wave.open(src); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32)/32768
x = x[int(t0*sr):int(t1*sr)]; hop = sr//10; n = len(x)//hop
e = 10*np.log10((x[:n*hop].reshape(n, hop, 2)**2).mean((1, 2)) + 1e-12)
def smooth(v, k): p = np.pad(v, k, mode='edge'); return np.convolve(p, np.ones(2*k+1)/(2*k+1), 'valid')
env = smooth(np.array([np.percentile(e[max(0, i-10):i+11], 70) for i in range(n)]), 8)     # ~2 s loudness envelope
g = np.clip(TARGET - env, -12, MAXG); g = smooth(g, 5)
gain = 10**(np.interp(np.arange(len(x)), (np.arange(n)+.5)*hop, g)/20); y = x*gain[:, None]
print('gain range %.1f .. %.1f dB;  levelled rms per 20 s:' % (g.min(), g.max()), ' '.join('%.0f' % (10*np.log10((y[i:i+20*sr]**2).mean()+1e-12)) for i in range(0, len(y)-20*sr, 20*sr)))
beat = 60/BPM; L = int(round(int((len(y)/sr - 6)/(16*beat))*16*beat*sr)); xf = int(2.0*sr)              # loop length = whole 16-beat phrases
segs = [y[:L+xf]]; total = L
while total < need*sr: segs.append(y[:L+xf]); total += L
outa = np.zeros((total + xf, 2), np.float32); pos = 0; fi = np.sin(np.linspace(0, np.pi/2, xf))[:, None]; fo = np.cos(np.linspace(0, np.pi/2, xf))[:, None]
for i, s in enumerate(segs):
    s = s.copy()
    if i > 0: s[:xf] *= fi
    if i < len(segs)-1: s[L:] *= fo
    else: s = s[:L]
    outa[pos:pos+len(s)] += s; pos += L
outa = outa[:int(need*sr)]; f = int(4*sr); outa[-f:] *= np.linspace(1, 0, f)[:, None]
outa = np.tanh(outa*1.0); ww = wave.open(out, 'w'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(sr); ww.writeframes((outa*32767).astype(np.int16).tobytes())
print(out, '%.1f s, loop %.2f s (%d beats), %d passes' % (len(outa)/sr, L/sr, round(L/sr/beat), len(segs)))
