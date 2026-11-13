"""v5 ending: Ron's render 7 after the 1:1 cut from L_build, same slow push, small Epsilon+ wordmark, fade with the music.

    python ending7.py <7FinalSedanFL.jpg> <Epsilon+ Logo.png> <outdir>
114 frames (track 33.161-36.971). The 1920 render is shown at the window the camera was solved for (1360 px across 1080),
black pad; its lit floor fades into the pad over canvas rows 1250-1500. Push 1.007 -> 1.07 about the frame centre (L_build's
last 12 frames push 1.000 -> 1.007, see push_tail in the v5 assembly notes). Wordmark 300 px, centred, y 1560, in on frame 62
(B7d 35.241) over 4 frames; picture fades to black over the last 15 frames (from B8a 36.471).
"""
import os, sys
import numpy as np
from PIL import Image

ron, logo, out = sys.argv[1:4]
W, H, CROP, N, LOGO_AT, FADE = 1080, 1920, 1360, 114, 62, 15
k = W / CROP
r = Image.open(ron).convert("RGB"); r = r.resize((round(r.width * k), round(r.height * k)), Image.LANCZOS)
x0 = (r.width - W) // 2; y0 = (H - r.height) // 2
can = np.zeros((H, W, 3), np.float32); can[y0:y0 + r.height] = np.asarray(r, np.float32)[:, x0:x0 + W]
f = np.ones(H, np.float32); f[1250:1500] = np.linspace(1, 0, 250) ** 1.5; f[1500:] = 0
can *= f[:, None, None]
base = Image.fromarray(can.round().astype(np.uint8))
lg = Image.open(logo).convert("RGBA"); lw = 300; lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)
box = can[1560 - 30:1560 + 30, (W - lw) // 2:(W + lw) // 2]; print("luma under wordmark max %.1f" % box.mean(2).max())
os.makedirs(out, exist_ok=True)
for j in range(N):
    s = 1.007 + (1.07 - 1.007) * j / (N - 1); w, h = W / s, H / s
    im = base.resize((W, H), Image.BICUBIC, box=((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2))
    if j >= LOGO_AT:
        al = min(1.0, (j - LOGO_AT + 1) / 4)
        l2 = lg.copy(); l2.putalpha(l2.getchannel("A").point(lambda v: int(v * al)))
        im.paste(l2, ((W - lw) // 2, 1560 - lg.height // 2), l2)
    if j >= N - FADE:
        im = Image.blend(im, Image.new("RGB", (W, H)), (j - (N - FADE) + 1) / FADE)
    im.save(f"{out}/f_{j + 1:04d}.png")
print("ok", out)
