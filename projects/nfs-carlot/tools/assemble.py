"""Assemble the car-lot reel: arrival (capture, untouched) + menu with the Epsilon cars, 9:16.

    python projects/nfs-carlot/tools/assemble.py [out.mp4]

Picture: the capture is 16:9 with the game's menu in a centred 4:3 box, so the frame is cropped to that
box (x 300-1842 of 2144), scaled to the reel's full width, and set on a blurred, darkened copy of itself.

Sound: the 1440p capture (a.wav) for the arrival. Its garage section is sped up 2x (user, v1 review), so
the menu uses the second capture (b.wav), which is real time: one continuous take from the menu opening
through three scrolls, then a jump to a later scroll for the last car so it can hold. The picture is cut
to that audio: every car change starts on the frame where the car starts to move in capture B
(B_SCROLLS, measured from B's picture), which keeps B's own scroll sound on it.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

W = Path("/home/user/media/work/nfs-carlot")
INTRO = (952, 1291)            # a60.mp4 frames (60 fps): "enter the shop?" (1 s), then the 350Z cutscene (4.65 s)
B_SCROLLS = [34.93, 37.87, 40.27, 42.00, 50.03]   # seconds in capture B where each of our five car changes starts
B_END = 51.86                                     # just before B's next scroll sound
LEAD = 0.08                                       # B's scroll sound starts up to this long before the car moves
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/nfs-carlot_v2.mp4")


def load(name):
    w = wave.open(str(W / name)); sr, ch = w.getframerate(), w.getnchannels()
    return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, ch) / 32768, sr


def rms_db(x):
    return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)


def audio():
    a, sr = load("a.wav"); b, _ = load("b.wav")
    meta = json.load(open(W / "menu_segments.json")); fps = meta["fps"]; seg = meta["segments"]
    intro = a[round(INTRO[0] / 60 * sr):round((INTRO[1] + 1) / 60 * sr)].copy()
    n_menu = round(meta["frames"] / fps * sr)
    menu = np.zeros((n_menu, 2), np.float32)
    # menu time of each car change = when that segment's scroll starts
    t_scroll = [(s["out_start"] + s["transition"][0] - s["src"][0]) / fps for s in seg]
    xf = int(0.02 * sr)

    def place(t_menu, b0, b1):
        i0 = round(t_menu * sr); src = b[round(b0 * sr):round(b1 * sr)].copy()
        if i0 < 0:
            src = src[-i0:]; i0 = 0
        src = src[:max(0, n_menu - i0)]
        ramp = np.linspace(0, 1, min(xf, len(src)))[:, None]
        src[:len(ramp)] *= ramp; src[-len(ramp):] *= ramp[::-1]
        menu[i0:i0 + len(src)] += src

    # take 1: menu opening through the 4th car change (continuous in B)
    place(0.0, B_SCROLLS[0] - t_scroll[0], B_SCROLLS[3] + (t_scroll[4] - t_scroll[3]) - LEAD)
    # take 2: the last car, from a later scroll in B, so it can hold until B_END
    place(t_scroll[4] - LEAD, B_SCROLLS[4] - LEAD, B_END)
    menu *= 10 ** ((rms_db(intro) - 5.0 - rms_db(menu[menu.any(1)])) / 20)       # menu sits 5 dB under the cutscene
    j = int(0.03 * sr); intro[-j:] *= np.linspace(1, 0, j)[:, None]
    y = np.concatenate([intro, menu])
    fo = int(0.4 * sr); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    fi = int(0.05 * sr); y[:fi] *= np.linspace(0, 1, fi)[:, None]
    out = W / "reel_audio.wav"
    ww = wave.open(str(out), "w"); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(sr)
    ww.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); ww.close()
    return out, len(y) / sr, [round(len(intro) / sr + t, 2) for t in t_scroll]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wav, dur, scrolls = audio()
    fc = (f"[0:v]trim=start_frame={INTRO[0]}:end_frame={INTRO[1] + 1},setpts=PTS-STARTPTS,fps=30[i];"
          "[1:v]setpts=PTS-STARTPTS,fps=30[m];[i][m]concat=n=2:v=1,split[a][b];"
          "[a]crop=1542:1206:300:0,scale=1080:846:flags=lanczos[fg];"
          "[b]scale=-2:1920,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.22:saturation=0.9[bg];"
          "[bg][fg]overlay=0:497,format=yuv420p[v];"
          "[2:a]loudnorm=I=-15:TP=-1.5:LRA=11[au]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "a60.mp4"), "-i", str(W / "menu.mp4"), "-i", str(wav),
                    "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(OUT)], check=True)
    print(OUT, "seconds", round(dur, 2), "car changes at", scrolls)


if __name__ == "__main__":
    main()
