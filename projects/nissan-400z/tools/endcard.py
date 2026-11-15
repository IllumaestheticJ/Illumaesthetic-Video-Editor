"""End card (user 2026-11-14: "add the Bomex logo at the end (from Sentra video)"): Sentra layout (nissan-sentra-sema
build_v6.seg_end) - Illumaesthetic logo, then the white Bomex mark (GR86_Bomex_Badge_34.8x9.8_RevE.ai, plate dropped,
+20 % height because the badge art is squashed), stacked, centred, equal gaps between visible ink; logo fades in, Bomex
14 frames later; whole card fades out at the end.
  python endcard.py out.mp4 frames"""
import subprocess, sys
from PIL import Image
out, n = sys.argv[1], int(sys.argv[2]); WD, HT = 1080, 1920
def ink(im): return im.crop(im.getchannel("A").getbbox())
logo = Image.open("remotion/public/illumaesthetic_logo.png").convert("RGBA"); logo = ink(logo)
logo = logo.resize((720, int(720 * logo.height / logo.width)), Image.LANCZOS)
bx = ink(Image.open("/home/user/media/nissan-400z/logo/bomex_white.png").convert("RGBA"))
bx = bx.resize((560, int(bx.height * 560 / bx.width * 1.2)), Image.LANCZOS)
gap = 170; total = logo.height + gap + bx.height; y0 = (HT - total) // 2; ys = [y0, y0 + logo.height + gap]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WD}x{HT}", "-r", "30", "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
fo = 24
for f in range(n):
    im = Image.new("RGB", (WD, HT), (0, 0, 0)); tail = min(1.0, max(0.0, (n - 1 - f) / fo))
    for k, (lg, yy) in enumerate(zip((logo, bx), ys)):
        al = (min(1.0, f / 8) if k == 0 else max(0.0, min(1.0, (f - 14) / 8))) * tail
        if al <= 0: continue
        l2 = lg.copy(); l2.putalpha(lg.getchannel("A").point(lambda v: int(v * al))); im.paste(l2, ((WD - lg.width) // 2, yy), l2)
    p.stdin.write(im.tobytes())
p.stdin.close(); p.wait(); print(out, n, "frames; logo", logo.size, "bomex", bx.size, "gap", gap)
