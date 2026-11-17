"""Ep 7 (big vs small printers): split the approved ElevenLabs dialogue take into lines, tighten the pauses, lay out shots.

Owner (2026-11-17): take 1 (job 340b8683) approved, "tighten the pauses and go ahead". Rules:
  - no speed-up, no pitch change (series rule): only silence is removed;
  - pauses BETWEEN lines are set to GAP (per-transition overrides for deliberate deadpan beats);
  - pauses INSIDE a line are capped at MAX_IN (energy-silent stretches only, so Gus's voiced sigh in line 8 stays);
  - line 13 (Pip, voice only over the logo card) is written as its own clip, not placed in the cartoon.

Writes:
  projects/pip-gus-ep6-printer-size/ep7_timeline.json     shots (frames), lines + words + sighs (cartoon seconds)
  /home/user/media/work/ep7/voice/proc/Lnn.wav             processed line clips (48 kHz mono, pilot voice polish)
  /home/user/media/work/ep7/out/ep7_dialogue.wav           cartoon dialogue stem (-14 LUFS, -1 dBTP)
  /home/user/media/work/ep7/out/ep7_L13_logo.wav           line 13 for the logo card (same level)

Usage: python ep7_timeline.py   (needs take1_words.json from faster-whisper small.en on the full take)
"""
import json, subprocess, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
VOICE = Path("/home/user/media/pip-gus-ep6-printer-size/voice")
TAKE = VOICE / "ep7_dialogue_take1.mp3"
WORDS = VOICE / "take1_words.json"
WORK = Path("/home/user/media/work/ep7")
PROC, OUT = WORK / "voice/proc", WORK / "out"
SR, FPS = 48000, 30

# n: (speaker, shot, word count, script text)
LINES = {
    1: ("PIP", "S1", 7, "It's cut! Which printer do we use?"),
    2: ("GUS", "S2", 6, "Big one? Fewer pieces. Fewer seams."),
    3: ("GUS", "S3", 3, "But it's slower..."),
    4: ("GUS", "S4", 7, "...and the bigger nozzle means less detail."),
    5: ("PIP", "S5", 4, "So small ones win!"),
    6: ("GUS", "S6", 8, "Sharper, sure. And you can run a few."),
    7: ("PIP", "S7", 4, "Is it done yet?"),
    8: ("GUS", "S7", 7, "...This piece is. Now glue them all."),
    9: ("PIP", "S8", 3, "So who wins?"),
    10: ("GUS", "S8", 7, "Depends on the part. We run both."),
    11: ("PIP", "S9", 6, "Wait. Illumaesthetic's big one is HUGE."),
    12: ("GUS", "S10", 2, "...Show-off."),
    13: ("PIP", "LOGO", 8, "Printer's ready. What do we load in it?"),
}
GAP = 0.22                                    # default pause between lines (speech end -> next speech start)
GAP_BEFORE = {3: 0.26, 4: 0.30, 8: 0.40, 11: 0.20, 12: 0.45}   # deliberate beats: "slower..."/"...and", deadpan "...This piece is", "...Show-off"
MAX_IN = 0.32                                 # longest silent pause kept inside a line
PRE, POST = 0.03, 0.06                        # padding kept around the speech edges of each clip
LEAD, TAIL = 0.17, 0.10                       # before the first line / after the last cartoon line
SHOT_EXTRA = {"S2": 0.25, "S6": 0.20, "S8": 0.15, "S10": 0.60}   # visual beats: split-screen, three printers, nudge, push into phone
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
    for w in ws:   # Whisper hears the brand as "Lumesthetics'": captions must read the real word (owner accepted the sound)
        if "esthetic" in w["w"].lower():
            w["w"] = "Illumaesthetic's"
    return ws


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
    # stems: every line level-matched, then two-pass loudnorm on the cartoon stem; line 13 gets the same gain
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
                    "-c:a", "pcm_s24le", str(OUT / "ep7_dialogue.wav")], check=True)
    tmp.unlink()
    # line 13 on its own: same integrated target as the cartoon stem
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(PROC / "L13.wav"), "-af",
                    f"apad=pad_dur=0.3,loudnorm=I={STEM_I}:TP={STEM_TP}:LRA=11", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s24le",
                    str(OUT / "ep7_L13_logo.wav")], check=True)
    lfin = loudness(OUT / "ep7_dialogue.wav")
    tl = dict(doc="Ep 7 cartoon timeline (real voices, approved take 1 job 340b8683, pauses tightened, no speed-up). Frames at 30 fps; "
                  "shot f1 exclusive; line/word times in cartoon seconds. Line 13 is the logo-card voice-over (not placed).",
              fps=FPS, total_frames=total, duration_s=round(total / FPS, 3), screen_full_frame=shots[-1]["f1"] - 1,
              shots=shots, lines=placed, logo_line=lines[13],
              dialogue=dict(file="ep7_dialogue.wav", integrated_lufs=round(lfin, 2)))
    (PROJ / "ep7_timeline.json").write_text(json.dumps(tl, indent=1))
    for s in shots:
        print(f"{s['id']:4s} {s['f0']:4d}-{s['f1']:4d}  {s['f0'] / FPS:6.2f}-{s['f1'] / FPS:6.2f} s")
    for L in placed:
        print(f"L{L['n']:02d} {L['speaker']} {L['t0']:6.2f}-{L['t1']:6.2f} ({L['dur']:.2f} s, cut {L['pauses_cut']:.2f}, sighs {L['sighs']}) {L['text']}")
    print(f"L13 logo VO {lines[13]['dur']:.2f} s")
    print(f"cartoon {total} frames = {total / FPS:.2f} s (take spoken span 34.1 s); dialogue {lfin:.1f} LUFS")


if __name__ == "__main__":
    main()
