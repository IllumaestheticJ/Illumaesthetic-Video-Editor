"""v8 non-CGI segments (short-form.md playbook from the Sentra reel):
  hook.mp4      146 f  real article, full frame, 3 % push (press/motorillustrated_art.png from tools/capture.js)
  answer.mp4     72 f  "HERE'S HOW." on black, Inter Display Black, red rule
  irl_3223_slow.mp4 72 f  the 1:1 reveal clip from 2.4 s (only 1.5 s of clip is left) slowed to 0.615x so the payoff holds 2.4 s;
                          frame 1 is the exact solved frame
    python build_v8_cards.py"""
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
M = "/home/user/media/nissan-frontier"; O = "/home/user/media/work/frontier/out"; W, H, FPS = 1080, 1920, 30


def pipe(path, frames):
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    n = 0
    for im in frames: p.stdin.write(np.asarray(im.convert("RGB")).tobytes()); n += 1
    p.stdin.close(); p.wait(); print(path, n)


def hook(n=146):
    src = Image.open(f"{M}/press/motorillustrated_art.png").convert("RGB").resize((W, H), Image.LANCZOS)
    for f in range(n):
        z = 1 + 0.03 * f / (n - 1); w, h = W / z, H / z
        yield src.resize((W, H), Image.BICUBIC, box=((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2))


def answer(n=72):
    ft = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", 190)
    for f in range(n):
        im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
        for i, (t, on) in enumerate((("HERE'S", 0), ("HOW.", 18))):          # second word lands one beat later
            if f >= on:
                d.text(((W - d.textlength(t, font=ft)) / 2, 760 + i * 200), t, font=ft, fill=(240, 240, 236))
        if f >= 18: d.rectangle([(W - 300) // 2, 1200, (W + 300) // 2, 1210], fill=(214, 40, 40))
        yield im


pipe(f"{O}/hook.mp4", hook()); pipe(f"{O}/answer.mp4", answer())
TM = "zscale=t=linear:npl=100,tonemap=hable,zscale=t=bt709:m=bt709:p=bt709:r=tv,format=yuv420p"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "2.4", "-i", f"{M}/sema/IMG_3223.mov", "-an", "-vf",
                f"{TM},setpts=PTS/0.615,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=none,scale={W}:{H}",
                "-frames:v", "72", "-r", "30", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", f"{O}/irl_3223_slow.mp4"], check=True)
