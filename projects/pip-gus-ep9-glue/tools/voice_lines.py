"""Ep 9: word times for the approved ElevenLabs take, grouped into the 17 script lines.

faster-whisper (medium.en, word timestamps) on the whole take; words are assigned to lines by the script's word counts
(brand-free script, so no merge needed); each line gets [t0, t1] = first/last word, and the cut between two lines sits in
the quietest 50 ms between them. No audio is altered. Writes projects/pip-gus-ep9-glue/voice_lines.json.

Usage: python voice_lines.py TAKE.mp3
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

LINES = [("PIP", "Now I've got a pile of pieces. How do we stick them together?"),
         ("GUS", "Superglue. Fast. Perfect for mold masters."),
         ("PIP", "Strong enough to hang on?"),
         ("GUS", "...Not that."),
         ("GUS", "Epoxy. Fills gaps."),
         ("PIP", "Is it done yet?"),
         ("GUS", "...No."),
         ("GUS", "Need it strong? Staples."),
         ("PIP", "Staples?!"),
         ("GUS", "Hot ones. Melted in across the seam."),
         ("GUS", "Or weld it. Melt plastic into the seam."),
         ("GUS", "ASA or ABS? Acetone welds those. Only those."),
         ("PIP", "So which one's best?"),
         ("GUS", "Depends what it's for."),
         ("PIP", "Wait. Show me you guys doing it!"),
         ("PIP", "I printed the bumper I wanted."),
         ("GUS", "You insisted.")]
SR = 16000


def nwords(t):
    return len(re.sub(r"[^A-Za-z' ]", " ", t).split())


def norm(w):
    return re.sub(r"[^a-z']", "", w.lower())


def align(heard, lines):
    """Map ASR words onto the script's words (difflib on normalised tokens). Script words the ASR merged or dropped get
    times interpolated between their matched neighbours, so every script word has a time; captions use the script text."""
    import difflib
    script = [w for _, t in lines for w in re.sub(r"[^A-Za-z' ]", " ", t).split()]
    a, b = [norm(w) for w in script], [norm(h["w"]) for h in heard]
    tm = [None] * len(script)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            h = heard[blk.b + k]
            tm[blk.a + k] = (h["t0"], h["t1"])
    i = 0
    while i < len(script):
        if tm[i] is None:
            j = i
            while j < len(script) and tm[j] is None:
                j += 1
            lo = tm[i - 1][1] if i > 0 else 0.0
            hi = tm[j][0] if j < len(script) else lo + 0.4 * (j - i)
            step = (hi - lo) / (j - i)
            for k in range(i, j):
                tm[k] = (round(lo + step * (k - i), 3), round(lo + step * (k - i + 1), 3))
            print("interpolated:", script[i:j], round(lo, 2), round(hi, 2))
            i = j
        else:
            i += 1
    return [dict(w=w, t0=t[0], t1=t[1]) for w, t in zip(script, tm)]


def main():
    src = sys.argv[1]
    x = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]), np.float32)
    m = WhisperModel(sys.argv[2] if len(sys.argv) > 2 else "small.en", compute_type="int8")
    prompt = " ".join(t for _, t in LINES)
    # one pass over the whole take drifts in its second half (words collapse onto line boundaries): transcribe in chunks cut
    # at the longest pauses, ~10 s each, and offset the word times back to take time
    hop0 = SR // 100
    e = np.sqrt((x[:len(x) // hop0 * hop0].reshape(-1, hop0) ** 2).mean(1) + 1e-12)
    e = np.convolve(e, np.ones(30) / 30, mode="same")
    bounds = [0]
    while len(x) / SR - bounds[-1] / 100 > 14:
        lo, hi = bounds[-1] + 800, min(bounds[-1] + 1300, len(e) - 1)
        bounds.append(lo + int(np.argmin(e[lo:hi])))
    bounds.append(len(e))
    ws = []
    for a, b in zip(bounds, bounds[1:]):
        segs, _ = m.transcribe(x[a * hop0:b * hop0], word_timestamps=True, condition_on_previous_text=False)
        ws += [dict(w=w.word.strip(), t0=round(w.start + a / 100, 3), t1=round(w.end + a / 100, 3)) for s in segs for w in s.words]
    print("chunks (s):", [b / 100 for b in bounds])
    counts = [nwords(t) for _, t in LINES]
    ws = align(ws, LINES)
    # Interpolated words checked against voiced-energy runs (-38 dB under peak, gaps <= 0.25 s bridged) of this take:
    # "mold masters" ends at 7.69 (the run 6.24-7.69); Gus's "Staples." is the run 17.28-17.95 and Pip's "Staples?!" the
    # run 18.37-19.51 (ASR heard only one "Staples"). Pinned here; only valid for take 75013adc.
    FIX = {("mold", 2): (6.84, 7.22), ("masters", 2): (7.22, 7.69), ("Staples", 8): (17.28, 17.95), ("Staples", 9): (18.37, 19.10)}
    hop = SR // 100
    nfr = len(x) // hop
    rms = np.sqrt((x[:nfr * hop].reshape(nfr, hop) ** 2).mean(1) + 1e-12)
    out, i = [], 0
    for n, ((who, text), c) in enumerate(zip(LINES, counts), 1):
        lw = ws[i:i + c]; i += c
        for w in lw:
            if (w["w"], n) in FIX:
                w["t0"], w["t1"] = FIX[(w["w"], n)]
        out.append(dict(n=n, who=who, text=text, t0=lw[0]["t0"], t1=lw[-1]["t1"], words=lw))
    for a, b in zip(out, out[1:]):
        lo, hi = int(a["t1"] * 100), max(int(a["t1"] * 100) + 1, int(b["t0"] * 100))
        win = np.convolve(rms[lo:hi], np.ones(5) / 5, mode="same") if hi - lo > 5 else rms[lo:hi]
        a["cut_after"] = round((lo + int(np.argmin(win))) / 100, 3)
    res = dict(src=src, dur=round(len(x) / SR, 3), model="faster-whisper " + (sys.argv[2] if len(sys.argv) > 2 else "small.en"), lines=out)
    p = Path(__file__).resolve().parent.parent / "voice_lines.json"
    p.write_text(json.dumps(res, indent=1))
    for L in out:
        print(f"{L['n']:2d} {L['who']} {L['t0']:6.2f}-{L['t1']:6.2f} cut {L.get('cut_after', '-')}  {' '.join(w['w'] for w in L['words'])}")


if __name__ == "__main__":
    main()
