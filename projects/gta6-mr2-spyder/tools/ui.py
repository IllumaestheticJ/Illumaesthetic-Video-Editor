"""Re-letter the mod shop's menus for the Epsilon parts list, keeping the game's layout, colours and panels.

    python projects/gta6-mr2-spyder/tools/ui.py            -> $W/ui/<state>.png (re-lettered reference frames) + sheet

Every text that changes is measured on the capture (its box, colour, baseline), painted out, and set again in
the matching face: Lexend for list and status text, Oswald 600 squeezed to 94 % for the condensed capitals
(compared against the capture's own lettering in fonts sheet; Bebas, Barlow, Saira and Antonio fit worse).
Numbers shown are the catalogue's (Epsilon-Site showroom/catalog/products.json, 2026-10-03): Sport Wing,
gloss black, $450. The stat bars and their numbers are the game's own and are left alone.
"""
import sys
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

W = Path("/home/user/media/work/gta6-mr2-spyder")
VID = "/home/user/media/gta6-mr2-spyder/capture/gta6_customization_1440p.mp4"
FONTS = Path("/home/user/media/gta6-mr2-spyder/fonts")
LEX = str(FONTS / "lexend-latin-400-normal.ttf"); OSW = str(FONTS / "oswald-latin-600-normal.ttf")
S = 4 / 3                                   # boxes below were read off 1920-wide views; frames are 2560 wide


def box(x0, y0, x1, y1):
    return tuple(int(round(v * S)) for v in (x0, y0, x1, y1))


def text_mask(img, b, dark=False, thr=30):
    x0, y0, x1, y1 = b
    P = 40                                                             # work on a padded area: the kernel is wider than small boxes
    ya, xa = max(0, y0 - P), max(0, x0 - P)
    g = cv2.cvtColor(img[ya:y1 + P, xa:x1 + P], cv2.COLOR_BGR2GRAY).astype(np.float32)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23))       # wider than any stroke: an opening removes light text, a closing dark text
    bg = cv2.morphologyEx(g, cv2.MORPH_CLOSE if dark else cv2.MORPH_OPEN, k)
    bg = cv2.GaussianBlur(bg, (0, 0), 4)
    m = (bg - g > thr) if dark else (g - bg > thr)
    return m[y0 - ya:y0 - ya + (y1 - y0), x0 - xa:x0 - xa + (x1 - x0)]


def erase(img, b, dark=False, thr=30, grow=5):
    x0, y0, x1, y1 = b
    m = text_mask(img, b, dark, thr)
    if not m.any():
        return None, None
    ys, xs = np.nonzero(m)
    col = np.percentile(img[y0:y1, x0:x1][m].reshape(-1, 3), 10 if dark else 90, 0)
    md = cv2.dilate(m.astype(np.uint8), np.ones((grow, grow), np.uint8))
    full = np.zeros(img.shape[:2], np.uint8); full[y0:y1, x0:x1] = md * 255
    img[:] = cv2.inpaint(img, full, 5, cv2.INPAINT_TELEA)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()), col


def draw(img, text, xy, font, size, color, squeeze=1.0, anchor="ls", track=0.0, alpha=1.0):
    """Draw text with its left baseline (anchor ls) or left-top of caps (lt) at xy, 4x supersampled."""
    K = 4
    f = ImageFont.truetype(font, int(round(size * K)))
    wid = int(sum(f.getlength(c) + track * K for c in text)) + 8 * K
    asc, desc = f.getmetrics()
    lay = Image.new("L", (wid, asc + desc + 8 * K), 0); d = ImageDraw.Draw(lay)
    x = 2 * K
    for c in text:
        d.text((x, 2 * K + asc), c, font=f, fill=255, anchor="ls"); x += f.getlength(c) + track * K
    a = np.asarray(lay.resize((max(1, int(wid * squeeze / K)), (asc + desc + 8 * K) // K), Image.LANCZOS)).astype(np.float32) / 255 * alpha
    bx = int(round(xy[0])) - int(2 * squeeze); by = int(round(xy[1])) - (2 * K + asc) // K
    h, w = a.shape; H, Wd = img.shape[:2]
    ya, xa = max(0, by), max(0, bx); yb, xb = min(H, by + h), min(Wd, bx + w)
    a = a[ya - by:yb - by, xa - bx:xb - bx, None]
    img[ya:yb, xa:xb] = (img[ya:yb, xa:xb] * (1 - a) + np.array(color, np.float32) * a).astype(np.uint8)


CAP = {OSW: 0.835, LEX: 0.70}               # capital height / font size, measured against the capture's lettering


def retitle(img, b, text, font, size=None, squeeze=1.0, dark=False, thr=30, dx=0, baseline=None, track=0.0):
    """Replace the text found in box b: same left edge, same baseline, same colour, and (size None) the same
    capital height. Only for originals without descenders when the size is automatic."""
    bb, col = erase(img, b, dark, thr)
    if bb is None:
        raise SystemExit(f"no text found in {b} for '{text}'")
    if size is None:
        size = (bb[3] - bb[1] + 1) / CAP[font]
    draw(img, text, (bb[0] + dx, (bb[3] + 1) if baseline is None else baseline), font, size, col, squeeze, track=track)
    return bb


ROW0, PITCH = 190.0, 62.5                  # list rows: centre of row 1 and row spacing, 1920-wide view
PARTS = ["Front Lip", "Sport Wing", "Side Skirts", "Rear Lip"]     # row 2 is the one the capture enters
LEX_ROW = 34.5; OSW_SQ = 0.94


def car_tag(img, y_top):
    """VAPID / JASON'S '70 GANADO  ->  KARIN / JASON'S '01 RUNABOUT. Karin is the GTA series' Toyota; no official counterpart of the
    MR2 Spyder was found, so the model name is ours (MR = "Midship Runabout"); the maker's badge is painted out."""
    retitle(img, box(1478, y_top + 10, 1700, y_top + 34), "KARIN", OSW, None, OSW_SQ, thr=22)
    retitle(img, box(1478, y_top + 36, 1740, y_top + 66), "JASON'S '01 RUNABOUT", OSW, None, OSW_SQ, thr=30)
    erase(img, box(1735, y_top + 2, 1886, y_top + 70), thr=9, grow=9)


def menu(img, sel):
    """Bodywork list. sel = highlighted row (1-based), as in the capture frame given."""
    base = None
    for k in range(1, 9):
        yc = ROW0 + PITCH * (k - 1)
        b = box(44, yc - 26, 480, yc + 26)
        if k == sel:
            x0, y0, x1, y1 = box(52, yc - 14, 80, yc + 14)
            hsv = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
            diamond = ((hsv[..., 1] > 110) & (hsv[..., 0] > 12) & (hsv[..., 0] < 36)).mean() > 0.08   # the yellow marker some rows carry: text starts after it
            b = box(84 if diamond else 44, yc - 24, 420, yc + 24)
            bb, col = erase(img, b, dark=True, thr=40)
            draw(img, PARTS[k - 1], (bb[0], (yc + 11.5) * S), LEX, LEX_ROW, col)
        else:
            bb, col = erase(img, b, thr=22)
            if k <= len(PARTS):
                draw(img, PARTS[k - 1], (bb[0], (yc + 11.5) * S), LEX, LEX_ROW, col)
        if k > len(PARTS):                 # rows the Civic has no part for: take the separator under them out too
            y = int(round((yc + PITCH / 2) * S))
            line = np.zeros(img.shape[:2], np.uint8); line[y - 3:y + 4, int(30 * S):int(600 * S)] = 255
            img[:] = cv2.inpaint(img, line, 4, cv2.INPAINT_TELEA)
    # counter "2 / 13" under the list -> "2 / 4" under the fourth row
    yc_old = 697.0
    bb, col = erase(img, box(30, yc_old - 20, 150, yc_old + 20), thr=18)
    y_new = (ROW0 + PITCH * len(PARTS) + 8 + 9.5) * S
    draw(img, f"{sel}", (bb[0], y_new), LEX, 30, (235, 235, 235))
    draw(img, "/", (bb[0] + 44, y_new), LEX, 30, col * 0.75)
    draw(img, f"{len(PARTS)}", (bb[0] + 80, y_new), LEX, 30, col * 0.75)
    car_tag(img, 920)


def spoiler(img, wing):
    retitle(img, box(30, 68, 420, 110), "SPORT WING", OSW, None, OSW_SQ)
    if wing:
        retitle(img, box(30, 902, 420, 940), "SPORT WING", OSW, None, OSW_SQ)
        # price: the game sets it in heavy grey figures with a dark edge; the whole figure box is painted out
        # (its dark edge is not found by the light-text mask) and set again
        x0, y0, x1, y1 = box(122, 846, 240, 894)
        g = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
        ys, xs = np.nonzero(g > np.median(g) + 40)
        col = np.percentile(img[y0:y1, x0:x1][g > np.median(g) + 40].reshape(-1, 3), 70, 0)
        m = np.zeros(img.shape[:2], np.uint8); m[y0:y1, x0:x1] = 255
        img[:] = cv2.inpaint(img, m, 7, cv2.INPAINT_TELEA)
        size = (ys.max() - ys.min() + 1) / CAP[OSW]
        for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2), (-2, -2), (2, -2), (-2, 2)):
            draw(img, "$450", (x0 + xs.min() + ox, y0 + ys.max() + 1 + oy), OSW, size, (28, 28, 30), 1.0)
        draw(img, "$450", (x0 + xs.min(), y0 + ys.max() + 1), OSW, size, col, 1.0)
        retitle(img, box(76, 955, 105, 990), "2", LEX, None, thr=20)
        retitle(img, box(128, 955, 165, 990), "2", LEX, None, thr=14)
    else:
        retitle(img, box(128, 955, 165, 990), "2", LEX, None, thr=14)
    car_tag(img, 555)


def kits(img, clean):
    """Full Kits screen. The badges ("EXCLUSIVE", "FREE"), the kit's name and its note are taken out by copying
    clean pixels from the menu screen (same camera, no text there); the counter row and rule are kept."""
    for ya, yb in ((800, 946), (1012, 1066)):
        x0, y0, x1, y1 = box(20, ya, 900, yb)
        img[y0:y1, x0:x1] = clean[y0:y1, x0:x1]
    white = (238, 238, 238)
    draw(img, "EPSILON FULL AERO KIT", (33 * S, 933 * S), OSW, 47, white, OSW_SQ)
    retitle(img, box(128, 955, 165, 990), "1", LEX, None, thr=14)
    draw(img, "Front Lip  \u00b7  Side Skirts  \u00b7  Rear Lip  \u00b7  Sport Wing", (36 * S, 1045 * S), LEX, LEX_ROW, white)
    car_tag(img, 555)


# ---- v2: parts are installed one after another (user, v1 review) -------------------------------------------
# The list is built, not patched: clean list background from the capture, then rows, the highlight bar (its
# transparency measured from the capture: the same row with and without the bar), the yellow marker on rows
# whose part is fitted, the counter, and the wallet, which starts at the four parts' total and pays for each.
PRICES = {"Front Lip": 285, "Side Skirts": 400, "Rear Lip": 285, "Sport Wing": 450}     # catalogue, base variants
ROWS = ["Front Lip", "Side Skirts", "Rear Lip", "Sport Wing"]


def money(n):
    return f"${n:,}"


def wallet(img, amount):
    """Top-right wallet figure ("$99" in the capture): painted out, set again right-aligned to the same edge."""
    x0, y0, x1, y1 = 2376, 36, 2468, 76
    m = np.zeros(img.shape[:2], np.uint8); m[y0:y1, x0:x1] = 255
    img[:] = cv2.inpaint(img, m, 5, cv2.INPAINT_TELEA)
    text = money(amount); size = 34.0
    f = ImageFont.truetype(OSW, int(size * 4)); wid = f.getlength(text) / 4
    x = 2462 - wid; base = 70
    for ox in range(-3, 4):
        for oy in range(-3, 4):
            if ox * ox + oy * oy <= 10 and (ox or oy):
                draw(img, text, (x + ox, base + oy), OSW, size, (24, 26, 24))
    draw(img, text, (x, base), OSW, size, (250, 250, 250))


def diamond(img, cx, cy, r=11.5):
    K = 4; n = int(r * 2 + 8) * K
    lay = np.zeros((n, n, 4), np.float32); c = n / 2
    pts = lambda rr: np.array([[c, c - rr * K], [c + rr * K, c], [c, c + rr * K], [c - rr * K, c]], np.int32)
    cv2.fillConvexPoly(lay, pts(r), (30, 40, 44, 255)); cv2.fillConvexPoly(lay, pts(r - 2.6), (72, 190, 250, 255))
    lay = cv2.resize(lay, (n // K, n // K), interpolation=cv2.INTER_AREA)
    x0, y0 = int(round(cx - n / K / 2)), int(round(cy - n / K / 2)); a = lay[..., 3:] / 255
    img[y0:y0 + n // K, x0:x0 + n // K] = (img[y0:y0 + n // K, x0:x0 + n // K] * (1 - a) + lay[..., :3] * a).astype(np.uint8)


class Menu:
    """Bodywork list rebuilt on the capture's menu frame."""

    def __init__(self, frame):
        a, b = frame(100), frame(1300)                    # row 2 highlighted / row 3 highlighted
        self.bar_rect = bx0, by0, bx1, by1 = box(28, 219, 524, 282)   # inside one row: the next row's bar starts at 283
        bg = a.copy(); bg[by0:by1, bx0:bx1] = b[by0:by1, bx0:bx1]          # row 2 without its bar
        pp_ = int(round(PITCH * S))                                         # the bar's bright lower edge: take the separator one row down
        bg[by1:by1 + 11, bx0:bx1] = bg[by1 + pp_:by1 + pp_ + 11, bx0:bx1]
        for k in range(1, 9):
            yc = ROW0 + PITCH * (k - 1)
            erase(bg, box(44, yc - 26, 480, yc + 26), thr=22)
            if k > len(ROWS):
                y = int(round((yc + PITCH / 2) * S)); line = np.zeros(bg.shape[:2], np.uint8); line[y - 3:y + 4, int(30 * S):int(600 * S)] = 255
                bg[:] = cv2.inpaint(bg, line, 4, cv2.INPAINT_TELEA)
        self.counter_bb, self.counter_col = erase(bg, box(30, 677, 150, 717), thr=18)
        for k in range(9, len(ROWS) + 1):                 # more rows than the capture's list shows: the rule above row k is the one above row 8, copied down
            ys_ = int(round((ROW0 + PITCH * 6.5) * S)); yd_ = int(round((ROW0 + PITCH * (k - 1.5)) * S)); xa, xb = int(30 * S), int(600 * S)
            d_ = bg[ys_ - 4:ys_ + 5, xa:xb].astype(np.int16) - bg[ys_ - 14:ys_ - 5, xa:xb].astype(np.int16)
            bg[yd_ - 4:yd_ + 5, xa:xb] = np.clip(bg[yd_ - 4:yd_ + 5, xa:xb].astype(np.int16) + d_, 0, 255).astype(np.uint8)
        bar = a.copy()
        erase(bar, box(44, ROW0 + PITCH - 24, 420, ROW0 + PITCH + 24), dark=True, thr=30)   # text and marker off the bar
        d = bar[by0:by1, bx0:bx1].astype(np.float32); u = bg[by0:by1, bx0:bx1].astype(np.float32)
        al = np.clip(((d - u) / np.maximum(250.0 - u, 8)).mean(2), 0, 1)
        self.bar_alpha = cv2.GaussianBlur(al, (0, 0), 1.0)[..., None]
        car_tag(bg, 920)
        self.bg = bg

    def render(self, sel, fitted, cash):
        img = self.bg.copy(); bx0, by0, bx1, by1 = self.bar_rect
        dy = int(round((sel - 2) * PITCH * S))
        reg = img[by0 + dy:by1 + dy, bx0:bx1].astype(np.float32)
        img[by0 + dy:by1 + dy, bx0:bx1] = (reg * (1 - self.bar_alpha) + 250 * self.bar_alpha).astype(np.uint8)
        for k, name in enumerate(ROWS, 1):
            yc = ROW0 + PITCH * (k - 1); mark = name in fitted
            if mark:
                diamond(img, 64 * S, yc * S + 1)
            col = (34, 30, 30) if k == sel else (238, 238, 238)
            draw(img, name, ((90 if mark else 49) * S, (yc + 11.5) * S), LEX, LEX_ROW, col)
        y = (ROW0 + PITCH * len(ROWS) + 8 + 9.5) * S; x = self.counter_bb[0]
        draw(img, f"{sel}", (x, y), LEX, 30, (235, 235, 235)); draw(img, "/", (x + 44, y), LEX, 30, self.counter_col * 0.75)
        draw(img, f"{len(ROWS)}", (x + 80, y), LEX, 30, self.counter_col * 0.75)
        wallet(img, cash)
        return img


def rear(frame, part, applied, cash):
    """Rear-view option screen for one part, built on the capture's priced option ("Custom Wing"): its price, name,
    1 / 1, and under the rule either nothing or the capture's own "Applied" line (from its "None" option)."""
    img = frame(900).copy(); none = frame(340)
    retitle(img, box(30, 68, 420, 110), part.upper(), OSW, None, OSW_SQ)
    retitle(img, box(30, 902, 420, 940), part.upper(), OSW, None, OSW_SQ)
    x0, y0, x1, y1 = box(122, 846, 240, 894)
    g = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY); br = g > np.median(g) + 40
    ys, xs = np.nonzero(br); col = np.percentile(img[y0:y1, x0:x1][br].reshape(-1, 3), 70, 0)
    m = np.zeros(img.shape[:2], np.uint8); m[y0:y1, x0:x1] = 255
    img[:] = cv2.inpaint(img, m, 7, cv2.INPAINT_TELEA)
    size = (ys.max() - ys.min() + 1) / CAP[OSW]; price = money(PRICES[part])
    for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2), (-2, -2), (2, -2), (-2, 2)):
        draw(img, price, (x0 + xs.min() + ox, y0 + ys.max() + 1 + oy), OSW, size, (28, 28, 30))
    draw(img, price, (x0 + xs.min(), y0 + ys.max() + 1), OSW, size, col)
    retitle(img, box(76, 955, 105, 990), "1", LEX, None, thr=20)
    retitle(img, box(128, 955, 165, 990), "1", LEX, None, thr=14)
    sx0, sy0, sx1, sy1 = box(10, 1014, 340, 1060)
    if applied:
        img[sy0:sy1, sx0:sx1] = none[sy0:sy1, sx0:sx1]
    else:
        m = np.zeros(img.shape[:2], np.uint8); m[sy0 + 4:sy1 - 2, sx0 + 6:sx1] = 255
        img[:] = cv2.inpaint(img, m, 6, cv2.INPAINT_TELEA)
    # stats panel as the capture shows it for the plain car (no gains from the game's own wing), our car's name
    px0, py0, px1, py1 = box(1466, 520, 1894, 996)
    img[py0:py1, px0:px1] = none[py0:py1, px0:px1]
    car_tag(img, 555)
    wallet(img, cash)
    return img


def build(frame):
    """All menu states of the v2 reel, by name."""
    M = Menu(frame); total = sum(PRICES.values()); p = PRICES
    st = {
        "m0": M.render(1, [], total),
        "m1": M.render(1, ["Front Lip"], total - p["Front Lip"]),
        "m2": M.render(2, ["Front Lip"], total - p["Front Lip"]),
        "m3": M.render(2, ["Front Lip", "Side Skirts"], total - p["Front Lip"] - p["Side Skirts"]),
        "m4": M.render(3, ["Front Lip", "Side Skirts"], total - p["Front Lip"] - p["Side Skirts"]),
        "mF": M.render(4, ROWS, 0),
        "a1": rear(frame, "Rear Lip", False, p["Rear Lip"] + p["Sport Wing"]),
        "a2": rear(frame, "Rear Lip", True, p["Sport Wing"]),
        "a3": rear(frame, "Sport Wing", False, p["Sport Wing"]),
        "a4": rear(frame, "Sport Wing", True, 0),
    }
    return st


def main():
    cap = cv2.VideoCapture(VID); (W / "ui").mkdir(exist_ok=True)

    def frame(f):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); return cap.read()[1]

    st = build(frame)
    for k, im in st.items():
        cv2.imwrite(str(W / "ui" / f"{k}.png"), im)
    t = [cv2.resize(st[k], (1280, 720)) for k in ("m0", "m3", "mF", "a1", "a2", "a4")]
    cv2.imwrite(str(W / "ui" / "sheet_v2.jpg"), np.vstack([np.hstack(t[:3]), np.hstack(t[3:])]), [cv2.IMWRITE_JPEG_QUALITY, 88])
    z = np.hstack([st["m3"][150:760, 0:860], st["a2"][1100:1430, 0:860].repeat(1, 0)[:610] if False else cv2.copyMakeBorder(st["a2"][1100:1430, 0:860], 0, 280, 0, 0, cv2.BORDER_CONSTANT)])
    cv2.imwrite(str(W / "ui" / "detail_v2.jpg"), np.hstack([z, cv2.copyMakeBorder(st["m3"][10:110, 2200:2560], 0, 510, 0, 0, cv2.BORDER_CONSTANT)]), [cv2.IMWRITE_JPEG_QUALITY, 90])


if __name__ == "__main__":
    main()
