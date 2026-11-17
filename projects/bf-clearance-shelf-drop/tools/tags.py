"""Price-tag card textures (front = was price, back = BF price) built ONLY from store_snapshot.json."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
snap = json.load(open(sys.argv[1])); out = sys.argv[2]
# knowledge/fonts.md: Akira for headlines/prices; Unbounded 700 stands in until the owner supplies Akira.
FD = "/home/user/Illumaesthetic-Video-Editor/assets/fonts/unbounded/"
F = FD + "Unbounded-700.ttf"     # Akira stand-in (title, BLACK FRIDAY, sale price)
FM = FD + "Unbounded-500.ttf"    # labels / was-price
W, H = 700, 900
def card(title, lines, sale):
    """Readable at phone size: few words, very large prices, high contrast."""
    im = Image.new("RGB", (W, H), (244, 245, 247)); d = ImageDraw.Draw(im)
    d.ellipse((W/2-20, 26, W/2+20, 66), fill=(20, 20, 22))
    d.rectangle((0, 0, W-1, H-1), outline=(10, 10, 12), width=10)
    y = 92
    for t in title.split("\n"):
        d.text((W/2, y), t, font=ImageFont.truetype(F, 60), fill=(10, 10, 12), anchor="mt"); y += 72
    if sale:
        d.rectangle((40, y + 10, W - 40, y + 84), fill=(10, 10, 12))
        d.text((W/2, y + 47), "BLACK FRIDAY", font=ImageFont.truetype(F, 46), fill=(244, 245, 247), anchor="mm")
        y += 96
    else:
        y += 40
    for label, was, now in lines:
        d.text((44, y + 10), label, font=ImageFont.truetype(FM, 36), fill=(40, 40, 46))
        base = y + 10 + 50 + 128
        if sale:
            fw = ImageFont.truetype(FM, 50)
            d.text((44, base - 20), was, font=fw, fill=(120, 120, 126), anchor="ls")
            bb = d.textbbox((44, base - 20), was, font=fw, anchor="ls"); my = (bb[1] + bb[3]) // 2
            d.line((bb[0] - 4, my, bb[2] + 4, my), fill=(10, 10, 12), width=9)
            d.text((W - 40, base), now, font=ImageFont.truetype(F, 112), fill=(10, 10, 12), anchor="rs")
        else:
            d.text((44, base), was, font=ImageFont.truetype(F, 104), fill=(10, 10, 12), anchor="ls")
        y = base + 14
    return im
for key, t in snap["tags"].items():
    lines = [(l["label"], l["was"], l["bf"]) for l in t["lines"]]
    card(t["title"], lines, False).save(f"{out}/tag_{key}_front.png")
    card(t["title"], lines, True).save(f"{out}/tag_{key}_back.png")
    print(key)
