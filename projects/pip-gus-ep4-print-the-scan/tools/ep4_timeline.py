"""Ep 4 Part A timeline from the approved voice take (ElevenLabs v4 dialogue job 3c709f12, owner-approved 2026-11-17).

The take is one file with all 16 lines in script order. Each line is cut out at the quietest 40 ms between it and its
neighbours (no audio lost, nothing time-stretched: owner rule "never speed it up"). Lines 1-15 keep the take's own spacing
except where a visual beat needs air (EXTRA). Line 16 (Pip's question over the logo card) is written as its own clip.

Writes:
  projects/pip-gus-ep4-print-the-scan/ep4_timeline.json   (shots in frames, lines + words in reel seconds; drives Blender)
  MEDIA/voice/lines/Lnn.wav                               (48 kHz mono clips, untouched)
  MEDIA/voice/partA_dialogue.wav                          (lines 1-15 at reel times, voice polish, -14 LUFS / -1 dBTP)
  MEDIA/voice/L16_logo.wav                                (line 16, same polish and gain)

Usage: python ep4_timeline.py
"""
import json, subprocess
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
MEDIA = Path("/home/user/media/pip-gus-ep4-print-the-scan")
SRC = MEDIA / "voice/ep4_take1_3c709f12.mp3"
WORDS = json.load(open(MEDIA / "voice/words.json"))
SR, FPS = 48000, 30

# n, speaker, shot, script text (caption tokens map 1:1 onto the heard words, in order)
LINES = [
    (1, "PIP", "E1", "OK, it's scanned. Can we print it now?"),
    (2, "PIP", "E2", "My bumper! Print my bumper!"),
    (3, "GUS", "E3", "That's a scan. It's a skin."),
    (4, "GUS", "E4", "A mesh of tiny triangles. Not necessarily solid."),   # v3 (owner): was "No thickness."
    (5, "PIP", "E5", "So... print it anyway?"),
    (6, "GUS", "E5", "Sure."),
    (7, "PIP", "E6", "Is it done yet?"),
    (8, "GUS", "E7", "...There's nothing to print."),
    (9, "GUS", "E8", "The scan is the reference."),
    (10, "GUS", "E8", "You can remake the original from it..."),
    (11, "GUS", "E9", "...or design a new one on it."),
    (12, "PIP", "E10", "So the scan is what makes it fit?"),
    (13, "GUS", "E10", "Every curve."),
    (14, "PIP", "E11", "Ooh! Illumaesthetic does both!"),
    (15, "GUS", "E12", "...Of course they do."),
    (16, "PIP", "LOGO", "If the scan's a mesh, what do you design in?"),
]
# extra silence (s) inserted AFTER a line, for a visual beat (never inside a line)
EXTRA = {8: 0.75,    # the empty build plate goes onto the failed-print shelf
         10: 0.15,   # the remade original clicks on before "...or design a new one"
         11: 0.35,   # Pip's bumper snaps on ("click")
         13: 0.25}   # the sparkle runs along the seam
LEAD = 0.20          # reel time before line 1
TAIL_END = 0.45      # after line 15: Gus leans in, push into the phone (last frame = all screen)
VOICE_FX = ("highpass=f=90:poles=2,equalizer=f=3500:t=q:w=1.1:g=3,treble=g=2:f=9000:t=s:w=0.7,"
            "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:knee=4:makeup=3")   # pilot v2 polish (owner: brighter)
STEM_I, STEM_TP = -14.0, -1.0


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def wav(path, x):
    import wave
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def quiet_cut(a, t_lo, t_hi):
    """Middle of the quietest 40 ms window between t_lo and t_hi (s)."""
    lo, hi = int(t_lo * SR), int(t_hi * SR)
    if hi - lo < int(0.05 * SR):
        return (t_lo + t_hi) / 2
    hop, win = int(0.005 * SR), int(0.04 * SR)
    best, bt = None, (t_lo + t_hi) / 2
    for s in range(lo, hi - win, hop):
        e = float(np.sqrt(np.mean(a[s:s + win] ** 2)))
        if best is None or e < best:
            best, bt = e, (s + win / 2) / SR
    return bt


def main():
    a = decode(SRC)
    # v3 (owner 2026-11-19): line 4 re-voiced ("Not necessarily solid" for "No thickness"), Harrison, ElevenLabs v4 job
    # cc6bde49. The whole line is swapped at the quiet points around it; later lines shift by a whole number of frames.
    global WORDS
    rev = decode(MEDIA / "voice/L04_rev_cc6bde49.mp3")
    rw = json.load(open(MEDIA / "voice/words_L04rev.json"))
    i0, i1 = 19, 26                                   # old line 4 = words 19..25
    cA = quiet_cut(a, WORDS[i0 - 1]["t1"], WORDS[i0]["t0"])
    cB = quiet_cut(a, WORDS[i1 - 1]["t1"], WORDS[i1]["t0"])
    pre, tail = WORDS[i0]["t0"] - cA, cB - WORDS[i1 - 1]["t1"]
    sp_end = rw[-1]["t1"] + 0.08
    new = rev[:int(sp_end * SR)].copy()
    old_sp = a[int(WORDS[i0]["t0"] * SR):int(WORDS[i1 - 1]["t1"] * SR)]
    new *= float(np.sqrt(np.mean(old_sp ** 2)) / np.sqrt(np.mean(new ** 2)))     # level-match to the old line
    k = int(0.01 * SR)
    new[-k:] *= np.linspace(1, 0, k)
    L_new = pre + sp_end + tail
    delta = L_new - (cB - cA)
    D = int(np.ceil(delta * FPS - 1e-6))
    padt = D / FPS - delta
    seg = np.concatenate([np.zeros(int(round(pre * SR)), np.float32), new, np.zeros(int(round((tail + padt) * SR)), np.float32)])
    a = np.concatenate([a[:int(cA * SR)], seg, a[int(cB * SR):]])
    sh = D / FPS
    WORDS = (WORDS[:i0] + [dict(w=w["w"], t0=round(cA + pre + w["t0"], 3), t1=round(cA + pre + w["t1"], 3)) for w in rw]
             + [dict(w=w["w"], t0=round(w["t0"] + sh, 3), t1=round(w["t1"] + sh, 3)) for w in WORDS[i1:]])
    print(f"line 4 swapped: later lines shift by {D} frames")
    dur = len(a) / SR
    # assign heard words to lines by token count
    toks = [t.split() for _, _, _, t in LINES]
    assert sum(map(len, toks)) == len(WORDS), (sum(map(len, toks)), len(WORDS))
    k, spans = 0, []
    for (n, spk, sh, text), tk in zip(LINES, toks):
        ws = WORDS[k:k + len(tk)]
        k += len(tk)
        spans.append([dict(w=c, t0=w["t0"], t1=w["t1"], heard=w["w"]) for c, w in zip(tk, ws)])
    # cut points between lines (source seconds)
    cuts = [0.0]
    for i in range(len(LINES) - 1):
        cuts.append(quiet_cut(a, spans[i][-1]["t1"], spans[i + 1][0]["t0"]))
    cuts.append(dur)
    lines_dir = MEDIA / "voice/lines"
    lines_dir.mkdir(parents=True, exist_ok=True)
    # reel placement: source time + LEAD + accumulated extras
    off, out_lines = LEAD, []
    for i, ((n, spk, sh, text), ws) in enumerate(zip(LINES, spans)):
        c0, c1 = cuts[i], cuts[i + 1]
        clip = a[int(c0 * SR):int(c1 * SR)]
        wav(lines_dir / f"L{n:02d}.wav", clip)
        L = dict(n=n, speaker=spk, shot=sh, text=text, file=f"lines/L{n:02d}.wav", src_cut=[round(c0, 3), round(c1, 3)],
                 reel_start=round(c0 + off, 3), t0=round(ws[0]["t0"] + off, 3), t1=round(ws[-1]["t1"] + off, 3),
                 words=[dict(w=w["w"], t0=round(w["t0"] + off, 3), t1=round(w["t1"] + off, 3)) for w in ws])
        out_lines.append(L)
        off += EXTRA.get(n, 0.0)
    partA = [L for L in out_lines if L["n"] <= 15]
    logo = out_lines[-1]
    # shots: cut halfway between the last line of one shot and the first line of the next (frame-snapped)
    order = []
    for L in partA:
        if not order or order[-1][0] != L["shot"]:
            order.append([L["shot"], L, L])
        else:
            order[-1][2] = L
    shots, f_prev = [], 0
    for j, (sid, first, last) in enumerate(order):
        if j + 1 < len(order):
            nxt = order[j + 1][1]
            gap0 = last["t1"] + EXTRA.get(last["n"], 0.0) * 0.6
            fcut = int(round(((gap0 + nxt["t0"]) / 2) * FPS))
        else:
            fcut = int(round((last["t1"] + TAIL_END) * FPS))
        shots.append(dict(id=sid, f0=f_prev, f1=fcut))
        f_prev = fcut
    total = shots[-1]["f1"]
    # dialogue stem: lines 1-15 at reel times, polished, loudness-normalised (two-pass)
    MEDIA.joinpath("voice").mkdir(exist_ok=True)
    mix = np.zeros(int(total / FPS * SR) + SR, np.float32)
    for L in partA:
        x = decode(MEDIA / "voice" / L["file"])
        s = int(L["reel_start"] * SR)
        e = min(len(mix), s + len(x))
        mix[s:e] += x[:e - s]
    mix = mix[:int(total / FPS * SR)]
    raw = MEDIA / "voice/partA_dialogue_raw.wav"
    wav(raw, mix)
    l16raw = MEDIA / "voice/L16_raw.wav"
    wav(l16raw, decode(MEDIA / "voice" / logo["file"]))

    def polish(src, dst, gain_db=None):
        if gain_db is None:
            r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af",
                                f"{VOICE_FX},loudnorm=I={STEM_I}:TP={STEM_TP}:LRA=7:print_format=json", "-f", "null", "-"],
                               capture_output=True, text=True).stderr
            js = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
            gain_db = STEM_I - float(js["input_i"])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
                        f"{VOICE_FX},volume={gain_db:.2f}dB,alimiter=limit={10 ** (STEM_TP / 20):.4f}:level=false",
                        "-ar", str(SR), "-ac", "1", str(dst)], check=True)
        return gain_db

    g = polish(raw, MEDIA / "voice/partA_dialogue.wav")
    polish(l16raw, MEDIA / "voice/L16_logo.wav", g)   # same gain as the stem: Pip sounds the same over the logo
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(MEDIA / "voice/partA_dialogue.wav"), "-af", "ebur128=peak=true",
                           "-f", "null", "-"], capture_output=True, text=True).stderr
    I = [l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1]
    TP = [l for l in meas.splitlines() if l.strip().startswith("Peak:")][-1].split()[1]
    tl = dict(doc="Ep 4 Part A timeline (real voices, take 3c709f12, no speed-ups). Frames are reel frames at 30 fps; shot f1 "
                  "is exclusive. Line/word times are reel seconds. Line 16 plays over the logo card (not in Part A).",
              fps=FPS, shift_v3=D, total_frames=total, duration_s=round(total / FPS, 3), screen_full_frame=total - 1,
              shots=shots, lines=partA, logo_line=logo,
              dialogue=dict(file="voice/partA_dialogue.wav", integrated_lufs=float(I), true_peak_dbtp=float(TP),
                            gain_db=round(g, 2)))
    json.dump(tl, open(PROJ / "ep4_timeline.json", "w"), indent=1)
    for s in shots:
        print(f"{s['id']:4s} {s['f0']:5d}-{s['f1']:5d}  {(s['f1'] - s['f0']) / FPS:5.2f} s")
    print(f"Part A {total} frames = {total / FPS:.2f} s; stem {I} LUFS, {TP} dBTP; logo line {logo['t1'] - logo['t0']:.2f} s")


if __name__ == "__main__":
    main()
