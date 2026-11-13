"""IRL opening for the 9:16 reel from landscape footage (honda-s2000): each output frame = the 16:9 source frame scaled
to the full 1080 width (a 1080x608 band centred at y=960) over a blurred, darkened fill of itself (fg2 canvas idea).
The scan render after the 1:1 cut uses the solved camera at 1080x1920 with the SAME horizontal FOV, so the car keeps its
pixels inside the band. Output frames end exactly on --last (the solved source frame).
    python projects/honda-s2000/tools/irl_band.py src_dir out_dir --last 8622 --n 28 [--src-fps 23.976 --fps 30]"""
import argparse, os
from PIL import Image, ImageFilter, ImageEnhance
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--last", type=int, required=True); ap.add_argument("--n", type=int, required=True)
ap.add_argument("--src-fps", type=float, default=23.976); ap.add_argument("--fps", type=float, default=30)
ap.add_argument("--dim", type=float, default=0.35)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
W, H = 1080, 1920
for i in range(a.n):
    k = a.last - round((a.n - 1 - i) * a.src_fps / a.fps)
    im = Image.open(f"{a.src}/f_{k:05d}.png").convert("RGB")
    bh = round(im.height * W / im.width); band = im.resize((W, bh), Image.LANCZOS)
    s = H / im.height; bg = im.resize((round(im.width * s), H), Image.LANCZOS)
    x0 = (bg.width - W) // 2; bg = bg.crop((x0, 0, x0 + W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(a.dim)
    bg.paste(band, (0, (H - bh) // 2)); bg.save(f"{a.out}/f_{i + 1:04d}.png")
print(a.out, a.n, "frames, last =", a.last)
