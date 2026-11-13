"""Machine transcription of every shop-sound moment in the CUT -> audio_review.md rows (faster_whisper, medium.en, CPU int8).

    python projects/smart-450-hellkitten/tools/audio_review.py

For each IRL shot that carries shop sound, the span of the shop-sound STEM (what is in the cut, at the cut's level) is normalised
to -3 dBFS peak and transcribed with word timestamps (so quiet speech is not missed), and the SOURCE clip is transcribed over the
span +-2 s for context (words cut in half at the shot edges show up there). Output: JSON of rows for the markdown writer.
Flags (profanity / slur / price) come from a keyword scan of both transcripts plus a manual check list; machine output only.
"""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SHOTS, DB, SM, FPS

SR = 16000
OUT = Path(SM) / "out"
model = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=2)


def load(path, ss, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ss:.4f}", "-t", f"{dur:.4f}", "-i", str(path), "-map", "0:a:0", "-f", "f32le",
                          "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def tr(x):
    segs, _ = model.transcribe(x, language="en", word_timestamps=True, vad_filter=False, condition_on_previous_text=False,
                               beam_size=5, temperature=0.0)
    words = []
    for s in segs:
        for w in s.words or []:
            words.append(dict(w=w.word.strip(), t0=round(w.start, 2), t1=round(w.end, 2), p=round(w.probability, 2),
                              nsp=round(s.no_speech_prob, 2)))
    return words


def main():
    rows = []
    for s in SHOTS:
        if s["kind"] != "irl" or not s.get("audio"):
            continue
        dur = s["n"] / FPS
        t_tl = s["start"] / FPS
        # stem span as in the cut
        stem = OUT / "stem_shopsound.wav"
        x = load(stem, t_tl, dur)
        pk = float(np.abs(x).max()) or 1e-6
        xs = x / pk * 0.7
        w_stem = tr(xs)
        # source context
        c0 = max(0.0, s["ss"] - 2.0)
        xc = load(f"{DB}/{s['src']}.mov", c0, dur + 4.0 + (s["ss"] - c0 - 2.0))
        w_ctx = tr(xc)
        a, b = s["ss"] - c0, s["ss"] - c0 + dur
        ctx = [w for w in w_ctx if w["t1"] > a and w["t0"] < b]
        rows.append(dict(shot=s["id"], timeline_s=[round(t_tl, 3), round(t_tl + dur, 3)], src=s["src"], src_s=[round(s["ss"], 3), round(s["ss"] + dur, 3)],
                         mode=s["audio"], stem_words=w_stem, src_words_in_span=ctx,
                         src_context=" ".join(w["w"] for w in w_ctx), stem_peak_dbfs=round(20 * np.log10(pk), 1)))
        print(s["id"], "|", " ".join(w["w"] for w in w_stem), "|| ctx:", " ".join(w["w"] for w in ctx), flush=True)
    (OUT / "audio_review_raw.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
