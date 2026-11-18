"""v0 overlays: price cards, BF tag, end card (no characters: owner, 2026-11-17).
Prices: projects/_blackfriday/PRICES.md (BF liquidation sheet: 'Current Price' struck -> 'BF 2026 Price')."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = "/home/user/Illumaesthetic-Video-Editor/"; O = "/home/user/media/bf-scan-teardown-prices/ov/"
# v0.7 (user): Akira-style wide display face. Akira Expanded is personal-use only, so Unbounded (Google Fonts, OFL,
# commercial use OK) Black/ExtraBold is used; TTFs fetched from fonts.googleapis.com into media/.../fonts/.
F = "/home/user/media/bf-scan-teardown-prices/fonts/"
# knowledge/fonts.md (owner rule): Akira for headlines/offers/prices -> Unbounded 900 stand-in until the owner supplies the
# Akira file; text beside the logo (URL) = Unbounded 400; part labels / was-prices = Unbounded 500 (repo assets/fonts/unbounded).
FR = "/home/user/Illumaesthetic-Video-Editor/assets/fonts/unbounded/"
import os, glob as _g
# Akira drop-in: the first .otf/.ttf in assets/fonts/akira/ (or $AKIRA) replaces the Unbounded 900 stand-in for headlines/prices.
AK = os.environ.get("AKIRA") or next(iter(sorted(_g.glob("/home/user/Illumaesthetic-Video-Editor/assets/fonts/akira/*.[ot]tf"))), None)
def font(w, s):
    return ImageFont.truetype({"b": AK or F + "Unbounded-900.ttf", "m": F + "Unbounded-800.ttf",
                               "l": FR + "Unbounded-500.ttf", "u": FR + "Unbounded-400.ttf"}[w], s)
OFF, SAGE, GREY = (242, 243, 241), (97, 159, 115), (140, 142, 140)

# --- price cards (top third, 80 px inside the edges)
def card(name, was, bf, pct, fn):
    """name / struck was-price + BF price (whole dollars, owner 2026-11-17) / '% OFF' pill.
    BF prices with cents are rounded UP to the dollar ($199.50 -> $200) so the video never shows less than checkout."""
    c = Image.new("RGBA", (1080, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    fN, fW, fB, fP = font("l", 54), font("l", 46), font("b", 92), font("b", 38)
    d.text((540, 150), name, font=fN, fill=OFF, anchor="ms")
    ww = d.textlength(was, font=fW); bw = d.textlength(bf, font=fB); gap = 36
    x0 = 540 - (ww + gap + bw) / 2
    d.text((x0, 300), was, font=fW, fill=GREY, anchor="ls")
    d.line((x0 - 4, 282, x0 + ww + 4, 282), fill=GREY, width=5)
    d.text((x0 + ww + gap, 300), bf, font=fB, fill=SAGE, anchor="ls")
    t = f"{pct}% OFF"; tw = d.textlength(t, font=fP)
    d.rounded_rectangle((540 - tw / 2 - 24, 330, 540 + tw / 2 + 24, 398), radius=12, fill=SAGE)
    d.text((540, 381), t, font=fP, fill=(11, 12, 11), anchor="ms")
    c.save(O + fn)
# prices: projects/_blackfriday/PRICES.md (liquidation sheet). % = the sheet's tier for each part (all 30 %).
card("FRONT LIP", "$285", "$200", 30, "p_lip.png")
card("SIDE SKIRTS", "$400", "$280", 30, "p_skirts.png")
card("REAR LIP", "$285", "$200", 30, "p_rear.png")
card("SPORT WING", "$450", "$315", 30, "p_wing.png")
def line(text, fn, size=72, col=OFF, y=170):
    c = Image.new("RGBA", (1080, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.text((540, y), text, font=font("b", size), fill=col, anchor="ms"); c.save(O + fn)
line("BLACK FRIDAY", "bf_tag.png", 70)
line("THE FULL EPSILON KIT", "kit_tag.png", 62)
# --- v0.7 end: text OVER Ron's render with depth (user: "partially behind, partially in front").
# end_back.png goes under the car (headline, its lower half hidden by the roof and wing via r/ron7_mask.png);
# end_front.png goes over the car (offer pill across the doors, site on the floor). Wordmark on top, clear of the car.
import json
W, H = 1080, 1920
back = Image.new("RGBA", (W, H), (0, 0, 0, 0)); front = Image.new("RGBA", (W, H), (0, 0, 0, 0))
db, dfr = ImageDraw.Draw(back), ImageDraw.Draw(front)
EB = []
def fit(txt, w, maxs):
    s = maxs
    while ImageDraw.Draw(back).textlength(txt, font=font("b", s)) > w: s -= 2
    return font("b", s)
def put(d, txt, xy, f, fill, lab):
    d.text(xy, txt, font=f, fill=fill, anchor="ms"); b = d.textbbox(xy, txt, font=f, anchor="ms")
    EB.append({"label": lab, "x": b[0], "y": b[1], "w": b[2] - b[0], "h": b[3] - b[1], "key": True})
logo = Image.open("/home/user/media/bf-scan-teardown-prices/logo/Epsilon+ Logo.png").convert("RGBA")
logo = logo.resize((560, int(logo.height * 560 / logo.width)), Image.LANCZOS)
back.paste(logo, (200, 330), logo); EB.append({"label": "end: wordmark", "x": 200, "y": 330, "w": logo.width, "h": logo.height, "key": True})
fH = fit("FRIDAY", 840, 220)
put(db, "BLACK", (484, 670), fH, OFF, "end: BLACK")
put(db, "FRIDAY", (484, 670 + int(fH.size * 0.98)), fH, OFF, "end: FRIDAY")
fP = font("b", 44); t = "30% OFF THE CIVIC FE KIT"
while dfr.textlength(t, font=fP) > 780: fP = font("b", fP.size - 2)
tw = dfr.textlength(t, font=fP); y = 1046
dfr.rounded_rectangle((484 - tw / 2 - 28, y - fP.size - 18, 484 + tw / 2 + 28, y + 22), radius=14, fill=SAGE + (255,))
put(dfr, t, (484, y), fP, (11, 12, 11), "end: offer")
put(dfr, "WWW.EPSILON.PLUS", (484, 1250), font("u", 42), OFF, "end: url")
back.save(O + "end_back.png"); front.save(O + "end_front.png")
json.dump(EB, open(O + "endcard_boxes.json", "w"))
print("ok", fH.size, fP.size)
