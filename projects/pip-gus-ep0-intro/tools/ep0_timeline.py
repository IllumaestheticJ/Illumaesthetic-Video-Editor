"""Ep 0 timeline: word times of the approved voice take (take 2) -> ep0_timeline.json (lines, words, shots, music offset).

  python3 tools/ep0_timeline.py            (needs faster-whisper; reads /home/user/media/pip-gus-ep0-intro/voice/ep0_take2_16k.wav)

Words come from faster-whisper base.en word timestamps and are assigned to the 11 script lines by word count (the script
text is authoritative, whisper only gives times). Reel time = take time + VOICE_AT.
"""
import json, re, wave, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
P = HERE.parent
VOICE = Path("/home/user/media/pip-gus-ep0-intro/voice/ep0_take2_16k.wav")
FPS = 30
VOICE_AT = 0.30          # the take starts 0.3 s into the reel
MUSIC_AT = 2.40          # music time 0 plays at reel 2.40 s: bass-entry lift (music 19.22 s) lands on line 7
BEAT0, BEAT = 0.0203, 0.6   # inquisitive_A (077bbd23): 100 BPM, 18 frames per beat

LINES = [
    ("GUS", "Hi, I'm Gus."),
    ("PIP", "And I'm Pip!"),
    ("PIP", "We are the Illumaesthetic mascots!"),
    ("GUS", "Here in the digital world to explain to you the tips and tricks we've learned along the way... from doing this for so long."),
    ("PIP", "Illumaesthetic scans whole cars in 3D..."),
    ("GUS", "...sells the scans, designs the parts, prints them... and everything in between."),
    ("PIP", "And we'll answer all the questions you keep asking us!"),
    ("GUS", "Scanning. Printing. Materials. Glue."),
    ("PIP", "And why we spray everything white!"),
    ("GUS", "...There's a lot to cover."),
    ("PIP", "What questions do you have?"),
]


def toks(s):
    return [w for w in re.split(r"\s+", re.sub(r"\.\.\.", " ", s).strip()) if re.search(r"[A-Za-z0-9]", w)]


def main():
    from faster_whisper import WhisperModel
    w = wave.open(str(VOICE))
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = WhisperModel("base.en", device="cpu", compute_type="int8").transcribe(a, word_timestamps=True)
    words = [x for s in segs for x in s.words]
    heard = [x.word.strip() for x in words]
    # whisper splits/merges differently ("Illumaesthetic" -> 1-2 tokens, "3D" ...): align by normalised letters
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    script = [(i, t) for i, (_, s) in enumerate(LINES) for t in toks(s)]
    out_words = [[] for _ in LINES]
    j = 0
    buf = ""
    for i, t in script:
        target = norm(t)
        t0 = None
        acc = ""
        while j < len(words):
            wn = norm(words[j].word)
            if t0 is None:
                t0 = words[j].start
            acc += wn
            t1 = words[j].end
            j += 1
            # accept when the heard letters cover the script word (or the heard word is a mis-hearing of similar length)
            if len(acc) >= len(target) - 2:
                break
        out_words[i].append(dict(w=t, t0=round(t0 + VOICE_AT, 3), t1=round(t1 + VOICE_AT, 3)))
    lines = []
    for n, ((spk, text), ws) in enumerate(zip(LINES, out_words), 1):
        lines.append(dict(n=n, speaker=spk, text=text, t0=ws[0]["t0"], t1=ws[-1]["t1"], words=ws))
    dur = round(len(a) / 16000 + VOICE_AT, 3)
    tl = dict(fps=FPS, voice_at=VOICE_AT, music_at=MUSIC_AT, beat0=round(MUSIC_AT + BEAT0, 4), beat=BEAT,
              voice_dur=dur, lines=lines, heard=" ".join(heard))
    json.dump(tl, open(P / "ep0_timeline.json", "w"), indent=1)
    for L in lines:
        print(f"{L['n']:2d} {L['speaker']} {L['t0']:6.2f}-{L['t1']:6.2f}  " + " ".join(f"{w['w']}@{w['t0']:.2f}" for w in L["words"]))


if __name__ == "__main__":
    main()
