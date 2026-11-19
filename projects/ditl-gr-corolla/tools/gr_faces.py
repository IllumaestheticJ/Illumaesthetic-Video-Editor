"""Face decals, screens, forms, signs and bubbles for the DITL GR Corolla short (PIL). python gr_faces.py <outdir>
Character numbers on the sales sheet live in NUMBERS: they come from the owner, never invented for a final cut."""
import sys, os, random
from PIL import Image, ImageDraw
from faces import face, font, sign, phone_base
INK = (10, 10, 10, 255); BLUE = (20, 40, 160, 255); RED = (205, 15, 15, 255)
# PLACEHOLDERS shown to the owner on 2026-11-19 for approval (owner asked for "a monthly amount with a high apr and high mark up").
NUMBERS = {"markup": "+$20,000", "apr": "29.99%", "monthly": "$1,499/mo", "term": "x 84 months"}

def card(out, car, name, comment, liked=False, typed=""):
    im, d = phone_base("r/whichcar"); d.text((24, 92), "which one should I buy?", font=font(34, True), fill=(20, 20, 20))
    p = f"{out}/thumb_{car}.png"; th = Image.open(p).convert("RGB").resize((480, 480)) if os.path.exists(p) else Image.new("RGB", (480, 480), (228, 232, 240))
    im.paste(th, (30, 150)); d.rectangle([30, 150, 510, 630], outline=(210, 210, 215), width=3)
    d.text((30, 650), name, font=font(58, True), fill=(20, 20, 20))
    d.rounded_rectangle([30, 740, 510, 860], 18, fill=(240, 240, 244)); d.text((48, 752), "top comment", font=font(20), fill=(120, 120, 120)); d.text((48, 786), comment, font=font(40, True), fill=(40, 40, 40))
    col = (230, 30, 60) if liked else (200, 200, 205); cx, cy, r = 110, 960, 46 if liked else 36
    d.ellipse([cx - r, cy - r, cx, cy], fill=col); d.ellipse([cx, cy - r, cx + r, cy], fill=col); d.polygon([(cx - r, cy - r * 0.45), (cx + r, cy - r * 0.45), (cx, cy + r)], fill=col)
    d.text((180, 930), "LIKED" if liked else "like", font=font(48, True), fill=col)
    if typed:
        d.rounded_rectangle([30, 1030, 510, 1100], 16, outline=(74, 74, 244), width=4, fill=(255, 255, 255)); d.text((48, 1040), typed, font=font(44, True), fill=(20, 20, 20))
    return im

def swipe(a, b, t):
    w, h = a.size; im = Image.new("RGB", (w, h), (255, 255, 255)); dx = int(w * t); im.paste(a, (-dx, 0)); im.paste(b, (w - dx, 0)); return im

def sheet(stage):
    """0: TOYOTA COROLLA. 1: GR scribbled in front. 2: + MARKET ADJUSTMENT stamp. 3: + signatures."""
    im = Image.new("RGBA", (600, 800), (238, 236, 226, 255)); d = ImageDraw.Draw(im)
    d.text((300, 44), "VEHICLE SALES SHEET", font=font(34, True), fill=INK, anchor="mm"); d.line([30, 76, 570, 76], fill=INK, width=6)
    d.text((40, 96), "MODEL:", font=font(30, True), fill=INK)
    d.text((300, 150), "TOYOTA", font=font(60, True), fill=INK, anchor="mm"); d.text((372 if stage else 300, 228), "COROLLA", font=font(78, True), fill=INK, anchor="mm")
    if stage >= 1:
        random.seed(4); d.text((98, 226), "GR", font=font(108, True), fill=BLUE, anchor="mm")
        for i in range(7): x = random.randint(20, 120); y = random.randint(282, 296); d.line([x, y, x + random.randint(20, 60), y + random.randint(-8, 8)], fill=BLUE, width=7)
    y = 318
    for lab, val in (("MARKUP", NUMBERS["markup"]), ("APR", NUMBERS["apr"]), ("PAYMENT", NUMBERS["monthly"])):
        d.text((40, y + 14), lab + ":", font=font(32, True), fill=INK); d.text((566, y), val, font=font(58, True), fill=RED if lab != "PAYMENT" else INK, anchor="ra"); y += 74
    d.text((566, y - 4), NUMBERS["term"], font=font(28, True), fill=INK, anchor="ra")
    d.text((40, 716), "Sign: ____________", font=font(34, True), fill=INK); d.text((40, 758), "Sign again: _______", font=font(34, True), fill=INK)
    if stage >= 2:
        st = Image.new("RGBA", (420, 120), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); sd.rectangle([6, 6, 414, 114], outline=RED, width=12)
        sd.text((210, 38), "MARKET", font=font(44, True), fill=RED, anchor="mm"); sd.text((210, 84), "ADJUSTED", font=font(44, True), fill=RED, anchor="mm")
        st = st.rotate(-8, expand=True, resample=Image.BICUBIC); im.alpha_composite(st, (30, 556))
    if stage >= 3:
        random.seed(6)
        for y0, x0 in ((722, 150), (764, 250)):
            p = [(x0, y0 + 14)]
            for i in range(16): p.append((x0 + i * 18, y0 + 14 + random.randint(-22, 22)))
            d.line(p, fill=BLUE, width=7)
    return im.convert("RGB")

def bubble(text, size=(900, 300)):
    im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im); w, h = size
    d.rounded_rectangle([8, 8, w - 8, h - 70], 50, fill=(255, 255, 255, 255), outline=INK, width=12)
    d.polygon([(w * 0.3, h - 76), (w * 0.42, h - 76), (w * 0.28, h - 6)], fill=(255, 255, 255, 255), outline=INK); d.line([(w * 0.3, h - 76), (w * 0.28, h - 6), (w * 0.42, h - 76)], fill=INK, width=12)
    d.rectangle([w * 0.3 + 8, h - 84, w * 0.42 - 8, h - 68], fill=(255, 255, 255, 255))
    d.text((w // 2, (h - 70) // 2 + 4), text, font=font(92, True), fill=INK, anchor="mm"); return im

def sticker(text="GR", size=(512, 320)):
    im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im); w, h = size
    d.rounded_rectangle([6, 6, w - 6, h - 6], 40, fill=(250, 250, 250, 255), outline=INK, width=12); d.rectangle([30, 30, w - 30, h - 30], fill=(215, 15, 20, 255))
    d.text((w // 2, h // 2), text, font=font(230, True), fill=(250, 250, 250, 255), anchor="mm"); return im

def dial(mode):
    im = Image.new("RGB", (320, 200), (6, 8, 10)); d = ImageDraw.Draw(im); col = {"60:40": (90, 200, 255), "30:70": (255, 170, 40), "50:50": (240, 50, 40)}[mode]
    d.text((160, 36), "GR-FOUR", font=font(34, True), fill=(230, 230, 230), anchor="mm"); d.text((160, 112), mode, font=font(92, True), fill=col, anchor="mm")
    d.text((160, 176), {"60:40": "FRONT", "30:70": "REAR", "50:50": "TRACK"}[mode], font=font(30, True), fill=col, anchor="mm"); return im

def pump():
    im = Image.new("RGB", (300, 400), (220, 222, 226)); d = ImageDraw.Draw(im); d.rectangle([20, 20, 280, 150], fill=(10, 14, 10)); d.text((150, 85), "PREMIUM", font=font(46, True), fill=(60, 230, 110), anchor="mm")
    d.text((150, 230), "91+", font=font(90, True), fill=(200, 30, 30), anchor="mm"); d.text((150, 330), "ONLY", font=font(56, True), fill=(40, 40, 40), anchor="mm"); return im

def cover():
    im = Image.new("RGB", (512, 256), (16, 16, 18)); d = ImageDraw.Draw(im); d.rectangle([150, 60, 362, 196], fill=(215, 15, 20)); d.text((256, 128), "GR", font=font(120, True), fill=(250, 250, 250), anchor="mm"); return im

def him_hat(expr, skin):
    im = face(expr, skin); d = ImageDraw.Draw(im); d.rectangle([0, 0, 384, 96], fill=(16, 16, 18, 255)); d.rectangle([0, 96, 384, 120], fill=(40, 40, 44, 255)); d.rectangle([150, 22, 234, 78], fill=(215, 15, 20, 255)); d.text((192, 50), "GR", font=font(44, True), fill=(250, 250, 250, 255), anchor="mm"); return im

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    WHO = {"sales": ((226, 182, 150), False), "gran": ((236, 200, 176), True), "kevin": ((150, 104, 70), False), "typer": ((222, 172, 130), False), "wrxguy": ((150, 100, 62), False), "pump": ((226, 182, 150), False), "clone": ((214, 160, 118), False)}
    for who, (skin, lash) in WHO.items():
        for e in ("smug", "grin", "proud", "talk", "horror", "pinpoint", "flat", "blink", "blank", "twitch"): face(e, skin, lash).save(f"{out}/face_{who}_{e}.png")
    for e in ("blank", "twitch", "pinpoint", "horror"): him_hat(e, (214, 160, 118)).save(f"{out}/face_him_{e}.png")
    tr = card(out, "fl5", "Civic Type R", "everyone has one"); wr = card(out, "wrx", "WRX", "everyone has one"); gr = card(out, "grc", "GR Corolla", "be different")
    tr.save(f"{out}/screen_tr.png"); wr.save(f"{out}/screen_wrx.png"); gr.save(f"{out}/screen_grc.png")
    for i, t in enumerate((0.35, 0.75)): swipe(tr, wr, t).save(f"{out}/screen_sw1_{i}.png"); swipe(wr, gr, t).save(f"{out}/screen_sw2_{i}.png")
    card(out, "grc", "GR Corolla", "be different", liked=True).save(f"{out}/screen_liked.png")
    for i, t in enumerate(("dif", "differ", "different.")): card(out, "grc", "GR Corolla", "be different", liked=True, typed=t).save(f"{out}/screen_typed{i}.png")
    for s in range(4): sheet(s).save(f"{out}/sheet{s}.png")
    bubble("Corolla for Kevin?").save(f"{out}/bubble_kevin.png"); bubble("Is that the hybrid?").save(f"{out}/bubble_hybrid.png"); sticker().save(f"{out}/sticker_gr.png")
    for m in ("60:40", "30:70", "50:50"): dial(m).save(f"{out}/awd_{m.replace(':', '')}.png")
    pump().save(f"{out}/pump.png"); cover().save(f"{out}/cover.png")
    sign("NO TEST DRIVES", (236, 196, 60), (20, 20, 20), size=(1024, 192)).save(f"{out}/sign_notest.png"); sign("TOYOTA", (200, 20, 24), (250, 250, 250)).save(f"{out}/sign_toyota.png")
    sign("SUPERMARKET", (30, 110, 60), (250, 250, 240), size=(1280, 192)).save(f"{out}/sign_super.png"); sign("GAS", (200, 20, 24), (250, 250, 250), size=(512, 192)).save(f"{out}/sign_gas.png")
