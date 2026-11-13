"""Kitten meows for the Smart 450 reel (v3): one-shots from CC0 / public-domain recordings, arranged on the 160 BPM lattice.

    python projects/smart-450-hellkitten/tools/meows.py        # writes sfx/oneshots/*.wav, meow_map.json, out/stem_meows_dry.wav

Sources (see sfx.md): three CC0 recordings in sfx/src/ (an archive.org recording of a cat, one 3 s 'meow!' clip, one Commons clip).
One-shot prep: segment cut at the measured start, high-pass 250 Hz (4th order), onset = first 2 ms-RMS sample above 20 % of the segment's
peak, trimmed to 3 ms before it (the onset sits at t = 3 ms +- 1 ms), 50 ms fade at the tail, peak-normalised, then pitch-shifted by
resampling (+-semitones, pitch and duration move together) toward the nearest tone of A minor (A C E G) where the shot is tonal.
The track is in A (bass 27 % A, chroma A min 0.64 / A maj 0.59).
Arrangement = ironic: deadpan mews against big kicks. times are lattice beats m: T(m) = 1.499 + 0.37583 m.
"""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfiltfilt
from scipy.signal import resample_poly
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SM, FPS, END, T

SR = 44100
SFX = Path(SM) / "sfx"; SRC = SFX / "src"; ONE = SFX / "oneshots"; ONE.mkdir(exist_ok=True, parents=True)
OUT = Path(SM) / "out"; OUT.mkdir(exist_ok=True)
HERE = Path(__file__).resolve().parent.parent
J, M, TS = "JorgeTheCatMeowing__Untitled3.ogg", "meow_20220616__meow_.wav", "wm__2015-11-24_Niaou_Tsester.flac"
# id: (file, start s, end s, role, target pitch class override or None, extra semitones)
SHOTS = {
    "tiny_a":   (J, 52.43, 52.71, "tiny polite mew", None, +4),
    "short_b":  (J, 40.75, 41.16, "short high mew", None, +3),
    "short_c":  (J, 25.67, 26.18, "short mew", None, +2),
    "mid_d":    (J, 5.89, 6.62, "plain meow", None, +2),
    "sad_e":    (TS, 0.17, 0.93, "small sad meow", None, +2),
    "big_f":    (M, 0.20, 0.91, "big confident meow", None, 0),
    "big_g":    (M, 2.42, 3.04, "second big meow", None, 0),
    "long_h":   (J, 32.23, 33.24, "long unimpressed meow", None, -2),
    "long_i":   (J, 26.75, 27.60, "long meow", None, 0),
    "chirp_j":  (J, 48.28, 48.44, "tiny chirp", None, +5),
}
MINOR = [9, 0, 4, 7]   # A C E G pitch classes


def dec(f):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC / f), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                        capture_output=True, check=True).stdout, np.float32).astype(np.float64)


def f0_est(x):
    """median autocorrelation pitch over 40 ms frames of the loudest part (Hz)."""
    hop, n = int(0.01 * SR), int(0.04 * SR)
    e = [np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n, hop)]
    thr = 0.5 * max(e); out = []
    for k, i in enumerate(range(0, len(x) - n, hop)):
        if e[k] < thr: continue
        s = x[i:i + n] - x[i:i + n].mean(); ac = np.correlate(s, s, "full")[n - 1:]
        lo, hi = int(SR / 1400), int(SR / 250); j = lo + int(np.argmax(ac[lo:hi]))
        if ac[j] > 0.5 * ac[0]: out.append(SR / j)
    return float(np.median(out)) if out else 0.0


def prep(name, spec):
    f, a, b, role, _, extra = spec
    x = dec(f)
    hp = sosfiltfilt(butter(4, 250, "high", fs=SR, output="sos"), x)
    i0, i1 = int((a - 0.03) * SR), int((b + 0.10) * SR)
    seg = hp[max(i0, 0):i1]
    w = int(0.002 * SR); env = np.sqrt(np.convolve(seg ** 2, np.ones(w) / w, "same"))
    pk = env[: int((b - a + 0.06) * SR)].max()
    on = int(np.argmax(env > 0.2 * pk))
    seg = seg[max(on - int(0.003 * SR), 0):]
    f0 = f0_est(seg[: int(0.5 * SR)])
    # tail fade: natural end at (b - a) + 0.08 s after the start
    L = int((b - a + 0.08) * SR); seg = seg[:L].copy()
    fl = int(0.05 * SR); seg[-fl:] *= np.linspace(1, 0, fl)
    shift = float(extra)
    if f0 > 0:   # nudge toward the nearest A-minor tone, within +-1 semitone of the requested shift
        best = None
        for d in np.arange(-1.0, 1.01, 0.25):
            pc = (round(12 * np.log2(f0 * 2 ** ((extra + d) / 12) / 440)) + 9) % 12
            cents = abs(12 * np.log2(f0 * 2 ** ((extra + d) / 12) / 440) - round(12 * np.log2(f0 * 2 ** ((extra + d) / 12) / 440)))
            if pc in MINOR and (best is None or cents < best[0] - 1e-9): best = (cents, d)
        if best: shift = extra + best[1]
    ratio = 2 ** (-shift / 12)                       # resample: playing faster = higher
    fr = Fraction(ratio).limit_denominator(2000)
    y = resample_poly(seg, fr.numerator, fr.denominator)
    y = y / np.abs(y).max()
    onset_s = 0.003 * ratio
    return y, dict(id=name, src=f, seg=[a, b], role=role, f0_hz=round(f0), shift_semitones=round(shift, 2), dur_s=round(len(y) / SR, 3), onset_in_file_ms=round(onset_s * 1000, 2))


# arrangement: (id, beat m, peak dBFS before the master gain, why)
ARR = [
    ("tiny_a", 0.5, -17, "drop 1 = the first huge kick; a tiny polite mew answers it half a beat later, on the intact car"),
    ("sad_e", 16.5, -15, "bare rear (S12): a small sad meow after the bumper-less tail"),
    ("big_f", 32.0, -8, "THE body-off swap on the drop: where a tough car would rev, one big confident meow"),
    ("short_b", 35.5, -14, "motif A (answers the kick, off-beat) while the camera pushes in on the bare structure"),
    ("short_c", 37.5, -14, "motif B, two beats later"),
    ("short_b", 39.5, -14, "motif A again, a bar later: the repeating 2-bar motif"),
    ("mid_d", 44.5, -12, "the Hellkitten body arrives on the structure: a plain, unimpressed meow"),
    ("long_i", 48.0, -11, "break 2: the kick drops out and a lone meow sits in the gap"),
    ("short_c", 54.0, -17, "rising stutter into the render, 1/4"),
    ("short_b", 54.5, -15, "rising stutter 2/4 (+2 semitones)"),
    ("tiny_a", 55.0, -13, "rising stutter 3/4"),
    ("chirp_j", 55.5, -12, "rising stutter 4/4, the chirp"),
    ("big_g", 56.0, -8, "DROP 3: the Hellkitten render appears: one big confident meow exactly on the drop"),
    ("long_h", 61.0, -9, "the question 'SHOULD WE BUILD THIS?' is on screen: one long unimpressed meow"),
    ("tiny_a", 64.0, -16, "logo card: a last small mew on the downbeat"),
]
STUTTER_STEP = {"short_c@54.0": 0, "short_b@54.5": 2, "tiny_a@55.0": 4, "chirp_j@55.5": 5}   # extra semitones for the rising run


def main():
    shots = {}
    for name, spec in SHOTS.items():
        y, info = prep(name, spec); shots[name] = (y, info)
        import wave
        with wave.open(str(ONE / f"{name}.wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767 * 0.7).astype(np.int16).tobytes())
        print(info)
    total = int(round(END / FPS * SR)); stem = np.zeros(total)
    mp = []
    for k, (name, m, pk_db, why) in enumerate(ARR):
        y, info = shots[name]
        extra = STUTTER_STEP.get(f"{name}@{m}")
        if extra:
            r = 2 ** (-extra / 12); fr = Fraction(r).limit_denominator(2000); y = resample_poly(y, fr.numerator, fr.denominator); y = y / np.abs(y).max()
        t = T(m); idx = int(round(t * SR)) - int(round(0.003 * SR * (2 ** (-(extra or 0) / 12))))
        g = 10 ** (pk_db / 20)
        seg = y * g
        stem[idx:idx + len(seg)] += seg[: total - idx]
        mp.append(dict(n=k + 1, time_s=round(t, 4), onset_sample=int(round(t * SR)), beat_m=m, bar=int(m // 4) + 1 if m >= 0 else 0, beat_in_bar=round(m % 4 + 1, 2),
                       frame=round(t * FPS, 2), shot=name, source=info["src"], pitch_shift_semitones=round(info["shift_semitones"] + (extra or 0), 2),
                       peak_dbfs_pre_master=pk_db, role=info["role"], why=why))
    (HERE / "meow_map.json").write_text(json.dumps(dict(bpm=159.64, note="onset of each meow = its 20 %-of-peak 2 ms-RMS crossing, placed on T(m)=1.499+0.37583m (the track's click lattice)",
                                                      count=len(mp), meows=mp), indent=1))
    np.save(OUT / "_stem_meows_dry.npy", stem)
    print(len(mp), "meows")


if __name__ == "__main__":
    main()
