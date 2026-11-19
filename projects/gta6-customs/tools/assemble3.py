"""Assemble v3: shop3.mp4 + EPSILON+ card, 9:16, with the game's own sounds.

    python projects/gta6-customs/tools/assemble3.py [out.mp4]

Sound: one bed of room tone (first capture, a stretch between two menu ticks, looped with 0.3 s crossfades),
then the game's sounds at the reel's events: the purchase sound (second capture, 3:33) at every purchase, the
first capture's row tick, select press and back tick. The mechanic's line has no audio: neither capture has it
and it was not generated without asking (it would spend the user's credits); it is on screen as a subtitle.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np, cv2

W = Path("/home/user/media/work/gta6-customs")
LOGO = Path("/home/user/Epsilon-Site/showroom/brand/eps-showroom-wordmark-white.png")
CARD_S = 2.5
TONE = (1500 / 60, 1888 / 60)                                  # first capture: room tone between two ticks
SFX = {"purchase": ("b", 213.80, 215.45), "row": ("a", 1276 / 60, 1281 / 60), "select": ("a", 274 / 60, 283 / 60), "back": ("a", 1158 / 60, 1164 / 60)}
PEAK = 0.5
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/gta6-customs_v3.mp4")
VOICE = W / "sfx/npc_line.wav"                                 # optional: laid at the "line" event if present


def read(p):
    w = wave.open(str(p)); sr = w.getframerate(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, ch) / 32768
    return (np.repeat(x, 2, 1) if ch == 1 else x), sr


def audio():
    xa, sr = read(W / "a.wav"); xb, _ = read(W / "b.wav")
    meta = json.load(open(W / "shop3_segments.json")); fps = meta["fps"]
    n = round((meta["frames"] / fps + CARD_S) * sr); y = np.zeros((n, 2), np.float32)
    cut = lambda x, t0, t1: x[round(t0 * sr):round(t1 * sr)].copy()

    def lay(t, src, fade):
        xf = int(fade * sr); i0 = max(0, round(t * sr)); src = src[:max(0, n - i0)]
        r = np.linspace(0, 1, min(xf, len(src)))[:, None]; src[:len(r)] *= r; src[-len(r):] *= r[::-1]
        y[i0:i0 + len(src)] += src

    tone = cut(xa, *TONE); L = len(tone) / sr; t = 0.0
    while t < n / sr:
        lay(t, tone.copy(), 0.3); t += L - 0.3
    for g, name in meta["events"]:
        if name == "line":
            if VOICE.exists():
                v, vsr = read(VOICE); assert vsr == sr; lay(g / fps, v, 0.01)
            continue
        which, t0, t1 = SFX[name]
        lay(g / fps - (0.0 if name == "purchase" else 0.01), cut(xa if which == "a" else xb, t0, t1), 0.03 if name == "purchase" else 0.004)
    y *= PEAK / np.abs(y).max()
    fo = int(1.2 * sr); y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    fi = int(0.05 * sr); y[:fi] *= np.linspace(0, 1, fi)[:, None]
    out = W / "reel3_audio.wav"
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
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "shop3.mp4"), "-i", str(wav), "-loop", "1", "-t", str(CARD_S), "-i", str(png),
                    "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(OUT)], check=True)
    print(OUT, "seconds", round(dur, 2))


if __name__ == "__main__":
    main()
