"""Assemble the car-lot reel: arrival (capture, untouched) + menu with the Epsilon cars, 9:16.

    python projects/nfs-carlot/tools/assemble.py [out.mp4]

Picture: the capture is 16:9 with the game's menu in a centred 4:3 box, so the frame is cropped to that
box (x 300-1842 of 2144), scaled to the reel's full width, and set on a blurred, darkened copy of itself.

Sound: the 1440p capture (a.wav) for the arrival. Its garage section is sped up 2x (user, v1 review), so
the menu uses the second capture (b.wav), which is real time, in two takes: the menu opening through two
scrolls, then B's last three scrolls, the click on Continue, the purchase prompt and the click on Yes, in
one piece, so the purchase sounds exactly as it does in the game. The EPSILON+ card cuts in on the Yes
click and B's audio plays on under it and fades. The picture is cut to that audio: every car change
starts on the frame where the car starts to move in capture B (B_SCROLLS, measured from B's picture),
and the prompt (B_PROMPT) and the click on Yes (B_YES) likewise.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

W = Path("/home/user/media/work/nfs-carlot")
INTRO = (952, 1291)            # a60.mp4 frames (60 fps): "enter the shop?" (1 s), then the 350Z cutscene (4.65 s)
B_SCROLLS = [34.93, 37.87, 40.27, 50.03, 52.03, 53.30]   # seconds in capture B where each of our six car changes starts
TAKE2 = 3                                         # index of the first car change that uses B's second take
B_PROMPT, B_YES = 54.10, 55.30                    # B: purchase prompt starts to fade in / Yes is clicked (prompt gone)
CARD_S = 3.0                                      # EPSILON+ end card, cut in on the Yes click; B's audio plays on under it (silent from 58.2 s)
LOGO = Path("/home/user/Epsilon-Site/showroom/brand/eps-showroom-wordmark-white.png")   # official EPSILON+ wordmark (site header artwork)
LEAD = 0.08                                       # B's scroll sound starts up to this long before the car moves
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/nfs-carlot_v5.mp4")


def load(name):
    w = wave.open(str(W / name)); sr, ch = w.getframerate(), w.getnchannels()
    return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, ch) / 32768, sr


def rms_db(x):
    return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)


def audio():
    a, sr = load("a.wav"); b, _ = load("b.wav")
    meta = json.load(open(W / "menu_segments.json")); fps = meta["fps"]; seg = meta["segments"]
    intro = a[round(INTRO[0] / 60 * sr):round((INTRO[1] + 1) / 60 * sr)].copy()
    n_menu = round((meta["frames"] / fps + CARD_S) * sr)          # menu + end card
    menu = np.zeros((n_menu, 2), np.float32)
    # menu time of each car change = when that segment's scroll starts
    t_scroll = [s["scroll_at"] / fps for s in seg]
    t_prompt = meta["dialog"]["out_start"] / fps; t_end = meta["frames"] / fps
    xf = int(0.02 * sr)

    def place(t_menu, b0, b1):
        i0 = round(t_menu * sr); src = b[round(b0 * sr):round(b1 * sr)].copy()
        if i0 < 0:
            src = src[-i0:]; i0 = 0
        src = src[:max(0, n_menu - i0)]
        ramp = np.linspace(0, 1, min(xf, len(src)))[:, None]
        src[:len(ramp)] *= ramp; src[-len(ramp):] *= ramp[::-1]
        menu[i0:i0 + len(src)] += src

    # take 1: menu opening through the car changes before TAKE2 (continuous in B), up to the cut to take 2
    place(0.0, B_SCROLLS[0] - t_scroll[0], B_SCROLLS[TAKE2 - 1] + (t_scroll[TAKE2] - t_scroll[TAKE2 - 1]) - LEAD)
    # take 2: B's last three scrolls, Continue, the prompt, Yes, and on under the end card
    off = B_SCROLLS[TAKE2] - t_scroll[TAKE2]                      # B time = menu time + off for the whole take
    place(t_scroll[TAKE2] - LEAD, B_SCROLLS[TAKE2] - LEAD, off + t_end + CARD_S)
    sync = {"scrolls": [round(B_SCROLLS[i] - (t_scroll[i] + (off if i >= TAKE2 else B_SCROLLS[0] - t_scroll[0])), 3) for i in range(len(seg))],
            "prompt": round(B_PROMPT - (t_prompt + off), 3), "yes": round(B_YES - (t_end + off), 3)}
    print("picture minus sound, seconds (0 = in sync):", sync)
    menu *= 10 ** ((rms_db(intro) - 3.0 - rms_db(menu[menu.any(1)])) / 20)       # menu (and its in-game song) 3 dB under the cutscene
    # capture B is silent for its first ~0.3 s of menu: let the cutscene's sound ring out over that instead of cutting dead
    tail = a[round((INTRO[1] + 1) / 60 * sr):round((INTRO[1] + 1) / 60 * sr) + int(0.45 * sr)].copy()
    tail *= np.linspace(1, 0, len(tail))[:, None] ** 2
    menu[:len(tail)] += tail
    y = np.concatenate([intro, menu])
    fo = int(1.8 * sr); y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    fi = int(0.05 * sr); y[:fi] *= np.linspace(0, 1, fi)[:, None]
    out = W / "reel_audio.wav"
    ww = wave.open(str(out), "w"); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(sr)
    ww.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); ww.close()
    return out, len(y) / sr, [round(len(intro) / sr + t, 2) for t in t_scroll]


def card():
    """Black 1080x1920 card with the white EPSILON+ wordmark, 800 px wide, centred slightly above the middle."""
    import cv2
    logo = cv2.imread(str(LOGO), cv2.IMREAD_UNCHANGED).astype(np.float32)
    wl = 800; hl = round(logo.shape[0] * wl / logo.shape[1])
    logo = cv2.resize(logo, (wl, hl), interpolation=cv2.INTER_AREA)
    im = np.zeros((1920, 1080, 3), np.float32)
    y0, x0 = 920 - hl // 2, (1080 - wl) // 2
    a = logo[..., 3:] / 255
    im[y0:y0 + hl, x0:x0 + wl] = logo[..., :3] * a
    out = W / "end_card.png"
    cv2.imwrite(str(out), im.astype(np.uint8))
    return out


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wav, dur, scrolls = audio()
    png = card()
    fc = (f"[0:v]trim=start_frame={INTRO[0]}:end_frame={INTRO[1] + 1},setpts=PTS-STARTPTS,fps=30[i];"
          "[1:v]setpts=PTS-STARTPTS,fps=30[m];[i][m]concat=n=2:v=1,split[a][b];"
          "[a]crop=1542:1206:300:0,scale=1080:846:flags=lanczos[fg];"
          "[b]scale=-2:1920,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.22:saturation=0.9[bg];"
          "[bg][fg]overlay=0:497,format=yuv420p,setsar=1[reel];"
          f"[3:v]fps=30,format=yuv420p,setsar=1,fade=t=in:st=0:d=0.25[card];"
          "[reel][card]concat=n=2:v=1[v];"
          "[2:a]loudnorm=I=-15:TP=-1.5:LRA=11[au]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "a60.mp4"), "-i", str(W / "menu.mp4"), "-i", str(wav),
                    "-loop", "1", "-t", str(CARD_S), "-i", str(png),
                    "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(OUT)], check=True)
    print(OUT, "seconds", round(dur, 2), "car changes at", scrolls, "end card at", round(dur - CARD_S, 2))


if __name__ == "__main__":
    main()
