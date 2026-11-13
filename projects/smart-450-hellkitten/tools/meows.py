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
PL, GO, SI, HE = "wm__Meow_of_a_pleading_cat.oga", "wm__GettingOutImpatient.ogg", "wm__Meow_of_a_Siamese_cat_-_freemaster2.wav", "wm__Maullido_de_gata_hembra.ogg"
# one-shot id: (file, start, end)
SEG = {
    "j01": (J, 1.38, 1.89), "j02": (J, 2.65, 3.26), "j03": (J, 8.33, 8.87), "j04": (J, 28.01, 28.73), "j05": (J, 29.11, 29.85),
    "j06": (J, 33.85, 34.66), "j07": (J, 35.17, 36.06), "j08": (J, 36.73, 37.62), "j09": (J, 41.77, 42.59), "j10": (J, 43.34, 44.28),
    "j11": (J, 40.75, 41.16), "j12": (J, 25.67, 26.18), "j13": (J, 5.89, 6.62), "j14": (J, 52.43, 52.71), "j15": (J, 48.28, 48.44),
    # v6: five more recordings (segments found with a 10 ms RMS gate; SNR 34-76 dB except h1 = 25 dB)
    "p1": (PL, 0.31, 1.14), "p2": (PL, 3.74, 4.72), "p3": (PL, 6.73, 7.52), "p4": (PL, 9.46, 10.06), "p5": (PL, 10.14, 11.23),
    "g1": (GO, 0.15, 0.62), "g2": (GO, 2.14, 3.28), "g3": (GO, 4.65, 5.43), "g4": (GO, 6.22, 7.07), "g5": (GO, 7.93, 9.31),
    "s1": (SI, 0.21, 1.03), "h1": (HE, 0.02, 0.92),
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


_dn = {}
def denoise(x):
    """v6 ('cleaner audio'): spectral gate. Noise profile = 15th-percentile magnitude per bin over the whole recording; bins under
    2.5x the profile are attenuated (floor -24 dB), gain smoothed over 3 frames and 3 bins. Leaves the meow harmonics, removes hiss/room."""
    from scipy.signal import stft, istft
    from scipy.ndimage import uniform_filter
    key = (len(x), float(x[:1000].sum()))
    if key in _dn: return _dn[key]
    f, t, Z = stft(x, SR, nperseg=1024, noverlap=768)
    mag = np.abs(Z); noise = np.percentile(mag, 15, axis=1, keepdims=True) + 1e-9
    g = np.clip((mag - 2.5 * noise) / (mag + 1e-9), 0.063, 1.0)
    g = uniform_filter(g, size=(3, 3))
    _, y = istft(Z * g, SR, nperseg=1024, noverlap=768)
    y = y[: len(x)] if len(y) >= len(x) else np.pad(y, (0, len(x) - len(y)))
    _dn[key] = y
    return y


def loud_norm(z, ref=0.25):
    """normalise by the loudest 100 ms RMS (not the peak), so different cats sit at the same loudness; peak capped at 0.98."""
    w = int(0.1 * SR)
    if len(z) <= w: r = np.sqrt(np.mean(z ** 2))
    else: r = np.sqrt(np.convolve(z ** 2, np.ones(w) / w, "valid").max())
    z = z * (ref / max(r, 1e-9))
    pk = np.abs(z).max()
    return z * min(1.0, 0.98 / pk)


_cache = {}
def base(sid):
    """high-passed, onset-trimmed, normalised mono segment, onset at 3 ms; returns (y, f0)."""
    if sid in _cache: return _cache[sid]
    f, a, b = SEG[sid]
    x = denoise(dec(f))
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
    return loud_norm(z), r


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
    """v6 (owner, 2026-11-13): louder, cleaner, REAL meows (whole meows at their natural pitch, at most +-2 semitones for variety; no chopped
    'hat' fragments, no rolls, no choir of one sample). Sparse at the start (a few transitions only), then one on every cut from the moment
    the Hellkitten appears (m 40), with stacks of different cats on the big moments. Meows also mark each green-screen cat's entrance.
    gain is dB relative to the one-shot's loudness reference (0 = a full single meow)."""
    def one(m, sid, g=0.0, pan=0.0, semis=0.0, crop=0.95, why=""):
        add(m, "meow", g, "solo", sid, semis, crop=crop, why=why, pan=pan)
    def stack(m, sids, g=-3.0, why="", crop=0.95):
        pans = np.linspace(-0.45, 0.45, len(sids))
        for sid, pan in zip(sids, pans):
            add(m, "stack", g, "stack", sid, 0.0, crop=crop, why=why, pan=float(pan))
    # --- start: sparse, transitions only (the huh cat's own HUH is the first sound, see audio_mix SFX)
    one(0.0, "p4", -2, 0.25, why="drop 1 / cut to the real car, the huh cat leaves: one short meow")
    one(8.0, "g1", -2, -0.25, why="cut to the scanner")
    one(12.0, "t_sad", -1, 0.2, why="cut to the panels on the floor: a small sad meow")
    one(20.0, "s1", 0, 0.0, why="break 1: the kick drops out, a lone meow sits in the gap")
    one(24.0, "p1", 0, -0.2, why="the 1:1 cut into the scan (drop 2)")
    stack(32.0, ["m_big1", "p2"], -2, "the body-off swap (and the spinning cat's spin starts here when that clip is in)")
    # --- the Hellkitten appears: a meow on every cut from here on
    one(40.0, "g3", 0, 0.3, why="cut to the Hellkitten shot")
    stack(41.0, ["m_big2", "p5"], -2, "the stripped scan becomes the Hellkitten body (swap on frame 506/507)")
    one(44.0, "g2", -1, -0.3, why="bar downbeat on the Hellkitten model")
    one(44.5, "h1", -2, 0.35, crop=0.8, why="the yapapa cat's first yell (frame 547) when that clip is in; otherwise an off-beat answer")
    one(46.0, "p3", -1, 0.3, why="half-bar on the Hellkitten model")
    one(48.0, "g5", 0, 0.0, crop=1.3, why="break 2: a long meow alone in the gap")
    one(50.0, "p1", 0, -0.3, semis=1.0, why="cut to the Blueprint")
    one(52.0, "j02", 0, 0.3, why="cut: render 4.r.2")
    one(53.0, "p4", 0, -0.3, why="cut: render 4.r.4")
    one(54.0, "g4", 0, 0.3, why="cut: render 4.r.5")
    one(55.0, "j07", 0, -0.3, why="cut: render 4.r.6")
    stack(56.0, ["m_big1", "p2", "s1"], -2.5, "DROP 3, cut to the hero render: three different cats at once")
    one(58.0, "g3", 0, 0.3, semis=-1.0, why="cut: street render")
    one(59.0, "p3", 0, -0.3, why="cut: night render")
    stack(60.0, ["p5", "g2", "h1", "m_big2"], -3, "cut to the final render and the question: four different cats at once")
    one(61.0, "j_long1", 0, 0.0, semis=-2.0, why="PUNCHLINE: one long unimpressed meow on 'should we build this?'")
    one(63.0, "p4", -2, 0.35, semis=2.0, why="the black cat is clapping (yeah-boy underneath): a short approving mew")
    stack(64.0, ["s1", "t_sad"], -3, "logo downbeat")
    one(66.0, "p1", -2, -0.3, why="logo, clap on beat 66")
    one(68.0, "g1", -3, 0.3, why="logo, clap on beat 68")
    one(70.0, "j14", -4, 0.0, crop=0.3, why="last tiny mew as the logo fades")


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
    secs = [("hook (m -4..0)", -4, 0), ("real car, drop 1 + break 1 (0..24)", 0, 24), ("scan (24..40)", 24, 40), ("Hellkitten model (40..50)", 40, 50),
            ("design renders (50..60)", 50, 60), ("question (60..64)", 60, 64), ("logo (64..72)", 64, 72)]
    dens = {n: sum(1 for m in mp if a <= m["beat_m"] < b) for n, a, b in secs}
    moments = len({m["beat_m"] for m in mp})
    (HERE / "meow_map.json").write_text(json.dumps(dict(bpm=159.64, count=len(mp), distinct_moments=moments, density_per_section=dens,
        note="onset of each meow = its 20 %-of-peak 2 ms-RMS crossing, placed on T(m)=1.499+0.37583m (the track's click lattice; 16th grid allowed); choir stacks are 4 layers on one onset",
        meows=mp), indent=1))
    np.save(OUT / "_stem_meows_dry.npy", stem)
    print(len(mp), "meows,", moments, "distinct moments;", dens)


if __name__ == "__main__":
    main()
