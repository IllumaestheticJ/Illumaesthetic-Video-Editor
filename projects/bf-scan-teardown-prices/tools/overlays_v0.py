"""v0 overlays: Del & Eps PLACEHOLDER cut-outs from the locked model sheet, price cards, BF tag, end card.
Prices: projects/_blackfriday/PRICES.md (BF liquidation sheet: 'Current Price' struck -> 'BF 2026 Price')."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = "/home/user/Illumaesthetic-Video-Editor/"; O = "/home/user/media/bf-scan-teardown-prices/ov/"
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + {"b": "InterDisplay-Bold.otf", "m": "InterDisplay-Medium.otf"}[w], s)
OFF, SAGE, GREY = (242, 243, 241), (97, 159, 115), (140, 142, 140)

# --- characters: key out the sheet's flat grey (195) background
sheet = Image.open(R + "knowledge/characters/del-and-eps/del-eps-model-sheet.jpg").convert("RGB")
def cut(box, name):
    im = sheet.crop(box); a = np.asarray(im).astype(int)
    d = np.abs(a - 195).max(2); alpha = np.clip((d - 8) * 16, 0, 255).astype(np.uint8)
    rgba = Image.fromarray(np.dstack([np.asarray(im), alpha]).astype(np.uint8), "RGBA")
    rgba.putalpha(Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)))
    rgba = rgba.crop(rgba.getbbox()); rgba.save(O + name); return rgba
eps = cut((150, 615, 400, 1140), "eps.png")
dele = cut((78, 0, 480, 600), "del.png")
def tag(img, h):
    """scale to height h and stamp a small PLACEHOLDER label under the feet"""
    s = img.resize((int(img.width * h / img.height), h), Image.LANCZOS)
    c = Image.new("RGBA", (max(s.width, 230), h + 34), (0, 0, 0, 0)); c.alpha_composite(s, ((c.width - s.width) // 2, 0))
    d = ImageDraw.Draw(c); f = font("m", 20); t = "PLACEHOLDER"
    w = d.textlength(t, font=f); d.text(((c.width - w) / 2, h + 8), t, font=f, fill=(255, 210, 31, 230))
    return c
tag(eps, 520).save(O + "eps_1to1.png")
tag(eps, 120).save(O + "eps_micro.png"); tag(dele, 130).save(O + "del_micro.png")

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
d.text((540, 990), "BLACK FRIDAY", font=font("b", 76), fill=OFF, anchor="ms")
d.text((540, 1080), "30% OFF THE CIVIC FE KIT", font=font("b", 50), fill=SAGE, anchor="ms")
d.text((540, 1170), "EPSILON.PLUS", font=font("m", 44), fill=GREY, anchor="ms")
e.save(O + "endcard.png")
print("ok")
