"""Phone screens and props for the track-guy short (PIL). python screens.py <texdir>
Product text is the live store listing, checked 2026-11-19: '[BACKORDER] TC Wing - Honda Civic Type R/Sport FK7/FK8', 66.5", $1,200.00.
The store is generic and unbranded (series rule)."""
import sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from faces import font, phone_base

TITLE = ("[BACKORDER] TC Wing -", "Honda Civic Type R/Sport FK7/FK8"); VARIANT = '[BACKORDER] 66.5"'; PRICE = "$1,200.00"


def signup(hover=False):
    im = Image.new("RGB", (540, 1110), (18, 20, 26)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 540, 70], fill=(30, 34, 44)); d.text((24, 20), "Events", font=font(28, True), fill=(240, 240, 240))
    d.rectangle([0, 70, 540, 420], fill=(40, 46, 60))
    for i in range(10): d.rectangle([i * 54, 330, i * 54 + 27, 357], fill=(235, 235, 235) if i % 2 == 0 else (20, 20, 20))   # chequered flag stripe
    d.text((270, 170), "OPEN TRACK DAY", font=font(52, True), fill=(255, 255, 255), anchor="mm")
    d.text((270, 240), "Novice group", font=font(34), fill=(200, 205, 215), anchor="mm")
    d.text((30, 470), "No experience needed!", font=font(32, True), fill=(240, 240, 240))
    d.text((30, 525), "Helmet required.", font=font(28), fill=(170, 175, 185)); d.text((30, 570), "Instructor in your car.", font=font(28), fill=(170, 175, 185))
    d.text((30, 615), "Spots left: plenty.", font=font(28), fill=(170, 175, 185))
    y = 880; d.rounded_rectangle([30, y, 510, y + 130], 26, fill=(255, 210, 40) if hover else (230, 60, 40))
    d.text((270, y + 65), "REGISTER", font=font(60, True), fill=(20, 20, 20) if hover else (255, 255, 255), anchor="mm")
    return im


def cart(pressed=False):
    im, d = phone_base("Cart")
    th = Image.open(os.path.join(TEX, "thumb_tcwing.png")).convert("RGB").resize((480, 480)); im.paste(th, (30, 100)); d.rectangle([30, 100, 510, 580], outline=(210, 210, 215), width=3)
    d.text((30, 605), TITLE[0], font=font(40, True), fill=(20, 20, 20)); d.text((30, 655), TITLE[1], font=font(28), fill=(40, 40, 40))
    d.text((30, 702), VARIANT, font=font(24), fill=(110, 110, 110)); d.text((30, 760), PRICE, font=font(84, True), fill=(20, 20, 20))
    y = 930; d.rounded_rectangle([30, y, 510, y + 120], 24, fill=(10, 90, 46) if pressed else (20, 150, 80))
    d.text((270, y + 60), "Confirm", font=font(56, True), fill=(255, 255, 255), anchor="mm")
    if pressed: d.text((270, y - 40), "cha-ching!", font=font(32, True), fill=(20, 150, 80), anchor="mm")
    return im


def weather():
    im = Image.new("RGB", (540, 1110), (70, 130, 210)); d = ImageDraw.Draw(im)
    for i in range(1110): d.line([0, i, 540, i], fill=(70 - i // 40, 130 - i // 25, 210 - i // 20))
    d.text((270, 120), "Today", font=font(46, True), fill=(255, 255, 255), anchor="mm")
    # one single small cloud, mostly sun
    d.ellipse([170, 230, 370, 430], fill=(255, 214, 60))
    for cx, cy, r in ((300, 420, 52), (350, 400, 64), (405, 425, 48)): d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 252))
    d.rectangle([250, 420, 455, 472], fill=(250, 250, 252))
    d.text((270, 560), "Mostly sunny", font=font(48, True), fill=(255, 255, 255), anchor="mm")
    d.text((270, 625), "one (1) cloud", font=font(34), fill=(225, 235, 250), anchor="mm")
    return im


def timer(text, running=True):
    im = Image.new("RGB", (540, 1110), (8, 8, 10)); d = ImageDraw.Draw(im)
    d.text((270, 120), "LAP TIMER", font=font(40, True), fill=(255, 210, 40), anchor="mm")
    d.text((270, 520), text, font=font(150, True), fill=(255, 255, 255), anchor="mm")
    d.text((270, 680), "LAP 1" if running else "NO LAPS", font=font(44, True), fill=(160, 160, 170), anchor="mm")
    d.ellipse([235, 880, 305, 950], fill=(230, 40, 40) if running else (70, 70, 74))
    return im


def plaque(text, size=(256, 96)):
    im = Image.new("RGB", size, (196, 160, 70)); d = ImageDraw.Draw(im); d.rectangle([4, 4, size[0] - 5, size[1] - 5], outline=(90, 70, 20), width=4)
    d.text((size[0] // 2, size[1] // 2), text, font=font(34 if len(text) < 10 else 26, True), fill=(40, 30, 10), anchor="mm"); return im


if __name__ == "__main__":
    TEX = sys.argv[1]
    signup().save(f"{TEX}/screen_signup.png"); signup(True).save(f"{TEX}/screen_signup_hover.png")
    cart().save(f"{TEX}/screen_cart.png"); cart(True).save(f"{TEX}/screen_cart_pressed.png")
    weather().save(f"{TEX}/screen_weather.png")
    for s in range(0, 100):   # walking-pace timer: 0:00 .. 0:99 tenths shown as m:ss
        timer(f"0:{s:02d}").save(f"{TEX}/timer_{s:03d}.png")
    timer("--:--", False).save(f"{TEX}/timer_none.png")
    plaque("ATTENDEE").save(f"{TEX}/plaque_attendee.png"); plaque("BOWLING").save(f"{TEX}/plaque_bowling.png")
    plaque("DRIVERS' MTG", (256, 96)).save(f"{TEX}/plaque_mtg.png")
else:
    TEX = "/home/user/media/ditl-time-attack-larper/tex"
