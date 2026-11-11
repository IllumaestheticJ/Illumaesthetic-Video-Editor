"""Measure every cut of an assembled reel against the broadband kick onset in its own decoded audio.
  cutcheck.py out.mp4 [--thresh 18]
Cuts: frames whose mean abs luma diff to the previous frame exceeds --thresh (64x114 grey).
Onset: 1 ms RMS envelope of the full-band signal; within +-120 ms of the cut, the strongest rise
(peak over the next 25 ms vs baseline of the previous 20 ms); onset = first sample where the envelope
crosses half-way between baseline and that peak (half-rise). A low-passed envelope reads 40-70 ms late,
so this stays broadband (relayed user rule, 2026-11-11)."""
import subprocess, sys
import numpy as np

def frames(path):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", "scale=64:114,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(p, np.uint8).reshape(-1, 114, 64).astype(np.float32)

def audio(path, sr=48000):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(sr),
                        "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(p, np.float32), sr

def main():
    path = sys.argv[1]
    th = float(sys.argv[sys.argv.index("--thresh") + 1]) if "--thresh" in sys.argv else 18.0
    fps = 30.0
    F = frames(path)
    d = np.abs(np.diff(F, axis=0)).mean((1, 2))
    cuts = [i + 1 for i in np.where(d > th)[0]]
    x, sr = audio(path)
    w = sr // 1000
    env = np.sqrt(np.convolve(x * x, np.ones(w) / w, "same"))
    ms = lambda t: int(t * sr)
    print(f"{len(F)} frames = {len(F)/fps:.3f} s; audio {len(x)/sr:.3f} s")
    print("cut_frame  cut_s    onset_s  offset_ms (cut - onset; + = cut late)")
    offs = []
    for c in cuts:
        t = c / fps
        best, bt, bb, bp = -1, None, 0, 0
        for s in range(ms(t - 0.12), ms(t + 0.12), sr // 2000):  # 0.5 ms steps
            if s < ms(0.02): continue
            base = np.median(env[s - ms(0.02):s]); pk = env[s:s + ms(0.025)].max()
            if pk - base > best: best, bt, bb, bp = pk - base, s, base, pk
        half = bb + 0.5 * (bp - bb)
        i = bt + int(np.argmax(env[bt:bt + ms(0.025)] >= half))
        on = i / sr; off = (t - on) * 1000; offs.append(off)
        print(f"{c:9d}  {t:7.3f}  {on:7.3f}  {off:+7.1f}")
    if offs:
        print(f"mean {np.mean(offs):+.1f} ms, max |off| {np.max(np.abs(offs)):.1f} ms (half frame = 16.7 ms)")

if __name__ == "__main__":
    main()
