"""Replace the player name in the menu ("Mohammad", the uploader's profile) with "Epsilon".

The name is part of the static menu layer, so the change is made once in the menu maps: the old letters are painted
out of the colour map A and the transmission map B, and the new word is typeset into them (JetBrains Mono SemiBold
Italic: a monospaced italic like the game's, matched to the old word's cap height, pitch, colour and softness).
composite.py then rebuilds that box in every frame from the patched maps.
    python name_patch.py <work>/ui "Epsilon"
"""
import sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
ui, word = sys.argv[1], sys.argv[2]
BOX = (1104, 1164, 1016, 1290)            # rows, cols of the name box
FONT = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-SemiBoldItalic.ttf"
out = {}
for st in ("mazda", "dodge"):
    A = np.load(f"{ui}/A_{st}.npy"); B = np.load(f"{ui}/B_{st}.npy")
    r0, r1, c0, c1 = BOX
    a = A[r0:r1, c0:c1].copy(); b = B[r0:r1, c0:c1].copy()
    lum = a.mean(2); base = cv2.medianBlur(lum.astype(np.uint8), 31).astype(np.float32)
    old = cv2.dilate(((lum - base) > 14).astype(np.uint8), np.ones((5, 5), np.uint8))
    ys, xs = np.nonzero((lum - base) > 40)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()          # old word's ink box (cap height = y1-y0)
    col = np.percentile(a[(lum - base) > 60], 80, axis=0)
    a0 = cv2.inpaint(np.clip(a, 0, 255).astype(np.uint8), old, 5, cv2.INPAINT_TELEA).astype(np.float32)
    b0 = cv2.inpaint((b * 255).astype(np.uint8), old, 5, cv2.INPAINT_TELEA).astype(np.float32) / 255
    b_text = float(np.percentile(b[(lum - base) > 60], 20))
    # typeset: cap height matched to the old capital M, letter pitch to the old word's
    cap = y1 - y0 + 1; pitch = (x1 - x0 + 1) / 8.0 * 1.02
    S = 4; f = ImageFont.truetype(FONT, 100)
    bb = f.getbbox("E"); px = int(round(100 * cap * S / (bb[3] - bb[1]))); f = ImageFont.truetype(FONT, px)
    im = Image.new("L", ((c1 - c0) * S, (r1 - r0) * S), 0); d = ImageDraw.Draw(im)
    bb = f.getbbox("E"); adv = f.getlength("E")
    for k, ch in enumerate(word):
        d.text((x0 * S + k * pitch * S + (pitch * S - adv) / 2 - 2 * S, y0 * S - bb[1]), ch, 255, font=f)
    t = cv2.resize(np.array(im), (c1 - c0, r1 - r0), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    t = cv2.GaussianBlur(t, (0, 0), 0.9)[..., None]
    A2 = a0 * (1 - t) + col * t; B2 = b0 * (1 - t[..., 0]) + b_text * t[..., 0]
    np.savez(f"{ui}/name_{st}.npz", A=A2.astype(np.float32), B=B2.astype(np.float32), old=old, box=np.array(BOX))
    out[st] = np.vstack([np.clip(a * 1.5, 0, 255), np.clip(A2 * 1.5, 0, 255)]).astype(np.uint8)
    print(st, "cap", cap, "pitch", round(pitch, 1), "colour", col.round(), "b_text", round(b_text, 3))
cv2.imwrite(f"{ui}/name_patch.jpg", cv2.resize(np.hstack([out["mazda"], out["dodge"]]), None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))
