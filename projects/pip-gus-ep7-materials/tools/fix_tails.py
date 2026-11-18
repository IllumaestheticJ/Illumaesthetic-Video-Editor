"""Ep 8 owner note 'bumper? gets cut off': split_take.py ended L09 (and L04) at the whisper word end + 0.12 s, but the voice
rings on past it (take energy -10 dB at 23.46 s, silent only from ~23.74 s). Re-lay those two lines from take 1 with their full
tails, in place: each line's start is found in the dialogue stem by cross-correlation, the longer clip overwrites it there (8 ms
fade in, 40 ms fade out). Nothing else moves: both tails end well before the next line, so the picture timing is unchanged.

    python projects/pip-gus-ep7-materials/tools/fix_tails.py
"""
import json, subprocess
from pathlib import Path
import numpy as np

V = Path("/home/user/media/pip-gus-ep7-materials/voice")
SR = 48000
NEW_END = {"L04": 9.40, "L09": 23.78}   # take seconds: first 40 ms window below -45 dB after the word (measured)


def dec(p, ch):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()


take = dec(V / "ep8_dialogue_take1.mp3", 1)[:, 0]
dia = dec(V / "ep8_dialogue.wav", 2)
src = V / "ep8_dialogue_pre_tailfix.wav"
if not src.exists():
    subprocess.run(["cp", str(V / "ep8_dialogue.wav"), str(src)], check=True)
else:
    dia = dec(src, 2)
split = json.loads((V / "split_opt3" / "split.json").read_text())
mono = dia.mean(1)
rep = {}
for ln, t1 in NEW_END.items():
    s = split[ln]
    a0, a1 = int(s["take_t0"] * SR), int(s["take_t1"] * SR)
    probe = take[a0:a0 + int(0.4 * SR)]
    # search near the stem position
    c0 = max(0, int((s["stem_t0"] - 1.0) * SR)); c1 = int((s["stem_t0"] + 3.0) * SR)
    seg = mono[c0:c1]
    corr = np.correlate(seg, probe, "valid")
    pos = c0 + int(np.argmax(corr))
    clip = take[a0:int(t1 * SR)].copy()
    fi, fo = int(0.008 * SR), int(0.04 * SR)
    clip[:fi] *= np.linspace(0, 1, fi); clip[-fo:] *= np.linspace(1, 0, fo)
    old_len = a1 - a0
    print(ln, "found at", round(pos / SR, 3), "corr", float(corr.max() / (np.linalg.norm(probe) ** 2 + 1e-9)))
    after = mono[pos + old_len + int(0.02 * SR): pos + len(clip) + int(0.05 * SR)]
    assert np.abs(after).max() < 0.01, (ln, "next line too close", float(np.abs(after).max()))
    gain = np.sqrt((mono[pos:pos + old_len] ** 2).mean() / max(1e-12, (take[a0:a1] ** 2).mean()))
    dia[pos:pos + old_len] = 0
    dia[pos:pos + len(clip)] = (clip * gain)[:, None]
    rep[ln] = dict(stem_s=round(pos / SR, 3), old_s=round(old_len / SR, 3), new_s=round(len(clip) / SR, 3), gain=round(float(gain), 4))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", "-c:a", "pcm_s24le", str(V / "ep8_dialogue.wav")],
               input=dia.astype(np.float32).tobytes(), check=True)
print(json.dumps(rep, indent=1))
