"""Generate cartoon voice tests with piper + ffmpeg rubberband, then transcribe with faster-whisper.

Usage: VOICE_SCRATCH=<dir> python voicetest.py [--transcribe-only]. Voices: kristin/john (public domain), joe (CC0).
"""
import json, os, re, subprocess, sys
from pathlib import Path

# Media never goes in the repo: voices/ (piper .onnx + MODEL_CARD) and voice_tests/ live under VOICE_SCRATCH.
S = Path(os.environ.get("VOICE_SCRATCH", "/tmp/claude-0/-home-user-Illumaesthetic-Video-Editor/82ade9fc-974d-5f22-af68-15eda8fddd9b/scratchpad"))
VOX = S / "voices"
OUT = S / "voice_tests"
OUT.mkdir(exist_ok=True)

LINES = {
    "A1": "So... how do you scan a whole car?",
    "A2": "The usual way? Dots. Lots of dots.",
    "B1": "Scan my car! Quick!",
    "B2": "Quick? Ha. Get the stickers.",
}
# name: (piper model, length_scale, rubberband pitch ratio, rubberband tempo, extra filter)
VOICES = {
    "squeaky": ("en_US-kristin-medium", 0.95, 1.41, 1.08, "highpass=f=180"),   # +6 st, formants shifted
    "dopey":   ("en_US-john-medium", 1.1, 0.79, 0.95, "lowpass=f=5000"),       # -4 st, slower
    "goofy":   ("en_US-joe-medium", 0.95, 1.19, 1.12, "highpass=f=120"),        # +3 st, faster
}


def norm(t):
    return re.sub(r"[^a-z ]", "", t.lower().replace("-", " ")).split()


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (r[i - 1] != h[j - 1]))
    return d[len(r)][len(h)] / max(1, len(r))


def main():
    files = []
    if "--transcribe-only" in sys.argv:
        files = [(l, v, VOICES[v][0], t, OUT / f"{l}_{v}.mp3") for v in VOICES for l, t in LINES.items()]
    for vname, (model, ls, pitch, tempo, extra) in VOICES.items():
        for lid, text in LINES.items():
            if "--transcribe-only" in sys.argv:
                break
            raw = OUT / f"_{lid}_{vname}_raw.wav"
            mp3 = OUT / f"{lid}_{vname}.mp3"
            subprocess.run(["nice", "-n", "19", sys.executable, "-m", "piper", "-m", str(VOX / f"{model}.onnx"),
                            "--length-scale", str(ls), "-f", str(raw)], input=text.encode(), check=True,
                           capture_output=True)
            af = f"rubberband=pitch={pitch}:tempo={tempo}:formant=shifted,{extra},loudnorm=I=-16:TP=-1.5"
            subprocess.run(["nice", "-n", "19", "ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af", af,
                            "-ar", "44100", "-ac", "1", "-b:a", "128k", str(mp3)], check=True)
            raw.unlink()
            files.append((lid, vname, model, text, mp3))

    from faster_whisper import WhisperModel
    m = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=1)
    rows = []
    for lid, vname, model, text, mp3 in files:
        import numpy as np
        pcm = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", str(mp3), "-f", "s16le", "-ac", "1",
                                       "-ar", "16000", "-"])
        audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
        segs, _ = m.transcribe(audio, language="en", beam_size=5)
        hyp = " ".join(s.text.strip() for s in segs)
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                             "csv=p=0", str(mp3)]).decode())
        rows.append(dict(line=lid, voice=vname, model=model, text=text, heard=hyp, wer=round(wer(text, hyp), 3),
                         dur=round(dur, 2), file=str(mp3)))
        print(json.dumps(rows[-1]), flush=True)
    (OUT / "transcription_check.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
