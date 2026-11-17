"""Ep 1 timeline: word times of the approved voice take 2 (job fe0cc2e8, 47.05 s) -> 14 script lines -> shots E01-E14.

The take is used whole, at natural pace (no splitting, no speed-up); it starts at reel time LEAD. Shot cuts sit between lines
(mid-gap). Writes projects/pip-gus-ep1-whole-bumper/ep1_timeline.json in the format partA_anim.py reads.
Usage: python ep1_timeline.py TAKE.mp3
"""
import json, subprocess, sys, wave, os
import numpy as np
from faster_whisper import WhisperModel

FPS, LEAD = 30, 0.2
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
LINES = [("PIP", "Can I 3D print whatever bumper I want?"), ("GUS", "Sure. Scan the car. Design it."),
         ("GUS", "Six or seven kilos of filament. The good stuff's about two hundred bucks."),
         ("GUS", "A print fails overnight. Again."), ("GUS", "Then glue. Filler. Sanding. Primer."), ("PIP", "Is it done yet?"),
         ("GUS", "...No. That's easily two hundred fifty hours of work."), ("GUS", "And it's still heavier. And weaker."),
         ("PIP", "...So I should just buy one?"),
         ("GUS", "If you can buy it? Yep. Printing a rep doesn't make financial sense... unless it's discontinued, or you're making them to sell."),
         ("PIP", "But I want a custom one!"), ("GUS", "...If you insist. We'll show you how."), ("PIP", "Where do we start?"),
         ("GUS", "We scan the car.")]
# whisper writes "200"/"250" as one token; script word counts in whisper tokens:
COUNTS = [8, 6, 12, 5, 5, 4, 7, 6, 6, 22, 6, 7, 4, 4]

src = sys.argv[1]
wav = os.path.join(os.path.dirname(src), "_tl16k.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", wav], check=True)
w = wave.open(wav)
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
dur = len(a) / 16000
words = []
for s in WhisperModel("small.en", compute_type="int8").transcribe(a, word_timestamps=True)[0]:
    words += [dict(w=x.word.strip(), t0=round(x.start + LEAD, 3), t1=round(x.end + LEAD, 3)) for x in s.words]
assert len(words) == sum(COUNTS), (len(words), sum(COUNTS), [x["w"] for x in words])
lines, i = [], 0
for n, ((spk, text), c) in enumerate(zip(LINES, COUNTS), 1):
    ws = words[i:i + c]; i += c
    lines.append(dict(n=n, speaker=spk, shot=f"E{n:02d}", text=text, heard=" ".join(x["w"] for x in ws), words=ws,
                      t0=ws[0]["t0"], t1=ws[-1]["t1"], sighs=[]))
end = round((LEAD + dur + 0.25) * FPS)
cuts = [0]
for A, B in zip(lines, lines[1:]):
    cuts.append(round((A["t1"] + B["t0"]) / 2 * FPS))
cuts.append(end)
shots = [dict(id=f"E{k:02d}", f0=cuts[k - 1], f1=cuts[k]) for k in range(1, 15)]
tl = dict(doc="Ep 1 cartoon timeline. Voice take 2 (fe0cc2e8) whole, starting at LEAD s; word times from faster-whisper small.en on "
              "the full take. Shot k = line k; cuts mid-gap between lines.",
          fps=FPS, lead=LEAD, total_frames=end, duration_s=round(end / FPS, 3), screen_full_frame=None, shots=shots, lines=lines,
          dialogue=dict(file=os.path.basename(src)))
json.dump(tl, open(os.path.join(PROJ, "ep1_timeline.json"), "w"), indent=1)
for s, L in zip(shots, lines):
    print(s["id"], s["f0"], s["f1"], f'{(s["f1"]-s["f0"])/FPS:.2f}s', L["speaker"], L["heard"])
print("total", end, "frames", end / FPS)
