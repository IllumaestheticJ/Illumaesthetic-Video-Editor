"""End card: a landscape photo on a blurred, darkened fill of itself (lesson: landscape photos in 9:16) with the
ILLUMAESTHETIC logo in the fill BELOW the photo (never over the truck). Slow 3 % push on the photo, fade in/out.
  photo_card.py photo.png logo.png out.mp4 --frames 120"""
import argparse, subprocess, tempfile
from PIL import Image, ImageFilter, ImageEnhance
ap = argparse.ArgumentParser(); ap.add_argument("photo"); ap.add_argument("logo"); ap.add_argument("out")
ap.add_argument("--frames", type=int, default=120); ap.add_argument("--logo-width", type=int, default=700)
a = ap.parse_args(); W, H, fps = 1080, 1920, 30
ph = Image.open(a.photo).convert("RGB"); lg = Image.open(a.logo).convert("RGBA")
fill = ph.resize((int(ph.width * H / ph.height), H), Image.LANCZOS)
fill = fill.crop(((fill.width - W) // 2, 0, (fill.width - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(40))
fill = ImageEnhance.Brightness(fill).enhance(0.28)
lw = a.logo_width; lgr = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
with tempfile.TemporaryDirectory() as td:
    for i in range(a.frames):
        t = i / fps; T = a.frames / fps; u = i / (a.frames - 1)
        s = 1.0 + 0.03 * u; pw = int(W * s); p = ph.resize((pw, int(ph.height * pw / ph.width)), Image.LANCZOS)
        fr = fill.copy().convert("RGBA"); py = int(H * 0.40) - p.height // 2
        fr.paste(p, ((W - pw) // 2, py))
        la = min(1.0, max(0.0, (t - 0.5) / 0.5)); l2 = lgr.copy(); l2.putalpha(l2.getchannel("A").point(lambda v: int(v * la)))
        fr.alpha_composite(l2, ((W - lw) // 2, int(H * 0.40) + int(ph.height * W / ph.width) // 2 + 150))
        k = min(1.0, t / 0.25, max(0.0, (T - t) / 0.7))
        Image.blend(Image.new("RGB", (W, H), (7, 7, 9)), fr.convert("RGB"), k).save(f"{td}/f_{i:04d}.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i", f"{td}/f_%04d.png", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", a.out], check=True)
print(a.out)
