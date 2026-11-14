"""which raw clip (and where in it) each half second of the rough cut's first 3 minutes came from: normalised cross-correlation at 8 kHz"""
import glob, subprocess, numpy as np, json, os
from scipy.signal import fftconvolve
R = 8000
def load(p, ss=None, t=None):
    c = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(t)] if t else []) + ['-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(R), '-']
    return np.frombuffer(subprocess.run(c, capture_output=True).stdout, np.float32)
def hp(x):   # speech band emphasis: first difference
    return np.diff(x, prepend=0)
rough = hp(load('work/audio48.wav', 0, 190))
names = sorted(glob.glob('raw_audio/*.flac')) + sorted(glob.glob('raw_audio/*.m4a')); clips = [hp(load(n)) for n in names]
off = np.cumsum([0] + [len(c) + R for c in clips]); big = np.zeros(off[-1], np.float32)
for c, o in zip(clips, off): big[o:o + len(c)] = c
print('raw total %.1f min' % (len(big)/R/60))
WIN, HOP = int(2.0*R), int(0.5*R); e2 = np.cumsum(np.concatenate([[0], big.astype(np.float64)**2])); out = []
for s in range(0, len(rough) - WIN, HOP):
    w = rough[s:s + WIN]; nw = np.sqrt((w.astype(np.float64)**2).sum())
    if nw < 1e-3: out.append((s/R, None, 0, 0)); continue
    cc = fftconvolve(big, w[::-1], mode='valid'); en = np.sqrt(np.maximum(e2[WIN:] - e2[:-WIN], 1e-9)); ncc = cc/(en*nw)
    k = int(np.argmax(ncc)); ci = int(np.searchsorted(off, k, side='right') - 1); out.append((s/R, os.path.basename(names[ci]), (k - off[ci])/R, float(ncc[k])))
json.dump(out, open('prproj/match.json', 'w'))
# runs: consecutive windows with the same clip and consistent lag
runs = []
for t, n, p, v in out:
    if n and v > 0.35 and runs and runs[-1]['clip'] == n and abs((p - t) - runs[-1]['lag']) < 0.03: runs[-1]['t1'] = t + WIN/R; runs[-1]['v'].append(v)
    elif n and v > 0.35: runs.append(dict(clip=n, lag=p - t, t0=t, t1=t + WIN/R, v=[v]))
for r in runs: print('%6.1f-%6.1f  %-34s clip time %7.2f  corr %.2f (%d win)' % (r['t0'], r['t1'], r['clip'], r['t0'] + r['lag'], np.mean(r['v']), len(r['v'])))
cov = np.zeros(190*2)
for r in runs: cov[int(r['t0']*2):int(r['t1']*2)] = 1
print('covered %.0f of 190 s; gaps:' % (cov.sum()/2), [(i/2) for i in range(len(cov)) if not cov[i]][:80])
