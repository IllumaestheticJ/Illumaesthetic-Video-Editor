"""Ep 3 music re-arrangement (owner 2026-11-17: "go with the re-arranged version").

Music A (job fc267bba) measured 96.0 BPM, grid t = 0.345 + 0.625*k, bars start on k = 3 mod 4
(2.22, 4.72, 7.22, 9.72 ...). Bass/drums enter at 9.72. The quiet intro bars 2.22-9.72 are looped
under the cartoon, then the arrangement jumps into the full band at orig 32.22 on timeline bar
32.22 (v2), which is the hard cut to the real footage. Final chord at orig ~40.0 -> timeline ~40.0 (v2: cartoon is 32.23 s with lead 0.16, so the jump is at 32.22).
Splice chroma similarity: loop 9.72->2.22 0.93, jump 4.72->32.22 0.979 (tools: see editlog).
"""
import sys, wave, numpy as np

SRC, OUT = sys.argv[1], sys.argv[2]
# (orig_start, orig_end) segments in timeline order
SEGS = [(0.0, 9.72)] + [(2.22, 9.72)] * 3 + [(32.22, 44.04)]
XF = 0.020  # equal-power crossfade at each splice, centred on the bar line

w = wave.open(SRC); p = w.getparams(); sr = p.framerate; ch = p.nchannels
a = np.frombuffer(w.readframes(p.nframes), np.int16).reshape(-1, ch).astype(np.float32)
h = int(XF * sr / 2)
out = np.zeros((0, ch), np.float32)
for i, (s, e) in enumerate(SEGS):
    s0, e0 = int(round(s * sr)), min(int(round(e * sr)), len(a))
    seg = a[max(0, s0 - h):min(len(a), e0 + h)].copy()
    if i == 0:
        out = seg
        continue
    n = 2 * h
    t = np.linspace(0, np.pi / 2, n)[:, None]
    tail = out[-n:] * np.cos(t)
    head = seg[:n] * np.sin(t)
    out = np.concatenate([out[:-n], tail + head, seg[n:]])
# fade the ring-out
f = int(1.0 * sr); out[-f:] *= np.linspace(1, 0, f)[:, None]
o = wave.open(OUT, "wb"); o.setparams(p); o.writeframes(np.clip(out, -32768, 32767).astype(np.int16).tobytes()); o.close()
print(f"{OUT}: {len(out)/sr:.3f} s; jump lands at {9.72 + 3*7.5:.2f} s")
