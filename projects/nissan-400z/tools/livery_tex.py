"""Bomex x Kaido House livery textures from the user's PSD (Drive '400Z export-version/400z-full.psd', 1920x1080 side view
of the kitted car's DRIVER side, nose at image left). Layers were extracted with ImageMagick (`convert 400z-full.psd[i]`;
psd-tools is not installed) to livery/layers/L<i>.png; offsets from `identify`.
  L2 car silhouette (alpha = projection mask/extent)   L4 flame/alligator graphic   L6 slogan   L7 BOMEX   L8 rear claw
  L23..L29 sponsor row (YOKOHAMA, BBS, SC, gktech, AR, AS) - the row visible in the PSD composite.
Out: livery/tex/side_left.png (driver, as drawn), side_right.png (passenger: text boxes pre-mirrored so they read after the
mirror-image projection), mask.png (L2 alpha), all cropped to the L2 bbox."""
import re, subprocess, os
import numpy as np
from PIL import Image, ImageOps
D = "/home/user/media/nissan-400z/livery"; O = f"{D}/tex"; os.makedirs(O, exist_ok=True)
ident = subprocess.run(["identify", f"{D}/400z-full.psd"], capture_output=True, text=True).stdout.splitlines()
off = {}
for l in ident:
    m = re.match(r".*\[(\d+)\] PSD (\d+)x(\d+) \d+x\d+([+-]\d+)([+-]\d+)", l)
    if m: off[int(m[1])] = (int(m[4]), int(m[5]))
W, H = 1920, 1080
WHITE = (6, 7)  # BOMEX + slogan are white in the PSD composite (layer colour effect, not in the raw layer pixels)
# v9 (user: "move the bomex logo on the sides backwards a little bit"): BOMEX + slogan shifted toward the rear (+x, nose is
# at image left), ~40 px = ~11 cm on the car
SHIFT = {6: (40, 0), 7: (40, 0)}
def lay(i, flip=False, side=False):
    im = Image.open(f"{D}/layers/L{i}.png").convert("RGBA")
    if i in WHITE:
        a = np.asarray(im).copy(); a[..., :3] = 245; im = Image.fromarray(a)
    if flip: im = ImageOps.mirror(im)
    o = off[i]
    if side and i in SHIFT: o = (o[0] + SHIFT[i][0], o[1] + SHIFT[i][1])
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); c.alpha_composite(im, o); return c
GRAPHIC = [4, 8]; TEXT = [6, 7, 23, 25, 26, 27, 28, 29]
mask = lay(2); bb = mask.getbbox(); print("silhouette bbox px", bb)
for nm, fl in (("side_left", False), ("side_right", True)):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i in GRAPHIC: c.alpha_composite(lay(i))
    for i in TEXT: c.alpha_composite(lay(i, fl, side=True))
    c.crop(bb).save(f"{O}/{nm}.png")
mask.crop(bb).save(f"{O}/mask.png")
print("wrote", O, Image.open(f"{O}/side_left.png").size)

# side glass: the dark (glass) pixels of the PSD's own car render (layer 1) inside the silhouette, upper body only
r = np.asarray(Image.open(f"{D}/layers/L1.png").convert("L")).astype(float)
from scipy import ndimage
g = (r < 95) & (np.asarray(mask)[..., 3] > 128); g[:500, :] &= True; g[560:, :] = False
g = ndimage.binary_opening(ndimage.binary_closing(g, np.ones((7, 7)), iterations=2), np.ones((3, 3)))
g = ndimage.binary_fill_holes(ndimage.binary_closing(g, np.ones((15, 15)), iterations=3))
lab, n = ndimage.label(g); sz = ndimage.sum(g, lab, range(1, n + 1)); keep = np.isin(lab, 1 + np.where(sz > 1500)[0])
w = np.zeros((H, W, 4), np.uint8); w[..., 3] = keep * 255
Image.fromarray(w).crop(bb).save(f"{O}/glass.png"); print("glass px", int(keep.sum()))

# hood decal (mockups hood-sponsor1-whitelogo / reference1): BOMEX + slogan in white, as one block, unmirrored
hd = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hd.alpha_composite(lay(7)); hd.alpha_composite(lay(6))
hb = hd.getbbox(); hd = hd.crop(hb); hd.save(f"{O}/hood.png"); print("hood decal px", hd.size)

# windscreen banner: the real KAIDO*HOUSE decal, taken from the user's own livery mock-up render (render/windshield.png:
# 4-point perspective rectify + 0.094 shear to upright, x3 cubic, soft threshold 125-175 -> logo/kaidohouse_white.png).
# v8 used a stand-in font; user v8 note: "properly resize and use the correct logo for the kaido house livery".
# Pre-sheared -0.2 so the strokes lean like the photo once projected along Y onto the raked, wrapped windscreen.
import cv2
im = cv2.imread(f"{D}/render/windshield.png")
src = np.float32([[770, 357.5], [1144, 509], [1115, 577.5], [727.5, 425]]); Hh, Ww, m, sh = 160, 825, 40, 0.094
M = cv2.getPerspectiveTransform(src, np.float32([[m, m], [Ww + m, m], [Ww + m, Hh + m], [m, Hh + m]]))
Sh = np.array([[1, sh, -sh * (Hh / 2 + m)], [0, 1, 0], [0, 0, 1]])
out = cv2.warpPerspective(im, np.diag([3, 3, 1.0]) @ Sh @ M, (3 * (Ww + 2 * m + 40), 3 * (Hh + 2 * m)), flags=cv2.INTER_CUBIC)
g = cv2.GaussianBlur(cv2.cvtColor(out, cv2.COLOR_BGR2GRAY), (5, 5), 0)
a = np.clip((g.astype(np.float32) - 125) * 255 / 50, 0, 255).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats((a > 128).astype(np.uint8))
keep = np.isin(lab, [i for i in range(1, n) if st[i, 4] > 60]).astype(np.uint8)
a = a * cv2.dilate(keep, np.ones((5, 5), np.uint8)); ys, xs = np.where(a > 128)
a = a[ys.min() - 6:ys.max() + 7, xs.min() - 6:xs.max() + 7]
logo = Image.fromarray(np.dstack([np.full_like(a, 255)] * 3 + [a])); logo.save("/home/user/media/nissan-400z/logo/kaidohouse_white.png")
w, h = logo.size; s2 = -0.2; pad = int(abs(s2) * h) + 4
ban = logo.transform((w + pad, h), Image.AFFINE, (1, -s2, s2 * h / 2 - pad / 2, 0, 1, 0), resample=Image.BICUBIC)
ban.save(f"{O}/banner.png"); print("banner px", ban.size)
