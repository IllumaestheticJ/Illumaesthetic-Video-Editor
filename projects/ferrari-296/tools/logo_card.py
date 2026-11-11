"""ILLUMAESTHETIC logo end card on pure black (no other text).

    python projects/ferrari-296/tools/logo_card.py remotion/public/illumaesthetic_logo.png out.mp4 [--secs 4.8]

Logo fades up over 0.4 s with a slow 4 % settle (scale 1.04 -> 1.00), holds, and fades to black over the
last 0.6 s with the music. Background matches the scan renders' black (0.004 linear ~ RGB 7,7,9 after AgX, measured).
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logo")
    ap.add_argument("out")
    ap.add_argument("--secs", type=float, default=4.8)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=860)
    ap.add_argument("--bg", default="7,7,9")
    ap.add_argument("--lead", type=float, default=0.0, help="seconds of black before the logo fades in (after a fade-out)")
    ap.add_argument("--fade-out", type=float, default=0.6)
    ap.add_argument("--tail", type=float, default=0.0, help="seconds of black after the logo has faded out")
    a = ap.parse_args()
    bg = tuple(int(v) for v in a.bg.split(","))
    logo = Image.open(a.logo).convert("RGBA")
    W, H = 1080, 1920
    n = int(round(a.secs * a.fps))
    with tempfile.TemporaryDirectory() as td:
        for i in range(n):
            t = i / a.fps - a.lead
            end = a.secs - a.lead - a.tail
            fade_in = min(1.0, max(0.0, t / 0.4))
            fade_out = min(1.0, max(0.0, (end - t) / a.fade_out))
            alpha = (fade_in * fade_out) ** 1.2
            u = min(1.0, max(0.0, t / max(1e-6, end)))
            s = 1.04 - 0.04 * (1 - (1 - u) ** 3)
            w = int(a.width * s)
            h = int(logo.height * w / logo.width)
            lg = logo.resize((w, h), Image.LANCZOS)
            lg.putalpha(lg.getchannel("A").point(lambda v: int(v * alpha)))
            fr = Image.new("RGBA", (W, H), bg + (255,))
            fr.alpha_composite(lg, ((W - w) // 2, int(H * 0.47) - h // 2))
            fr.convert("RGB").save(f"{td}/f_{i:04d}.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(a.fps), "-i", f"{td}/f_%04d.png",
                        "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", a.out], check=True)
    print(a.out)


if __name__ == "__main__":
    main()
