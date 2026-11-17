"""v0 overlays: price cards, BF tag, end card (no characters: owner, 2026-11-17).
Prices: projects/_blackfriday/PRICES.md (BF liquidation sheet: 'Current Price' struck -> 'BF 2026 Price')."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = "/home/user/Illumaesthetic-Video-Editor/"; O = "/home/user/media/bf-scan-teardown-prices/ov/"
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + {"b": "InterDisplay-Bold.otf", "m": "InterDisplay-Medium.otf"}[w], s)
OFF, SAGE, GREY = (242, 243, 241), (97, 159, 115), (140, 142, 140)

# --- price cards (top third, 80 px inside the edges)
def card(name, was, bf, fn):
    c = Image.new("RGBA", (1080, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    fN, fW, fB = font("b", 62), font("m", 54), font("b", 104)
    d.text((540, 150), name, font=fN, fill=OFF, anchor="ms")
    ww = d.textlength(was, font=fW); bw = d.textlength(bf, font=fB); gap = 36
    x0 = 540 - (ww + gap + bw) / 2
    d.text((x0, 300), was, font=fW, fill=GREY, anchor="ls")
    d.line((x0 - 4, 282, x0 + ww + 4, 282), fill=GREY, width=5)
    d.text((x0 + ww + gap, 300), bf, font=fB, fill=SAGE, anchor="ls")
    c.save(O + fn)
card("FRONT LIP", "$285", "$199.50", "p_lip.png")
card("SIDE SKIRTS", "$400", "$280", "p_skirts.png")
card("REAR LIP", "$285", "$199.50", "p_rear.png")
card("SPORT WING", "$450", "$315", "p_wing.png")
def line(text, fn, size=72, col=OFF, y=170):
    c = Image.new("RGBA", (1080, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.text((540, y), text, font=font("b", size), fill=col, anchor="ms"); c.save(O + fn)
line("BLACK FRIDAY", "bf_tag.png", 84)
line("THE FULL EPSILON KIT", "kit_tag.png", 62)
# --- end card: Epsilon+ wordmark 720 px + offer line (v0 default wording) + site
logo = Image.open("/home/user/media/bf-scan-teardown-prices/logo/Epsilon+ Logo.png").convert("RGBA")
logo = logo.resize((720, int(logo.height * 720 / logo.width)), Image.LANCZOS)
e = Image.new("RGB", (1080, 1920), (11, 12, 11)); e.paste(logo, (180, 780), logo); d = ImageDraw.Draw(e)
import json
EB = [{"label": "end: wordmark", "x": 180, "y": 780, "w": logo.width, "h": logo.height, "key": True}]
def tb(txt, xy, f, lab):
    b = d.textbbox(xy, txt, font=f, anchor="ms"); EB.append({"label": lab, "x": b[0], "y": b[1], "w": b[2] - b[0], "h": b[3] - b[1], "key": True})
d.text((540, 990), "BLACK FRIDAY", font=font("b", 76), fill=OFF, anchor="ms"); tb("BLACK FRIDAY", (540, 990), font("b", 76), "end: BLACK FRIDAY")
d.text((540, 1080), "30% OFF THE CIVIC FE KIT", font=font("b", 50), fill=SAGE, anchor="ms"); tb("30% OFF THE CIVIC FE KIT", (540, 1080), font("b", 50), "end: offer")
d.text((540, 1170), "EPSILON.PLUS", font=font("m", 44), fill=GREY, anchor="ms"); tb("EPSILON.PLUS", (540, 1170), font("m", 44), "end: site")
json.dump(EB, open(O + "endcard_boxes.json", "w"))
e.save(O + "endcard.png")
print("ok")
