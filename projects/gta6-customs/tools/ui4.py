"""v4 menu states (user, v3 review): every part on its own camera, Epsilon branding, painted-part prices, live wallet.

Changes from ui3: Front Lip on the second capture's front-bumper camera (F) and Side Skirts on its side camera (D);
the parts carry an EPSILON+ badge in the game's badge style and "Epsilon ..." names; prices are the catalogue's
for parts painted Sonic Gray Pearl (the car's colour), since the parts arrive paint matched; no amount is baked into
the wallet (compose4 draws it per frame so it can count down).

v3 notes: parts, respray, suspension, wheels, exit.

Views: M list (first capture), E exhaust angle (second capture, used for the rear lip), A rear view (first capture,
wing), respray on the first capture's option-screen frames with the second capture's swatch block laid over,
S suspension and W wheel close-up (second capture). Epsilon parts carry catalogue prices; the respray (free in
the capture), the lowered suspension kit ($750) and the rims ($560) keep the game's own prices and stat changes.
Each state is {"img": frame with the state's panels, "rects": what to paste from it, "overlay": BGRA drawn over the car}.
"""
import sys
from pathlib import Path
import cv2, numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import ui as U
from ui import box, erase, draw, retitle, car_tag, wallet, money, OSW, LEX, OSW_SQ, CAP, S

VID_B = "/home/user/media/gta6-customs/capture/gta6_customization_B_1440p.mp4"
# catalogue (Epsilon-Site showroom/catalog/products.json, 2026-10-03), variant "Sonic Gray Pearl - NH877P" = painted to match
PRICES = {"Front Lip": 485, "Side Skirts": 800, "Rear Lip": 485, "Sport Wing": 850}; GAME = {"Suspension": 750, "Wheels": 560}
ROWS = ["Front Lip", "Side Skirts", "Rear Lip", "Sport Wing"]      # plain names on the list (user, v6 review); the part screens carry the Epsilon name and badge
BADGE_BGR, BADGE_INK = (253, 225, 106), (75, 54, 33)        # the game's "EXCLUSIVE" badge colours (second capture, frame 2100)
TOTAL = sum(PRICES.values()) + sum(GAME.values())
R = lambda *a: box(*a)
RECTS = {"M": [R(0, 150, 640, 760), R(1466, 915, 1894, 998), R(1730, 20, 1905, 80)],
         "A": [R(0, 0, 640, 130), R(0, 840, 640, 1066), R(1466, 520, 1894, 996), R(1730, 20, 1905, 80)],
         "E": [R(0, 0, 640, 130), R(0, 840, 640, 1066), R(1466, 520, 1894, 996), R(1730, 20, 1905, 80)],
         "P": [R(0, 0, 640, 130), R(0, 790, 1080, 1066), R(1466, 520, 1894, 996), R(1730, 20, 1905, 80)],
         "S": [R(0, 0, 640, 130), R(0, 795, 470, 1066), R(1466, 520, 1894, 996), R(1730, 20, 1905, 80), R(815, 1008, 1105, 1052)],
         "W": [R(0, 0, 640, 130), R(0, 1005, 420, 1066), R(20, 765, 430, 815), R(1466, 915, 1894, 998), R(1730, 20, 1905, 80)]}
STATUS = box(10, 1014, 340, 1060)


def price(img, text):
    x0, y0, x1, y1 = box(122, 846, 240, 894)
    g = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY); br = g > np.median(g) + 40
    ys, xs = np.nonzero(br); col = np.percentile(img[y0:y1, x0:x1][br].reshape(-1, 3), 70, 0)
    m = np.zeros(img.shape[:2], np.uint8); m[y0:y1, x0:x1] = 255
    img[:] = cv2.inpaint(img, m, 7, cv2.INPAINT_TELEA)
    size = (ys.max() - ys.min() + 1) / CAP[OSW]
    for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2), (-2, -2), (2, -2), (-2, 2)):
        draw(img, text, (x0 + xs.min() + ox, y0 + ys.max() + 1 + oy), OSW, size, (28, 28, 30))
    draw(img, text, (x0 + xs.min(), y0 + ys.max() + 1), OSW, size, col)


def wallet_clear(img):
    """Paint the capture's wallet figure out; compose4 draws the live amount."""
    x0, y0, x1, y1 = 2330, 30, 2468, 82
    g = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY).astype(np.float32)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23))
    m = (g - cv2.morphologyEx(g, cv2.MORPH_OPEN, k) > 40) | (cv2.morphologyEx(g, cv2.MORPH_CLOSE, k) - g > 60)
    full = np.zeros(img.shape[:2], np.uint8); full[y0:y1, x0:x1] = cv2.dilate(m.astype(np.uint8), np.ones((7, 7), np.uint8)) * 255
    img[:] = cv2.inpaint(img, full, 5, cv2.INPAINT_TELEA)


def wallet_text(img, amount):
    text = money(int(round(amount))); size = 34.0
    from PIL import ImageFont
    wid = ImageFont.truetype(OSW, int(size * 4)).getlength(text) / 4
    x = 2462 - wid; base = 70
    for ox in range(-3, 4):
        for oy in range(-3, 4):
            if ox * ox + oy * oy <= 10 and (ox or oy):
                draw(img, text, (x + ox, base + oy), OSW, size, (24, 26, 24))
    draw(img, text, (x, base), OSW, size, (250, 250, 250))


def badge(img, x=43, y=1064):
    """EPSILON+ in the game's badge style, above the price row."""
    from PIL import ImageFont
    size = 33.0; w = int(ImageFont.truetype(OSW, int(size * 4)).getlength("EPSILON+") / 4 * OSW_SQ) + 22
    cv2.rectangle(img, (x, y), (x + w, y + 50), BADGE_BGR, -1)
    draw(img, "EPSILON+", (x + 11, y + 39), OSW, size, BADGE_INK, OSW_SQ)


def clear_status(img):
    x0, y0, x1, y1 = STATUS
    m = np.zeros(img.shape[:2], np.uint8); m[y0 + 4:y1 - 2, x0 + 6:x1] = 255
    img[:] = cv2.inpaint(img, m, 6, cv2.INPAINT_TELEA)


def build(frameA, frameB):
    none = frameA(340)
    # "Applied" with its tick, lifted from the first capture's "None" option as glyphs (not as a rectangle of floor)
    x0, y0, x1, y1 = STATUS
    g = cv2.cvtColor(none[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
    am = cv2.GaussianBlur(cv2.dilate((g > 150).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 0.8)[..., None]
    apx = none[y0:y1, x0:x1].astype(np.float32)

    def applied(img):
        clear_status(img)
        img[y0:y1, x0:x1] = (img[y0:y1, x0:x1] * (1 - am) + apx * am).astype(np.uint8)

    def panel_from_A(img):
        px0, py0, px1, py1 = box(1466, 520, 1894, 996)
        img[py0:py1, px0:px1] = none[py0:py1, px0:px1]

    st = {}
    p = PRICES; cash = TOTAL
    U.ROWS = ROWS; M = U.Menu(frameA)
    m0 = M.render(1, [], 0); wallet_clear(m0); st["m0"] = {"img": m0, "view": "M"}

    def part(base, name, c, done, view):
        img = base.copy()
        retitle(img, box(30, 68, 420, 110), name.upper(), OSW, None, OSW_SQ)
        retitle(img, box(30, 902, 420, 940), "EPSILON " + name.upper(), OSW, None, OSW_SQ)
        price(img, money(PRICES[name])); badge(img)
        retitle(img, box(76, 955, 105, 990), "1", LEX, None, thr=20); retitle(img, box(128, 955, 165, 990), "1", LEX, None, thr=14)
        applied(img) if done else clear_status(img)
        panel_from_A(img); car_tag(img, 555); wallet_clear(img)
        return {"img": img, "view": view}
    eb = frameB(17960)

    def block_overlay(name, done):
        """A part's option block as a layer (BGRA) for screens that have none of their own: built on the exhaust
        screen, then everything that differs from the floor behind it is kept."""
        full = part(eb, name, 0, done, "E")["img"]
        x0, y0, x1, y1 = box(0, 785, 640, 1066)
        reg = full[y0:y1, x0:x1]
        floor = cv2.medianBlur(reg, 151)
        d = np.abs(reg.astype(np.float32) - floor).max(2)
        al = np.clip((d - 26) / 30.0, 0, 1); al = cv2.GaussianBlur(cv2.morphologyEx(al, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)), (0, 0), 0.6)
        lay = np.zeros(full.shape[:2] + (4,), np.float32); lay[y0:y1, x0:x1, :3] = reg; lay[y0:y1, x0:x1, 3] = al * 255
        return lay

    def own_cam(base, name, done, view, small_base, big_base):
        """Front Lip / Side Skirts on the second capture's front and side cameras: title re-set, block as a layer."""
        img = base.copy()
        erase(img, box(22, 28, 262, 64), thr=16); erase(img, box(22, 66, 430, 112), thr=24)
        draw(img, "BODYWORK /", (45, small_base), OSW, 31, (150, 150, 158), OSW_SQ)
        draw(img, name.upper(), (45, big_base), OSW, 55, (240, 240, 240), OSW_SQ)
        car_tag(img, 920); wallet_clear(img)
        return {"img": img, "view": view, "overlay": block_overlay(name, done)}
    fbase, dbase = frameB(14700), frameB(15740)
    st["f1"] = own_cam(fbase, "Front Lip", False, "F", 83, 144); st["f2"] = own_cam(fbase, "Front Lip", True, "F", 83, 144)
    st["d1"] = own_cam(dbase, "Side Skirts", False, "D", 83, 144); st["d2"] = own_cam(dbase, "Side Skirts", True, "D", 83, 144)
    cash -= p["Front Lip"] + p["Side Skirts"]
    st["e1"] = part(eb, "Rear Lip", cash, False, "E"); cash -= p["Rear Lip"]; st["e2"] = part(eb, "Rear Lip", cash, True, "E")
    ab = frameA(900)
    st["a1"] = part(ab, "Sport Wing", cash, False, "A"); cash -= p["Sport Wing"]; st["a2"] = part(ab, "Sport Wing", cash, True, "A")

    # respray: first capture's option screen (camera M) cleared of its own block, second capture's swatch block as an overlay
    def respray(done):
        img = frameA(1700).copy(); clean = frameA(100)
        bx0, by0, bx1, by1 = box(20, 790, 1080, 1066); img[by0:by1, bx0:bx1] = clean[by0:by1, bx0:bx1]
        retitle(img, box(30, 30, 172, 62), "COSMETICS", OSW, None, OSW_SQ * 0.9, thr=14)
        retitle(img, box(30, 68, 420, 110), "RESPRAY", OSW, None, OSW_SQ)
        panel_from_A(img); car_tag(img, 555); wallet_clear(img)
        r = frameB(5160).copy(); plain = frameB(2300)
        # explicit size and baseline: on the second capture's frames the text mask fills the whole box (measured: cap height 38 px)
        retitle(r, box(22, 718, 330, 760), "BOOST BLUE", OSW, 45.5, OSW_SQ, baseline=1007)
        if done:
            applied(r)
        d = cv2.absdiff(r, plain).max(2).astype(np.float32)
        al = cv2.morphologyEx((d > 18).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)).astype(np.float32)
        al = np.maximum(al, np.clip((d - 8) / 24, 0, 1)); al = cv2.GaussianBlur(al, (0, 0), 0.8)
        keep = np.zeros_like(al); keep[900:1070, 0:560] = 1; keep[1070:1420, 0:1010] = 1     # the block only: the game's car differs between the two frames too
        return {"img": img, "view": "P", "overlay": np.dstack([r.astype(np.float32), al * keep * 255])}
    st["p1"] = respray(False); st["p2"] = respray(True)

    def susp(done, c):
        img = frameB(2100).copy()
        retitle(img, box(30, 68, 420, 110), "SUSPENSION", OSW, None, OSW_SQ)
        applied(img) if done else clear_status(img)
        hx0, hy0, hx1, hy1 = box(815, 1008, 1105, 1052)                       # "Respray the Ganado" hint names the game's car
        m = np.zeros(img.shape[:2], np.uint8); m[hy0:hy1, hx0:hx1] = 255; img[:] = cv2.inpaint(img, m, 6, cv2.INPAINT_TELEA)
        car_tag(img, 555); wallet_clear(img)
        return {"img": img, "view": "S"}
    st["s1"] = susp(False, cash); cash -= GAME["Suspension"]; st["s2"] = susp(True, cash)

    def rims(done, c):
        img = frameB(20040).copy()
        retitle(img, box(30, 768, 420, 812), "CUSTOM 6-SPOKE RIMS", OSW, 51.5, OSW_SQ, dx=5, baseline=1075)
        applied(img) if done else clear_status(img)
        car_tag(img, 920); wallet_clear(img)
        return {"img": img, "view": "W"}
    st["w1"] = rims(False, cash); cash -= GAME["Wheels"]; st["w2"] = rims(True, cash)
    assert cash == 0, cash
    return st


if __name__ == "__main__":
    W = Path("/home/user/media/work/gta6-customs")
    ca, cb = cv2.VideoCapture(U.VID), cv2.VideoCapture(VID_B)
    def fa(f): ca.set(1, f); return ca.read()[1]
    def fb(f): cb.set(1, f); return cb.read()[1]
    st = build(fa, fb); (W / "ui4").mkdir(exist_ok=True)
    tiles = []
    for k in ("m0", "f1", "d2", "e2", "a2", "w2"):
        im = st[k]["img"].copy()
        if st[k].get("overlay") is not None:
            o = st[k]["overlay"]; a = o[..., 3:] / 255; im = (im * (1 - a) + o[..., :3] * a).astype(np.uint8)
        cv2.imwrite(str(W / "ui4" / f"{k}.png"), im); tiles.append(cv2.resize(im, (1280, 720)))
    cv2.imwrite(str(W / "ui4" / "sheet.jpg"), np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])]), [cv2.IMWRITE_JPEG_QUALITY, 86])
    print("total", TOTAL)
