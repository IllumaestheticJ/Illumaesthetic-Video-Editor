"""Split the ElevenLabs Part A dialogue (one file, 14 lines in script order) into per-line takes for partA_timeline.py.

Lines are found by aligning the faster-whisper word list to the script's word counts; each cut sits in the middle of the
quietest 50 ms stretch between one line's last word and the next line's first word (energy, 10 ms hops), so no audio is lost
and nothing is time-stretched. Writes <out>/L01e.wav ... L13e.wav and L10Be.wav (48 kHz mono) + split.json.

Usage: python el_split.py FULL_AUDIO WORDS_JSON OUT_DIR
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

ORDER = [("L01e", 8), ("L02e", 7), ("L03e", 4), ("L04e", 4), ("L05e", 2), ("L06e", 4), ("L07e", 6), ("L08e", 4), ("L09e", 1),
         ("L10e", 6), ("L10Be", 7), ("L11e", 6), ("L12e", 7), ("L13e", 2)]
SR = 48000


def main():
    src, wj, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
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
    meta = []
    for k, (name, ws) in enumerate(groups):
        a, b = cuts[k], cuts[k + 1]
        seg = x[int(a * SR):int(b * SR)]
        with wave.open(str(out / f"{name}.wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(seg, -1, 1) * 32767).astype(np.int16).tobytes())
        meta.append(dict(take=name, src_t0=round(a, 3), src_t1=round(b, 3), text=" ".join(w["w"] for w in ws)))
        print(name, round(a, 2), round(b, 2), meta[-1]["text"])
    (out / "split.json").write_text(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
