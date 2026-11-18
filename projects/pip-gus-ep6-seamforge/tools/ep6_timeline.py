"""Ep 6 (SeamForged, cutting step): split the approved ElevenLabs dialogue take into lines, tighten the pauses, lay out shots.
Adapted from Ep 7's tools/ep7_timeline.py (claude/pip-gus-ep6-printer-size).

Owner (2026-11-17): take v2 (job 37e7501f) approved. Rules:
  - no speed-up, no pitch change (series rule): only silence is removed;
  - pauses BETWEEN lines are set to GAP (per-transition overrides for deliberate deadpan beats);
  - pauses INSIDE a line are capped at MAX_IN;
  - line 10 (Pip, voice only over the logo card) is written as its own clip, not placed in the cartoon.
Also processes the Part B voice-over take (job 8e7195cb, 4 lines) into clips with the same polish and level.

Writes:
  projects/pip-gus-ep6-seamforge/ep6_timeline.json     shots (frames), lines + words (cartoon seconds), Part B VO clips
  /home/user/media/work/ep6/voice/proc/Lnn.wav, Bnn.wav processed line clips (48 kHz mono, pilot voice polish)
  /home/user/media/work/ep6/out/ep6_dialogue.wav        cartoon dialogue stem (-14 LUFS, -1 dBTP)
  /home/user/media/work/ep6/out/ep6_L10_logo.wav        line 10 for the logo card (same level)

Usage: python ep6_timeline.py
"""
import json, subprocess, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
VOICE = Path("/home/user/media/pip-gus-ep6-seamforge/voice")
TAKE = VOICE / "ep6_dialogue_v2.mp3"
TAKE_B = VOICE / "ep6_partB_vo_v1.mp3"
WORDS = VOICE / "ep6_words_v2.json"
WORK = Path("/home/user/media/work/ep6")
PROC, OUT = WORK / "voice/proc", WORK / "out"
SR, FPS = 48000, 30

# n: (speaker, shot, word count, script text)
LINES = {
    1: ("PIP", "S1", 5, "It's bigger than the printer..."),
    2: ("GUS", "S2", 7, "So we cut it up. By hand."),
    3: ("GUS", "S3", 3, "Number every piece..."),
    4: ("GUS", "S4", 9, "...then lay each one flat on the print bed."),
    5: ("PIP", "S5", 4, "Is it done yet?"),
    6: ("GUS", "S5", 1, "...No."),
    7: ("PIP", "S6", 7, "There has to be a better way."),
    8: ("GUS", "S7", 3, "...We made one."),
    9: ("PIP", "S7", 2, "Show me!"),
    10: ("PIP", "LOGO", 7, "It's cut! Which printer do we use?"),
}
LOGO_N = 10
# Part B voice-over (over the SeamForged screen capture and the printed piece): (speaker, shot, text)
VO_B = {1: ("GUS", "B1", "One click. Cut to fit."), 2: ("GUS", "B2", "Every piece numbered on the inside."),
        3: ("GUS", "B3", "Laid out on the beds, ready to print."), 4: ("PIP", "B4", "Whoa. There's the number!")}
VO_B_COUNTS = (5, 6, 8, 4)
GAP = 0.22                                    # default pause between lines (speech end -> next speech start)
GAP_BEFORE = {4: 0.12, 6: 0.40, 8: 0.45}   # "piece..." runs on into "...then lay"; Gus answers "No" mid-task; deadpan "...We made one."
MAX_IN = 0.32                                 # longest silent pause kept inside a line
PRE, POST = 0.03, 0.06                        # padding kept around the speech edges of each clip
LEAD, TAIL = 0.17, 0.10                       # before the first line / after the last cartoon line
SHOT_EXTRA = {"S1": 0.30, "S2": 0.45, "S3": 0.30, "S4": 0.70, "S5": 0.45, "S7": 0.60}   # laptop beat, hand-cut insert, numbering, placing pieces, "No" while placing, push into phone
VOICE_FX = ("highpass=f=90:poles=2,equalizer=f=3500:t=q:w=1.1:g=3,treble=g=2:f=9000:t=s:w=0.7,"
            "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:knee=4:makeup=3")   # pilot v2 polish
STEM_I, STEM_TP = -14.0, -1.0


def decode(p):
    pcm = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", str(p), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0


def energy_on(x, db=-42.0):
    """10 ms frames that are voiced (RMS within db of the take's peak frame)."""
    hop = SR // 100
    n = len(x) // hop
    rms = np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(rms / rms.max()) > db


def runs(on, a, b, bridge=8, min_len=3):
    """Voiced runs (seconds) inside [a, b], bridging gaps shorter than bridge frames."""
    i0, i1 = int(a * 100), min(len(on), int(b * 100) + 1)
    out, i = [], i0
    while i < i1:
        if on[i]:
            j = i
            while j < i1 and on[j]:
                j += 1
            if out and i - out[-1][1] < bridge:
                out[-1] = (out[-1][0], j)
            else:
                out.append((i, j))
            i = j
        else:
            i += 1
    return [(s / 100, e / 100) for s, e in out if e - s >= min_len]


def write_wav(path, y):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    return float([l for l in r.stderr.splitlines() if "I:" in l and "LUFS" in l][-1].split("I:")[1].split("LUFS")[0])


def merge_brand(ws):
    return ws   # no brand word in this episode's dialogue


def main():
    x = decode(TAKE)
    on = energy_on(x)
    ws = merge_brand(json.loads(WORDS.read_text()))
    assert len(ws) == sum(v[2] for v in LINES.values()), (len(ws), "word count does not match the script")
    k, words = 0, {}
    for n, (_, _, cnt, _) in LINES.items():
        words[n] = ws[k:k + cnt]
        k += cnt
    # line boundaries: the silent gap (between voiced runs at -35 dB) nearest to the midpoint of whisper's boundary words.
    # Cut on real silences, not on whisper times (whisper puts "Wait!" over the tail of "both").
    on = energy_on(x, -35.0)
    allr = runs(on, 0.0, len(x) / SR)
    gaps = [(p1, q0) for (p0, p1), (q0, q1) in zip(allr, allr[1:]) if q0 - p1 >= 0.2]
    bound = {}
    for n in list(LINES)[:-1]:
        mid = (words[n][-1]["t1"] + words[n + 1][0]["t0"]) / 2
        bound[n] = min(gaps, key=lambda g: abs((g[0] + g[1]) / 2 - mid))
    span = {}
    for n in LINES:
        a = bound[n - 1][1] - PRE if n - 1 in bound else max(0.0, allr[0][0] - PRE)
        b = bound[n][0] + POST if n in bound else min(len(x) / SR, allr[-1][1] + POST)
        span[n] = (a, b, [r for r in allr if r[1] > a and r[0] < b])
    PROC.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    lines = {}
    for n, (spk, shot, _, text) in LINES.items():
        a, b, rs = span[n]
        rs = [(max(a, r0), min(b, r1)) for r0, r1 in rs if r1 > a and r0 < b]
        keep, cur = [], a
        for (p0, p1), (q0, q1) in zip(rs, rs[1:]):            # silent stretches inside the line longer than MAX_IN
            if q0 - p1 > MAX_IN:
                keep.append((cur, p1 + MAX_IN / 2))
                cur = q0 - MAX_IN / 2
        keep.append((cur, b))
        fade = int(0.008 * SR)
        parts = []
        for s0, s1 in keep:
            seg = x[int(s0 * SR):int(s1 * SR)].copy()
            seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
            parts.append(seg)

        def mapt(t, keep=keep):
            acc = 0.0
            for s0, s1 in keep:
                if t < s0:
                    return acc
                if t <= s1:
                    return acc + (t - s0)
                acc += s1 - s0
            return acc

        raw, out = PROC / f"_L{n:02d}.wav", PROC / f"L{n:02d}.wav"
        write_wav(raw, np.concatenate(parts))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(raw), "-af", VOICE_FX, "-ar", str(SR), "-ac", "1",
                        "-c:a", "pcm_s16le", str(out)], check=True)
        raw.unlink()
        wl = []
        for w in words[n]:
            t0 = min(max(w["t0"], a), b - 0.06)
            t1 = min(max(w["t1"], t0 + 0.06), b)
            wl.append(dict(w=w["w"], t0=round(mapt(t0), 3), t1=round(mapt(t1), 3)))
        # sighs: voiced runs outside the spoken words (Gus's "is... [sigh] now"); whisper stretches "is..." over it, so a
        # voiced run that starts > 0.3 s after a word's onset and ends before the next word counts as a sigh
        sighs = []
        if spk == "GUS":
            for (p0, p1) in rs:
                for w, nx in zip(words[n], words[n][1:]):
                    if p0 > w["t0"] + 0.3 and p1 < nx["t0"] + 0.02 and p1 - p0 >= 0.25:
                        sighs.append([round(mapt(p0), 3), round(mapt(p1), 3)])
        lines[n] = dict(n=n, speaker=spk, shot=shot, text=text, src_span=[round(a, 3), round(b, 3)],
                        pauses_cut=round((b - a) - sum(s1 - s0 for s0, s1 in keep), 3), dur=round(len(decode(out)) / SR, 3),
                        words=wl, sighs=sighs, file=out.name)
    # layout: cartoon lines 1-12, shots on whole frames
    shots, order = [], [s for s in dict.fromkeys(L["shot"] for L in lines.values()) if s != "LOGO"]
    t = 0.0
    for i, sid in enumerate(order):
        ls = [lines[n] for n in sorted(lines) if lines[n]["shot"] == sid]
        s0 = t
        tt = s0 + (LEAD if i == 0 else 0.0)
        for L in ls:
            if L is not ls[0]:
                tt += GAP_BEFORE.get(L["n"], GAP) - PRE - POST    # speech edge to speech edge
            L["t0"], L["t1"] = round(tt, 3), round(tt + L["dur"], 3)
            tt = L["t1"]
        nxt = ls[-1]["n"] + 1
        gap_after = 0.0 if nxt not in lines or lines[nxt]["shot"] == "LOGO" else GAP_BEFORE.get(nxt, GAP) - PRE - POST
        s1 = tt + SHOT_EXTRA.get(sid, 0.0) + (gap_after if i + 1 < len(order) else TAIL)
        f0, f1 = int(round(s0 * FPS)), int(round(s1 * FPS))
        shots.append(dict(id=sid, f0=f0, f1=f1))
        t = f1 / FPS
    total = shots[-1]["f1"]
    placed = [lines[n] for n in sorted(lines) if lines[n]["shot"] != "LOGO"]
    for L in placed:
        L["words"] = [dict(w=w["w"], t0=round(L["t0"] + w["t0"], 3), t1=round(L["t0"] + w["t1"], 3)) for w in L["words"]]
        L["sighs"] = [[round(L["t0"] + a, 3), round(L["t0"] + b, 3)] for a, b in L["sighs"]]
    # stems: every line level-matched, then two-pass loudnorm on the cartoon stem; line 10 gets the same gain
    def gain_to(path):
        return 10 ** ((STEM_I - loudness(path)) / 20)
    mix = np.zeros(int(total / FPS * SR), np.float32)
    for L in placed:
        y = decode(PROC / L["file"]) * gain_to(PROC / L["file"])
        i0 = int(round(L["t0"] * SR))
        mix[i0:i0 + len(y)] += y[: len(mix) - i0]
    tmp = OUT / "_dlg.wav"
    write_wav(tmp, mix * 0.5)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(tmp), "-af",
                        f"loudnorm=I={STEM_I}:TP={STEM_TP}:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I={STEM_I}:TP={STEM_TP}:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-af", ln, "-ar", str(SR), "-ac", "2",
                    "-c:a", "pcm_s24le", str(OUT / "ep6_dialogue.wav")], check=True)
    tmp.unlink()
    # line 10 on its own: same integrated target as the cartoon stem
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(PROC / f"L{LOGO_N:02d}.wav"), "-af",
                    f"apad=pad_dur=0.3,loudnorm=I={STEM_I}:TP={STEM_TP}:LRA=11", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s24le",
                    str(OUT / "ep6_L10_logo.wav")], check=True)
    # Part B VO: cut between lines at the quietest 50 ms between one line's last word and the next line's first word
    # (whisper words, ep6_partB_words.json); words per line from VO_B_COUNTS
    xb = decode(TAKE_B)
    wb = json.loads((VOICE / "ep6_partB_words.json").read_text())
    assert len(wb) == sum(VO_B_COUNTS), (len(wb), "Part B word count does not match")
    hop = SR // 100
    nb = len(xb) // hop
    rmsb = np.sqrt((xb[: nb * hop].reshape(nb, hop) ** 2).mean(1) + 1e-12)
    cuts, k = [0.0], 0
    for c in VO_B_COUNTS[:-1]:
        k += c
        lo, hi = int(wb[k - 1]["t1"] * 100) - 5, int(wb[k]["t0"] * 100) + 3
        win = np.convolve(rmsb[lo:hi], np.ones(5) / 5, mode="same")
        cuts.append((lo + int(np.argmin(win))) / 100)
    cuts.append(len(xb) / SR)
    rb = runs(energy_on(xb, -40.0), 0.0, len(xb) / SR)
    vo_b = {}
    for i, n in enumerate(VO_B):
        rr = [r for r in rb if r[1] > cuts[i] and r[0] < cuts[i + 1]]
        a, b = max(cuts[i], rr[0][0] - PRE), min(cuts[i + 1], rr[-1][1] + POST)
        seg = xb[int(a * SR):int(b * SR)].copy()
        f8 = int(0.008 * SR); seg[:f8] *= np.linspace(0, 1, f8); seg[-f8:] *= np.linspace(1, 0, f8)
        raw, outp = PROC / f"_B{n:02d}.wav", PROC / f"B{n:02d}.wav"
        write_wav(raw, seg)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(raw), "-af", VOICE_FX + f",volume=1.0", "-ar", str(SR),
                        "-ac", "1", "-c:a", "pcm_s16le", str(outp)], check=True)
        raw.unlink()
        g = 10 ** ((STEM_I - loudness(outp)) / 20)
        y = decode(outp) * g
        write_wav(outp, y * min(1.0, 0.89 / max(1e-6, np.abs(y).max())))
        spk, shot, text = VO_B[n]
        vo_b[n] = dict(n=n, speaker=spk, shot=shot, text=text, src_span=[round(a, 3), round(b, 3)], dur=round(len(y) / SR, 3),
                       file=outp.name)
        print(f"B{n:02d} {spk} {vo_b[n]['dur']:.2f} s  {text}")
    lfin = loudness(OUT / "ep6_dialogue.wav")
    tl = dict(doc="Ep 6 cartoon timeline (real voices, approved take v2 job 37e7501f, pauses tightened, no speed-up). Frames at 30 fps; "
                  "shot f1 exclusive; line/word times in cartoon seconds. Line 10 is the logo-card voice-over (not placed).",
              fps=FPS, total_frames=total, duration_s=round(total / FPS, 3), screen_full_frame=shots[-1]["f1"] - 1,
              shots=shots, lines=placed, logo_line=lines[LOGO_N], vo_b=vo_b,
              dialogue=dict(file="ep6_dialogue.wav", integrated_lufs=round(lfin, 2)))
    (PROJ / "ep6_timeline.json").write_text(json.dumps(tl, indent=1))
    for s in shots:
        print(f"{s['id']:4s} {s['f0']:4d}-{s['f1']:4d}  {s['f0'] / FPS:6.2f}-{s['f1'] / FPS:6.2f} s")
    for L in placed:
        print(f"L{L['n']:02d} {L['speaker']} {L['t0']:6.2f}-{L['t1']:6.2f} ({L['dur']:.2f} s, cut {L['pauses_cut']:.2f}, sighs {L['sighs']}) {L['text']}")
    print(f"L10 logo VO {lines[LOGO_N]['dur']:.2f} s")
    print(f"cartoon {total} frames = {total / FPS:.2f} s ; dialogue {lfin:.1f} LUFS")


if __name__ == "__main__":
    main()
