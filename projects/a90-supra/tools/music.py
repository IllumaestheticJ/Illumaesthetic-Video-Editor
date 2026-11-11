"""Procedural score for the Temerario-style scan reels (numpy/scipy only; no samples, no downloads).

    python projects/a90-supra/tools/music.py out.wav [--cues cues.json]

Dark, cinematic, minimal: sub bass, detuned pads, a restrained kick + hat pulse, a riser into the
exploded view, an impact on the reassembly and a reverb tail under the logo. Everything is placed on a
bar grid derived from the shot plan, so every cut lands on a beat/bar. Reuse for another car by
passing a cues JSON (same keys as CUES below; times in bars, 1-based like a DAW = bar 1 starts at 0 s).
"""
import argparse
import json

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000

# A90 plan @ 96 BPM (bar = 2.5 s). Shots: s01 bars 1-2, s02 3-4, s03 5, s04 6, s05 7, s06 8, s07 9-10,
# s08 explode 11-13 (out on 11, back home on 13), logo 14-15 (+ tail).
CUES = {
    "bpm": 96, "beats_per_bar": 4, "bars": 15, "tail_s": 1.0,
    "chords": ["Dm", "Dm", "Bb", "Bb", "Gm", "A", "Dm", "Bb", "Gm", "Gm", "Dm", "Dm", "Bb", "Dm", "Dm"],  # one per bar
    "hats_from": 3, "kick_from": 5, "drop_drums": [9, 10, 11, 12],  # bars without the full groove
    "accent_bars": [3, 5, 6, 7, 8, 9],     # soft metallic tick on these downbeats (cuts)
    "riser": [9.0, 11.0],                   # bars: start -> resolves on the explode downbeat
    "hit": [11.0],                          # lighter hit as the panels separate
    "reverse": [12.0, 13.0],                # reverse swell into the reassembly
    "impact": [13.0],                       # big impact: panels land
    "logo": 14.0,                           # final low hit + chord, reverb tail
}

NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
        "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def chord_notes(name, octave=3):
    minor = name.endswith("m")
    root = NOTE[name[:-1] if minor else name]
    base = 12 * (octave + 1) + root
    return base, [base, base + (3 if minor else 4), base + 7, base + 12 + (3 if minor else 4)]


def lp(x, fc, order=2):
    return sosfilt(butter(order, min(fc, SR / 2.2), "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, min(hi, SR / 2.2)], "band", fs=SR, output="sos"), x)


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + phase) % 1.0) - 1


def adsr(n, a, d, s, r):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    env = np.full(n, s, dtype=np.float64)
    env[:a] = np.linspace(0, 1, a, endpoint=False) if a else env[:a]
    env[a:a + d] = np.linspace(1, s, len(env[a:a + d]))
    if r:
        env[-r:] *= np.linspace(1, 0, len(env[-r:]))
    return env


def reverb_ir(seconds=3.2, decay=3.0, seed=7):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal((2, n)) * np.exp(-decay * t)
    ir = np.stack([lp(ir[0], 6000), lp(ir[1], 5500)])
    ir[:, : int(0.012 * SR)] = 0  # pre-delay
    return ir / np.abs(ir).sum(1, keepdims=True) * 40


def render(cues):
    spb = 60.0 / cues["bpm"]
    bar = spb * cues["beats_per_bar"]
    total = cues["bars"] * bar + cues["tail_s"]
    N = int(total * SR)
    dry = np.zeros((2, N))
    wet_send = np.zeros((2, N))
    rng = np.random.default_rng(1)
    T = lambda b: (b - 1) * bar  # bar number (1-based, fractional ok) -> seconds
    I = lambda s: int(round(s * SR))

    def add(buf, sig, t0, pan=0.0, gain=1.0):
        i = I(t0)
        if i >= N:
            return
        sig = sig[: N - i]
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        buf[0, i:i + len(sig)] += sig * gain * l * 1.414
        buf[1, i:i + len(sig)] += sig * gain * r * 1.414

    # ---- pads (detuned saws, slow filter swell), one chord per bar, overlap for legato
    for bi, ch in enumerate(cues["chords"]):
        b = bi + 1
        _, notes = chord_notes(ch, 3)
        n = I(bar * 1.35)
        pad = np.zeros(n)
        for k, m in enumerate(notes):
            for det in (-0.09, 0.0, 0.08):
                pad += saw(hz(m + det), n, phase=rng.random()) * (0.6 if k == 3 else 1.0)
        intensity = 0.55 if b < 3 else (0.8 if b < 11 else 1.0)
        cut = 500 + 900 * intensity * (0.6 + 0.4 * np.sin(np.linspace(0, np.pi, n)))
        pad = lp(pad, 1400 * intensity) * 0.5 + lp(pad, 380) * 0.5
        env = adsr(n, 0.9 if b > 1 else 2.2, 0.4, 0.85, 1.0)
        pad *= env * 0.028 * (0.45 if b in cues["drop_drums"][:2] else 1.0)
        add(dry, pad, T(b), pan=-0.35, gain=0.8)
        add(dry, np.roll(pad, I(0.011)), T(b), pan=0.35, gain=0.8)
        add(wet_send, pad, T(b), gain=0.9)
        _ = cut

    # ---- sub bass: root, pulsing on beats 1 and 3 from bar 3, long drone before
    for bi, ch in enumerate(cues["chords"]):
        b = bi + 1
        root, _ = chord_notes(ch, 1)
        if b < 3 or b in (11, 12):
            n = I(bar)
            s = np.sin(2 * np.pi * hz(root) * np.arange(n) / SR) * adsr(n, 0.6, 0.2, 0.9, 0.5)
            add(dry, np.tanh(s * 1.4) * 0.22, T(b))
        else:
            for beat in (0, 2):
                n = I(spb * 1.9)
                t = np.arange(n) / SR
                s = np.sin(2 * np.pi * hz(root) * t) * np.exp(-t * 1.6) * adsr(n, 0.01, 0.05, 1.0, 0.15)
                add(dry, np.tanh(s * 1.8) * 0.26, T(b) + beat * spb)

    # ---- kick (restrained, half-time: beats 1 and 3) and hats (8ths, swung velocities)
    def kick(gain=1.0):
        n = I(0.45)
        t = np.arange(n) / SR
        f = 45 + 75 * np.exp(-t * 28)
        ph = 2 * np.pi * np.cumsum(f) / SR
        k = np.sin(ph) * np.exp(-t * 9) + 0.15 * hp(rng.standard_normal(n), 3000) * np.exp(-t * 180)
        return np.tanh(k * 1.6) * gain

    def hat(gain=1.0, open_=False):
        n = I(0.18 if open_ else 0.06)
        t = np.arange(n) / SR
        h = hp(rng.standard_normal(n), 7500, 4) * np.exp(-t * (25 if open_ else 70))
        return h * gain

    for b in range(1, cues["bars"] + 1):
        if b >= cues["logo"]:
            break
        drop = b in cues["drop_drums"]
        if b >= cues["kick_from"] and not drop:
            for beat in (0, 2):
                add(dry, kick(0.55), T(b) + beat * spb)
        if b in (9, 10):  # top-down: kick on 1 only
            add(dry, kick(0.45), T(b))
        if b >= cues["hats_from"] and b not in (11, 12):
            for e in range(8):
                v = (0.10 if e % 2 else 0.06) * (0.6 if drop else 1.0)
                add(dry, hat(v, open_=(e == 7 and b % 2 == 0)), T(b) + e * spb / 2, pan=0.25)
        if b == 13:  # reassembled: full groove + 16th hats for one bar of energy
            for e in range(16):
                add(dry, hat(0.05 + 0.04 * (e % 4 == 2)), T(b) + e * spb / 4, pan=-0.2)

    # ---- accent ticks on cut downbeats (metallic ping)
    for b in cues["accent_bars"]:
        n = I(0.9)
        t = np.arange(n) / SR
        p = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((1760, 1), (2637, 0.5), (4186, 0.25))) * np.exp(-t * 7)
        add(dry, p * 0.03, T(b), pan=0.4)
        add(wet_send, p * 0.05, T(b))

    # ---- riser into the explode: filtered noise with rising band + rising sine, crescendo
    r0, r1 = T(cues["riser"][0]), T(cues["riser"][1])
    n = I(r1 - r0)
    x = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    seg = 2048
    out = np.zeros(n)
    for i in range(0, n, seg):  # time-varying band-pass in blocks
        fc = 300 * (40 ** x[i])
        out[i:i + seg] = bp(noise[max(0, i - 4096):i + seg], fc * 0.7, fc * 1.6)[-len(out[i:i + seg]):]
    tone = np.sin(2 * np.pi * np.cumsum(110 * (4 ** x)) / SR)
    riser = (out * 0.5 + tone * 0.12) * (x ** 2.2)
    add(dry, riser * 0.18, r0)
    add(wet_send, riser * 0.25, r0)

    # ---- hits / impacts
    def boom(dur, f0, f1, gain, noise_amt=0.6, lpf=900):
        n = I(dur)
        t = np.arange(n) / SR
        f = f1 + (f0 - f1) * np.exp(-t * 6)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4)
        nz = lp(rng.standard_normal(n), lpf) * np.exp(-t * 5) * noise_amt
        return np.tanh((s + nz) * 1.5) * gain

    for b in cues["hit"]:
        add(dry, boom(2.0, 90, 38, 0.45, 0.5), T(b))
        add(wet_send, boom(2.0, 90, 38, 0.3, 0.8, 2500), T(b))
    # reverse swell (reversed reverb'd noise burst) into the impact
    q0, q1 = T(cues["reverse"][0]), T(cues["reverse"][1])
    n = I(q1 - q0)
    sw = lp(rng.standard_normal(n), 3500) * np.linspace(0, 1, n) ** 3
    add(dry, sw * 0.10, q0)
    add(wet_send, sw * 0.12, q0)
    for b in cues["impact"]:
        add(dry, boom(3.0, 120, 34, 0.75, 0.9, 1800), T(b))
        add(dry, kick(0.8), T(b))
        add(wet_send, boom(3.0, 120, 34, 0.5, 1.0, 4000), T(b))

    # ---- logo: low hit + sustained Dm voicing, mostly wet (reverb tail)
    L = T(cues["logo"])
    add(dry, boom(4.0, 70, 30, 0.6, 0.5), L)
    _, notes = chord_notes("Dm", 3)
    n = I(total - L)
    pad = sum(saw(hz(m + d), n, rng.random()) for m in notes + [notes[0] + 12] for d in (-0.07, 0.07))
    pad = lp(pad, 900) * adsr(n, 0.05, 0.6, 0.5, max(0.5, total - L - 2.0)) * 0.03
    add(dry, pad, L, gain=0.6)
    add(wet_send, pad, L, gain=1.6)
    n = I(1.5)
    t = np.arange(n) / SR
    bell = sum(np.sin(2 * np.pi * hz(m + 24) * t) * np.exp(-t * 2.5) for m in notes[:3]) * 0.02
    add(wet_send, bell, L)
    add(dry, bell, L, gain=0.5)

    # ---- mix: reverb send, glue, master
    ir = reverb_ir()
    wet = np.stack([fftconvolve(wet_send[0], ir[0])[:N], fftconvolve(wet_send[1], ir[1])[:N]])
    mix = dry + wet * 0.55
    mix = hp(mix, 25)
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)
    fo = I(1.2)
    mix[:, -fo:] *= np.linspace(1, 0, fo) ** 2
    mix /= np.abs(mix).max() / 0.89  # -1 dBFS
    return mix.T.astype(np.float32), {"bpm": cues["bpm"], "bar_s": bar, "duration_s": total,
                                      "downbeats": [round(T(b), 3) for b in range(1, cues["bars"] + 1)]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--cues")
    a = ap.parse_args()
    cues = dict(CUES, **(json.load(open(a.cues)) if a.cues else {}))
    audio, info = render(cues)
    wavfile.write(a.out, SR, (audio * 32767).astype(np.int16))
    print(json.dumps(info))
