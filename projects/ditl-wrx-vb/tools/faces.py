"""Ink-drawn face decals, screens and props for the DITL WRX short (PIL). python faces.py <outdir>"""
import sys, os, random
from PIL import Image, ImageDraw, ImageFont
W, H = 384, 480
INK = (18, 14, 12, 255); WHT = (250, 250, 244, 255)

def font(sz, bold=False):
    return ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-%s.otf" % ("Bold" if bold else "Regular"), sz)

def face(expr, skin=(214, 150, 96), lashes=False):
    im = Image.new("RGBA", (W, H), skin + (255,)); d = ImageDraw.Draw(im); sk = skin + (255,)
    ex, ey, er = (118, 266), 190, 52
    def eye(cx, rx=er, ry=er, pupil=14, look=(0, 0), lid=0.0):
        d.ellipse([cx - rx, ey - ry, cx + rx, ey + ry], fill=WHT, outline=INK, width=7)
        d.ellipse([cx + look[0] - pupil, ey + look[1] - pupil, cx + look[0] + pupil, ey + look[1] + pupil], fill=INK)
        if lid > 0:
            yl = ey - ry + 2 * ry * lid
            d.chord([cx - rx, ey - ry, cx + rx, ey + ry], 180, 360, fill=sk, outline=INK, width=7)
            d.rectangle([cx - rx + 6, min(ey - 4, yl), cx + rx - 6, max(ey - 4, yl)], fill=sk) if yl > ey - 4 else None; d.line([cx - rx, yl, cx + rx, yl], fill=INK, width=7)
        if lashes:
            for k in (-1, 0, 1): d.line([cx + k * 26, ey - ry + 4, cx + k * 34, ey - ry - 18], fill=INK, width=5)
    def closed(cx, up=True):
        d.arc([cx - 46, ey - 30, cx + 46, ey + 40], 200 if up else 20, 340 if up else 160, fill=INK, width=9)
    def brow(cx, tilt, y=110): d.line([cx - 50, y + tilt, cx + 50, y - tilt], fill=INK, width=10)
    def teeth(box, n=6):
        x0, y0, x1, y1 = box
        for i in range(1, n): x = x0 + (x1 - x0) * i / n; d.line([x, y0, x, y1], fill=INK, width=4)
    def nose(): d.line([192, 222, 180, 290, 204, 294], fill=INK, width=6)
    if expr == "smug":
        for cx in ex: eye(cx, ry=40, pupil=13, look=(14, 8), lid=0.45)
        brow(ex[0], -14); brow(ex[1], 22, y=96); d.arc([110, 300, 300, 400], 20, 150, fill=INK, width=9); d.line([292, 352, 310, 336], fill=INK, width=8)
    elif expr == "grin":
        for cx in ex: eye(cx, pupil=12)
        brow(ex[0], -10, 100); brow(ex[1], 10, 100)
        d.chord([86, 270, 298, 440], 0, 180, fill=WHT, outline=INK, width=8); d.line([86, 355, 298, 355], fill=INK, width=8); teeth((100, 356, 284, 420), 7)
    elif expr == "proud":
        for cx in ex: closed(cx)
        brow(ex[0], -8, 104); brow(ex[1], 8, 104); d.line([296, 200, 304, 250], fill=(120, 190, 235, 255), width=8)
        d.chord([96, 280, 288, 430], 0, 180, fill=WHT, outline=INK, width=8); d.line([96, 355, 288, 355], fill=INK, width=8); teeth((108, 356, 276, 414), 6)
    elif expr == "talk":
        for cx in ex: eye(cx, ry=44, pupil=13, look=(10, 4), lid=0.3)
        brow(ex[0], -12); brow(ex[1], 16, y=98); d.ellipse([140, 330, 250, 420], fill=(40, 8, 8, 255), outline=INK, width=8); d.rectangle([158, 334, 232, 350], fill=WHT)
    elif expr == "horror":
        for cx in ex: eye(cx, rx=60, ry=66, pupil=6)
        brow(ex[0], 26, 92); brow(ex[1], -26, 92)
        for k in range(3): d.arc([70 + k * 12, 40 + k * 10, 314 - k * 12, 110 + k * 10], 200, 340, fill=INK, width=4)
        d.rounded_rectangle([120, 318, 264, 462], 46, fill=(40, 8, 8, 255), outline=INK, width=8)
        d.rectangle([134, 322, 250, 346], fill=WHT, outline=INK, width=4); teeth((134, 322, 250, 346), 6)
        for cx in (84, 300): d.line([cx, 270, cx - 6, 310], fill=(120, 190, 235, 255), width=7)
    elif expr == "pinpoint":
        for cx in ex: eye(cx, rx=58, ry=60, pupil=5)
        brow(ex[0], 18, 96); brow(ex[1], -18, 96); d.ellipse([172, 366, 212, 402], fill=(40, 8, 8, 255), outline=INK, width=7)
    elif expr == "flat":
        for cx in ex: eye(cx, ry=30, pupil=12, lid=0.4)
        d.line([150, 370, 236, 370], fill=INK, width=9)
    elif expr == "blink":
        for cx in ex: d.line([cx - 46, ey, cx + 46, ey], fill=INK, width=9)
        d.line([150, 370, 236, 370], fill=INK, width=9)
    elif expr == "blank":
        for cx in ex: eye(cx, pupil=12)
        brow(ex[0], 4, 104); brow(ex[1], -4, 104); d.line([156, 372, 228, 372], fill=INK, width=9)
    elif expr == "twitch":
        eye(ex[0], pupil=9); eye(ex[1], ry=34, pupil=9, lid=0.35)
        brow(ex[0], 16, 100); brow(ex[1], -6, 104); d.line([150, 380, 190, 368, 236, 384], fill=INK, width=9)
    elif expr == "squish":
        d.ellipse([20, 150, 170, 250], fill=WHT, outline=INK, width=7); d.ellipse([210, 130, 370, 240], fill=WHT, outline=INK, width=7)
        d.ellipse([110, 190, 136, 216], fill=INK); d.ellipse([230, 176, 256, 202], fill=INK)
        d.ellipse([130, 250, 270, 330], outline=INK, width=7, fill=tuple(min(255, c + 25) for c in skin) + (255,))
        d.ellipse([60, 340, 330, 450], fill=(200, 90, 100, 255), outline=INK, width=8); d.line([70, 395, 320, 395], fill=INK, width=6)
        return im
    nose(); return im

def paper(title, lines, scrib=0, size=(600, 800)):
    im = Image.new("RGB", size, (246, 244, 236)); d = ImageDraw.Draw(im)
    d.text((size[0] // 2, 70), title, font=font(46, True), fill=(20, 20, 20), anchor="mm"); d.line([40, 115, size[0] - 40, 115], fill=(20, 20, 20), width=4)
    y = 160
    for ln in lines: d.text((50, y), ln, font=font(30), fill=(40, 40, 40)); y += 70
    if scrib:
        random.seed(3); f = font(92, True)
        d.text((60, 300), "GED", font=f, fill=(20, 40, 160))
        if scrib > 1: d.text((60, 420), "pending", font=f, fill=(20, 40, 160))
        for i in range(10 * scrib):
            x, y0 = random.randint(30, 520), random.randint(280, 760); d.line([x, y0, x + random.randint(-90, 90), y0 + random.randint(-50, 50)], fill=(20, 40, 160), width=7)
    return im

def scribble():
    im = Image.new("RGBA", (512, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(im); random.seed(8); p = [(20, 128)]
    for i in range(40): p.append((20 + i * 12, 128 + random.randint(-90, 90)))
    d.line(p, fill=(20, 40, 160, 255), width=9); return im

def sign(text, bg, fg, size=(768, 192)):
    im = Image.new("RGB", size, bg); ImageDraw.Draw(im).text((size[0] // 2, size[1] // 2), text, font=font(int(size[1] * 0.5), True), fill=fg, anchor="mm"); return im

def phone_base(title="Checkout"):
    im = Image.new("RGB", (540, 1110), (255, 255, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 540, 70], fill=(245, 245, 247)); d.text((24, 20), title, font=font(28, True), fill=(20, 20, 20)); d.text((440, 24), "Secure", font=font(20), fill=(110, 110, 110))
    return im, d

ITEMS = [("part_front_bumper", "Front Bumper – Subaru WRX (VB 2022+)", "Front Bumper w/ Fog Lights", "$2,000.00"),
         ("part_rear_bumper", "Rear Bumper – Subaru WRX (VB 2022+)", "", "$1,500.00"),
         ("part_side_skirts", "Side Skirts – Subaru WRX (VB, 2022+)", "ACM", "$800.00"),
         ("part_wrc_wing", "WRC Wing – Subaru WRX/STI (VB, 2022+)", "Plastic Composite / World Rally Blue Pearl - K7X", "$1,150.00")]

def thumb(out, part, sz):
    p = f"{out}/thumb_{part}.png"
    return Image.open(p).convert("RGB").resize((sz, sz)) if os.path.exists(p) else Image.new("RGB", (sz, sz), (228, 232, 240))

def item_card(out, i):
    part, t, v, p = ITEMS[i]; im, d = phone_base("Cart")
    im.paste(thumb(out, part, 480), (30, 110)); d.rectangle([30, 110, 510, 590], outline=(210, 210, 215), width=3)
    a, b = t.split(" – "); d.text((30, 620), a, font=font(46, True), fill=(20, 20, 20)); d.text((30, 680), b, font=font(30), fill=(40, 40, 40))
    d.text((30, 730), v[:40], font=font(22), fill=(110, 110, 110)); d.text((30, 800), p, font=font(84, True), fill=(20, 20, 20))
    d.rounded_rectangle([30, 940, 510, 1040], 20, fill=(20, 20, 20)); d.text((270, 990), "Added to cart ✓", font=font(36, True), fill=(255, 255, 255), anchor="mm"); return im

def checkout(out, pressed=False, balance=False):
    im, d = phone_base()
    if balance:
        d.ellipse([200, 130, 340, 270], outline=(30, 160, 90), width=10); d.line([236, 202, 262, 230, 308, 174], fill=(30, 160, 90), width=12)
        d.text((270, 320), "Order confirmed", font=font(40, True), fill=(20, 20, 20), anchor="mm")
        d.rounded_rectangle([30, 400, 510, 700], 24, fill=(74, 74, 244)); d.text((270, 460), "Affirm balance", font=font(32), fill=(255, 255, 255), anchor="mm")
        d.text((270, 555), "$115,000.00", font=font(76, True), fill=(255, 255, 255), anchor="mm"); d.text((270, 645), "30% APR", font=font(34, True), fill=(255, 255, 255), anchor="mm"); return im
    y = 92
    for part, t, v, p in ITEMS:
        im.paste(thumb(out, part, 76), (20, y)); d.text((110, y + 4), t, font=font(19, True), fill=(20, 20, 20)); d.text((110, y + 32), v[:44], font=font(15), fill=(110, 110, 110))
        d.text((520, y + 52), p, font=font(21, True), fill=(20, 20, 20), anchor="ra"); y += 98
    d.line([20, y, 520, y], fill=(220, 220, 220), width=2); d.text((24, y + 16), "Subtotal", font=font(26), fill=(20, 20, 20)); d.text((520, y + 16), "$5,450.00", font=font(28, True), fill=(20, 20, 20), anchor="ra")
    y += 80; d.text((24, y), "Payment", font=font(22, True), fill=(20, 20, 20)); y += 40
    d.rounded_rectangle([20, y, 520, y + 150], 16, outline=(74, 74, 244), width=4, fill=(244, 244, 255))
    d.ellipse([40, y + 26, 68, y + 54], outline=(74, 74, 244), width=4); d.ellipse([47, y + 33, 61, y + 47], fill=(74, 74, 244))
    d.text((86, y + 20), "affirm", font=font(40, True), fill=(20, 20, 20)); d.text((86, y + 78), "Pay over time", font=font(22), fill=(90, 90, 90)); d.text((500, y + 76), "30% APR", font=font(44, True), fill=(200, 30, 30), anchor="rm")
    y += 190; d.rounded_rectangle([20, y, 520, y + 110], 22, fill=(10, 90, 46) if pressed else (20, 150, 80)); d.text((270, y + 55), "Confirm", font=font(48, True), fill=(255, 255, 255), anchor="mm")
    if pressed: d.text((270, y + 150), "cha-ching!", font=font(30, True), fill=(20, 150, 80), anchor="mm")
    return im

def accessport(state):
    im = Image.new("RGB", (320, 480), (6, 8, 10)); d = ImageDraw.Draw(im)
    if state == "off": return im
    val, col = ("1.00", (60, 230, 110)) if state == "ok" else ("0.88", (240, 50, 40))
    d.text((160, 44), "COBB", font=font(40, True), fill=(230, 230, 230), anchor="mm"); d.text((160, 86), "ACCESSPORT", font=font(22), fill=(160, 160, 160), anchor="mm")
    d.arc([40, 130, 280, 370], 150, 390, fill=(50, 54, 60), width=22); d.arc([40, 130, 280, 370], 150, 390 if state == "ok" else 330, fill=col, width=22)
    d.text((160, 250), val, font=font(84, True), fill=col, anchor="mm"); d.text((160, 330), "DAM", font=font(40, True), fill=(230, 230, 230), anchor="mm")
    if state != "ok": d.rectangle([20, 400, 300, 460], fill=(240, 50, 40)); d.text((160, 430), "KNOCK", font=font(36, True), fill=(255, 255, 255), anchor="mm")
    return im

def badge(kind):
    im = Image.new("RGBA", (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "roundel":
        d.ellipse([4, 4, 252, 252], fill=(20, 20, 20, 255)); d.ellipse([44, 44, 212, 212], fill=(255, 255, 255, 255))
        d.pieslice([44, 44, 212, 212], 180, 270, fill=(30, 110, 200, 255)); d.pieslice([44, 44, 212, 212], 0, 90, fill=(30, 110, 200, 255))
    else:
        d.rounded_rectangle([20, 30, 236, 226], 40, fill=(215, 215, 220, 255), outline=(60, 60, 60, 255), width=10); d.text((128, 128), "H", font=font(170, True), fill=(60, 60, 60, 255), anchor="mm")
    return im

def mirror_bg():
    im = Image.new("RGB", (720, 250), (26, 26, 30)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([70, 40, 650, 215], 26, fill=(150, 190, 240)); d.rectangle([70, 150, 650, 215], fill=(120, 124, 130))
    d.rectangle([70, 178, 650, 215], fill=(14, 60, 170)); d.rectangle([150, 118, 570, 136], fill=(20, 20, 24))
    for x in (150, 556): d.rectangle([x, 118, x + 16, 180], fill=(14, 60, 170))
    for x in (260, 360, 460): d.rectangle([x, 136, x + 8, 180], fill=(14, 60, 170))
    for x in (40, 668): d.rectangle([x, 0, x + 26, 250], fill=(16, 16, 18))
    return im

def tags():
    im = Image.new("RGB", (256, 400), (170, 172, 176)); d = ImageDraw.Draw(im)
    for i, t in enumerate(("RINGLAND", "J. T.", "O POS", "USMC", "NO PREF")): d.text((128, 70 + i * 62), t, font=font(34, True), fill=(60, 62, 66), anchor="mm")
    return im

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    WHO = {"lady": ((226, 182, 150), True), "recruiter": ((126, 84, 58), False), "beamer": ((222, 172, 130), False), "mom": ((236, 196, 168), True), "kid": ((236, 196, 168), False), "him": ((150, 100, 62), False)}
    for who, (skin, lash) in WHO.items():
        for e in ("smug", "grin", "proud", "talk", "horror", "pinpoint", "flat", "blink", "blank", "twitch", "squish"): face(e, skin, lash).save(f"{out}/face_{who}_{e}.png")
    paper("WITHDRAWAL FORM", ["Student: ______________", "Reason for leaving:", "   “gonna buy a WRX”", "Parent signature: ______", "", "[ ] I understand this is", "    a bad idea"]).save(f"{out}/form_withdraw.png")
    for s in (0, 1, 2): paper("ENLISTMENT", ["DIPLOMA:  [   ]", "", "", "", "", "", "Sign here: ___________"], s).save(f"{out}/form_enlist{s}.png")
    scribble().save(f"{out}/scribble.png")
    sign("FRONT OFFICE", (30, 60, 110), (240, 240, 230)).save(f"{out}/sign_office.png"); sign("RECRUITING", (150, 20, 24), (236, 196, 60)).save(f"{out}/sign_recruit.png")
    for i in range(4): item_card(out, i).save(f"{out}/screen_item{i}.png")
    checkout(out).save(f"{out}/screen_checkout.png"); checkout(out, pressed=True).save(f"{out}/screen_pressed.png"); checkout(out, balance=True).save(f"{out}/screen_balance.png")
    for s in ("off", "ok", "bad"): accessport(s).save(f"{out}/ap_{s}.png")
    mirror_bg().save(f"{out}/mirror_bg.png"); badge("roundel").save(f"{out}/roundel.png"); badge("h").save(f"{out}/hbadge.png"); tags().save(f"{out}/tags.png")
