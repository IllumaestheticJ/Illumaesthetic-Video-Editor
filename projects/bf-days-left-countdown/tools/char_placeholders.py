"""v0 placeholders for Del & Eps: cut the front views out of the locked model sheet (no generation).
python char_placeholders.py <model-sheet.jpg> <out_dir>"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
CROPS = {"del": (60, 0, 495, 605), "eps": (135, 610, 410, 1150)}  # px in the 2048-wide sheet (front views)


def cutout(rgb):
    a = np.asarray(rgb).astype(int)
    bgc = np.median(np.concatenate([a[:4].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)]), 0)
    near = np.abs(a - bgc).max(2) < 16
    # flood from the border through background-like pixels
    m = np.zeros(near.shape, bool)
    m[0], m[-1], m[:, 0], m[:, -1] = near[0], near[-1], near[:, 0], near[:, -1]
    while True:
        g = m.copy()
        g[1:] |= m[:-1]; g[:-1] |= m[1:]; g[:, 1:] |= m[:, :-1]; g[:, :-1] |= m[:, 1:]
        g &= near
        if (g == m).all():
            break
        m = g
    alpha = Image.fromarray(((~m) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
    rgba = rgb.convert("RGBA"); rgba.putalpha(alpha)
    return rgba.crop(rgba.getbbox())


for k, box in CROPS.items():
    cutout(im.crop(box)).save(f"{out}/{k}_placeholder.png")
    print(k, Image.open(f"{out}/{k}_placeholder.png").size)
