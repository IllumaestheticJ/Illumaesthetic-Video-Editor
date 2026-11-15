"""Part A timeline from the real voice takes (stage 3).

Picks one take per line, trims it to its speech span (energy runs at -40 dB under the take's peak, 80 ms gaps bridged),
tightens internal pauses to at most MAX_GAP, speeds it up with rubberband (pitch kept) by at most 1.12, and maps the
faster-whisper word times through those edits. Then lays the lines out shot by shot (lead before the line, tail after it)
and writes:
  - projects/scan-tedium-explainer-reel/partA_timeline.json   (shots in frames, lines + words in reel seconds; drives Blender)
  - /home/user/media/work/scan-tedium/voice/proc/Lnn.wav       (processed line clips, 48 kHz mono)
  - OUT/partA_dialogue.wav                                     (voices only at their reel times, -16 LUFS integrated, -1.5 dBTP)
Swapping a take (e.g. L11b once the owner has listened) = edit TAKES and re-run; Blender reads the new word times.

Usage: python partA_timeline.py [--out /home/user/media/work/scan-tedium/out]
"""
import json, math, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
TAKES_DIR = Path("/home/user/media/work/scan-tedium/voice/el_b/lines_annoyed")   # v4; v3: el_b/lines; v1/v2: voice/takes
PROC = Path("/home/user/media/work/scan-tedium/voice/proc")
OUT = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else Path("/home/user/media/work/scan-tedium/out")
SR = 48000
FPS = 30
MAX_GAP = 0.18          # longest pause kept inside a line
TEMPO_MAX = 1.12

# line: (take, speaker, shot, tempo, max internal gap override)
# v3 (owner): ElevenLabs dialogue job 18e5f0b0 (Pip = Kiki natural pitch, Gus = Harrison), one file split per line by
# tools/el_split.py. NO speed-ups (natural pacing) and no tightening inside lines; only the gaps between lines are set here.
TAKES_V2 = {
    1: ("L01b", "PIP", "S1", 1.12, 0.28), 2: ("L02a", "GUS", "S2", 1.12, None), 3: ("L03d", "GUS", "S3", 1.12, None),
    4: ("L04b", "PIP", "S4", 1.12, None), 5: ("L05a", "GUS", "S5", 1.06, None), 6: ("L06b", "GUS", "S6", 1.12, 0.26),
    7: ("L07b", "GUS", "S7", 1.10, None), 8: ("L08b", "PIP", "S8", 1.12, None), 9: ("L09a", "GUS", "S8", 1.0, None),
    10: ("L10a", "GUS", "S9", 1.12, None), 14: ("L10Ba", "PIP", "S10", 1.12, None), 11: ("L11a", "PIP", "S10", 1.12, 0.26),
    12: ("L12a", "PIP", "S11", 1.12, None), 13: ("L13b", "GUS", "S12", 1.0, None)}
NO_TIGHTEN = 99.0
TAKES_V3 = {
    1: ("L01e", "PIP", "S1", 1.0, NO_TIGHTEN), 2: ("L02e", "GUS", "S2", 1.0, NO_TIGHTEN), 3: ("L03e", "GUS", "S3", 1.0, NO_TIGHTEN),
    4: ("L04e", "PIP", "S4", 1.0, NO_TIGHTEN), 5: ("L05e", "GUS", "S5", 1.0, NO_TIGHTEN), 6: ("L06e", "GUS", "S6", 1.0, NO_TIGHTEN),
    7: ("L07e", "GUS", "S7", 1.0, NO_TIGHTEN), 8: ("L08e", "PIP", "S8", 1.0, NO_TIGHTEN), 9: ("L09e", "GUS", "S8", 1.0, NO_TIGHTEN),
    10: ("L10e", "GUS", "S9", 1.0, NO_TIGHTEN), 14: ("L10Be", "PIP", "S10", 1.0, NO_TIGHTEN),
    11: ("L11e", "PIP", "S10", 1.0, NO_TIGHTEN), 12: ("L12e", "PIP", "S11", 1.0, NO_TIGHTEN), 13: ("L13e", "GUS", "S12", 1.0, NO_TIGHTEN)}
# v4 (owner): the annoyed ElevenLabs take (job 1e219ae5): Gus sighs and groans, Pip impatient/frustrated. Same rules as v3.
TAKES = {n: (t[:-1] + "n", spk, sh, tp, gp) for n, (t, spk, sh, tp, gp) in TAKES_V3.items()}
# per shot: (lead s before its first line, tail s after its last line, extra s for the shot's visual beat)
SHOTS = [("S1", 0.17, 0.07, 0.0), ("S2", 0.05, 0.07, 0.0), ("S3", 0.05, 0.07, 0.10), ("S4", 0.05, 0.07, 0.05),
         ("S5", 0.05, 0.07, 0.10), ("S6", 0.05, 0.07, 0.15), ("S7", 0.05, 0.07, 0.15), ("S8", 0.07, 0.10, 0.0),
         ("S9", 0.05, 0.07, 0.10), ("S10", 0.05, 0.07, 0.0), ("S11", 0.05, 0.07, 0.0), ("S12", 0.05, 0.10, 0.25)]
GAP_8_9 = 0.20           # PIP "Is it done yet?" ... beat ... GUS "No."
GAPS = {"S8": GAP_8_9, "S10": 0.35}   # S10: deflated "better way" ... a beat ... perks up on "Wait."
# v2 voice polish (owner: too muted and dull): high-pass, presence, air, gentle 3:1 compression; stem to -14 LUFS / -1 dBTP
VOICE_FX = ("highpass=f=90:poles=2,equalizer=f=3500:t=q:w=1.1:g=3,treble=g=2:f=9000:t=s:w=0.7,"
            "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:knee=4:makeup=3")
STEM_I, STEM_TP = -14.0, -1.0


def decode(p):
    pcm = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", str(p), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0


def runs(x, db=-40.0, bridge=8, min_len=3):
    hop = SR // 100
    n = len(x) // hop
    rms = np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    on = 20 * np.log10(rms / rms.max()) > db
    out, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if out and i - out[-1][1] < bridge:
                out[-1] = (out[-1][0], j)
            else:
                out.append((i, j))
            i = j
        else:
            i += 1
    return [(a / 100, b / 100) for a, b in out if b - a >= min_len]


def process(line, meas):
    take, spk, shot, tempo, gap_over = TAKES[line]
    assert 1.0 <= tempo <= TEMPO_MAX
    x = decode(TAKES_DIR / f"{take}.wav")
    rs = runs(x)
    t0, t1 = max(0.0, rs[0][0] - 0.04), min(len(x) / SR, rs[-1][1] + 0.06)
    mg = gap_over or MAX_GAP
    # pauses: gaps between energy runs, plus gaps between whisper words (room tone can keep a pause above the energy gate);
    # each pause longer than mg is cut down to mg (its centre removed)
    ws = meas["words"]
    gaps = [(b, c) for (a, b), (c, d) in zip(rs, rs[1:])]
    for k in range(len(ws) - 1):
        a = ws[k]["t1"]
        b = ws[k + 1]["t0"]
        if b - a > mg and not any(ga < (a + b) / 2 < gb for ga, gb in gaps):
            gaps.append((a, b))
    keep, cur = [], t0
    for b, c in sorted(gaps):
        if c - b > mg and b > cur:
            keep.append((cur, b + mg / 2))
            cur = c - mg / 2
    keep.append((cur, t1))
    fade = int(0.008 * SR)
    parts = []
    for a, b in keep:
        seg = x[int(a * SR):int(b * SR)].copy()
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        parts.append(seg)
    y = np.concatenate(parts)

    def mapt(t):   # source time -> processed time (before tempo)
        acc = 0.0
        for a, b in keep:
            if t < a:
                return acc
            if t <= b:
                return acc + (t - a)
            acc += b - a
        return acc

    PROC.mkdir(parents=True, exist_ok=True)
    raw = PROC / f"_L{line:02d}_cut.wav"
    out = PROC / f"L{line:02d}.wav"
    import wave
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    af = (f"rubberband=tempo={tempo}:pitch=1:transients=crisp:formant=preserved," if tempo != 1.0 else "") + VOICE_FX
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), "-ac", "1",
                    "-c:a", "pcm_s16le", str(out)], check=True)
    raw.unlink()
    dur = len(decode(out)) / SR
    # words: whisper times, first word start clamped to the energy onset (faster-whisper pins it to 0.0)
    words = []
    for k, wd in enumerate(meas["words"]):
        a, b = wd["t0"], wd["t1"]
        if k == 0:
            a = max(a, rs[0][0])
        b = max(b, a + 0.06)
        words.append(dict(w=wd["w"], t0=round(mapt(a) / tempo, 3), t1=round(min(mapt(b), mapt(t1)) / tempo, 3)))
    sighs = [[round(mapt(a) / tempo, 3), round(mapt(b) / tempo, 3)] for a, b in meas.get("sighs", [])]
    return dict(n=line, take=take, speaker=spk, shot=shot, tempo=tempo, src_span=[round(t0, 3), round(t1, 3)], sighs=sighs,
                pauses_cut=round((t1 - t0) - sum(b - a for a, b in keep), 3), dur=round(dur, 3), words=words,
                text=meas["script"], heard=meas["heard"], wer=meas["wer"], file=str(out))


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    lines = [l for l in r.stderr.splitlines() if "I:" in l and "LUFS" in l]
    return float(lines[-1].split("I:")[1].split("LUFS")[0])


def main():
    meas = json.loads((PROJ / "voice_takes_measured.json").read_text())
    lines = {n: process(n, meas[f"{TAKES[n][0]}.wav"]) for n in TAKES}
    # lay out shots
    t = 0.0
    shots, placed = [], []
    for sid, lead, tail, extra in SHOTS:
        ls = [lines[n] for n in TAKES if lines[n]["shot"] == sid]   # TAKES order = spoken order
        s0 = t
        tt = s0 + lead
        for i, L in enumerate(ls):
            if i:
                tt += GAPS.get(sid, GAP_8_9)
            L["t0"] = round(tt, 3)
            L["t1"] = round(tt + L["dur"], 3)
            tt = L["t1"]
            placed.append(L)
        s1 = tt + tail + extra
        f0, f1 = int(round(s0 * FPS)), int(round(s1 * FPS))
        shots.append(dict(id=sid, f0=f0, f1=f1))
        t = f1 / FPS   # shots on whole frames
    total = shots[-1]["f1"]
    for L in placed:
        L["words"] = [dict(w=w["w"], t0=round(L["t0"] + w["t0"], 3), t1=round(L["t0"] + w["t1"], 3)) for w in L["words"]]
        L["sighs"] = [[round(L["t0"] + a, 3), round(L["t0"] + b, 3)] for a, b in L.get("sighs", [])]
    # dialogue stem
    mix = np.zeros(int(total / FPS * SR) + SR // 2, np.float32)
    for L in placed:
        y = decode(L["file"])
        g = 10 ** ((STEM_I - loudness(L["file"])) / 20)   # level-match each line first
        i0 = int(round(L["t0"] * SR))
        mix[i0:i0 + len(y)] += y * g
    mix = mix[: int(total / FPS * SR)]
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_dialogue_raw.wav"
    import wave
    mix *= 0.25   # headroom (float), loudnorm brings it back up
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(tmp)],
                   input=mix.astype(np.float32).tobytes(), check=True)
    peak = float(20 * np.log10(np.abs(mix).max() + 1e-9))
    gain = 0.0
    # two-pass loudnorm to -16 LUFS integrated, -1.5 dBTP (dialogue level, no music)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(tmp), "-af", f"loudnorm=I={STEM_I}:TP={STEM_TP}:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I={STEM_I}:TP={STEM_TP}:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-af", ln, "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s24le",
                    str(OUT / "partA_dialogue.wav")], check=True)
    tmp.unlink()
    lfin = loudness(OUT / "partA_dialogue.wav")
    s12 = [s for s in shots if s["id"] == "S12"][0]
    tl = dict(doc="Part A timeline (stage 3, real voices). Frames are reel frames at 30 fps; shot f1 is exclusive. Line and word "
                  "times are reel seconds of the processed clips (trimmed, pauses tightened, tempo applied).",
              fps=FPS, total_frames=total, duration_s=round(total / FPS, 3), screen_full_frame=s12["f1"] - 1,
              shots=shots, lines=[{k: v for k, v in L.items() if k != "file"} | {"file": Path(L["file"]).name} for L in placed],
              dialogue=dict(file="partA_dialogue.wav", integrated_lufs=round(lfin, 2), gain_db=round(gain, 2)))
    (PROJ / "partA_timeline.json").write_text(json.dumps(tl, indent=1))
    for s in shots:
        print(f"{s['id']:4s} {s['f0']:4d}-{s['f1']:4d} {s['f0'] / FPS:6.2f}-{s['f1'] / FPS:6.2f} s ({s['f1'] - s['f0']} f)")
    for L in placed:
        print(f"L{L['n']:02d} {L['take']} x{L['tempo']} {L['t0']:6.2f}-{L['t1']:6.2f} ({L['dur']:.2f} s, pauses cut {L['pauses_cut']:.2f})")
    print(f"Part A: {total} frames = {total / FPS:.2f} s; dialogue {lfin:.1f} LUFS (gain {gain:.1f} dB, raw peak {peak:.1f})")


if __name__ == "__main__":
    main()
