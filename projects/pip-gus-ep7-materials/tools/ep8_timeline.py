"""Ep 8 timeline: per-line takes (tools/split_take.py output) -> reel times, word times, shots, dialogue track.

No time-stretch. Lines keep their own internal pauses; only the gaps between lines are set here (GAP, plus EXTRA where a gag
needs a beat: the vent needs time to droop before "It's melting!"). Word times come from the whisper transcript of the full
take (take1_words.json), mapped through each line's offset.
Writes projects/pip-gus-ep7-materials/ep8_timeline.json (drives Blender) and MEDIA/voice/ep8_dialogue.wav (cartoon lines at
reel times) + ep8_vo.wav (Pip's logo-card line).
Usage: python ep8_timeline.py
"""
import json, subprocess
from pathlib import Path
import numpy as np

PROJ = Path(__file__).resolve().parent.parent
MEDIA = Path("/home/user/media/pip-gus-ep7-materials/voice")
SPLIT = MEDIA / "split_opt3"
FPS, SR = 30, 48000
LEAD = 0.30                       # silence before line 1
GAP = 0.20                        # added between trimmed lines (each line already carries ~0.12 s air at both ends)
EXTRA = {"L04": 0.60, "L09": 0.25, "L10": 0.10, "L14": 0.25}   # extra beat BEFORE these lines
LINES = [  # n, id, speaker, text (script v4, option 3)
    (1, "L01", "PIP", "Printer's ready! What do we load in it?"),
    (2, "L02", "PIP", "This one! PLA!"),
    (3, "L03", "GUS", "Sure. Print a vent and leave it in the sun."),
    (4, "L04", "PIP", "...It's melting!"),
    (5, "L05", "GUS", "PLA's easy to print. It just hates heat."),
    (6, "L06", "GUS", "Inside the car? PETG. Tougher, handles more heat."),
    (7, "L07", "PIP", "So I'll print it in black!"),
    (8, "L08", "GUS", "...Black soaks up too much sun. Even PETG melts."),
    (9, "L09", "PIP", "And my bumper?"),
    (10, "L10", "GUS", "Outside? ASA. It's made for sun and rain."),
    (14, "L14", "GUS", "And it depends what it's for. Molds and masters? PETG. Things don't stick to it. Or ASA-GF. Warps less, nicer finish."),
    (15, "L15", "PIP", "Like these?!"),
    (16, "L16", "GUS", "...Yeah. Like those."),
]
# shot -> the lines it carries (a shot starts LEAD_IN before its first line and runs to the next shot)
SHOTS = [("A1", [1]), ("A2", [2]), ("A3", [3]), ("A4", [4]), ("A5", [5]), ("A6", [6]), ("A7", [7, 8]), ("A8", [9]),
         ("A9", [10]), ("A10", [14]), ("A11", [15]), ("A12", [16])]
LEAD_IN = 0.18
TAIL_A12 = 0.25                   # after "Like those." the push ends; screen full frame on the last A12 frame
WORDS_TAKE = json.load(open(PROJ / "voice/take1_words.json"))
SPL = json.load(open(SPLIT / "split.json"))
# Owner review v1 overrides (no re-split of take 1, nothing sped up):
#  - L04/L09: split_take ended them at whisper word end + 0.12 s, clipping the ring-out ("bumper? gets cut off"); re-cut from
#    take 1 to the first window below -45 dB. L04's extra tail sits in its following gap (ABSORB) so A1-A8 keep their timing.
#  - L10/L14: re-recorded (Gus only, one elevenlabs_v4 dialogue call, job 628b5c63): ASA said as letters, ASA-GF + PETG wording.
TAKE2 = MEDIA / "gus_asa_take2.mp3"
TAKE3 = MEDIA / "gus_black_take3.mp3"      # owner v3: black absorbs light (job d03fdb6e, 0.46 credits)
W3 = [dict(w=w["w"], s=w["t0"], e=w["t1"]) for w in json.load(open(PROJ / "voice/take3_words.json"))]
W2 = [dict(w=w["w"], s=w["t0"], e=w["t1"]) for w in json.load(open(PROJ / "voice/take2_words.json"))]
OVR = {"L04": (MEDIA / "ep8_dialogue_take1.mp3", 8.10, 9.40, WORDS_TAKE, True),
       "L09": (MEDIA / "ep8_dialogue_take1.mp3", 22.545, 23.78, WORDS_TAKE, False),
       "L08": (TAKE3, 0.10, 4.40, W3, False),     # onset 0.20 s; under -45 dB by 4.25 s
       "L10": (TAKE2, 0.10, 4.70, W2, False),     # onset 0.22 s; ring-out under -45 dB by ~4.6 s
       "L14": (TAKE2, 4.79, 14.50, W2, False)}    # onset 4.91 s; tail under -45 dB at 14.44 s
_src = {}


def clip(path, a, b):
    if path not in _src:
        _src[path] = load(path)
    x = _src[path][int(a * SR):int(b * SR)].copy()
    fi, fo = int(0.008 * SR), int(0.04 * SR)
    x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    return x


def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                        capture_output=True, check=True).stdout, np.float32)


def write(p, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(p)],
                   input=x.astype(np.float32).tobytes(), check=True)


t = LEAD
lines, clips = [], []
for n, lid, spk, text in LINES:
    if lines:
        t += GAP + EXTRA.get(lid, 0.0)
    s = SPL[lid]
    a = load(SPLIT / f"{lid}.wav")
    adv = len(a) / SR
    src_t0, src_t1, wsrc = s["take_t0"], s["take_t1"], WORDS_TAKE
    if lid in OVR:
        path, src_t0, src_t1, wsrc, absorb = OVR[lid]
        a = clip(path, src_t0, src_t1)
        adv = adv if absorb else len(a) / SR
    off = t - src_t0
    ws = [dict(w=w["w"].strip(), t0=round(w["s"] + off, 3), t1=round(w["e"] + off, 3)) for w in wsrc
          if src_t0 <= (w["s"] + w["e"]) / 2 <= src_t1]
    lines.append(dict(n=n, id=lid, speaker=spk, text=text, t0=round(ws[0]["t0"], 3), t1=round(ws[-1]["t1"], 3),
                      clip_t0=round(t, 3), words=ws))
    clips.append((t, a))
    t += adv
end_dialogue = t
# shots in frames
sf = []
starts = [round(max(0.0, min(L["t0"] for L in lines if L["n"] in ns) - LEAD_IN) * FPS) if i else 0 for i, (sid, ns) in enumerate(SHOTS)]
START_AFTER = {"A4": (3, 0.10)}   # A4 (the sun test) starts right after line 3 so the vent droops in the beat before 'It's melting!'
for i, (sid, ns) in enumerate(SHOTS):
    if sid in START_AFTER:
        ln, pad = START_AFTER[sid]
        starts[i] = round((next(L["t1"] for L in lines if L["n"] == ln) + pad) * FPS)
last_t1 = max(L["t1"] for L in lines if L["n"] == 16)
end_f = round((last_t1 + TAIL_A12) * FPS)
for i, (sid, ns) in enumerate(SHOTS):
    f1 = starts[i + 1] if i + 1 < len(SHOTS) else end_f
    sf.append(dict(id=sid, f0=starts[i], f1=f1, lines=ns))
dur = end_f / FPS
mix = np.zeros(int((dur + 1.0) * SR), np.float32)
for t0, a in clips:
    i = int(round(t0 * SR)); mix[i:i + len(a)] += a
write(MEDIA / "ep8_dialogue.wav", mix[:int(dur * SR)])
vo = load(SPLIT / "VO.wav"); write(MEDIA / "ep8_vo.wav", vo)
TL = dict(fps=FPS, duration_s=round(dur, 3), frames=end_f, screen_full_frame=end_f - 1, lines=lines, shots=sf,
          vo=dict(text="They're printed! ...Now I've got a pile of pieces.", dur=round(len(vo) / SR, 3)),
          note="Cartoon part only. Real footage (4.5 s) and the logo card (+ Pip VO) follow in the assembly.")
json.dump(TL, open(PROJ / "ep8_timeline.json", "w"), indent=1)
for s in sf:
    print(s["id"], s["f0"], s["f1"], round((s["f1"] - s["f0"]) / FPS, 2), "s")
print("cartoon", round(dur, 2), "s,", end_f, "frames; VO", round(len(vo) / SR, 2), "s")
