"""Split the ElevenLabs Part A dialogue (one file, 14 lines in script order) into per-line takes for partA_timeline.py.

Lines are found by aligning the faster-whisper word list to the script's word counts; each cut sits in the middle of the
quietest 50 ms stretch between one line's last word and the next line's first word (energy, 10 ms hops), so no audio is lost
and nothing is time-stretched. Writes <out>/L01e.wav ... L13e.wav and L10Be.wav (48 kHz mono) + split.json.

Usage: python el_split.py FULL_AUDIO WORDS_JSON OUT_DIR [--suffix e] [--counts 8,7,...] [--measured JSON]

v4: --measured also writes each take's entry into the measured-takes JSON with word times taken from the FULL-file
transcription (faster-whisper pins a clip's first word to 0.0, which would swallow a sigh before the line), the brand word
merged back to "Illumaesthetic" for captions (Whisper splits/mis-hears it), and "sighs": voiced stretches >= 0.25 s outside
any word (Gus's sighs and groans), so the animation can deflate him on them.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

ORDER = [("L01e", 8), ("L02e", 7), ("L03e", 4), ("L04e", 4), ("L05e", 2), ("L06e", 4), ("L07e", 6), ("L08e", 4), ("L09e", 1),
         ("L10e", 6), ("L10Be", 7), ("L11e", 6), ("L12e", 7), ("L13e", 2)]
SR = 48000


BRAND = ("alum", "illum", "aluminum", "aesthetic", "esthetic")


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def merge_brand(ws):
    """Whisper hears the brand as 'Alumesthetic' / 'aluminum aesthetic': caption text must read 'Illumaesthetic'."""
    out, i = [], 0
    while i < len(ws):
        w = ws[i]
        lw = w["w"].lower().strip(".,?!")
        if lw.startswith(BRAND[:3]) or lw in BRAND[:3]:
            j = i
            if j + 1 < len(ws) and ws[j + 1]["w"].lower().strip(".,?!") in BRAND[3:]:
                j += 1
            out.append(dict(w="Illumaesthetic", t0=w["t0"], t1=ws[j]["t1"], p=min(x.get("p", 1) for x in ws[i:j + 1])))
            i = j + 1
            continue
        out.append(w)
        i += 1
    return out


def main():
    src, wj, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    suffix = arg("--suffix", "e")
    global ORDER
    if arg("--counts"):
        ORDER = [(nm[:-1] + suffix, int(c)) for (nm, _), c in zip(ORDER, arg("--counts").split(","))]
    else:
        ORDER = [(nm[:-1] + suffix, c) for nm, c in ORDER]
    out.mkdir(parents=True, exist_ok=True)
    words = json.loads(wj.read_text())
    assert len(words) == sum(n for _, n in ORDER), (len(words), sum(n for _, n in ORDER))
    pcm = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    hop = SR // 100
    nfr = len(x) // hop
    rms = np.sqrt((x[: nfr * hop].reshape(nfr, hop) ** 2).mean(1) + 1e-12)
    groups, i = [], 0
    for name, n in ORDER:
        groups.append((name, words[i:i + n]))
        i += n
    cuts = [0.0]
    for (_, a), (_, b) in zip(groups, groups[1:]):
        lo, hi = int(a[-1]["t0"] * 100) + 5, int(b[0]["t0"] * 100) + 2   # from inside the last word to the next word's start
        win = np.convolve(rms[lo:hi], np.ones(5) / 5, mode="same")
        cuts.append((lo + int(np.argmin(win))) / 100)
    cuts.append(len(x) / SR)
    lv = 20 * np.log10(rms / rms.max())
    meta = []
    meas_path = arg("--measured")
    meas = json.loads(Path(meas_path).read_text()) if meas_path and Path(meas_path).exists() else {}
    script = {1: "So... how do you scan a whole car?", 2: "The usual way? Dots. Lots of dots.", 3: "One every few inches.",
              4: "Then you scan it?", 5: "In pieces.", 6: "Front. Side. Roof. Back.", 7: "Then I line them all up.",
              8: "Is it done yet?", 9: "No.", 10: "Now we peel the dots off.", 14: "There has to be a better way.",
              11: "Wait. I saw an Illumaesthetic video...", 12: "They did a whole car way faster!", 13: "...Show me."}
    for k, (name, ws) in enumerate(groups):
        a, b = cuts[k], cuts[k + 1]
        if meas_path:
            line = 14 if name.startswith("L10B") else int(name[1:3])
            wl = merge_brand([dict(w=w["w"], t0=round(max(0.0, w["t0"] - a), 3), t1=round(w["t1"] - a, 3), p=w.get("p", 1)) for w in ws])
            # sighs: voiced (> -38 dB under the file peak) stretches >= 0.25 s inside this take not covered by a word (+-50 ms)
            sig, cur = [], None
            for f in range(int(a * 100), int(b * 100)):
                t = f / 100
                unc = lv[min(f, len(lv) - 1)] > -38 and not any(w["t0"] - 0.05 <= t <= w["t1"] + 0.05 for w in ws)
                if unc and cur is None:
                    cur = t
                if not unc and cur is not None:
                    if t - cur >= 0.25:
                        sig.append([round(cur - a, 3), round(t - a, 3)])
                    cur = None
            heard = " ".join(w["w"] for w in wl)
            meas[f"{name}.wav"] = dict(line=line, script=script[line], dur=round(b - a, 3), heard=heard, wer=None, words=wl,
                                       sighs=sig, src=src, src_span=[round(a, 3), round(b, 3)])
        seg = x[int(a * SR):int(b * SR)]
        with wave.open(str(out / f"{name}.wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(seg, -1, 1) * 32767).astype(np.int16).tobytes())
        meta.append(dict(take=name, src_t0=round(a, 3), src_t1=round(b, 3), text=" ".join(w["w"] for w in ws)))
        print(name, round(a, 2), round(b, 2), meta[-1]["text"])
    (out / "split.json").write_text(json.dumps(meta, indent=1))
    if meas_path:
        Path(meas_path).write_text(json.dumps(meas, indent=1))


if __name__ == "__main__":
    main()
