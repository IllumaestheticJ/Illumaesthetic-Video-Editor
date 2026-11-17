"""Split the Ep 8 dialogue take into per-line wavs (no time-stretch) and build a trimmed stem.

Line spans come from the whisper transcript (start of first word, end of last word per script line). Each cut sits in the
quietest 50 ms stretch (10 ms hops) of the gap between two lines, so breaths/sighs stay with their line.
Usage: python split_take.py TAKE.mp3 OUT_DIR [--drop 11,12,13] [--gap 0.35]
Writes OUT_DIR/L01.wav..., split.json (per-line span in the take + position in the stem) and stem.wav (kept lines,
inter-line silence = --gap, trailing VO line kept separate as VO.wav for the logo card).
"""
import json, subprocess, sys
import numpy as np

SR = 48000
# script lines (v4) -> (start, end) of speech in take 1 (job 266e47f8), from whisper word times
SPANS = {"L01": (0.00, 2.36), "L02": (2.76, 4.46), "L03": (4.92, 7.70), "L04": (8.22, 9.04), "L05": (9.82, 12.74),
         "L06": (13.10, 17.22), "L07": (17.76, 19.06), "L08": (19.62, 22.14), "L09": (22.62, 23.34), "L10": (24.08, 27.68),
         "L11": (28.26, 31.86), "L12": (32.58, 34.50), "L13": (35.22, 39.44), "L14": (39.92, 45.56), "L15": (46.24, 46.86),
         "L16": (47.36, 48.96), "VO": (49.56, 53.14)}


def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


take, out = sys.argv[1], sys.argv[2]
drop = {f"L{int(x):02d}" for x in arg("--drop", "").split(",") if x}
gap = float(arg("--gap", "0.35"))
subprocess.run(["mkdir", "-p", out], check=True)
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", take, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(pcm, np.float32)
names = list(SPANS)
cuts = [0]
for n0, n1 in zip(names, names[1:]):
    g0, g1 = int(SPANS[n0][1] * SR), int(SPANS[n1][0] * SR)
    w, h = int(0.05 * SR), int(0.01 * SR)
    best = min(range(g0, max(g0 + 1, g1 - w), h), key=lambda i: float(np.mean(a[i:i + w] ** 2)))
    cuts.append(best + w // 2)
cuts.append(len(a))


def write(path, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", path],
                   input=x.astype(np.float32).tobytes(), check=True)


info, stem, t = {}, [], 0.0
for i, n in enumerate(names):
    seg = a[cuts[i]:cuts[i + 1]]
    # trim silence around the line to the speech span +-0.12 s (keeps breaths/sighs just outside words)
    s0 = max(cuts[i], int((SPANS[n][0] - 0.12) * SR)); s1 = min(cuts[i + 1], int((SPANS[n][1] + 0.12) * SR))
    seg = a[s0:s1]
    fade = int(0.008 * SR); seg = seg.copy(); seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    write(f"{out}/{n}.wav", seg)
    info[n] = {"take_t0": s0 / SR, "take_t1": s1 / SR, "dur": len(seg) / SR, "dropped": n in drop}
    if n in drop or n == "VO":
        continue
    if stem:
        stem.append(np.zeros(int(gap * SR), np.float32)); t += gap
    info[n]["stem_t0"] = t; stem.append(seg); t += len(seg) / SR
write(f"{out}/stem.wav", np.concatenate(stem))
write(f"{out}/VO.wav", a[int((SPANS['VO'][0] - 0.12) * SR):int((SPANS['VO'][1] + 0.3) * SR)])
info["_stem_dur"] = t
json.dump(info, open(f"{out}/split.json", "w"), indent=1)
print(json.dumps({k: (round(v["stem_t0"], 2) if isinstance(v, dict) and "stem_t0" in v else v) for k, v in info.items()}))
