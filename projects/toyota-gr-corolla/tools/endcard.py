"""End card: the 720 px Illumaesthetic logo card + a contact line under it (user: "Illumaesthetic / contact us for
your engineering/scanning needs (or similar)"). House text style (Inter Display, off-white, tracking), centred,
fades in after the logo has landed. The web address is the site the logo file came from (clips.md) - no invented info.
    python projects/toyota-gr-corolla/tools/endcard.py logo_card_720.mp4 out.mp4"""
import subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
COL = (232, 236, 242)
LINES = [("CONTACT US FOR YOUR", 40, 1060), ("ENGINEERING & SCANNING NEEDS", 40, 1116), ("ILLUMAESTHETIC.COM", 30, 1210)]
TRACK = 5

def tracked_width(f, t): return sum(f.getlength(c) + TRACK for c in t) - TRACK

src, out = sys.argv[1:3]
im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
for text, size, y in LINES:
    f = ImageFont.truetype(FONT, size); x = (1080 - tracked_width(f, text)) / 2
    col = COL + (255,) if size >= 40 else (170, 176, 186, 255)
    for c in text:
        d.text((x, y), c, font=f, fill=col); x += f.getlength(c) + TRACK
with tempfile.TemporaryDirectory() as td:
    im.save(f"{td}/t.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-i", f"{td}/t.png", "-filter_complex",
                    "[1:v]format=rgba,fade=t=in:st=0.5:d=0.3:alpha=1[t];[0:v][t]overlay=shortest=1,format=yuv420p",
                    "-c:v", "libx264", "-crf", "16", "-r", "30", "-an", out], check=True)
print(out)
