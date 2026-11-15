"""Measure every voice take: speech start/end (energy, 10 ms frames, -38 dB under the take's peak, gaps < 250 ms bridged)
and word times (faster-whisper medium.en, word_timestamps=True). Audio is decoded to a numpy array with ffmpeg (av.open in this
faster-whisper build fails on files). Word error rate against the script line (lower-case, punctuation stripped).

Usage: python voice_measure.py TAKES_DIR OUT_JSON
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

SCRIPT = {  # script A, revised ending (script.md); 12 as the coordinator's brief words it
    1: "So... how do you scan a whole car?", 2: "The usual way? Dots. Lots of dots.",
    3: "One every few inches.", 4: "Then you scan it?", 5: "In pieces.",
    6: "Front. Side. Roof. Back.", 7: "Then I line them all up.", 8: "Is it done yet?", 9: "No.",
    10: "Now we peel the dots off.", 11: "Wait. I saw an Illumaesthetic video...", 14: "There has to be a better way.",
    12: "They did a whole car way faster!", 13: "...Show me."}


def norm(t):
    return re.sub(r"[^a-z ]", "", t.lower().replace("-", " ")).split()


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = [[i + j if i * j == 0 else 0 for j in range(len(h) + 1)] for i in range(len(r) + 1)]
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1][-1] / max(1, len(r))


def decode(path, sr):
    pcm = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"])
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0


def speech_span(x, sr, db=-38.0, bridge=0.25):
    hop = sr // 100
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    lv = 20 * np.log10(rms / rms.max())
    on = np.nonzero(lv > db)[0]
    if not len(on):
        return None
    # keep the longest run after bridging short gaps (drops isolated clicks/breaths at the edges)
    runs, s, p = [], on[0], on[0]
    for k in on[1:]:
        if k - p > bridge * 100:
            runs.append((s, p))
            s = k
        p = k
    runs.append((s, p))
    tot = sum(b - a for a, b in runs)
    keep = [r for r in runs if (r[1] - r[0]) > 0.04 * 100 or tot < 10]
    return round(keep[0][0] / 100, 3), round((keep[-1][1] + 1) / 100, 3)


def main():
    takes, out = Path(sys.argv[1]), Path(sys.argv[2])
    from faster_whisper import WhisperModel
    m = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=4)
    only = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    res = json.loads(out.read_text()) if (only and out.exists()) else {}
    for f in sorted(takes.glob("L*.wav")):
        if only and f.stem not in only:
            continue
        line = 14 if f.stem.startswith("L10B") else int(f.stem[1:3])   # L10B* = PIP "There has to be a better way." (v2)
        x48 = decode(f, 48000)
        x16 = decode(f, 16000)
        span = speech_span(x48, 48000)
        segs, _ = m.transcribe(x16, language="en", beam_size=5, word_timestamps=True)
        words = [dict(w=w.word.strip(), t0=round(w.start, 3), t1=round(w.end, 3), p=round(w.probability, 2))
                 for s in segs for w in s.words]
        text = " ".join(w["w"] for w in words)
        res[f.name] = dict(line=line, script=SCRIPT[line], dur=round(len(x48) / 48000, 3), speech=span, heard=text,
                           wer=round(wer(SCRIPT[line], text), 3), words=words)
        print(f.name, res[f.name]["dur"], span, round(wer(SCRIPT[line], text), 2), "|", text, flush=True)
    out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
