"""Assemble the mod-shop reel: composited menu (shop.mp4) + EPSILON+ card, 9:16, with the capture's own sound.

    python projects/gta6-customs/tools/assemble.py [out.mp4]

Picture: the game's menu uses the full 16:9 width (list at the far left, stats at the far right), so the frame
is not cropped: it is scaled to the reel's width and set on a blurred, darkened copy of itself.
Sound: the capture's audio for exactly the frames shown, segment by segment (room tone and the menu's ticks;
there is no music or speech in it, so cuts between segments fall in room tone, 8 ms crossfades). On top, the
game's own sounds for what the reel does (SFX): the purchase sound from the second capture at each install
(user: "confirmation sound effect", "include the audio and sounds" of the second video), and the first
capture's row, option and back ticks where the rebuilt menu moves. One fixed gain.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np, cv2

W = Path("/home/user/media/work/gta6-customs")
LOGO = Path("/home/user/Epsilon-Site/showroom/brand/eps-showroom-wordmark-white.png")
CARD_S = 2.5
B_WAV = W / "b.wav"                                            # second capture (has the game's purchase sound)
SFX = {                                                        # name -> (capture wav, start s, end s)
    "purchase": ("b", 213.80, 215.45),                         # the kit purchase at 3:33 of the second capture
    "row": ("a", 1276 / 60, 1281 / 60),                        # cursor moves one row (first capture, frame 1277)
    "option": ("a", 618 / 60, 624 / 60),                       # option changes on a part's screen
    "back": ("a", 1158 / 60, 1164 / 60),                       # back out of a part's screen
}
PEAK = 0.5                                                     # fixed gain brings the loudest sample to this
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/gta6-customs_v2.mp4")


def read(p):
    w = wave.open(str(p)); sr = w.getframerate()
    return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32768, sr


def audio():
    xa, sr = read(W / "a.wav"); xb, srb = read(B_WAV); assert sr == srb
    meta = json.load(open(W / "shop_segments.json")); fps = meta["fps"]
    n = round((meta["frames"] / fps + CARD_S) * sr); y = np.zeros((n, 2), np.float32)

    def lay(t, src, fade=0.008):
        src = src.copy(); xf = int(fade * sr)
        i0 = max(0, round(t * sr)); src = src[:max(0, n - i0)]
        r = np.linspace(0, 1, min(xf, len(src)))[:, None]; src[:len(r)] *= r; src[-len(r):] *= r[::-1]
        y[i0:i0 + len(src)] += src

    cut = lambda x, t0, t1: x[round(t0 * sr):round(t1 * sr)]
    for s in meta["segments"]:                                      # room tone (and the capture's own ticks) for the frames shown
        f0 = s["audio_from"]
        lay(s["out_start"] / fps - 0.004, cut(xa, f0 / 60, (f0 + s["frames"] * 2 + 0.5) / 60))
    for g, name in meta["events"]:
        which, t0, t1 = SFX[name]
        lay(g / fps - (0.0 if name == "purchase" else 0.01), cut(xa if which == "a" else xb, t0, t1), fade=0.03 if name == "purchase" else 0.004)
    lay(meta["frames"] / fps - 0.004, cut(xa, 100 / 60, 100 / 60 + CARD_S))        # room tone under the card, fading
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
