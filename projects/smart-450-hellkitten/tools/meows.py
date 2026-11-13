"""Kitten meow 'drum kit' for the Smart 450 reel (v4): one-shots from CC0 / public-domain cat recordings, arranged on the 160 BPM lattice.

    python projects/smart-450-hellkitten/tools/meows.py      # writes sfx/oneshots/*.wav, meow_map.json, out/_stem_meows_dry.npy (stereo)

Kit: hats = the first 0.16 s of a mew (pitched up), mids = short whole mews on the backbeat, lows = 'MRROW' (long meows pitched down about an octave less),
choir = 4 layers of one big meow tuned to A C E A, rolls = rising retrigger runs, punchline = the long unimpressed meow.
Two voices (A: lower, panned left; B: higher, panned right) answer each other. Onset of every one-shot = its 20 %-of-peak 2 ms-RMS crossing, trimmed to
3 ms before it, and placed on T(m) = 1.499 + 0.37583 m (16th grid allowed). Key of the track: A (bass chroma 27 % A).
"""
import json, os, sys, wave
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.signal import butter, sosfiltfilt, resample_poly
sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SM, FPS, END, T

SR = 44100
SFX = Path(SM) / "sfx"; SRC = SFX / "src"; ONE = SFX / "oneshots"; ONE.mkdir(exist_ok=True, parents=True)
OUT = Path(SM) / "out"; OUT.mkdir(exist_ok=True)
HERE = Path(__file__).resolve().parent.parent
J, M, TS = "JorgeTheCatMeowing__Untitled3.ogg", "meow_20220616__meow_.wav", "wm__2015-11-24_Niaou_Tsester.flac"
# one-shot id: (file, start, end)
SEG = {
    "j01": (J, 1.38, 1.89), "j02": (J, 2.65, 3.26), "j03": (J, 8.33, 8.87), "j04": (J, 28.01, 28.73), "j05": (J, 29.11, 29.85),
    "j06": (J, 33.85, 34.66), "j07": (J, 35.17, 36.06), "j08": (J, 36.73, 37.62), "j09": (J, 41.77, 42.59), "j10": (J, 43.34, 44.28),
    "j11": (J, 40.75, 41.16), "j12": (J, 25.67, 26.18), "j13": (J, 5.89, 6.62), "j14": (J, 52.43, 52.71), "j15": (J, 48.28, 48.44),
    "j_long1": (J, 32.23, 33.24), "j_long2": (J, 26.75, 27.60), "m_big1": (M, 0.20, 0.91), "m_big2": (M, 2.42, 3.04), "t_sad": (TS, 0.17, 0.93),
}
MID = ["j01", "j02", "j03", "j04", "j05", "j06", "j07", "j08", "j09", "j10", "j11", "j12", "j13", "t_sad"]
HAT = ["j01", "j03", "j04", "j06", "j08", "j09", "j10", "j11", "j12", "j14", "j15", "j05"]
LOWS = ["j_long2", "j_long1", "t_sad", "j13", "m_big1"]
TONES_HZ = {"A": 440.0, "C": 523.25, "E": 659.25, "A5": 880.0, "G": 392.0}


def dec(f):
    import subprocess
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC / f), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                        capture_output=True, check=True).stdout, np.float32).astype(np.float64)


_cache = {}
def base(sid):
    """high-passed, onset-trimmed, normalised mono segment, onset at 3 ms; returns (y, f0)."""
    if sid in _cache: return _cache[sid]
    f, a, b = SEG[sid]
    x = dec(f)
    hp = sosfiltfilt(butter(4, 250, "high", fs=SR, output="sos"), x)
    seg = hp[max(int((a - 0.03) * SR), 0):int((b + 0.10) * SR)]
    w = int(0.002 * SR); env = np.sqrt(np.convolve(seg ** 2, np.ones(w) / w, "same"))
    pk = env[: int((b - a + 0.06) * SR)].max(); on = int(np.argmax(env > 0.2 * pk))
    seg = seg[max(on - int(0.003 * SR), 0): max(on - int(0.003 * SR), 0) + int((b - a + 0.08) * SR)].copy()
    fl = int(0.05 * SR); seg[-fl:] *= np.linspace(1, 0, fl)
    # f0
    n, hop = int(0.04 * SR), int(0.01 * SR); e = [np.sqrt(np.mean(seg[i:i + n] ** 2)) for i in range(0, min(len(seg), int(0.5 * SR)) - n, hop)]
    f0s = []
    for k, i in enumerate(range(0, min(len(seg), int(0.5 * SR)) - n, hop)):
        if e[k] < 0.5 * max(e): continue
        s = seg[i:i + n] - seg[i:i + n].mean(); ac = np.correlate(s, s, "full")[n - 1:]
        lo, hi = int(SR / 1400), int(SR / 250); j = lo + int(np.argmax(ac[lo:hi]))
        if ac[j] > 0.5 * ac[0]: f0s.append(SR / j)
    f0 = float(np.median(f0s)) if f0s else 600.0
    _cache[sid] = (seg / np.abs(seg).max(), f0)
    return _cache[sid]


def shifted(y, semis, crop=None, fade=0.04):
    r = 2 ** (-semis / 12); fr = Fraction(r).limit_denominator(2000)
    z = resample_poly(y, fr.numerator, fr.denominator)
    if crop:
        z = z[: int(crop * SR)].copy(); fl = int(fade * SR); z[-fl:] *= np.linspace(1, 0, min(fl, len(z)))[-fl:] if len(z) >= fl else 1
    return z / np.abs(z).max(), r


def shot(sid, semis=0.0, crop=None, tune=None, fade=0.04):
    """tune: a note name -> shift (clamped to [-9, +7] semitones) that brings the sample's f0 to that note, plus `semis`."""
    y, f0 = base(sid)
    s = semis
    if tune: s = float(np.clip(12 * np.log2(TONES_HZ[tune] / f0), -9, 7)) + semis
    z, r = shifted(y, s, crop, fade)
    return z, round(s, 2), r


EV = []
def add(m, kind, gain_db, voice, sid, semis=0.0, crop=None, tune=None, why="", pan=None):
    EV.append(dict(m=m, kind=kind, gain=gain_db, voice=voice, sid=sid, semis=semis, crop=crop, tune=tune, why=why, pan=pan))


def arrange():
    rng = np.random.default_rng(11)
    last = []
    def pick(pool, k=3):
        c = [p for p in pool if p not in last[-k:]]; p = c[int(rng.integers(len(c)))]; last.append(p); return p
    VA, VB = dict(pan=-0.33, semis=0.0), dict(pan=0.33, semis=3.0)
    def mid(m, v, g=-11, why="", jitter=True, sid=None):
        V = VA if v == "A" else VB; sid = sid or pick(MID)
        add(m, "mid", g, v, sid, V["semis"] + (float(rng.choice([-1, 0, 1, 2])) if jitter else 0), crop=0.5, why=why, pan=V["pan"])
    def hat(m, v, g=-15, semis=0.0, why=""):
        V = VA if v == "A" else VB; sid = pick(HAT)
        add(m, "hat", g, v, sid, V["semis"] + 3 + semis, crop=0.16, fade=None, why=why, pan=V["pan"]) if False else add(m, "hat", g, v, sid, V["semis"] + 3 + semis, crop=0.16, why=why, pan=V["pan"])
    def low(m, g=-9, why="", sid=None, semis=0.0):
        sid = sid or pick(LOWS, 2); add(m, "low", g, "C", sid, semis, crop=0.55, tune="G", why=why, pan=0.0)
    def roll(m0, n, step=0.25, g=-14, v="B", up=1.0, why=""):
        for i in range(n):
            V = VA if (i % 2 == 0 and v == "AB") else VB if v in ("B", "AB") else VA
            sid = pick(HAT)
            add(m0 + i * step, "roll", g + i * 0.8, v if v != "AB" else ("A" if i % 2 == 0 else "B"), sid, V["semis"] + 3 + up * i, crop=0.2, why=why, pan=V["pan"])
    def choir(m, g, why, sid="m_big2"):
        for tone, pan, dg in (("A", -0.4, 0), ("C", -0.15, -1), ("E", 0.15, -1), ("A5", 0.4, -3)):
            add(m, "choir", g + dg, "choir", sid, 0.0, crop=0.8, tune=tone, why=why, pan=pan)
    # --- hook: "THIS IS A SMART CAR?"
    mid(-2.0, "A", -11, "the question 'this is a Smart car?'"); mid(-1.5, "B", -11, "the answer, a fifth-ish higher, from the other voice")
    roll(-0.5, 2, 0.25, -13, "B", why="2-note pickup into drop 1")
    # --- drop 1 (real car, powder): lows on bar downbeats, off-beat hats, backbeat mids, a roll into the scanner
    for k, m in enumerate((0, 4, 8, 12, 16)): low(float(m), -9, "MRROW doubles the kick on the section downbeat" if m == 0 else "MRROW on the bar downbeat")
    for k, m in enumerate((2, 6, 10, 14, 18)): hat(m + 0.5, "A" if k % 2 == 0 else "B", -15, why="hat-like mew on the off-beat of beat 3")
    for k, m in enumerate((3, 7, 11, 15)): mid(float(m), "B" if k % 2 == 0 else "A", -11, "backbeat mew (beat 4)")
    roll(7.5, 2, 0.25, -13, "AB", why="roll into the scanner shot (m 8)")
    # --- break 1: call and response, then a rising roll into the 1:1 cut
    mid(20.5, "A", -11, "call"); mid(21.0, "B", -11, "response"); mid(21.5, "A", -10, "call, a little louder")
    roll(23.25, 3, 0.25, -14, "AB", up=1.5, why="rising roll into the 1:1 cut / drop 2")
    # --- drop 2: lows, off-beat hats, roll into the body-off swap, choir on the Hellkitten reveal
    for m in (24, 28, 36, 40, 44): low(float(m), -9, "MRROW on the bar downbeat" if m != 24 else "MRROW on the 1:1 cut / drop 2")
    add(32.0, "low", -6, "C", "m_big1", 0.0, crop=0.8, tune="G", why="the body-off swap: where a tough car revs, a big MRROW", pan=0.0)
    add(32.0, "mid", -7, "C", "m_big2", 0.0, crop=0.7, tune="E", why="...and a big confident meow on top of it", pan=0.0)
    for k, m in enumerate((26, 30, 34, 38, 42, 46)): hat(m + 0.5, "A" if k % 2 == 0 else "B", -15, why="off-beat hat-mew")
    roll(31.5, 2, 0.25, -13, "AB", why="roll into the swap")
    choir(44.5, -11, "the Hellkitten body arrives: a four-voice meow choir tuned to A minor")
    # --- break 2: lone meow, stutter rolls rising into drop 3
    add(48.0, "mid", -9, "C", "j_long2", 0.0, crop=0.9, tune="A", why="break 2: the kick drops out and a lone long meow sits in the gap", pan=0.0)
    roll(53.0, 4, 0.25, -14, "B", up=1.0, why="stutter roll 1 (retriggered mew, +1 semitone per hit)")
    for i, m in enumerate((54.0, 54.5, 55.0, 55.25, 55.5, 55.75)):
        sid = pick(MID); add(m, "roll", -12 + i * 0.8, "AB", sid, 3 + 1.2 * i, crop=0.25, why="stutter roll 2, rising pitch into drop 3", pan=0.33 if i % 2 else -0.33)
    # --- drop 3 and the question
    add(56.0, "mid", -6, "C", "m_big2", 0.0, crop=0.75, tune="E", why="DROP 3: the render appears: one big confident meow", pan=0.0)
    low(56.0, -7, "MRROW doubles the drop-3 kick")
    mid(58.0, "A", -10, "backbeat"); mid(59.0, "B", -10, "backbeat")
    roll(59.5, 2, 0.25, -12, "B", up=1.5, why="roll into the choir")
    choir(60.0, -10, "'should we build this?' a four-voice 'yes' choir")
    add(61.0, "punch", -7, "C", "j_long1", -2.0, crop=0.95, why="PUNCHLINE: one long unimpressed meow on the question", pan=0.0)
    # --- logo
    mid(64.0, "A", -13, "logo: a small mew on the downbeat", sid="j14"); mid(66.0, "B", -13, "answer"); hat(68.5, "A", -15, why="last tiny mew")


def main():
    arrange()
    total = int(round(END / FPS * SR)); stem = np.zeros((total, 2)); mp = []
    for k, e in enumerate(sorted(EV, key=lambda d: (d["m"], d["kind"]))):
        z, s, r = shot(e["sid"], e["semis"], e["crop"], e["tune"])
        t = T(e["m"]); idx = int(round(t * SR)) - int(round(0.003 * SR * r))
        g = 10 ** (e["gain"] / 20); pan = e["pan"]; th = (pan + 1) * np.pi / 4
        seg = z * g
        L, R = np.cos(th), np.sin(th)
        end = min(idx + len(seg), total)
        stem[idx:end, 0] += seg[: end - idx] * L * np.sqrt(2) / 1.0 * 0.7071
        stem[idx:end, 1] += seg[: end - idx] * R * np.sqrt(2) / 1.0 * 0.7071
        mp.append(dict(n=k + 1, time_s=round(t, 4), onset_sample=int(round(t * SR)), beat_m=e["m"], bar=(int(e["m"] // 4) + 1) if e["m"] >= 0 else 0,
                       beat_in_bar=round(e["m"] % 4 + 1, 2), sixteenth_grid=bool(abs(e["m"] * 4 - round(e["m"] * 4)) < 1e-9), frame=round(t * FPS, 2),
                       kind=e["kind"], voice=e["voice"], sample=e["sid"], source=SEG[e["sid"]][0], pan=e["pan"], pitch_shift_semitones=s,
                       peak_dbfs_pre_master=round(e["gain"], 1), why=e["why"]))
    # density per section
    secs = [("hook (m -4..0)", -4, 0), ("drop 1 (0..20)", 0, 20), ("break 1 (20..24)", 20, 24), ("drop 2 (24..48)", 24, 48), ("break 2 (48..56)", 48, 56),
            ("drop 3 + question (56..64)", 56, 64), ("logo (64..72)", 64, 72)]
    dens = {n: sum(1 for m in mp if a <= m["beat_m"] < b) for n, a, b in secs}
    moments = len({m["beat_m"] for m in mp})
    (HERE / "meow_map.json").write_text(json.dumps(dict(bpm=159.64, count=len(mp), distinct_moments=moments, density_per_section=dens,
        note="onset of each meow = its 20 %-of-peak 2 ms-RMS crossing, placed on T(m)=1.499+0.37583m (the track's click lattice; 16th grid allowed); choir stacks are 4 layers on one onset",
        meows=mp), indent=1))
    np.save(OUT / "_stem_meows_dry.npy", stem)
    print(len(mp), "meows,", moments, "distinct moments;", dens)


if __name__ == "__main__":
    main()
