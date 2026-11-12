"""v4 ending: all-kit scan still -> hard 1:1 cut to Ron's render 1, one shared slow push, small Epsilon+ wordmark.

    python ending.py <W_kit still.png> <ron render.jpg> <Epsilon+ Logo.png> <outdir>
Writes <outdir>/W_kit/f_####.png (37 frames, push 1.000 -> 1.022) and <outdir>/R_ron/f_####.png (100 frames, 1.022 -> 1.08).
The render (1920 square) is shown at the crop the camera was solved for (1520 px across the 1080 frame), padded with black;
its lit floor fades into the pad. Wordmark: 300 px wide, centred at y 1370, from frame 56 of R_ron (track 38.323 s), 4-frame
fade in, fades out over the last 15 frames with the music. Push = scale about the frame centre.
"""
import os, sys
import numpy as np
from PIL import Image

still, ron, logo, out = sys.argv[1:5]
W, H, CROP = 1080, 1920, 1520
NW, NR, LOGO_AT = 37, 100, 56
k = W / CROP
r = Image.open(ron).convert("RGB"); r = r.resize((round(r.width * k), round(r.height * k)), Image.LANCZOS)
ra = np.asarray(r, np.float32)
fade = np.ones(r.height, np.float32); n = 260; fade[-n:] = np.linspace(1, 0, n) ** 1.5   # floor band -> black pad
ra *= fade[:, None, None]
can = np.zeros((H, W, 3), np.float32); x0 = (W - r.width) // 2; y0 = (H - r.height) // 2
can[y0:y0 + r.height] = ra[:, -x0:-x0 + W]
ron_c = Image.fromarray(can.round().astype(np.uint8))
kit = Image.open(still).convert("RGB").resize((W, H), Image.LANCZOS)
lg = Image.open(logo).convert("RGBA"); lw = 300; lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)


def push(im, s):
    w, h = W / s, H / s
    return im.resize((W, H), Image.BICUBIC, box=((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2))


tot = NW + NR
for d, im, a, b in (("W_kit", kit, 0, NW), ("R_ron", ron_c, NW, tot)):
    os.makedirs(f"{out}/{d}", exist_ok=True)
    for i in range(a, b):
        s = 1.0 + 0.022 * i / NW if i < NW else 1.022 + (1.08 - 1.022) * (i - NW) / (NR - 1)
        f = push(im, s)
        j = i - a
        if d == "R_ron" and j >= LOGO_AT:
            al = min(1.0, (j - LOGO_AT + 1) / 4) * min(1.0, (NR - 1 - j) / 15)
            l2 = lg.copy(); l2.putalpha(l2.getchannel("A").point(lambda v: int(v * al)))
            f.paste(l2, ((W - lw) // 2, 1370 - lg.height // 2), l2)
        f.save(f"{out}/{d}/f_{j + 1:04d}.png")
print("ok", out)
