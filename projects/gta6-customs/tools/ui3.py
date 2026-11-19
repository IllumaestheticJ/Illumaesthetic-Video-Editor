"""v3 menu states (user, v2 review): parts, respray, suspension, wheels, exit.

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
PRICES = dict(U.PRICES); GAME = {"Suspension": 750, "Wheels": 560}
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
    M = U.Menu(frameA)

    def menu(key, sel, fitted, c):
        st[key] = {"img": M.render(sel, fitted, c), "view": "M"}
    menu("m0", 1, [], cash); cash -= p["Front Lip"]
    menu("m1", 1, ["Front Lip"], cash); menu("m2", 2, ["Front Lip"], cash); cash -= p["Side Skirts"]
    menu("m3", 2, ["Front Lip", "Side Skirts"], cash); menu("m4", 3, ["Front Lip", "Side Skirts"], cash)

    def part(base, name, c, done, view):
        img = base.copy()
        retitle(img, box(30, 68, 420, 110), name.upper(), OSW, None, OSW_SQ)
        retitle(img, box(30, 902, 420, 940), name.upper(), OSW, None, OSW_SQ)
        price(img, money(PRICES[name]))
        retitle(img, box(76, 955, 105, 990), "1", LEX, None, thr=20); retitle(img, box(128, 955, 165, 990), "1", LEX, None, thr=14)
        applied(img) if done else clear_status(img)
        panel_from_A(img); car_tag(img, 555); wallet(img, c)
        return {"img": img, "view": view}
    eb = frameB(17960)
    st["e1"] = part(eb, "Rear Lip", cash, False, "E"); cash -= p["Rear Lip"]; st["e2"] = part(eb, "Rear Lip", cash, True, "E")
    ab = frameA(900)
    st["a1"] = part(ab, "Sport Wing", cash, False, "A"); cash -= p["Sport Wing"]; st["a2"] = part(ab, "Sport Wing", cash, True, "A")

    # respray: first capture's option screen (camera M) cleared of its own block, second capture's swatch block as an overlay
    def respray(done):
        img = frameA(1700).copy(); clean = frameA(100)
        bx0, by0, bx1, by1 = box(20, 790, 1080, 1066); img[by0:by1, bx0:bx1] = clean[by0:by1, bx0:bx1]
        retitle(img, box(30, 30, 172, 62), "COSMETICS", OSW, None, OSW_SQ * 0.9, thr=14)
        retitle(img, box(30, 68, 420, 110), "RESPRAY", OSW, None, OSW_SQ)
        panel_from_A(img); car_tag(img, 555); wallet(img, cash)
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
        car_tag(img, 555); wallet(img, c)
        return {"img": img, "view": "S"}
    st["s1"] = susp(False, cash); cash -= GAME["Suspension"]; st["s2"] = susp(True, cash)

    def rims(done, c):
        img = frameB(20040).copy()
        retitle(img, box(30, 768, 420, 812), "CUSTOM 6-SPOKE RIMS", OSW, 51.5, OSW_SQ, dx=5, baseline=1075)
        applied(img) if done else clear_status(img)
        car_tag(img, 920); wallet(img, c)
        return {"img": img, "view": "W"}
    st["w1"] = rims(False, cash); cash -= GAME["Wheels"]; st["w2"] = rims(True, cash)
    assert cash == 0, cash
    return st


if __name__ == "__main__":
    W = Path("/home/user/media/work/gta6-customs")
    ca, cb = cv2.VideoCapture(U.VID), cv2.VideoCapture(VID_B)
    def fa(f): ca.set(1, f); return ca.read()[1]
    def fb(f): cb.set(1, f); return cb.read()[1]
    st = build(fa, fb); (W / "ui3").mkdir(exist_ok=True)
    tiles = []
    for k in ("m0", "e2", "a2", "p1", "s2", "w2"):
        im = st[k]["img"].copy()
        if st[k].get("overlay") is not None:
            o = st[k]["overlay"]; a = o[..., 3:] / 255; im = (im * (1 - a) + o[..., :3] * a).astype(np.uint8)
        cv2.imwrite(str(W / "ui3" / f"{k}.png"), im); tiles.append(cv2.resize(im, (1280, 720)))
    cv2.imwrite(str(W / "ui3" / "sheet.jpg"), np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])]), [cv2.IMWRITE_JPEG_QUALITY, 86])
    print("total", TOTAL)
