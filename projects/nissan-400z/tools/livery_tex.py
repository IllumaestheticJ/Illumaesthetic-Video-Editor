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
def lay(i, flip=False):
    im = Image.open(f"{D}/layers/L{i}.png").convert("RGBA")
    if i in WHITE:
        a = np.asarray(im).copy(); a[..., :3] = 245; im = Image.fromarray(a)
    if flip: im = ImageOps.mirror(im)
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); c.alpha_composite(im, off[i]); return c
GRAPHIC = [4, 8]; TEXT = [6, 7, 23, 25, 26, 27, 28, 29]
mask = lay(2); bb = mask.getbbox(); print("silhouette bbox px", bb)
for nm, fl in (("side_left", False), ("side_right", True)):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i in GRAPHIC: c.alpha_composite(lay(i))
    for i in TEXT: c.alpha_composite(lay(i, fl))
    c.crop(bb).save(f"{O}/{nm}.png")
mask.crop(bb).save(f"{O}/mask.png")
print("wrote", O, Image.open(f"{O}/side_left.png").size)
