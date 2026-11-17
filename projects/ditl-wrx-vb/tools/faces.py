"""Ink-drawn face decals and screen textures for the DITL WRX short (PIL). python faces.py <outdir>"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
W, H = 384, 480
INK = (18, 14, 12, 255)

def face(expr, skin=(214, 150, 96)):
    im = Image.new("RGBA", (W, H), skin + (255,))
    d = ImageDraw.Draw(im)
    ex, ey, er = (118, 266), 190, 52
    def eye(cx, rx=er, ry=er, pupil=14, look=(0, 0), lid=0.0):
        d.ellipse([cx - rx, ey - ry, cx + rx, ey + ry], fill=(250, 250, 244, 255), outline=INK, width=7)
        d.ellipse([cx + look[0] - pupil, ey + look[1] - pupil, cx + look[0] + pupil, ey + look[1] + pupil], fill=INK)
        if lid > 0:
            d.pieslice([cx - rx, ey - ry, cx + rx, ey + ry], 180, 360, fill=skin + (255,), outline=INK, width=7)
            d.rectangle([cx - rx + 4, ey - ry * (1 - lid) - 2, cx + rx - 4, ey - 2 + ry * (lid * 2 - 1) * 0], fill=skin + (255,))
            d.line([cx - rx, ey - ry * (1 - 2 * lid) * 0.2, cx + rx, ey - ry * (1 - 2 * lid) * 0.2], fill=INK, width=7)
    def brow(cx, tilt, y=110):
        d.line([cx - 50, y + tilt, cx + 50, y - tilt], fill=INK, width=10)
    def teeth(box, n=6):
        x0, y0, x1, y1 = box
        for i in range(1, n):
            x = x0 + (x1 - x0) * i / n
            d.line([x, y0, x, y1], fill=INK, width=4)
    if expr == "smug":
        for cx in ex: eye(cx, ry=40, pupil=13, look=(14, 6), lid=0.55)
        brow(ex[0], -14); brow(ex[1], 22, y=96)
        d.arc([110, 300, 300, 400], 20, 150, fill=INK, width=9)
        d.line([292, 352, 310, 336], fill=INK, width=8)
    elif expr == "grin":
        for cx in ex: eye(cx, pupil=12)
        brow(ex[0], -10, 100); brow(ex[1], 10, 100)
        d.chord([86, 270, 298, 440], 0, 180, fill=(250, 250, 244, 255), outline=INK, width=8)
        d.line([86, 355, 298, 355], fill=INK, width=8); teeth((100, 356, 284, 420), 7)
    elif expr == "horror":
        for cx in ex: eye(cx, rx=60, ry=66, pupil=6)
        brow(ex[0], 26, 92); brow(ex[1], -26, 92)
        for k in range(3): d.arc([70 + k * 12, 40 + k * 10, 314 - k * 12, 110 + k * 10], 200, 340, fill=INK, width=4)
        d.rounded_rectangle([120, 318, 264, 462], 46, fill=(40, 8, 8, 255), outline=INK, width=8)
        d.rectangle([134, 322, 250, 346], fill=(250, 250, 244, 255), outline=INK, width=4); teeth((134, 322, 250, 346), 6)
        for cx in (84, 300): d.line([cx, 270, cx - 6, 310], fill=(120, 190, 235, 255), width=7)
    elif expr == "flat":
        for cx in ex: eye(cx, ry=30, pupil=12, lid=0.5)
        d.line([150, 370, 236, 370], fill=INK, width=9)
    elif expr == "blank":
        for cx in ex: eye(cx, pupil=12)
        d.line([156, 372, 228, 372], fill=INK, width=9)
    elif expr == "twitch":
        eye(ex[0], pupil=9); eye(ex[1], ry=34, pupil=9, lid=0.4)
        brow(ex[0], 16, 100); brow(ex[1], -6, 104)
        d.line([150, 380, 190, 368, 236, 384], fill=INK, width=9)
    d.line([192, 222, 180, 290, 204, 294], fill=INK, width=6)  # nose
    return im

def font(sz, bold=False):
    return ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-%s.otf" % ("Bold" if bold else "Regular"), sz)

def checkout(balance=False):
    im = Image.new("RGB", (540, 1110), (255, 255, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 540, 70], fill=(245, 245, 247)); d.text((24, 20), "Checkout", font=font(28, True), fill=(20, 20, 20))
    d.text((440, 24), "Secure", font=font(20), fill=(110, 110, 110))
    if balance:
        d.ellipse([200, 150, 340, 290], outline=(30, 160, 90), width=10); d.line([236, 222, 262, 250, 308, 194], fill=(30, 160, 90), width=12)
        d.text((270, 340), "Order confirmed", font=font(40, True), fill=(20, 20, 20), anchor="mm")
        d.rounded_rectangle([30, 430, 510, 700], 24, fill=(74, 74, 244))
        d.text((270, 490), "Affirm balance", font=font(30), fill=(255, 255, 255), anchor="mm")
        d.text((270, 580), "$115,000.00", font=font(72, True), fill=(255, 255, 255), anchor="mm")
        d.text((270, 655), "30% APR", font=font(30, True), fill=(255, 255, 255), anchor="mm")
        return im
    items = [("Front Bumper – Subaru WRX (VB 2022+)", "Front Bumper w/ Fog Lights", "$2,000.00"),
             ("Rear Bumper – Subaru WRX (VB 2022+)", "", "$1,500.00"),
             ("Side Skirts – Subaru WRX (VB, 2022+)", "ACM", "$800.00"),
             ("WRC Wing – Subaru WRX/STI (VB, 2022+)", "Plastic Composite / World Rally Blue Pearl - K7X", "$1,150.00")]
    y = 92
    for t, v, p in items:
        d.rounded_rectangle([20, y, 96, y + 76], 10, fill=(228, 232, 240), outline=(200, 204, 212))
        d.text((110, y + 4), t, font=font(19, True), fill=(20, 20, 20)); d.text((110, y + 32), v[:44], font=font(15), fill=(110, 110, 110))
        d.text((520, y + 52), p, font=font(21, True), fill=(20, 20, 20), anchor="ra"); y += 98
    d.line([20, y, 520, y], fill=(220, 220, 220), width=2)
    d.text((24, y + 16), "Subtotal", font=font(26), fill=(20, 20, 20)); d.text((520, y + 16), "$5,450.00", font=font(28, True), fill=(20, 20, 20), anchor="ra")
    y += 80; d.text((24, y), "Payment", font=font(22, True), fill=(20, 20, 20)); y += 40
    d.rounded_rectangle([20, y, 520, y + 150], 16, outline=(74, 74, 244), width=4, fill=(244, 244, 255))
    d.ellipse([40, y + 26, 68, y + 54], outline=(74, 74, 244), width=4); d.ellipse([47, y + 33, 61, y + 47], fill=(74, 74, 244))
    d.text((86, y + 20), "affirm", font=font(40, True), fill=(20, 20, 20)); d.text((86, y + 78), "Pay over time", font=font(22), fill=(90, 90, 90))
    d.text((500, y + 76), "30% APR", font=font(44, True), fill=(200, 30, 30), anchor="rm")
    y += 190; d.rounded_rectangle([20, y, 520, y + 110], 22, fill=(20, 150, 80)); d.text((270, y + 55), "Confirm", font=font(48, True), fill=(255, 255, 255), anchor="mm")
    return im

def roundel():
    im = Image.new("RGBA", (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([4, 4, 252, 252], fill=(20, 20, 20, 255)); d.ellipse([44, 44, 212, 212], fill=(255, 255, 255, 255))
    d.pieslice([44, 44, 212, 212], 180, 270, fill=(30, 110, 200, 255)); d.pieslice([44, 44, 212, 212], 0, 90, fill=(30, 110, 200, 255))
    return im

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for who, skin in (("beamer", (222, 172, 130)), ("him", (150, 100, 62))):
        for e in ("smug", "grin", "horror", "flat", "blank", "twitch"): face(e, skin).save(f"{out}/face_{who}_{e}.png")
    checkout().save(f"{out}/screen_checkout.png"); checkout(True).save(f"{out}/screen_balance.png"); roundel().save(f"{out}/roundel.png")
