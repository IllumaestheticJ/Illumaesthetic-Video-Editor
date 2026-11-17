"""Dark-on-transparent brand logo -> version for the black scan background (user's new Jackson Racing logo, v13):
black/grey ink -> off-white, coloured ink (the red JR mark) kept, alpha kept, cropped to the ink, upscaled 4x (LANCZOS).
    python projects/toyota-gr-corolla/tools/logo_reverse.py logo.png out.png"""
import sys
import numpy as np
from PIL import Image
src, out = sys.argv[1:3]
im = Image.open(src).convert("RGBA")
im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
im = im.resize((im.width * 4, im.height * 4), Image.LANCZOS)
a = np.asarray(im).astype(np.float32) / 255
rgb, al = a[..., :3], a[..., 3:]
sat = rgb.max(-1, keepdims=True) - rgb.min(-1, keepdims=True)
ink = np.clip(1 - sat / 0.25, 0, 1)                      # 1 = neutral (black/grey) ink, 0 = coloured
white = np.array([0.94, 0.95, 0.96])
out_rgb = ink * white + (1 - ink) * rgb
Image.fromarray((np.dstack([out_rgb, al]) * 255).round().astype(np.uint8), "RGBA").save(out)
print(out, im.size)
