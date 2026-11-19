"""Assemble the mod-shop reel: composited menu (shop.mp4) + EPSILON+ card, 9:16, with the capture's own sound.

    python projects/gta6-customs/tools/assemble.py [out.mp4]

Picture: the game's menu uses the full 16:9 width (list at the far left, stats at the far right), so the frame
is not cropped: it is scaled to the reel's width and set on a blurred, darkened copy of itself.
Sound: the capture's audio for exactly the frames shown, segment by segment (room tone and the menu's ticks;
there is no music or speech in it, so cuts between segments fall in room tone, 8 ms crossfades). Where the
picture jumps over something the capture did with a tick (the option change to the wing, the change of
screen to Full Kits), that tick is laid in from another place in the capture (TICKS). One fixed gain.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np, cv2

W = Path("/home/user/media/work/gta6-customs")
LOGO = Path("/home/user/Epsilon-Site/showroom/brand/eps-showroom-wordmark-white.png")
CARD_S = 2.5
TICKS = {"wing_on": (618, 624), "whip_out": (1158, 1164), "full_kit": (274, 281)}       # segment -> capture frames holding a menu tick to lay at its start
PEAK = 0.5                                                     # fixed gain brings the loudest tick to this
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/gta6-customs_v1.mp4")


def audio():
    w = wave.open(str(W / "a.wav")); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32768
    meta = json.load(open(W / "shop_segments.json")); fps = meta["fps"]
    n = round((meta["frames"] / fps + CARD_S) * sr); y = np.zeros((n, 2), np.float32); xf = int(0.008 * sr)

    def lay(t, f0, f1, gain=1.0):
        src = x[round(f0 / 60 * sr):round(f1 / 60 * sr)].copy() * gain
        i0 = max(0, round(t * sr)); src = src[:max(0, n - i0)]
        r = np.linspace(0, 1, min(xf, len(src)))[:, None]; src[:len(r)] *= r; src[-len(r):] *= r[::-1]
        y[i0:i0 + len(src)] += src

    for s in meta["segments"]:
        t = s["out_start"] / fps
        lay(t - 0.004, s["src"][0], s["src"][0] + s["frames"] * 2 + 0.5)
        if s["name"] in TICKS:
            lay(t - 0.01, *TICKS[s["name"]])
    t_end = meta["frames"] / fps                                    # room tone carries on under the card and fades
    lay(t_end - 0.004, 100, 100 + CARD_S * 60)
    y *= PEAK / np.abs(y).max()
    fo = int(1.2 * sr); y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    fi = int(0.05 * sr); y[:fi] *= np.linspace(0, 1, fi)[:, None]
    out = W / "reel_audio.wav"
    ww = wave.open(str(out), "w"); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(sr)
    ww.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); ww.close()
    return out, n / sr


def card():
    logo = cv2.imread(str(LOGO), cv2.IMREAD_UNCHANGED).astype(np.float32)
    wl = 800; hl = round(logo.shape[0] * wl / logo.shape[1]); logo = cv2.resize(logo, (wl, hl), interpolation=cv2.INTER_AREA)
    im = np.zeros((1920, 1080, 3), np.float32); y0, x0 = 920 - hl // 2, (1080 - wl) // 2
    im[y0:y0 + hl, x0:x0 + wl] = logo[..., :3] * (logo[..., 3:] / 255)
    out = W / "end_card.png"; cv2.imwrite(str(out), im.astype(np.uint8)); return out


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wav, dur = audio(); png = card()
    fc = ("[0:v]fps=30,split[a][b];[a]scale=1080:608:flags=lanczos[fg];"
          "[b]scale=-2:1920,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.20:saturation=0.9[bg];"
          "[bg][fg]overlay=0:656,format=yuv420p,setsar=1[reel];"
          "[2:v]fps=30,format=yuv420p,setsar=1,fade=t=in:st=0:d=0.25[card];[reel][card]concat=n=2:v=1[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "shop.mp4"), "-i", str(wav), "-loop", "1", "-t", str(CARD_S), "-i", str(png),
                    "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(OUT)], check=True)
    print(OUT, "seconds", round(dur, 2))


if __name__ == "__main__":
    main()
