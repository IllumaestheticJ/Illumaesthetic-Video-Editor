"""Soundtrack for the DITL WRX short: music + voice + synthesized SFX. python sound.py <out.wav>"""
import sys, subprocess, numpy as np
SR = 48000; M = "/home/user/media/ditl-wrx-vb/"; DUR = 33.5
CUT = [0, 65, 113, 160, 208, 255, 302, 350, 445, 492, 539, 634, 682, 729, 776, 855, 1005]
def T(shot, frame=0): return (CUT[shot - 1] + frame) / 30.0
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
    f = np.linspace(rpm0, rpm1, int(d * SR)) / 60 * 2; x = sum(tone(f * h, d, "saw") / h for h in (1, 2, 3, 4)); am = 1 + 0.45 * np.sin(2 * np.pi * np.cumsum(f / 2) / SR)
    return fade(np.tanh(bp(x * am, 40, 2500) * 0.8) * g, 0.03, 0.06)
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

mix = np.zeros((int(DUR * SR) + SR, 2))
def put(x, at, g=1.0, pan=0.0):
    x = np.asarray(x, dtype=np.float64); i = int(at * SR)
    if x.ndim == 1: x = np.stack([x * (1 - max(0, pan)), x * (1 + min(0, pan))], 1)
    n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n] += x[:n] * g

# ---- music: from 0:30, dead at the Odyssey pass ----
mend = T(15); mus = load(M + "music/first_time.mp3", ss=30.0, to=mend); g = np.ones(len(mus)); g[-int(0.02 * SR):] = np.linspace(1, 0, int(0.02 * SR))
VO = [(M + "voice/take3/1_semperfi.wav", T(8) + 0.55, 2.6), (M + "voice/take3/2_exchange.wav", T(11, 70) - 1.84, 1.5), (M + "voice/take3/3_ringlands.wav", T(16, 122) - 0.25, 2.8)]
for pth, at, vg in VO:
    v = load(pth); i0, i1 = int((at - 0.15) * SR), int((at + len(v) / SR + 0.15) * SR); r = int(0.12 * SR)
    for i, j, a, b in ((i0 - r, i0, 1, 0.3), (i0, i1, 0.3, 0.3), (i1, i1 + r, 0.3, 1)):
        i, j = max(0, i), min(len(g), j)
        if j > i: g[i:j] = np.minimum(g[i:j], np.linspace(a, b, j - i))
    put(np.tanh(v * vg * 1.2), at, 1.0)
put(mus * g[:, None], 0, 0.5)

# ---- per-shot beds and effects ----
put(hum(T(2)), 0, 0.5); put(bell(0.9), 0.05, 0.5)
for sf in (7, 19, 30, 40, 49, 57, 64): put(slap(), T(1, sf), 1.3)
put(scratch(), T(1, 58), 0.9)
put(hum(T(4) - T(2), 100), T(2), 0.4); put(pen(1.5), T(2, 2), 0.9); put(boing(), T(2, 36), 0.9)
put(whoosh(0.25, 800, 5000), T(3, 3), 0.6); put(brass((392, 523, 659, 784), 0.13), T(3, 6), 0.8); put(bonk(), T(3, 29), 1.6); put(womp(), T(3, 31), 0.6)
put(hum(T(7) - T(4), 60), T(4), 0.3)
for i, f in enumerate((11, 21, 31, 41)): put(whoosh(0.15, 1500, 6000), T(4, f - 3), 0.5); put(ding(1320 * 2 ** (i / 6), 0.35), T(4, f), 0.7)
f = 6.0; gap = 6.0
while f < 46: put(chaching(), T(5, int(round(f))), 0.9); f += gap; gap = max(2.6, gap * 0.82)
put(ding(1760, 0.6), T(6, 1), 0.7); put(brass((523, 659, 784, 1047), 0.09), T(6, 9), 0.6); put(trombone(), T(6, 18), 0.9)
lot0, lot1 = T(7), T(10); put(birds(lot1 - lot0), lot0, 0.5); put(traffic(lot1 - lot0), lot0, 0.25)
for f in (1, 4, 7, 10, 13): put(rip(0.22), T(7, f), 0.9, pan=(-0.4 if f % 2 else 0.4))
put(whoosh(0.3, 300, 4000), T(7, 15), 1.0); put(choir(), T(7, 21), 1.3)
for f in range(1, 95, 5): put(knock(), T(8, f + 2), 1.1)
put(heartbeat(3.0), T(8), 1.2); put(bp(noise(0.9), 3000, 9000) * np.linspace(0.2, 1, int(0.9 * SR)) * 0.25, T(8, 22)); put(whoosh(1.2, 500, 2500), T(8, 44), 0.5)
for f in range(4, 95, 16): put(ms(tick(), ding(3200, 0.08) * 0.3), T(8, f), 0.5)
put(whoosh(0.4, 300, 3000), T(9, 12), 0.8); put(squeak(), T(9, 24), 0.8); put(kiss(), T(9, 28), 1.6); put(squeak(0.4), T(9, 34), 0.5)
cab0 = T(10); put(traffic(T(15) - cab0), cab0, 0.3); put(engine(T(14) - cab0, 850, 880, 0.22), cab0)
for f in (6, 14, 22): put(ms(slap(1.2), knock()), T(10, f), 1.2)
put(levelup(), T(10, 27), 0.9)
for f in range(0, 143, 20): put(tick(), T(11, f), 0.6); put(tick(), T(11, f + 9), 0.4)
put(engine(T(14) - T(11), 760, 790, 0.14), T(11), 1.0, pan=0.5); put(womp(), T(11, 93), 1.0)
for rf in (4, 17, 30): put(rev(0.42), T(12, rf), 0.9, pan=-0.3); put(rev(0.42, 4700), T(12, rf), 0.7, pan=0.5); put(whoosh(0.35, 400, 2500), T(12, rf), 0.7)
put(airhorn(0.45), T(12, 31), 1.0)
put(whoosh(0.2, 500, 5000), T(13, 1), 0.9); put(toy(T(14) - T(13)), T(13), 0.35, pan=-0.5)
for sf in (10, 17): put(slap(1.4), T(13, sf), 1.3); put(squeak(0.12), T(13, sf + 1), 0.6)
put(ms(fade(bp(noise(0.3), 300, 1500) * dec(0.3, 0.1)), boing() * 0.3), T(13, 20), 0.9)
for pf in (3, 8, 13): put(ms(slap(0.9), knock()), T(14, pf), 1.1)
put(screech(1.0), T(14, 17), 1.1); put(engine(1.0, 2500, 6800, 0.9), T(14, 17)); put(whoosh(1.0, 600, 5000), T(14, 17), 0.8); put(whistle(True, 0.7), T(14, 18), 0.5)
put(crunch(), T(14, 46), 1.4)
put(bov(), T(15, 1), 1.4); put(engine(1.4, 5200, 1500, 0.5), T(15, 2)); put(engine(T(17) - T(15) - 1.2, 1400, 900, 0.2), T(15, 40))
d15 = T(17) - T(15); put(wind(d15, 0.9, 0.25), T(15), 0.5)
vh = hum(2.6, 95) * np.sin(np.pi * t_(2.6) / 2.6) ** 0.7; put(vh, T(15), 2.2, pan=-0.6); put(toy(2.6) * np.sin(np.pi * t_(2.6) / 2.6), T(15), 0.6, pan=-0.6); put(whoosh(0.9, 200, 2500), T(15, 14), 1.2, pan=-0.5)
put(whistle(False, 0.9), T(15, 36), 0.6)
for f in (16, 20, 24): put(beep(), T(16, f), 0.9)
for f in (36, 41, 46, 51): put(knock() * 0.5, T(16, f + 2), 0.7)
for f in range(30, 150, 17): put(ms(tick(), ding(2600, 0.06) * 0.2), T(16, f), 0.6)
put(siren(4.0), T(16, 20)); put(shutdown(), T(16, 66), 0.5)
out = mix[:int(DUR * SR)]; out[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))[:, None]
out = np.tanh(out * 0.9)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", "loudnorm=I=-14:TP=-1.2:LRA=11", "-ar", "48000", sys.argv[1]], input=out.astype(np.float32).tobytes())
