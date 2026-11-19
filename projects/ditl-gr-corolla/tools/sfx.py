"""Synthesized sound effects (from the WRX build's sound.py), importable. Boxer engine() plus the helpers."""
import subprocess, numpy as np
SR = 48000
rng = np.random.default_rng(7)
def t_(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR))
def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def dec(d, tau): return np.exp(-t_(d) / tau)
def fade(x, a=0.005, r=0.02):
    n = len(x); e = np.ones(n); ia, ir = int(a * SR), int(r * SR); e[:ia] = np.linspace(0, 1, ia); e[n - ir:] = np.linspace(1, 0, ir); return x * e
def tone(f, d, shape="sin"):
    ph = 2 * np.pi * np.cumsum(np.broadcast_to(f, (int(d * SR),))) / SR
    if shape == "sin": return np.sin(ph)
    if shape == "saw": return 2 * ((ph / (2 * np.pi)) % 1) - 1
    return np.sign(np.sin(ph))
def load(path, ss=None, to=None):
    a = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-t", str(to)] if to else []) + ["-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(a, capture_output=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)

# ---- effects ----
def slap(g=1.0): return fade(bp(noise(0.12), 300, 6000) * dec(0.12, 0.02)) * g + fade(tone(110, 0.12) * dec(0.12, 0.03)) * 0.6 * g
def knock(): return fade(tone(np.linspace(190, 120, int(0.09 * SR)), 0.09) * dec(0.09, 0.02)) + 0.3 * fade(bp(noise(0.09), 800, 3000) * dec(0.09, 0.008))
def scratch():
    d = 0.5; f = 900 + 700 * np.sin(2 * np.pi * 5 * t_(d)); return fade(bp(noise(d), 500, 5000) * (0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.linspace(1, 0.3, int(d * SR)))
def boing(): d = 0.5; return fade(tone(180 + 120 * np.sin(2 * np.pi * 14 * t_(d)) * dec(d, 0.2), d) * dec(d, 0.18))
def bonk(): d = 0.25; return fade(tone(np.linspace(520, 300, int(d * SR)), d) * dec(d, 0.06) + 0.5 * tone(np.linspace(1040, 600, int(d * SR)), d) * dec(d, 0.03))
def brass(notes, nd=0.16):
    out = []
    for f in notes:
        x = sum(tone(f * h, nd, "saw") / h for h in (1, 2, 3)); out.append(fade(bp(x, 200, 3500), 0.01, 0.03))
    return np.concatenate(out) * 0.5
def ding(f=1320, d=0.5): return fade((tone(f, d) + 0.5 * tone(f * 2.76, d)) * dec(d, 0.15))
def chaching():
    d = 0.32; x = np.zeros(int(d * SR)); a = ding(2100, 0.2) * 0.8; b = ding(2800, 0.24); x[:len(a)] += a; x[int(0.07 * SR):int(0.07 * SR) + len(b)] += b
    return x + 0.25 * fade(bp(noise(d), 3000, 9000) * dec(d, 0.03))
def trombone():
    out = []
    for f, nd in ((233, 0.3), (220, 0.3), (208, 0.3), (196, 0.7)):
        v = f * (1 + 0.01 * np.sin(2 * np.pi * 6 * t_(nd))) * (np.linspace(1, 0.94, int(nd * SR)) if nd > 0.5 else 1); out.append(fade(bp(tone(v, nd, "saw"), 150, 1800), 0.02, 0.05))
    return np.concatenate(out) * 0.7
def choir(d=1.1):
    x = sum(tone(f * (1 + 0.004 * np.sin(2 * np.pi * 5 * t_(d) + i)), d, "saw") for i, f in enumerate((261.6, 329.6, 392, 523.3, 659.3)))
    return fade((bp(x, 500, 1100) + 0.6 * bp(x, 2300, 3200)) * 0.25, 0.05, 0.4)
def rip(d=0.3): return fade(bp(noise(d), 1500, 9000) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 70 * t_(d)))) * np.linspace(0.6, 1, int(d * SR)))
def kiss(): d = 0.22; return fade(bp(noise(d), 1800, 6000) * dec(d, 0.05) * 0.6 + tone(np.linspace(900, 2400, int(d * SR)), d) * dec(d, 0.04) * 0.5)
def squeak(d=0.25): return fade(tone(2200 + 500 * np.sin(2 * np.pi * 9 * t_(d)), d) * 0.3 + bp(noise(d), 2000, 4000) * 0.2)
def levelup(): return np.concatenate([fade(tone(f, 0.09, "sq") * 0.3 + tone(f, 0.09) * 0.5) for f in (523, 659, 784, 1047, 1319)])
def womp(): d = 0.5; return fade(bp(tone(np.linspace(150, 70, int(d * SR)), d, "saw"), 50, 700) * dec(d, 0.25)) * 1.2
def airhorn(d=0.5):
    x = sum(tone(f, d, "saw") for f in (392, 415, 466, 494)); return fade(np.tanh(bp(x, 300, 4000) * 1.5) * 0.6, 0.01, 0.08)
def engine(d, rpm0, rpm1, g=1.0):
    """Subaru boxer four on unequal-length headers: the four exhaust pulses per cycle arrive in two uneven pairs,
    so the note sits at half the firing frequency with an off-beat burble instead of an even inline-four buzz."""
    n = int(d * SR); f = np.linspace(rpm0, rpm1, n) / 60 * 2; ph = np.cumsum(f / 4) / SR; x = np.zeros(n)
    for o, a_ in ((0.0, 1.0), (0.2, 0.55), (0.5, 0.9), (0.72, 0.5)):
        u = (ph - o) % 1.0; x += a_ * np.exp(-u * 16) * np.sin(2 * np.pi * u * 5.5)
    x += 0.5 * np.sin(2 * np.pi * np.cumsum(f / 2) / SR) + 0.25 * np.sin(2 * np.pi * np.cumsum(f * 0.75) / SR)
    x += 0.12 * bp(noise(d)[:n], 300, 2400) * (0.4 + np.exp(-((ph * 2) % 1.0) * 6))
    return fade(np.tanh(bp(x, 30, 2600) * 1.1) * g, 0.03, 0.06)
def rev(d=0.45, top=5200): return engine(d * 0.45, 1100, top, 1.0).tolist() and np.concatenate([engine(d * 0.45, 1100, top), engine(d * 0.55, top, 1300, 0.8)])
def whoosh(d=0.6, lo=300, hi=3000): e = np.sin(np.pi * t_(d) / d) ** 2; return fade(bp(noise(d), lo, hi) * e)
def bov(): d = 0.45; return fade(bp(noise(d), 2500, 11000) * dec(d, 0.14) * (0.7 + 0.3 * np.sign(np.sin(2 * np.pi * 38 * t_(d)))))
def screech(d=0.9): f = 1500 + 250 * np.sin(2 * np.pi * 7 * t_(d)); return fade((tone(f, d, "saw") * 0.25 + bp(noise(d), 1200, 2600) * 0.9) * np.linspace(1, 0.5, int(d * SR)), 0.01, 0.2)
def crunch(): d = 0.18; return fade(bp(noise(d), 200, 2500) * (np.sign(np.sin(2 * np.pi * 55 * t_(d))) * 0.5 + 0.5) * dec(d, 0.08))
def whistle(up=True, d=0.7): f = np.linspace(500, 1900, int(d * SR)) if up else np.linspace(1900, 400, int(d * SR)); return fade(tone(f * (1 + 0.01 * np.sin(2 * np.pi * 7 * t_(d))), d) * 0.5, 0.02, 0.08)
def beep(f=1900, d=0.12): return fade(tone(f, d, "sq") * 0.35)
def tick(): return fade(bp(noise(0.02), 2000, 9000) * dec(0.02, 0.004))
def heartbeat(d): 
    x = np.zeros(int(d * SR)); b = fade(tone(np.linspace(70, 45, int(0.12 * SR)), 0.12) * dec(0.12, 0.04))
    for t0 in np.arange(0, d - 0.5, 0.85):
        for o in (0, 0.22): i = int((t0 + o) * SR); x[i:i + len(b)] += b * (1 if o == 0 else 0.7)
    return x
def pen(d): return fade(bp(noise(d), 2500, 7000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 11 * t_(d)))) * 0.6)
def bell(d=1.0): return fade(sum(tone(f, d) for f in (2093, 2637, 3136)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 28 * t_(d)))) * 0.2, 0.005, 0.3)
def shutdown(): return np.concatenate([fade((tone(f, 0.38) + 0.3 * tone(f * 2, 0.38)) * dec(0.38, 0.3)) for f in (831, 622, 415, 466)]) * 0.5
def toy(d):
    notes = (523, 523, 784, 784, 880, 880, 784, 0, 698, 698, 659, 659, 587, 587, 523, 0); x = np.concatenate([fade(tone(f, 0.2, "sq") * 0.2 + tone(f, 0.2) * 0.4) if f else np.zeros(int(0.2 * SR)) for f in notes])
    return np.tile(x, int(d / 3.2) + 1)[:int(d * SR)]
def birds(d):
    x = np.zeros(int(d * SR))
    for t0 in rng.uniform(0, d - 0.3, int(d * 2.5)):
        c = fade(tone(np.linspace(rng.uniform(3000, 4500), rng.uniform(2400, 5200), int(0.09 * SR)), 0.09)) * rng.uniform(0.2, 0.6); i = int(t0 * SR); x[i:i + len(c)] += c
    return x
def hum(d, f=120): return (tone(f, d) + 0.5 * tone(f * 2, d) + 0.3 * tone(f * 3, d)) * 0.15 + bp(noise(d), 200, 2500) * 0.03
def traffic(d): return bp(noise(d), 40, 400) * 0.5 * (1 + 0.3 * np.sin(2 * np.pi * 0.3 * t_(d)))
def wind(d, g0=0.2, g1=1.0): return bp(noise(d), 150, 1800) * np.linspace(g0, g1, int(d * SR)) * (1 + 0.2 * np.sin(2 * np.pi * 0.8 * t_(d)))
def siren(d): return fade(tone(700 + 250 * np.sin(2 * np.pi * 0.45 * t_(d)), d) * 0.06, 0.5, 0.5)

def ms(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs: o[:len(x)] += x
    return o

