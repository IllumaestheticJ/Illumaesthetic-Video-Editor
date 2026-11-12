"""Livery textures for the Ronin section from the user's files (uploaded 2026-11-12):
  RONIN-livery-final2-draft.psd (side view, truck's LEFT side: nose at image left) -> side_left.png / side_right.png
  (RGBA, alpha = truck-base silhouette; right-side version has the RONIN logo flipped so it reads after mirroring),
  topology group1/group2 SVGs -> topo_tile.png (teal base + dark and gold contour lines) for hood/roof/front/rear.
Out: /home/user/media/nissan-frontier/livery/tex/"""
import io, os
import numpy as np
from PIL import Image, ImageOps
from psd_tools import PSDImage
import cairosvg
D = "/home/user/media/nissan-frontier/livery"; O = f"{D}/tex"; os.makedirs(O, exist_ok=True)
psd = PSDImage.open(f"{D}/073909c1-RONIN-livery-final2-draft.psd")
W, H = psd.size
def layer(name):
    l = [x for x in psd.descendants() if x.name == name][0]
    im = l.composite() if l.kind != "pixel" else l.topil()
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0)); c.paste(im.convert("RGBA"), (l.bbox[0], l.bbox[1])); return c
base = layer("truck-base"); mask = np.asarray(base)[..., 3]
comp = np.asarray(psd.composite().convert("RGB")).astype(int)
teal = (78, 134, 134)  # dominant body colour in the PSD composite (the truck-base shape layer itself reads darker)
def build(flip_logo):
    c = Image.new("RGBA", (W, H), teal + (255,))
    for n in ("topo-main", "topo-rear", "front slash", "middleslash", "rear slash"):
        c.alpha_composite(layer(n))
    lg = layer("smaller-logo")
    if flip_logo:
        l = [x for x in psd.descendants() if x.name == "smaller-logo"][0]
        box = l.bbox; crop = ImageOps.mirror(lg.crop(box)); lg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lg.paste(crop, (box[0], box[1]))
    c.alpha_composite(lg)
    a = np.asarray(c).copy(); a[..., 3] = mask
    return Image.fromarray(a)
bb = Image.fromarray(mask).getbbox(); print("truck bbox px", bb)
for nm, fl in (("side_left", False), ("side_right", True)):
    build(fl).crop(bb).save(f"{O}/{nm}.png")
# windows + utility areas (bumper, lamps, flares) are the flat (52,52,52) grey in the composite; the logo is excluded
wm = (np.abs(comp - 52).max(2) < 8); wm[790:895, 940:1540] = False
wimg = np.zeros((H, W, 4), np.uint8); wimg[..., 3] = wm * 255
Image.fromarray(wimg).crop(bb).save(f"{O}/window_util.png")
# topo tile
def svg(name, w=2048):
    f = [x for x in os.listdir(D) if x.endswith(name)][0]
    return np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(url=f"{D}/{f}", output_width=w))).convert("RGBA"))[..., 3] / 255.0
g1, g2 = svg("group1.svg"), svg("group2.svg")
h = min(g1.shape[0], g2.shape[0]); g1, g2 = g1[:h], g2[:h]
# sample the line colours from the PSD topo layer: dark and gold
t = np.asarray(layer("topo-main")); px = t[t[..., 3] > 120][:, :3].astype(int)
sat = px.max(1) - px.min(1); lum = px.sum(1)
gold = tuple(int(v) for v in np.median(px[(px[:, 0] > px[:, 2] + 40)], axis=0)) if (px[:, 0] > px[:, 2] + 40).any() else (222, 184, 120)
dark = (16, 34, 30)  # thin contour lines read near-black in the PSD
print("line colours", dark, gold)
img = np.ones((h, g1.shape[1], 3)) * np.array(teal)
img = img * (1 - g1[..., None]) + np.array(dark) * g1[..., None]
img = img * (1 - g2[..., None]) + np.array(gold) * g2[..., None]
Image.fromarray(img.astype(np.uint8)).save(f"{O}/topo_tile.png")
import json; json.dump({"teal": teal, "dark": dark, "gold": gold, "truck_bbox_px": bb, "psd_size": [W, H]}, open(f"{O}/info.json", "w"))
