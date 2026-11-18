"""Ep 5 reel timeline from the approved voice take (take 3, job f00302ca), natural pace, nothing re-timed.

The cartoon keeps the take's own timing (lines sit at their source times; the gaps are the performed pauses). After L15
("Illumaesthetic does that. Look!") the real section (render_real.py, 132 frames) plays; the closing card follows with
L16/L17 as voice only. Writes ep5_timeline.json in the pilot's partA_timeline.json schema (fps, duration_s, shots, lines with
reel-time words, screen_full_frame) so the pilot's talk/blink helpers can drive the Ep 5 animation, plus the dialogue stem.

Usage: python ep5_timeline.py LINES_DIR OUT_WAV
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
FPS, SR = 30, 48000
REAL_FRAMES = 132
CARD_LEAD, CARD_GAP, CARD_TAIL = 0.35, 0.25, 0.9      # s: card -> L16, L16 -> L17, L17 -> end
# shot id -> lines it covers (cartoon), in order
SHOTS = [("E1", [1]), ("E2", [2]), ("E3", [3]), ("E4", [4]), ("E5", [5]), ("E6", [6]), ("E7", [7]), ("E8", [8]),
         ("E9", [9, 10]), ("E10", [11, 12]), ("E11", [13, 14]), ("E12", [15])]


def main():
    lines_dir, out_wav = Path(sys.argv[1]), Path(sys.argv[2])
    meas = json.loads((PROJ / "voice_takes_measured.json").read_text())
    L = {int(k[1:3]): dict(v, take=k) for k, v in meas.items()}
    lines, place = [], {}
    for n in range(1, 16):                       # cartoon lines at their source times
        place[n] = L[n]["src_span"][0]
    end15 = L[15]["src_span"][1]
    f_real0 = round(end15 * FPS)
    f_card0 = f_real0 + REAL_FRAMES
    place[16] = f_card0 / FPS + CARD_LEAD
    place[17] = place[16] + L[16]["dur"] + CARD_GAP - 0.0
    f_end = round((place[17] + L[17]["dur"] + CARD_TAIL) * FPS)
    for n in range(1, 18):
        v = L[n]; a = place[n]
        ws = [dict(w=w["w"], t0=round(a + w["t0"], 3), t1=round(a + w["t1"], 3)) for w in v["words"]]
        lines.append(dict(n=n, speaker=v["speaker"], take=v["take"], script=v["script"], start=round(a, 3),
                          t0=ws[0]["t0"], t1=ws[-1]["t1"], words=ws, sighs=[]))
    shots = []
    for sid, ns in SHOTS:
        f0 = round(place[ns[0]] * FPS)
        f1 = round((place[ns[-1]] + L[ns[-1]]["dur"]) * FPS) if ns[-1] < 15 else f_real0
        shots.append(dict(id=sid, f0=f0, f1=f1, lines=ns))
    for a, b in zip(shots, shots[1:]):           # contiguous
        b["f0"] = a["f1"]
    shots.append(dict(id="REAL", f0=f_real0, f1=f_card0, lines=[]))
    shots.append(dict(id="CARD", f0=f_card0, f1=f_end, lines=[16, 17]))
    tl = dict(fps=FPS, duration_s=round(f_end / FPS, 3), frames=f_end, shots=shots, lines=lines,
              screen_full_frame=f_real0 - 1, take="f00302ca (take 3)", real_frames=REAL_FRAMES)
    (PROJ / "ep5_timeline.json").write_text(json.dumps(tl, indent=1))
    # dialogue stem
    out = np.zeros(int(f_end / FPS * SR) + SR, np.float32)
    for ln in lines:
        w = wave.open(str(lines_dir / ln["take"]))
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        i = int(round(ln["start"] * SR)); out[i:i + len(x)] += x
    out = out[: int(f_end / FPS * SR)]
    with wave.open(str(out_wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
    for s in shots:
        print(f"{s['id']:5s} {s['f0']:5d}-{s['f1']:5d} ({(s['f1'] - s['f0']) / FPS:5.2f}s) lines {s['lines']}")
    print(f"total {f_end} frames = {f_end / FPS:.2f} s")


if __name__ == "__main__":
    main()
