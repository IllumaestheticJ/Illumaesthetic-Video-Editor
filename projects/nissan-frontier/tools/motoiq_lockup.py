"""MotoIQ lockup as used on the Sentra end card ("full motoiq lockup: white moto, red iq box", nissan-sentra-sema feedback 2026-11-13).
That PNG was a user upload in the Sentra session and is not reachable here, so it is rebuilt from the flattened 3D wordmark
(logo_from_stl.py): straightened, 'moto' white, 'iq' white on a red box.
    python motoiq_lockup.py motoiq_white.png motoiq_lockup_white.png"""
import sys
import numpy as np
from PIL import Image, ImageDraw
src = Image.open(sys.argv[1]).getchannel("A")
A0 = np.asarray(src) > 128
def edge(x0, x1, f):
    return f([f(np.nonzero(A0[:, x])[0]) for x in range(x0, x1) if A0[:, x].any()])
o1 = edge(int(0.26 * src.width), int(0.42 * src.width), np.min); o2 = edge(int(0.56 * src.width), int(0.74 * src.width), np.min)
ang = np.degrees(np.arctan2(o2 - o1, 0.31 * src.width))          # tops of the two 'o's -> baseline tilt
best = (0, ang)
m = src.rotate(best[1], resample=Image.BICUBIC, expand=True); m = m.crop(m.getbbox()); A = np.asarray(m) > 128
col = A.sum(0); gaps = [x for x in range(1, len(col)) if col[x] == 0 and col[x - 1] > 0]
starts = [x for x in range(1, len(col)) if col[x] > 0 and col[x - 1] == 0]
i0 = starts[-2]                                   # 'i' starts at the second-to-last glyph start
pad = int(0.07 * m.height); W, H = m.width + 2 * pad, m.height + 2 * pad
out = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(out)
d.rectangle([i0 + pad - pad, 0, W - 1, H - 1], fill=(221, 30, 37, 255))   # red box behind 'iq'
white = Image.new("RGBA", m.size, (255, 255, 255, 255)); out.paste(white, (pad, pad), m)
out.save(sys.argv[2]); print("rotated", round(best[1], 1), "size", out.size, "iq from", i0)
