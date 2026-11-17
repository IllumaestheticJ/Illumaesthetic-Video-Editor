"""Price-tag card textures (front = was price, back = BF price) built ONLY from store_snapshot.json."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
snap = json.load(open(sys.argv[1])); out = sys.argv[2]
F = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FM = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
W, H = 600, 760
def card(title, lines, sale):
    im = Image.new("RGB", (W, H), (236, 238, 242)); d = ImageDraw.Draw(im)
    d.ellipse((W/2-22, 34, W/2+22, 78), fill=(20, 20, 22))          # string hole
    d.rectangle((0, 0, W-1, H-1), outline=(20, 20, 22), width=6)
    y = 120
    for t in title.split("\n"):
        f = ImageFont.truetype(F, 54); d.text((W/2, y), t, font=f, fill=(15, 15, 18), anchor="mt"); y += 64
    if sale:
        f = ImageFont.truetype(F, 44); d.text((W/2, y + 14), "BLACK FRIDAY", font=f, fill=(15, 15, 18), anchor="mt"); y += 70
    y += 40
    for label, was, now in lines:
        fl = ImageFont.truetype(FM, 40); d.text((50, y), label, font=fl, fill=(60, 60, 66))
        base = y + 140
        if sale:
            fw = ImageFont.truetype(FM, 50)
            d.text((50, base - 12), was, font=fw, fill=(110, 110, 116), anchor="ls")
            bb = d.textbbox((50, base - 12), was, font=fw, anchor="ls"); my = (bb[1] + bb[3]) // 2
            d.line((bb[0] - 4, my, bb[2] + 4, my), fill=(15, 15, 18), width=7)
            fn = ImageFont.truetype(F, 96); d.text((W - 46, base), now, font=fn, fill=(10, 10, 12), anchor="rs")
        else:
            fn = ImageFont.truetype(F, 96); d.text((50, base), was, font=fn, fill=(10, 10, 12), anchor="ls")
        y = base + 40
    return im
for key, t in snap["tags"].items():
    lines = [(l["label"], l["was"], l["bf"]) for l in t["lines"]]
    card(t["title"], lines, False).save(f"{out}/tag_{key}_front.png")
    card(t["title"], lines, True).save(f"{out}/tag_{key}_back.png")
    print(key)
