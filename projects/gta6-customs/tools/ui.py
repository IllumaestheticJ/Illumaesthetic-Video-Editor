"""Re-letter the mod shop's menus for the Epsilon parts list, keeping the game's layout, colours and panels.

    python projects/gta6-customs/tools/ui.py            -> $W/ui/<state>.png (re-lettered reference frames) + sheet

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

W = Path("/home/user/media/work/gta6-customs")
VID = "/home/user/media/gta6-customs/capture/gta6_customization_1440p.mp4"
FONTS = Path("/home/user/media/gta6-customs/fonts")
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
    """VAPID / JASON'S '70 GANADO  ->  HONDA / JASON'S '22 CIVIC; the maker's badge is painted out."""
    retitle(img, box(1478, y_top + 10, 1700, y_top + 34), "HONDA", OSW, None, OSW_SQ, thr=22)
    retitle(img, box(1478, y_top + 36, 1740, y_top + 66), "JASON'S '22 CIVIC", OSW, None, OSW_SQ, thr=30)
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


# menu2 / menu2b: row 2 highlighted with and without the yellow marker (it is gone when the capture returns to the menu)
STATES = {"menu2": (100, lambda im, c: menu(im, 2)), "menu2b": (1200, lambda im, c: menu(im, 2)), "menu3": (1300, lambda im, c: menu(im, 3)),
          "none": (340, lambda im, c: spoiler(im, False)), "wing": (900, lambda im, c: spoiler(im, True)),
          "kit": (1700, lambda im, c: kits(im, c))}


def main():
    cap = cv2.VideoCapture(VID); (W / "ui").mkdir(exist_ok=True)

    def frame(f):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); return cap.read()[1]

    clean = frame(100)
    tiles = []
    for name, (f, fn) in STATES.items():
        src = frame(f); im = src.copy(); fn(im, clean)
        cv2.imwrite(str(W / "ui" / f"{name}.png"), im); cv2.imwrite(str(W / "ui" / f"{name}_src.png"), src)
        tiles.append(np.vstack([cv2.resize(src, (1280, 720)), cv2.resize(im, (1280, 720))]))
    for i in range(0, len(tiles), 2):
        cv2.imwrite(str(W / "ui" / f"sheet{i // 2}.jpg"), np.hstack(tiles[i:i + 2]), [cv2.IMWRITE_JPEG_QUALITY, 88])


if __name__ == "__main__":
    main()
