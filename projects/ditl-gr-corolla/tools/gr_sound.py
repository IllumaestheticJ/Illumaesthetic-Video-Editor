"""Soundtrack for the DITL GR Corolla short: voice + synthesized SFX (+ music when the owner supplies a track).
python gr_sound.py <out.wav> [music.mp3 start_s tempo]"""
import sys, subprocess, numpy as np
from sfx import *
M = "/home/user/media/ditl-gr-corolla/"; NF = [65, 48, 47, 95, 47, 48, 47, 47, 95, 48, 47, 48, 95, 213]
CUT = [sum(NF[:i]) for i in range(len(NF) + 1)]; DUR = CUT[-1] / 30.0
def T(shot, frame=0): return (CUT[shot - 1] + frame) / 30.0

def triple(d, rpm0, rpm1, g=1.0):
    """GR Corolla G16E-GTS: turbo inline three. Three evenly spaced pulses per cycle (1.5 x rpm/60 Hz) with a strong
    half-order growl, a raspy top end and a turbo whistle that rises with revs."""
    n = int(d * SR); r = np.linspace(rpm0, rpm1, n); f = r / 60 * 1.5; ph = np.cumsum(f) / SR; u = ph % 1.0
    x = np.exp(-u * 9) * np.sin(2 * np.pi * u * 3.2) + 0.7 * np.sin(2 * np.pi * ph) + 0.45 * np.sin(2 * np.pi * ph * 0.5) + 0.3 * np.sin(2 * np.pi * ph * 1.5)
    x += 0.2 * bp(noise(d)[:n], 900, 4200) * (0.3 + np.exp(-u * 5))
    x = np.tanh(bp(x, 40, 4200) * 1.6); wh = np.sin(2 * np.pi * np.cumsum(2500 + r * 0.9) / SR) * np.clip((r - 2500) / 4000, 0, 1) * 0.12
    return fade((x + wh) * g, 0.03, 0.06)
def vtec(d, rpm0, rpm1, g=1.0):
    """Type R K20C1: even inline four (2 x rpm/60 Hz), smooth and high, harmonics opening up at the top."""
    n = int(d * SR); r = np.linspace(rpm0, rpm1, n); f = r / 60 * 2; ph = np.cumsum(f) / SR; top = np.clip((r - 4500) / 2500, 0, 1)
    x = np.sin(2 * np.pi * ph) + 0.5 * np.sin(2 * np.pi * ph * 2) + (0.25 + 0.6 * top) * np.sin(2 * np.pi * ph * 3) + 0.4 * top * np.sin(2 * np.pi * ph * 4) + 0.3 * np.sin(2 * np.pi * ph * 0.5)
    x += 0.08 * bp(noise(d)[:n], 1500, 6000)
    return fade(np.tanh(bp(x, 60, 7000) * 1.2) * g, 0.03, 0.06)
def revs(fn, d, top): return np.concatenate([fn(d * 0.45, 1100, top), fn(d * 0.55, top, 1300, 0.8)])
def click(): return fade(bp(noise(0.03), 1500, 7000) * dec(0.03, 0.006)) + 0.6 * fade(tone(1800, 0.03) * dec(0.03, 0.008))
def thud(): d = 0.22; return fade(tone(np.linspace(140, 60, int(d * SR)), d) * dec(d, 0.06)) * 1.4 + 0.5 * fade(bp(noise(d), 200, 1500) * dec(d, 0.03))
def cricket(d):
    x = np.zeros(int(d * SR)); c = fade(tone(4300, 0.05) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 60 * t_(0.05)))))
    for t0 in np.arange(0.2, d - 0.4, 0.75):
        for o in (0, 0.08, 0.16): i = int((t0 + o) * SR); x[i:i + len(c)] += c * 0.3
    return x
def meep(): return fade(tone(540, 0.16, "sq") * 0.3 + tone(680, 0.16, "sq") * 0.2, 0.005, 0.03)
def violin(d=0.5): f = np.linspace(1900, 2600, int(d * SR)) * (1 + 0.01 * np.sin(2 * np.pi * 9 * t_(d))); return fade(bp(tone(f, d, "saw"), 1500, 6000) * 0.5, 0.01, 0.05)
def rattle(d): return fade(bp(noise(d), 1500, 5000) * (0.4 + 0.6 * (np.sin(2 * np.pi * 17 * t_(d)) > 0.3)) * 0.4)

mix = np.zeros((int(DUR * SR) + SR, 2))
def put(x, at, g=1.0, pan=0.0):
    x = np.asarray(x, dtype=np.float64); i = int(at * SR)
    if x.ndim == 1: x = np.stack([x * (1 - max(0, pan)), x * (1 + min(0, pan))], 1)
    n = min(len(x), len(mix) - i)
    if n > 0: mix[i:i + n] += x[:n] * g

# ---- music (owner's track, when supplied): from start_s, played at <tempo>, dead at the meet (shot 13) ----
mend = T(13); g = None; MOFF = 0.0
if len(sys.argv) > 2:
    ss, tempo = float(sys.argv[3]), float(sys.argv[4])
    mus = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", sys.argv[2], "-af", "atempo=%s" % tempo, "-t", str(mend), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)
    g = np.ones(len(mus)); g[-int(0.02 * SR):] = np.linspace(1, 0, int(0.02 * SR))
# ---- voice: exchange.wav = "I wanted something different." (0.16-1.62 s) + "Same." (2.19-2.70 s); whisper.wav = "...different." ----
ex = load(M + "voice/exchange.wav"); him = ex[:int(1.9 * SR)]; same = ex[int(2.05 * SR):]
def pitch(x, k):   # resample: k > 1 is higher and shorter (the second "Same." voice)
    i = np.arange(0, len(x) - 1, k); return np.stack([np.interp(i, np.arange(len(x)), x[:, c]) for c in range(2)], 1)
VO = [(him, T(9, 6), 2.4, 0.0), (same, T(9, 58), 2.6, 0.45), (pitch(same, 0.9), T(9, 58) + 0.01, 2.4, -0.45), (load(M + "voice/whisper.wav"), T(14, 150), 3.0, 0.0)]
for v, at, vg, pan in VO:
    if g is not None:
        i0, i1 = int((at - 0.15) * SR), int((at + len(v) / SR + 0.15) * SR); r = int(0.12 * SR)
        for i, j, a, b in ((i0 - r, i0, 1, 0.3), (i0, i1, 0.3, 0.3), (i1, i1 + r, 0.3, 1)):
            i, j = max(0, i), min(len(g), j)
            if j > i: g[i:j] = np.minimum(g[i:j], np.linspace(a, b, j - i))
    put(np.tanh(v * vg * 1.2) * np.array([1 - max(0, pan), 1 + min(0, pan)]), at, 1.0)
if g is not None: put(mus * g[:, None], MOFF, 0.5)

# ---- 1 phone ----
put(hum(T(2), 60), 0, 0.3)
for f in (15, 33): put(whoosh(0.18, 1500, 6000), T(1, f - 2), 0.7); put(womp() * 0.5, T(1, f + 3), 0.5)
put(ms(slap(1.2), ding(1760, 0.5)), T(1, 53), 1.3)
for f in (57, 60, 63): put(click(), T(1, f), 0.9)
# ---- 2-3 dealer ----
put(hum(T(4) - T(2), 100), T(2), 0.4); put(pen(0.33), T(2, 2), 1.0); put(whoosh(0.2, 400, 3000), T(2, 18), 0.8); put(ms(thud(), slap(1.2)), T(2, 24), 1.5); put(whoosh(0.2, 600, 5000), T(2, 37), 0.7); put(boing(), T(2, 40), 0.7)
put(pen(0.9), T(3, 1), 1.0); put(pen(0.9) * 0.8, T(3, 3), 0.9, pan=-0.4); put(chaching(), T(3, 14), 1.3); put(chaching(), T(3, 28), 1.4); put(brass((523, 659, 784, 1047), 0.09), T(3, 30), 0.6)
# ---- 4 unboxing ----
lot0, lot1 = T(4), T(6); put(birds(lot1 - lot0), lot0, 0.5); put(traffic(lot1 - lot0), lot0, 0.25)
for f in (1, 4, 7, 10): put(rip(0.22), T(4, f), 0.9, pan=(-0.4 if f % 2 else 0.4))
for i in range(5):
    s0 = 11 + i * 16; put(rip(0.12), T(4, s0), 0.6); put(whoosh(0.26, 300, 4000), T(4, s0 + 6), 1.1); put(ms(crunch(), ding(880 * 1.189 ** i, 0.35) * 0.7), T(4, s0 + 12), 1.3, pan=-0.3)
put(choir(0.6), T(4, 78), 1.1); put(levelup(), T(4, 80), 0.5)
# ---- 5 cylinders ----
for i, f in enumerate((6, 13, 20)): put(ms(knock(), ding(1047 * 1.26 ** i, 0.3)), T(5, f), 1.1)
put(whistle(True, 0.3), T(5, 24), 0.4); put(boing(), T(5, 31), 0.9); put(womp(), T(5, 37), 0.7)
for f in (43, 47): put(ms(slap(0.9), knock()), T(5, f), 1.0)
# ---- 6 AWD dial ----
cab0 = T(6); put(traffic(T(9) - cab0), cab0, 0.3); put(triple(T(8) - cab0, 900, 940, 0.2), cab0)
for i in range(11): put(ms(click(), beep(1500 + 300 * (i % 3), 0.05) * 0.5), T(6, 1 + i * 4), 1.1)
put(screech(0.35), T(6, 26), 0.5); put(whoosh(0.25, 500, 4000), T(6, 27), 0.6); put(rattle(0.6), T(6, 30), 0.9, pan=-0.5)
# ---- 7 Kevin ----
put(thud(), T(7, 2), 1.2); put(whoosh(0.2, 500, 4000), T(7, 3), 0.7); put(ding(1568, 0.4), T(7, 11), 0.9); put(ding(2093, 0.4), T(7, 13), 0.7); put(click(), T(7, 20), 1.0); put(scratch(), T(7, 24), 0.8)
# ---- 8 grandma ----
put(triple(0.3, 1200, 800, 0.15), T(8)); put(meep(), T(8, 9), 0.9, pan=0.5); put(meep(), T(8, 14), 0.9, pan=0.5); put(trombone(), T(8, 22), 0.9); put(whistle(False, 0.5), T(8, 28), 0.5)
# ---- 9-10 red light ----
rl0 = T(9); d9 = T(11) - rl0; put(traffic(d9), rl0, 0.3); put(triple(d9, 880, 900, 0.2), rl0); put(vtec(d9, 820, 840, 0.1), rl0, 1.0, pan=-0.5); put(engine(d9, 760, 790, 0.12), rl0, 1.0, pan=0.5)
for f in range(0, 95, 20): put(tick(), T(9, f), 0.6); put(tick(), T(9, f + 9), 0.4)
put(whoosh(0.2, 500, 5000), T(9, 50), 0.8); put(whoosh(0.2, 500, 5000), T(9, 76), 0.8); put(womp(), T(9, 72), 1.0)
for rf in (4, 17, 30): put(revs(triple, 0.42, 6200), T(10, rf), 0.9); put(revs(vtec, 0.42, 7000), T(10, rf), 0.7, pan=-0.5); put(revs(engine, 0.42, 4900), T(10, rf), 0.7, pan=0.5); put(whoosh(0.35, 400, 2500), T(10, rf), 0.6)
put(airhorn(0.45), T(10, 31), 1.0)
# ---- 11 hybrid ----
gs0 = T(11); put(traffic(T(12) - gs0), gs0, 0.3); put(hum(T(12) - gs0, 180), gs0, 0.25)
for f in (2, 6): put(beep(2100, 0.08), T(11, f), 0.6)
put(ding(1568, 0.4), T(11, 9), 0.9); put(violin(0.5), T(11, 28), 0.9); put(squeak(0.5), T(11, 32), 0.9)
# ---- 12 stickers ----
put(birds(T(13) - T(12)), T(12), 0.4)
for i, sf in enumerate((9, 22, 35)): put(rip(0.12), T(12, sf - 5), 0.6); put(ms(slap(1.3), ding(1320 * 1.26 ** i, 0.3) * 0.6), T(12, sf), 1.4)
# ---- 13 meet: silence ----
put(wind(T(14) - T(13), 0.3, 0.5), T(13), 0.25); put(cricket(T(14) - T(13)), T(13), 0.6); put(scratch(), T(13, 0), 0.7)
for i in range(6): put(bp(noise(0.25), 3000, 9000) * np.linspace(0.2, 1, int(0.25 * SR)) * 0.3, T(13, 54 + i * 3), 1.0, pan=-0.6 + i * 0.24)
put(womp(), T(13, 52), 0.9)
# ---- 14 mirror ----
d14 = T(15) - T(14); put(wind(d14, 0.3, 0.2), T(14), 0.2); put(cricket(d14), T(14), 0.4)
for f in (16, 21, 27, 33, 39): put(knock() * 0.5, T(14, f), 0.7)
for f in range(50, 213, 17): put(ms(tick(), ding(2600, 0.06) * 0.2), T(14, f), 0.6)
put(meep(), T(14, 104), 0.7, pan=-0.4); put(ding(1760, 0.4), T(14, 106), 0.5); put(heartbeat(2.5), T(14, 118), 1.0); put(shutdown(), T(14, 186), 0.4)
out = mix[:int(DUR * SR)]; out[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))[:, None]
out = np.tanh(out * 0.9)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", "loudnorm=I=-13.0:TP=-1.2:LRA=11", "-ar", "48000", sys.argv[1]], input=out.astype(np.float32).tobytes())
