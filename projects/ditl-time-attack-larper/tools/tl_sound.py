"""Mix for the track-guy short: approved voice takes + scene SFX + meme SFX, no music. python tl_sound.py <out.wav>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tl_sound_fx import *

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

V = M + "voice/"
ex = load(V + "take1/exchange.wav"); solo = load(V + "take1/solo.wav"); sigh = load(V + "take2/sigh.wav")
aero = solo[:int(1.8 * SR)]                                   # "Aero's working." (0.15-1.64 s of the solo take)

# 1 bedroom: alarm, slap, whip, spoon on the visor x5 with milk
for f in range(1, 7, 2): put(beep(1900, 0.09), T(1, f), 0.8)
put(slap(1.2), T(1, 6), 1.3); put(whoosh(0.3, 500, 4000), T(1, 14), 0.8); put(hum(T(2), 90), 0, 0.25)
for f in (22, 26, 30): put(knock() * 0.5, T(1, f), 0.6)                         # footsteps to the mirror
put(ms(choir(1.3), ding(1760, 0.5) * 0.6), T(1, 33), 1.0); put(levelup(), T(1, 42), 0.4)   # the reveal: already suited up
# 2 sign-up: heartbeat while the thumb hovers, swipe away
put(heartbeat(1.6), T(2), 1.1); put(whoosh(0.22, 800, 5000), T(2, 35), 0.9)
# 3 cart: cha-ching on every Confirm tap (same schedule as tl_shots.s3)
f = 4.0; gap = 6.0
while f < 45: put(chaching(), T(3, int(round(f))), 0.9); f += gap; gap = max(2.6, gap * 0.8)
# 4 driveway: rip, throw, slam onto the hatch, choir, kiss
put(birds(T(5) - T(4)), T(4), 0.45)
for f in (1, 4, 7, 10): put(rip(0.22), T(4, f), 0.9, pan=(-0.4 if f % 2 else 0.4))
put(whoosh(0.4, 300, 4000), T(4, 24), 1.1); put(ms(crunch(), bonk() * 0.5), T(4, 33), 1.4); put(choir(1.4), T(4, 34), 1.1); put(levelup(), T(4, 40), 0.45)
put(whoosh(0.3, 300, 2500), T(4, 58), 0.6); put(kiss(), T(4, 68), 1.6); put(kiss(), T(4, 78), 1.2); put(squeak(0.3), T(4, 84), 0.4)
# 5 trophies: reverent hum, a clink per straightened trophy
put(choir(1.6) * 0.35, T(5), 0.8)
for i in range(5): put(ding(1500 + 120 * i, 0.25), T(5, 2 + i * 9 + 6), 0.5)
# 6 harness click, timer start
put(engine(T(7) - T(6), 850, 880, 0.18), T(6))
put(whoosh(0.3, 400, 3000), T(6, 8), 0.6); put(ms(knock(), tick(), slap(0.5)), T(6, 22), 1.3); put(beep(2400, 0.1), T(6, 40), 0.9); put(levelup(), T(6, 41), 0.4)
# 7 school zone: walking-pace timer beeps, kids, whistle
put(engine(T(8) - T(7), 800, 830, 0.22), T(7))
put(toy(T(8) - T(7)) * 0.3, T(7), 0.5, pan=0.4)
for f in range(1, 48, 12): put(beep(2400, 0.06), T(7, f), 0.5)
put(whistle(True, 0.5), T(7, 30), 0.4, pan=0.5)
# 8 speed bump: scrape, sparks, satisfied line
put(engine(T(9) - T(8), 900, 1100, 0.35), T(8)); put(ms(crunch(), screech(0.5) * 0.4), T(8, 12), 1.4); put(crunch(), T(8, 16), 1.0)
put(np.tanh(aero * 1.3), T(8, 22) - 0.15, 1.0)
# 9 roundabout: heel-toe blips while sawing the wheel; the cyclist's bell
put(engine(T(10) - T(9), 1200, 1500, 0.25), T(9))
for rf in range(2, 46, 8): put(rev(0.35, 5200), T(9, rf), 0.6)
put(ding(2600, 0.25), T(9, 18), 0.6, pan=0.5); put(ding(2600, 0.25), T(9, 21), 0.5, pan=0.5); put(whoosh(0.5, 400, 2500), T(9, 18), 0.5, pan=0.5)
# 10 garage bar: bonk
put(engine(T(11) - T(10), 850, 900, 0.25), T(10)); put(ms(bonk(), knock()), T(10, 20), 1.6); put(boing(), T(10, 21), 0.8); put(womp(), T(10, 30), 0.7)
# 11 the exchange (approved take 1), then two beats of silence
put(hum(T(12) - T(11), 60) * 0.5, T(11), 0.6); put(np.tanh(ex * 1.2), T(11, 4), 1.0)
# 12 tyre: gauge hiss, marker on the glove
put(hiss(0.6), T(12, 9), 0.8); put(pen(0.6), T(12, 32), 0.9)
# 13 weather: gasp sting, blanket
put(ms(gasp(), womp() * 0.8), T(13, 15), 1.2); put(bp(noise(1.2), 40, 300) * dec(1.2, 0.5), T(13, 16), 1.2); put(whoosh(0.4, 300, 2000), T(13, 26), 1.0)
# 14 track gate: cars howl past, then the indicator and a sad trombone as he U-turns
for i, f0 in enumerate((2, 14, 27, 38)):
    put(rev(0.5, 7000), T(14, f0 + 4), 1.0, pan=-0.6)
    put(whoosh(0.5, 500, 4000), T(14, f0 + 4), 0.8, pan=0.6)
put(engine(T(15) - T(14), 850, 900, 0.18), T(14))
for f in range(47, 82, 8): put(tick(), T(14, f), 1.0); put(tick(), T(14, f + 4), 0.7)
put(trombone(), T(14, 56), 0.9)
# 15 mirror: mouth-revving and rowing the 6-speed, then the sigh and "...next season."
for f in range(8, 90, 14): put(mouthrev(0.42), T(15, f), 0.9)
g = 8
for rep in range(2):
    for k in range(6): put(knock() * 0.7, T(15, g + 1), 0.9); g += 6
put(sigh, T(15, 95), 1.15)

out = mix[:int(DUR * SR)]; out[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))[:, None]
out = np.tanh(out * 0.9)
raw = out.astype(np.float32).tobytes(); IN = ["ffmpeg", "-v", "info", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-"]
PRE = "alimiter=limit=0.6:attack=2:release=60:level=false"
import json, re
m = subprocess.run(IN + ["-af", PRE + ",loudnorm=I=-14:TP=-1.2:LRA=11:print_format=json", "-f", "null", "-"], input=raw, capture_output=True, text=False).stderr.decode()
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
ln = "loudnorm=I=-14:TP=-1.2:LRA=11:linear=true:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s" % (j["input_i"], j["input_tp"], j["input_lra"], j["input_thresh"], j["target_offset"])
subprocess.run(IN[:2] + ["error"] + IN[3:] + ["-af", PRE + "," + ln, "-ar", "48000", sys.argv[1]], input=raw)
