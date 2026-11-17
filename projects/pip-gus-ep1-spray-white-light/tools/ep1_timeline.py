"""Ep 1 timeline: split the approved ElevenLabs take into lines, lay them out on the reel clock, define the shots.

  python ep1_timeline.py TAKE.wav WORDS.json OUT_DIR TIMELINE.json [--gap 0.45] [--lead 0.25]

- Words come from a faster-whisper (medium.en) pass over the WHOLE take (word timestamps); they are assigned to the script's
  15 lines by matching each line's normalised tokens in order.
- Every line keeps its own audio exactly as performed (no time-stretch, no cuts inside a line). Only the silence BETWEEN
  lines is capped at --gap seconds; each cut sits in the quietest 30 ms between two lines.
- Line 15 ("What do you spray with?") is the audience-question card line: it is written as its own file and is not part of
  the cartoon dialogue.
- Writes OUT_DIR/dialogue_cartoon.wav (48 kHz mono), OUT_DIR/L15_card.wav and TIMELINE.json (fps 30; lines with reel-time
  word times; shots with frame ranges, cut at line boundaries).
"""
import json, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

SR = 48000
FPS = 30
LINES = [  # n, speaker, text, shot
    (1, "PIP", "Why are you spraying the windows white?", "A"),
    (2, "GUS", "The scanner shines a pattern of light on the car.", "B"),
    (3, "GUS", "A camera watches the lines bend.", "C"),
    (4, "GUS", "From that angle, it knows where every point is.", "C"),
    (5, "PIP", "So what's wrong with windows?", "D"),
    (6, "GUS", "Light goes straight through glass.", "E"),
    (7, "GUS", "Chrome's a mirror. It throws the light away.", "F"),
    (8, "GUS", "And black just swallows it.", "G"),
    (9, "PIP", "So you only spray the tricky bits?", "H"),
    (10, "GUS", "Glass. Chrome. Black. Badges. Now the light comes back.", "I"),
    (11, "PIP", "Why the squiggles?", "J"),
    (12, "GUS", "Smooth panels all look the same. It needs something to track.", "K"),
    (13, "PIP", "Does it come off?", "L"),
    (14, "GUS", "...Depends on the spray.", "M"),
    (15, "PIP", "What do you spray with?", "CARD"),
]


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def norm(s):
    return [t for t in re.sub(r"[^a-z' ]", " ", s.lower().replace("’", "'")).split() if t]


def main():
    src, wj, out, tl_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    gap, lead = float(arg("--gap", "0.45")), float(arg("--lead", "0.25"))
    out.mkdir(parents=True, exist_ok=True)
    words = json.loads(wj.read_text())
    toks = [(norm(w["w"]) or [""])[0] for w in words]
    # assign words to lines in order
    i, spans = 0, []
    for n, spk, text, shot in LINES:
        want = norm(text)
        j = i
        for t in want:
            assert toks[j] == t, (n, t, toks[j], j)
            j += 1
        spans.append((i, j))
        i = j
    assert i == len(words), (i, len(words))
    pcm = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    hop = int(0.01 * SR)
    env = np.sqrt(np.convolve(x ** 2, np.ones(int(0.03 * SR)) / int(0.03 * SR), "same"))

    def quiet(a, b):   # quietest point between a and b (s)
        ia, ib = int(a * SR), int(b * SR)
        if ib - ia < 2 * hop:
            return (a + b) / 2
        k = np.argmin(env[ia:ib:hop])
        return (ia + k * hop) / SR

    # source cut points between lines
    cuts = [0.0]
    for k in range(len(LINES) - 1):
        a = words[spans[k][1] - 1]["t1"]
        b = words[spans[k + 1][0]]["t0"]
        cuts.append(quiet(a, b))
    cuts.append(len(x) / SR)
    segs = []
    for k, (n, spk, text, shot) in enumerate(LINES):
        a, b = cuts[k], cuts[k + 1]
        w0, w1 = words[spans[k][0]]["t0"], words[spans[k][1] - 1]["t1"]
        # trim silence at the segment edges down to gap/2 each side (never into a word or a breath before it)
        pre = w0 - a
        post = b - w1
        a2 = w0 - min(pre, gap / 2) if n != 12 else a      # line 12 keeps its sigh before the first word
        b2 = w1 + min(post, gap / 2)
        segs.append((a2, b2))
    # lay out the cartoon (lines 1-14) on the reel clock
    lines, t, cart = [], lead, [np.zeros(int(lead * SR), np.float32)]
    for k, (n, spk, text, shot) in enumerate(LINES):
        a, b = segs[k]
        clip = x[int(a * SR):int(b * SR)].copy()
        fade = int(0.008 * SR)
        clip[:fade] *= np.linspace(0, 1, fade)
        clip[-fade:] *= np.linspace(1, 0, fade)
        ws = [dict(w=words[q]["w"], t0=round(words[q]["t0"] - a, 3), t1=round(words[q]["t1"] - a, 3))
              for q in range(*spans[k])]
        if n == 15:
            wav_write(out / "L15_card.wav", clip)
            lines.append(dict(n=n, speaker=spk, text=text, shot=shot, file="L15_card.wav", dur=round(len(clip) / SR, 3),
                              words=ws, src_span=[round(a, 3), round(b, 3)]))
            continue
        off = t
        lines.append(dict(n=n, speaker=spk, text=text, shot=shot, src_span=[round(a, 3), round(b, 3)],
                          t0=round(off + ws[0]["t0"], 3), t1=round(off + ws[-1]["t1"], 3), seg0=round(off, 3),
                          words=[dict(w=w["w"], t0=round(off + w["t0"], 3), t1=round(off + w["t1"], 3)) for w in ws]))
        if n == 12:   # the sigh: voiced audio before the first word
            lines[-1]["sighs"] = [[round(off, 3), round(off + ws[0]["t0"] - 0.05, 3)]]
        cart.append(clip)
        t += len(clip) / SR
    tail = 0.35
    cart.append(np.zeros(int(tail * SR), np.float32))
    y = np.concatenate(cart)
    wav_write(out / "dialogue_cartoon.wav", y)
    dur = len(y) / SR
    # shots: cut at the start of each shot's first line segment (snapped to frames), last shot ends at the cartoon end
    starts = {}
    for L in lines:
        if L["shot"] == "CARD":
            continue
        starts.setdefault(L["shot"], L["seg0"])
    ids = list(starts)
    shots = []
    for k, sid in enumerate(ids):
        f0 = 0 if k == 0 else int(round(starts[sid] * FPS))
        f1 = int(round(dur * FPS)) if k == len(ids) - 1 else int(round(starts[ids[k + 1]] * FPS))
        shots.append(dict(id=sid, f0=f0, f1=f1))
    tl = dict(doc="Ep 1 cartoon timeline (reel time = cartoon audio time). Lines 1-14 are in dialogue_cartoon.wav; line 15 is "
                  "the question-card line (L15_card.wav). Gaps between lines capped; no speed changes.",
              fps=FPS, duration_s=round(dur, 3), total_frames=int(round(dur * FPS)), gap_cap=gap, lead=lead,
              take="cd66de56-ff8e-4c87-b849-4e16d0d4558c", shots=shots, lines=lines)
    tl_path.write_text(json.dumps(tl, indent=1))
    print(f"cartoon {dur:.2f} s = {tl['total_frames']} frames")
    for s in shots:
        print(s["id"], s["f0"], s["f1"], f"{(s['f1'] - s['f0']) / FPS:.2f} s")


def wav_write(p, y):
    with wave.open(str(p), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    main()
