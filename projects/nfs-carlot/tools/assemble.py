"""Assemble the car-lot reel: arrival (capture, untouched) + menu with the Epsilon cars, 9:16.

    python projects/nfs-carlot/tools/assemble.py [out.mp4]

Picture: the capture is 16:9 with the game's menu in a centred 4:3 box, so the frame is cropped to that
box (x 300-1842 of 2144), scaled to the reel's full width, and set on a blurred, darkened copy of itself.
Sound: the capture's own audio for exactly the frames used. Every cut in the menu sits on the first
frame of a scroll, so the game's scroll sound covers the jump in the menu music; a 12 ms crossfade
removes the click.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

W = Path("/home/user/media/work/nfs-carlot")
INTRO = (952, 1291)            # a60.mp4 frames: "enter the shop?" (1 s), then the 350Z cutscene (4.65 s)
FPS = 60
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/nfs-carlot_v1.mp4")


def audio():
    w = wave.open(str(W / "a.wav")); sr, ch = w.getframerate(), w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, ch) / 32768
    seg = json.load(open(W / "menu_segments.json"))["segments"]
    ranges = [INTRO] + [tuple(s["src"]) for s in seg]
    parts, n = [], int(0.012 * sr)
    for i, (f0, f1) in enumerate(ranges):
        a, b = round(f0 / FPS * sr), round((f1 + 1) / FPS * sr)
        p = x[a:b].copy()
        if i:                                   # crossfade from the previous range's own continuation
            pa = round((ranges[i - 1][1] + 1) / FPS * sr)
            wgt = np.linspace(0, 1, n)[:, None]
            p[:n] = p[:n] * wgt + x[pa:pa + n] * (1 - wgt)
        parts.append(p)
    y = np.concatenate(parts)
    fo = int(0.35 * sr); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    fi = int(0.05 * sr); y[:fi] *= np.linspace(0, 1, fi)[:, None]
    out = W / "reel_audio.wav"
    ww = wave.open(str(out), "w"); ww.setnchannels(ch); ww.setsampwidth(2); ww.setframerate(sr)
    ww.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); ww.close()
    return out, len(y) / sr


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wav, dur = audio()
    fc = (f"[0:v]trim=start_frame={INTRO[0]}:end_frame={INTRO[1] + 1},setpts=PTS-STARTPTS[i];"
          "[1:v]setpts=PTS-STARTPTS[m];[i][m]concat=n=2:v=1,split[a][b];"
          "[a]crop=1542:1206:300:0,scale=1080:846:flags=lanczos[fg];"
          "[b]scale=-2:1920,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.22:saturation=0.9[bg];"
          "[bg][fg]overlay=0:497,fps=30,format=yuv420p[v];"
          "[2:a]loudnorm=I=-15:TP=-1.5:LRA=11[au]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "a60.mp4"), "-i", str(W / "menu.mp4"), "-i", str(wav),
                    "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(OUT)], check=True)
    print(OUT, "audio seconds", round(dur, 2))


if __name__ == "__main__":
    main()
