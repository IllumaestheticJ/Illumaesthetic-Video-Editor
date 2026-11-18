"""Split the approved Ep 5 ElevenLabs dialogue take (one file) into per-line WAVs at natural pace.

Each cut sits in the quietest 50 ms between one line's last word and the next line's first word (10 ms RMS hops), so no
audio is lost and nothing is time-stretched (same method as scan-tedium-explainer-reel/tools/el_split.py).
Word times come from faster-whisper on the full file; the brand word is captioned "Illumaesthetic" whatever Whisper hears,
and "nerves"/"nerbs" is captioned "NURBS".

Usage: python split_voice.py FULL_AUDIO WORDS_JSON OUT_DIR MEASURED_JSON
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

SR = 48000
# (take name, speaker, whisper word count, caption text) in script order (script v6, take 3 job f00302ca)
LINES = [
    ("L01", "PIP", 4, "Wait... what's a mesh?"),
    ("L02", "GUS", 6, "A scan is millions of points."),
    ("L03", "GUS", 11, "Join them up into tiny triangles. That's a mesh. An STL."),
    ("L04", "GUS", 6, "Perfect for printing. Terrible to edit."),
    ("L05", "PIP", 2, "And STEP?"),
    ("L06", "GUS", 6, "STEP is NURBS. Not points... equations."),
    ("L07", "GUS", 10, "Smooth at any zoom. Change a hole... it just updates."),
    ("L08", "PIP", 3, "So which one?"),
    ("L09", "GUS", 7, "Just printing it? The STL's fine."),
    ("L10", "GUS", 10, "Making it on a machine? It has to be STEP."),
    ("L11", "PIP", 7, "And turning a scan into a STEP?"),
    ("L12", "GUS", 6, "You rebuild it. Surface by surface."),
    ("L13", "PIP", 4, "Is it done yet?"),
    ("L14", "GUS", 1, "...No."),
    ("L15", "PIP", 4, "Illumaesthetic does that. Look!"),
    ("L16", "PIP", 4, "Design's done. Hit print!"),
    ("L17", "GUS", 5, "It's bigger than the printer."),
]
FIX = {"nerves": "NURBS", "nerbs": "NURBS", "step": "STEP", "stl": "STL"}


def caption_word(w):
    core = w.strip(".,?!").lower()
    if core.startswith(("illum", "ilum", "alum")):
        return "Illumaesthetic" + w[len(w.rstrip(".,?!")):]
    if core in FIX:
        return FIX[core] + w[len(w.rstrip(".,?!")):]
    return w


def main():
    src, wj, out, meas_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    out.mkdir(parents=True, exist_ok=True)
    words = json.loads(wj.read_text())
    assert len(words) == sum(n for _, _, n, _ in LINES), (len(words), sum(n for _, _, n, _ in LINES))
    pcm = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    hop = SR // 100
    nfr = len(x) // hop
    rms = np.sqrt((x[: nfr * hop].reshape(nfr, hop) ** 2).mean(1) + 1e-12)
    groups, i = [], 0
    for name, spk, n, text in LINES:
        groups.append((name, spk, text, words[i:i + n]))
        i += n
    cuts = [0.0]
    for a, b in zip(groups, groups[1:]):
        # Whisper can place a line's first word too early (L10 "Making" at 27.96 s; real onset 28.6 s), so search up to
        # the next line's SECOND word and take the quietest stretch (longest true pause) in that window.
        nxt = b[3][1] if len(b[3]) > 1 else b[3][0]
        lo, hi = int(a[3][-1]["t0"] * 100) + 5, int(nxt["t0"] * 100) + 2
        win = np.convolve(rms[lo:hi], np.ones(5) / 5, mode="same")
        cuts.append((lo + int(np.argmin(win))) / 100)
    cuts.append(len(x) / SR)
    meas = {}
    for k, (name, spk, text, ws) in enumerate(groups):
        a, b = cuts[k], cuts[k + 1]
        seg = x[int(a * SR):int(b * SR)]
        with wave.open(str(out / f"{name}.wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(seg, -1, 1) * 32767).astype(np.int16).tobytes())
        wl = [dict(w=caption_word(w["w"]), t0=round(max(0.0, w["t0"] - a), 3), t1=round(w["t1"] - a, 3)) for w in ws]
        meas[f"{name}.wav"] = dict(speaker=spk, script=text, dur=round(b - a, 3), heard=" ".join(w["w"] for w in ws),
                                   words=wl, src=src, src_span=[round(a, 3), round(b, 3)])
        print(f"{name} {spk} {a:6.2f}-{b:6.2f} ({b - a:4.2f}s) {text}")
    meas_path.write_text(json.dumps(meas, indent=1))


if __name__ == "__main__":
    main()
