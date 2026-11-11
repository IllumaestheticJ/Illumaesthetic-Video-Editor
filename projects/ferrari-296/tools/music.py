"""Procedural score for scan reels: dark, cinematic, minimal. numpy only (no samples, no downloads).

    python projects/ferrari-296/tools/music.py projects/ferrari-296/cues.json out.wav

Everything is driven by a cue file built from the shot plan, so every cut and key motion moment gets
a hit exactly where the picture needs it. Reusable by other reels: write a new cues.json.

cues.json
{
  "bpm": 100, "length": 39.6, "key_root": 50,          # MIDI root (50 = D3)
  "chords": [[0, "m"], [-4, ""], [-7, "m"], [-5, ""]],  # semitone offset from root + quality, 2 bars each
  "sections": [{"start": 0, "end": 4.8, "kick": "none|half|four", "hats": 0..1, "pad": 0..1, "sub": 0..1}],
  "hits":   [{"t": 4.8, "kind": "cut|swell|whoosh|impact|big|chord", "gain": 1.0}],
  "risers": [{"start": 24.0, "end": 26.4, "gain": 1.0}],
  "fade_out": [36.0, 39.6]
}
"""
from __future__ import annotations

import json
import sys
import wave

import numpy as np

SR = 48000


def midi_hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def fft_filter(x, lo=None, hi=None, slope=4):
    """Zero-phase band filter in the frequency domain (whole-signal, cheap for a 40 s cue)."""
    n = len(x)
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / (1 + (f / hi) ** (2 * slope))
    if lo:
        g *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** (2 * slope))
    return np.fft.irfft(X * (g[:, None] if x.ndim == 2 else g), n=n, axis=0)


def conv(x, ir):
    n = len(x) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:len(x)]


def reverb(st, secs=3.2, mix=0.35, seed=7, pre=0.02):
    rng = np.random.default_rng(seed)
    t = np.arange(int(secs * SR)) / SR
    out = st.copy()
    for c in range(2):
        ir = rng.standard_normal(len(t)) * np.exp(-t / (secs / 6.9))
        ir = fft_filter(ir, lo=120, hi=6000, slope=1)
        ir[: int(pre * SR)] = 0
        ir /= np.sqrt((ir ** 2).sum())
        out[:, c] = st[:, c] + mix * conv(st[:, c], ir)
    return out


def env_adsr(n, a, d, s, r, total):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), 1.0)
    e = np.where((t >= a) & (t < a + d), 1 - (1 - s) * (t - a) / max(d, 1e-4), e)
    e = np.where(t >= a + d, s, e)
    rel = np.clip((t - (total - r)) / max(r, 1e-4), 0, 1)
    return e * (1 - rel)


def saw(freq, n, phase=0.0):
    ph = (phase + np.arange(n) * freq / SR) % 1.0
    return 2 * ph - 1


def place(buf, sig, t):
    i = int(round(t * SR))
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def kick(gain=1.0):
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    f = 42 + 95 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.32)
    click = np.random.default_rng(1).standard_normal(n) * np.exp(-t / 0.004) * 0.15
    return np.tanh(1.6 * (body + click)) * 0.8 * gain


def hat(gain=1.0, seed=0):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    x = np.random.default_rng(seed).standard_normal(n)
    x = np.diff(np.diff(x, prepend=0), prepend=0)  # crude high-pass
    return x * np.exp(-t / 0.022) * 0.06 * gain


def cut_hit(gain=1.0):
    """Soft low thump + air: marks a cut without shouting."""
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    f = 55 + 60 * np.exp(-t / 0.05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.45) * 0.55
    nz = fft_filter(np.random.default_rng(3).standard_normal(n), lo=1500, hi=9000, slope=2) * np.exp(-t / 0.08) * 0.08
    return (s + nz) * gain


def impact(gain=1.0, big=False):
    n = int((5.0 if big else 3.0) * SR)
    t = np.arange(n) / SR
    f = 30 + (110 if big else 80) * np.exp(-t / (0.09 if big else 0.06))
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (1.4 if big else 0.7))
    rng = np.random.default_rng(11 if big else 12)
    crack = fft_filter(rng.standard_normal(n), lo=300, hi=7000, slope=1) * np.exp(-t / (0.12 if big else 0.07)) * 0.35
    metal = sum(np.sin(2 * np.pi * fr * t + p) for fr, p in [(523.0, 0.1), (787.4, 1.2), (1193.0, 2.0)]) \
        * np.exp(-t / (1.1 if big else 0.5)) * (0.05 if big else 0.03)
    return np.tanh(1.3 * (boom + crack + metal)) * (1.0 if big else 0.75) * gain


def whoosh(dur=1.2, gain=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.random.default_rng(5).standard_normal(n)
    lo = fft_filter(x, lo=200, hi=1200, slope=1)
    hi = fft_filter(x, lo=1500, hi=6000, slope=1)
    u = t / dur
    e = np.sin(np.pi * np.clip(u, 0, 1)) ** 2
    return (lo * (1 - u) + hi * u) * e * 0.12 * gain


def riser(dur, gain=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    u = t / dur
    f = 110 * 2 ** (3.0 * u ** 1.6)  # three octaves up
    tone = sum(np.sin(2 * np.pi * np.cumsum(f * d) / SR) for d in (1.0, 1.006, 0.994)) / 3
    x = np.random.default_rng(9).standard_normal(n)
    bands = [fft_filter(x, lo=f0, hi=f0 * 2.5, slope=1) for f0 in (300, 800, 2000, 5000)]
    w = np.clip(u * 4 - np.arange(4)[:, None] * 0.9, 0, 1)  # brighter bands fade in over time
    noise = sum(b * wi for b, wi in zip(bands, w))
    e = u ** 2.2
    return (tone * 0.18 + noise * 0.22) * e * gain


def chord_notes(root, off, q):
    third = 3 if q == "m" else 4
    r = root + off
    return [r - 12, r, r + 7, r + third + 12, r + 14 if q == "m" else r + 11]


def render(cues: dict) -> np.ndarray:
    bpm = cues["bpm"]
    beat = 60.0 / bpm
    bar = 4 * beat
    L = cues["length"]
    n = int(L * SR)
    pad = np.zeros(n)
    sub = np.zeros(n)
    drums = np.zeros(n)
    fx = np.zeros(n)
    root = cues.get("key_root", 50)
    chords = cues["chords"]

    def sec_at(t):
        for s in cues["sections"]:
            if s["start"] <= t < s["end"]:
                return s
        return {"kick": "none", "hats": 0, "pad": 0.6, "sub": 0.6}

    # pads + sub, one chord per 2 bars
    span = 2 * bar
    for i in range(int(np.ceil(L / span))):
        t0 = i * span
        off, q = chords[i % len(chords)]
        seg = int((span + 1.5) * SR)
        s = sec_at(t0 + 0.01)
        e = env_adsr(seg, 1.2, 0.5, 0.85, 1.4, span + 1.5)
        voice = np.zeros(seg)
        for k, m in enumerate(chord_notes(root, off, q)):
            for d in (-0.07, 0.0, 0.08):
                voice += saw(midi_hz(m + d), seg, phase=(k * 0.13 + d) % 1) * (0.5 if k == 0 else 0.33)
        place(pad, voice * e * 0.06 * s.get("pad", 1.0), t0)
        f0 = midi_hz(root + off - 24)
        st = np.arange(seg) / SR
        sb = np.tanh(1.8 * np.sin(2 * np.pi * f0 * st)) * env_adsr(seg, 0.3, 0.3, 0.9, 1.0, span + 1.5)
        place(sub, sb * 0.32 * s.get("sub", 1.0), t0)
    pad = fft_filter(pad, hi=1800, slope=2)

    # drums on the grid
    nbeats = int(L / beat) + 1
    duck = np.ones(n)
    for b in range(nbeats):
        t = b * beat
        s = sec_at(t + 1e-3)
        pos = b % 4
        k = s.get("kick", "none")
        if (k == "four") or (k == "half" and pos in (0, 2)) or (k == "one" and pos == 0):
            place(drums, kick(s.get("kick_gain", 0.8)), t)
            i = int(t * SR)
            dn = int(0.35 * SR)
            duck[i:i + dn] = np.minimum(duck[i:i + dn], 0.35 + 0.65 * np.linspace(0, 1, len(duck[i:i + dn])) ** 0.5)
        h = s.get("hats", 0)
        if h:
            place(drums, hat(h * 1.0, seed=b), t + beat / 2)
            if s.get("ticks"):
                place(drums, hat(h * 0.45, seed=b + 999), t + beat / 4)
                place(drums, hat(h * 0.45, seed=b + 777), t + 3 * beat / 4)
    sub *= duck
    pad *= 0.6 + 0.4 * duck

    for h in cues.get("hits", []):
        g = h.get("gain", 1.0)
        kind = h["kind"]
        if kind == "cut":
            place(fx, cut_hit(g), h["t"])
        elif kind == "impact":
            place(fx, impact(g), h["t"])
        elif kind == "big":
            place(fx, impact(g, big=True), h["t"])
            # suck the bed out right before the lock so it lands harder
            i = int((h["t"] - 0.25) * SR)
            j = int(h["t"] * SR)
            ramp = np.linspace(1, 0.25, j - i)
            for buf in (pad, sub, drums):
                buf[i:j] *= ramp
        elif kind == "whoosh":
            d = h.get("dur", 1.2)
            place(fx, whoosh(d, g), h["t"] - d * 0.6)  # peak a little before t, settles on t
        elif kind == "swell":
            d = h.get("dur", 1.2)
            sw = whoosh(d, g)[::-1] * np.linspace(0.2, 1, int(d * SR)) ** 2
            place(fx, sw, h["t"] - d)
        elif kind == "chord":  # final logo chord
            off, q = h.get("chord", [0, "m"])
            d = h.get("dur", 6.0)
            seg = int(d * SR)
            v = np.zeros(seg)
            for m in chord_notes(root, off, q)[1:]:
                for dt in (-0.06, 0.0, 0.06):
                    v += np.sin(2 * np.pi * midi_hz(m + 12 + dt) * np.arange(seg) / SR)
            v *= env_adsr(seg, 0.02, 0.6, 0.35, d * 0.8, d) * 0.05 * g
            place(fx, v, h["t"])
    for r in cues.get("risers", []):
        d = r["end"] - r["start"]
        place(fx, riser(d, r.get("gain", 1.0)), r["start"])

    # stereo: pad wide (Haas + detune already), drums centre, fx through a big hall
    st = np.zeros((n, 2))
    dl = int(0.011 * SR)
    st[:, 0] += pad
    st[dl:, 1] += pad[:-dl]
    st += sub[:, None]
    st += drums[:, None]
    wet = reverb(np.stack([fx, fx], 1), secs=4.5, mix=0.9, seed=3)
    st += wet
    st = reverb(st, secs=2.2, mix=0.18)
    if cues.get("fade_out"):
        a, b = cues["fade_out"]
        t = np.arange(n) / SR
        st *= np.clip((b - t) / (b - a), 0, 1)[:, None] ** 1.5
    st = fft_filter(st, lo=28, slope=2)
    st /= np.abs(st).max() + 1e-9
    st = np.tanh(1.4 * st) / np.tanh(1.4)  # gentle glue / peak control
    rms = np.sqrt((st ** 2).mean())
    st *= min(0.89 / np.abs(st).max(), 0.16 / rms)  # ~-16 dBFS RMS, peaks <= -1 dBFS
    return st


def write_wav(path, st):
    pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    cues = json.load(open(sys.argv[1]))
    st = render(cues)
    write_wav(sys.argv[2], st)
    print(json.dumps({"out": sys.argv[2], "seconds": round(len(st) / SR, 3),
                      "peak_dbfs": round(20 * np.log10(np.abs(st).max()), 2),
                      "rms_dbfs": round(20 * np.log10(np.sqrt((st ** 2).mean())), 2)}))
