"""v0 placeholder characters: crop figures from the Del & Eps model sheet and key out the flat grey background
(flood fill from the crop border, so grey knee pads etc. inside the figure survive)."""
import sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
sheet = Image.open(sys.argv[1]).convert("RGB")
out = sys.argv[2]
boxes = {"del_front": (70, 0, 490, 610), "del_34": (610, 0, 975, 610),
         "eps_front": (130, 610, 410, 1150), "eps_34": (610, 610, 900, 1150)}
for name, b in boxes.items():
    im = sheet.crop(b)
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    bg = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0)
    close = (np.abs(a - bg).sum(-1) < 30)
    # flood fill from border over "close to bg" pixels
    mask = np.zeros((h, w), bool)
    stack = [(y, x) for x in range(w) for y in (0, h - 1)] + [(y, x) for y in range(h) for x in (0, w - 1)]
    while stack:
        y, x = stack.pop()
        if 0 <= y < h and 0 <= x < w and not mask[y, x] and close[y, x]:
            mask[y, x] = True
            stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    alpha = Image.fromarray(((~mask) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.convert("RGBA"); rgba.putalpha(alpha)
    bb = alpha.getbbox(); rgba = rgba.crop(bb)
    rgba.save(f"{out}/{name}.png"); print(name, rgba.size)
