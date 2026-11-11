"""Rank candidate TTS takes against a reference narration (no cloning - picks the closest PRESET): median F0, F0 spread,
pace (voiced onsets/s over speech time), and long-term average spectrum distance (1/3-oct bands 300-5000 Hz, level-normalised).
usage: voicematch.py REF START END cand.wav ..."""
import sys
import numpy as np
from voicestats import load, f0_track


def ltas(x, sr):
    fr = np.fft.rfftfreq(2048, 1 / sr)
    S = (np.abs(np.fft.rfft(x[: len(x) // 2048 * 2048].reshape(-1, 2048) * np.hanning(2048), axis=1)) ** 2)
    e = S.sum(1); S = S[e > np.percentile(e, 40)].mean(0)           # speech frames only
    c = 300 * 2 ** (np.arange(0, 12.5) / 3); b = []
    for f in c:
        m = (fr >= f / 2 ** (1 / 6)) & (fr < f * 2 ** (1 / 6)); b.append(10 * np.log10(S[m].mean() + 1e-12))
    b = np.array(b); return b - b.mean()


def feat(p, a=None, b=None):
    x, sr = load(p, a, b); f = f0_track(x, sr); v = f[f > 0]
    on = np.flatnonzero(np.diff((f > 0).astype(int)) == 1)
    speech = (np.convolve((f > 0).astype(float), np.ones(50), "same") > 0).mean() * len(x) / sr   # time within 0.5 s of voicing
    return dict(f0=float(np.median(v)), iqr=float(np.subtract(*np.percentile(v, [75, 25]))), pace=len(on) / speech, lt=ltas(x, sr))


if __name__ == "__main__":
    ref = feat(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
    print(f"REF f0 {ref['f0']:.0f} iqr {ref['iqr']:.0f} pace {ref['pace']:.2f}")
    for p in sys.argv[4:]:
        c = feat(p); d = np.sqrt(np.mean((c["lt"] - ref["lt"]) ** 2))
        st = 12 * np.log2(c["f0"] / ref["f0"])
        print(f"{p.split('/')[-1]:14s} f0 {c['f0']:.0f} ({st:+.1f} st) iqr {c['iqr']:.0f} pace {c['pace']:.2f} (x{ref['pace']/c['pace']:.2f} needed) timbre-dist {d:.1f} dB")
