"""Rebuild the sound of the rough cut's front section (0-190 s) from the raw camera clips and the original voice-over
recording, so none of the rough cut's music is left in it.   usage: python cleanfront.py <media_dir>
Needs <media_dir>/prproj/match.json (scripts/match.py: which raw clip each half second came from) and raw_audio/*.flac|m4a.
Writes work/front_clean48.wav (mono, 48 kHz, same timeline as the rough cut) and prints how well each stretch lines up."""
import sys, json, subprocess, wave, numpy as np
M = sys.argv[1]; SR = 48000; N = 190*SR
def load(p, ss=None, t=None):
    c = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(t)] if t else []) + ['-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-']
    return np.frombuffer(subprocess.run(c, capture_output=True).stdout, np.float32)
rough = load(f'{M}/work/audio48.wav', 0, 190)*np.float32(0.70711); WIN = 2.0      # ffmpeg's mono downmix is (L+R)*0.707; per-channel level is what the mix needs
runs = []
for t, n, p, v in json.load(open(f'{M}/prproj/match.json')):
    if not n or v <= 0.35: continue
    if runs and runs[-1]['clip'] == n and abs((p - t) - runs[-1]['lag']) < 0.03: runs[-1]['t1'] = t + WIN; runs[-1]['n'] += 1
    else: runs.append(dict(clip=n, lag=p - t, t0=t, t1=t + WIN, n=1))
runs = [r for r in runs if r['n'] >= 2 or r['clip'].startswith('AUDIO')]            # single stray windows are false matches
raw = {}
def clip(n):
    if n not in raw: raw[n] = load(f'{M}/raw_audio/{n}')
    return raw[n]
def seg(r, a, b):          # raw audio that belongs at rough-cut time a..b for run r
    x = clip(r['clip']); i = int(round((a + r['lag'])*SR)); k = int(round((b - a)*SR)); out = np.zeros(k, np.float32)
    j0 = max(i, 0); j1 = min(i + k, len(x))
    if j1 > j0: out[j0 - i:j1 - i] = x[j0:j1]
    return out
def ncc(a, b): n = min(len(a), len(b)); a, b = a[:n], b[:n]; return float(a@b/(np.sqrt((a@a)*(b@b)) + 1e-12))
for r in runs:             # refine the lag to the sample
    a, b = r['t0'] + .3, min(r['t1'] - .3, r['t0'] + 6); q = rough[int(a*SR):int(b*SR)]; best = (-1, 0)
    for d in range(-960, 961, 4):
        r2 = dict(r, lag=r['lag'] + d/SR); c = ncc(q, seg(r2, a, b))
        if c > best[0]: best = (c, d)
    r['lag'] += best[1]/SR; r['fit'] = best[0]
# where one run hands over to the next: the first 50 ms step where the next run fits the rough cut better
cuts = []
for A, B in zip(runs, runs[1:]):
    lo, hi = B['t0'], min(A['t1'], B['t1']); c = (lo + hi)/2
    if hi > lo:
        best = None
        for t in np.arange(lo, hi, 0.05):
            q = rough[int(t*SR):int((t + .25)*SR)]
            if len(q) < 100: break
            if ncc(q, seg(B, t, t + .25)) > ncc(q, seg(A, t, t + .25)) + .05: best = t; break
        c = best if best is not None else hi
    cuts.append(float(c))
edges = [runs[0]['t0']] + cuts + [min(runs[-1]['t1'], 190.0)]; out = np.zeros(N, np.float32)
for r, a, b in zip(runs, edges, edges[1:]):
    if b - a >= 0.05: r['a'], r['b'] = a, b
# The editor filtered and levelled the dialogue. Per clip, estimate that processing as a transfer curve H(f) = |Sxy|/Sxx between
# the raw audio x and the rough cut y (the music is uncorrelated with x, so it drops out), and apply it to the raw audio.
NF = 4096; fr = np.fft.rfftfreq(NF, 1/SR); H = {}
for n in sorted({r['clip'] for r in runs if 'a' in r}):
    Sxy = np.zeros(NF//2 + 1, complex); Sxx = np.zeros(NF//2 + 1)
    for r in runs:
        if r['clip'] != n or 'a' not in r: continue
        x = seg(r, r['a'], r['b']); q = rough[int(round(r['a']*SR)):int(round(r['a']*SR)) + len(x)]; x = x[:len(q)]
        for k in range(0, len(x) - NF, NF//2):
            X = np.fft.rfft(x[k:k + NF]*np.hanning(NF)); Q = np.fft.rfft(q[k:k + NF]*np.hanning(NF)); Sxy += np.conj(X)*Q; Sxx += np.abs(X)**2
    h = 20*np.log10(np.abs(Sxy)/(Sxx + 1e-12) + 1e-6)
    sm = np.array([h[(fr >= f/1.12) & (fr <= f*1.12)].mean() if f > 30 else h[1:4].mean() for f in fr]); md = np.median(sm[(fr > 200) & (fr < 2000)]); H[n] = np.clip(sm, md - 4, md + 4)      # level plus gentle tone only: the estimate is noisy at the extremes
    print('%-32s editor curve (dB) at 50/100/200/500/1k/2k/4k/8k/12k Hz: %s' % (n, ' '.join('%+.0f' % np.interp(f, fr, H[n]) for f in (50, 100, 200, 500, 1000, 2000, 4000, 8000, 12000))))
def shape(x, n):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/SR); return np.fft.irfft(X*10**(np.interp(f, fr, H[n])/20), len(x)).astype(np.float32)
F = int(.012*SR); PAD = 0.5
for r in runs:
    if 'a' not in r: continue
    a, b = r['a'], r['b']; x = shape(seg(r, a - PAD, b + PAD), r['clip']); k = int((PAD - .012)*SR); x = x[k:len(x) - k].copy(); x[:2*F] *= np.linspace(0, 1, 2*F); x[-2*F:] *= np.linspace(1, 0, 2*F)
    p = int(round((a - .012)*SR)); p0 = max(p, 0); x = x[p0 - p:]; x = x[:N - p0]; out[p0:p0 + len(x)] += x
    q = rough[int(a*SR):int(b*SR)]; y = out[int(a*SR):int(b*SR)]
    print('%6.2f-%6.2f  %-32s clip %7.2f s  match %.2f' % (a, b, r['clip'], a + r['lag'], ncc(q, y[:len(q)])))
w = wave.open(f'{M}/work/front_clean48.wav', 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1)*32767).astype(np.int16).tobytes())
res = rough - out; e = lambda v: 20*np.log10(np.sqrt((v**2).mean()) + 1e-9)
print('rough %.1f dB, rebuilt dialogue %.1f dB, what is left when the dialogue is subtracted (the old music + effects) %.1f dB' % (e(rough[:184*SR]), e(out[:184*SR]), e(res[:184*SR])))
