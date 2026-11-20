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

VID_B = "/home/user/media/gta6-integra/capture/gta6_customization_B_1440p.mp4"
# Catalogue list prices (the store's compare-at prices, read 2026-11-20 through the Shopify connector; they match the
# figures quoted from Epsilon-Site showroom/catalog/products.json). Parts arrive paint matched to the entrance colour,
# Apex Blue Pearl: Rear Trunk Lip and Sport Wing are charged at their Apex Blue Pearl - B621P variants (300, 950).
# Front Lip, Fender Flare Widebody, Side Skirts and Rear Spats are sold in polyurethane only (no painted variant), so
# their one catalogue price is charged.
PRICES = {"Front Lip": 285, "Fender Flares": 800, "Side Skirts": 400, "Rear Spats": 175, "Trunk Lip": 300, "Rear Wing": 950}
ITEM = {"Fender Flares": "EPSILON WIDEBODY FLARES"}            # item line on the part's own screen; default "EPSILON <ROW>"
GAME = {"Suspension": 750, "Wheels": 560}
ROWS = list(PRICES)      # lookbook part order; plain names on the list; "Rear Wing" = the catalogue's Sport Wing (Civic v8 review)
# The DE4/DE5 factory colours as the store lists them for its painted variants (names and paint codes from the catalogue),
# in the order the cursor runs: the entrance colour (Apex Blue Pearl) first, the colour bought last. sRGB: Platinum White and Lunar Silver
# from the lookbook data used on the Civic reel; the last is the lookbook's photographed grey for this car (#848586),
# lettered Urban Gray Pearl (my reading of which factory grey that is); the rest are my approximations for the swatches.
OEM = [("APEX BLUE", "PEARL", "#1f4aa5"), ("DOUBLE APEX BLUE", "PEARL", "#16306e"), ("PERFORMANCE RED", "PEARL", "#a3121c"),
       ("TIGER EYE", "PEARL", "#c7801d"), ("MAJESTIC BLACK", "PEARL", "#0e0f12"), ("PLATINUM WHITE", "PEARL", "#f2f0e9"),
       ("SOLAR SILVER", "METALLIC", "#c9cbcc"), ("LUNAR SILVER", "METALLIC", "#a8acb0"), ("LIQUID CARBON", "METALLIC", "#4f5256"),
       ("URBAN GRAY", "PEARL", "#848586")]
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


TABS = {"PRO BUILDS": (108, 338), "COSMETICS": (342, 520), "BODYWORK": (523, 742), "PERFORMANCE": (747, 965), "WHEELS": (969, 1103),
        "INTERIOR": (1108, 1263)}                  # x ranges of the tab boxes on the first capture's menu frame; rows 104-148
TAB_Y = (104, 148)


def set_tab(img, name):
    """Move the tab bar's highlight from BODYWORK (as captured) to another tab."""
    if name == "BODYWORK":
        return
    y0, y1 = TAB_Y
    # 1. BODYWORK back to an unselected tab: the box filled across from its neighbours, its lettering and marker set light
    x0, x1 = TABS["BODYWORK"]
    hsv = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2HSV); dm = (hsv[..., 1] > 110) & (hsv[..., 2] > 150)
    dys, dxs = np.nonzero(dm)
    # lettering size and baseline from a neighbour (COSMETICS), gap between marker and lettering from PRO BUILDS
    cx = TABS["COSMETICS"]; cg = img[y0:y1, cx[0]:cx[1]]; cm = cv2.cvtColor(cg, cv2.COLOR_BGR2GRAY) > 170
    cys = np.nonzero(cm.any(1))[0]; cap_h, base = cys.max() - cys.min() + 1, cys.max() + 1
    light = np.percentile(cg[cm].reshape(-1, 3), 80, 0)
    px = TABS["PRO BUILDS"]; pg = img[y0:y1, px[0]:px[1]]; ph = cv2.cvtColor(pg, cv2.COLOR_BGR2HSV)
    pmark = (ph[..., 1] > 110) & (ph[..., 2] > 150); ptxt = (cv2.cvtColor(pg, cv2.COLOR_BGR2GRAY) > 170) & ~cv2.dilate(pmark.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
    pm_x = np.nonzero(pmark.any(0))[0]; pt_x = np.nonzero(ptxt.any(0))[0]
    gap = int(pt_x[pt_x > pm_x.max()].min() - pm_x.max()) if len(pm_x) else 16
    L = img[y0:y1, x0 - 14:x0 - 8].astype(np.float32).mean(1, keepdims=True); Rr = img[y0:y1, x1 + 12:x1 + 18].astype(np.float32).mean(1, keepdims=True)
    t = np.linspace(0, 1, x1 - x0 + 16)[None, :, None]
    img[y0:y1, x0 - 8:x1 + 8] = (L * (1 - t) + Rr * t).astype(np.uint8)
    draw(img, "BODYWORK", (x0 + dxs.max() + gap, y0 + base), OSW, cap_h / CAP[OSW], light, OSW_SQ)
    U.diamond(img, x0 + (dxs.min() + dxs.max()) / 2, y0 + (dys.min() + dys.max()) / 2, r=(pm_x.max() - pm_x.min()) / 2 + 1)
    # 2. the new tab: white box, its lettering dark (any marker kept)
    x0, x1 = TABS[name]
    reg = img[y0:y1, x0:x1].copy(); gg = cv2.cvtColor(reg, cv2.COLOR_BGR2GRAY)
    hs = cv2.cvtColor(reg, cv2.COLOR_BGR2HSV); mark = (hs[..., 1] > 110) & (hs[..., 2] > 150)
    txt = cv2.GaussianBlur(((gg > 150) & ~cv2.dilate(mark.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)).astype(np.float32), (0, 0), 0.6)[..., None]
    box_ = np.full_like(reg, 246, np.float32)
    box_ = box_ * (1 - txt) + np.array([34, 30, 30], np.float32) * txt
    poly = np.array([[x0 + 5, y0], [x1 + 3, y0], [x1 - 5, y1], [x0 - 3, y1]], np.int32)          # the selected tab leans, like the captured one
    m = np.zeros(img.shape[:2], np.uint8); cv2.fillConvexPoly(m, poly, 255, lineType=cv2.LINE_AA)
    full = img.astype(np.float32); patch = full.copy(); patch[y0:y1, x0:x1] = box_
    patch[y0:y1, :x0] = 246; patch[y0:y1, x1:] = 246
    a = (m / 255.0)[..., None]
    out = full * (1 - a) + patch * a
    if mark.any():
        mk = cv2.dilate(mark.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
        out[y0:y1, x0:x1][mk] = reg[mk]
    img[:] = np.clip(out, 0, 255).astype(np.uint8)


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
    mb = M.bg.copy(); wallet_clear(mb); st["m_blank"] = {"img": mb, "view": "M"}     # list screen without rows or bar: what gets blurred in a whip

    # navigation between sections, as the game does it (user, v8 review): back to the list, shoulder button to the next tab,
    # the tab's own rows (read off the second capture), down to the entry, select
    menus = {}

    def nav(key, tab, rows, sel, fitted):
        U.ROWS = rows
        if tuple(rows) not in menus:
            menus[tuple(rows)] = U.Menu(frameA)
        img = menus[tuple(rows)].render(sel, fitted, 0); wallet_clear(img); set_tab(img, tab)
        st[key] = {"img": img, "view": "M"}; U.ROWS = ROWS
    COS = ["Respray", "Customizable Liveries", "Curated Liveries", "Plates"]; WHL = ["Tire Style", "Rim Style", "Rim Colors"]
    PERF = ["Full Engine", "Suspension", "Brakes", "Transmission", "Boost"]     # the game's Performance rows plus a Suspension row (mine)
    # between the aero parts (user, v11 review: "it's skipping steps"): back on the list the bought row carries its marker,
    # the cursor moves down one, select
    for k_ in range(1, len(ROWS)):
        nav(f"l{k_}", "BODYWORK", ROWS, k_, ROWS[:k_]); nav(f"l{k_}b", "BODYWORK", ROWS, k_ + 1, ROWS[:k_])
    nav("n1a", "BODYWORK", ROWS, len(ROWS), ROWS); nav("n1b", "COSMETICS", COS, 1, [])
    nav("n2a", "COSMETICS", COS, 1, ["Respray"]); nav("n2x", "BODYWORK", ROWS, 1, ROWS)
    nav("n2b", "PERFORMANCE", PERF, 1, []); nav("n2c", "PERFORMANCE", PERF, 2, [])
    nav("n3a", "PERFORMANCE", PERF, 2, ["Suspension"]); nav("n3b", "WHEELS", WHL, 1, []); nav("n3c", "WHEELS", WHL, 2, [])

    def part(base, name, c, done, view):
        img = base.copy()
        retitle(img, box(30, 68, 420, 110), name.upper(), OSW, None, OSW_SQ)
        retitle(img, box(30, 902, 420, 940), ITEM.get(name, "EPSILON " + name.upper()), OSW, None, OSW_SQ)
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
        panel_from_A(img); car_tag(img, 555); wallet_clear(img)      # stats panel like the other part screens (user, v14 review)
        return {"img": img, "view": view, "overlay": block_overlay(name, done)}
    fbase, dbase = frameB(14700), frameB(15740)
    st["f1"] = own_cam(fbase, "Front Lip", False, "F", 83, 144); st["f2"] = own_cam(fbase, "Front Lip", True, "F", 83, 144)
    # Side Skirts (v8; user: "point the camera down lower, the skirts don't fit in the frame"): on the second capture's low
    # front-quarter screen (its "Wheel Kits" camera), re-lettered like the other part screens
    def skirts(done):
        img = frameB(2100).copy()
        retitle(img, box(30, 30, 186, 62), "BODYWORK", OSW, None, OSW_SQ * 0.9, thr=14)
        hx0, hy0, hx1, hy1 = box(815, 1008, 1105, 1052)                       # "Respray the Ganado" hint
        m = np.zeros(img.shape[:2], np.uint8); m[hy0:hy1, hx0:hx1] = 255; img[:] = cv2.inpaint(img, m, 6, cv2.INPAINT_TELEA)
        d = part(img, "Side Skirts", 0, done, "D")
        d["overlay"] = block_overlay("Side Skirts", done)     # the front wheel stands where the block is: block goes on top
        d["overlay"][:, 570:, 3] = 0                          # nothing of the layer beyond the lettering (floor specks came with it)
        return d
    st["d1"] = skirts(False); st["d2"] = skirts(True)
    # Fender Flares: the second capture's high rear three-quarter screen (Rear Bed / Accessories, frame 16860). Its own option
    # block sits higher than the other screens' (it has an extra note line), so it is masked with the game's car and the part
    # block is laid on as a layer, like the Front Lip screen.
    rbase_ = frameB(16860)
    st["r1"] = own_cam(rbase_, "Fender Flares", False, "R", 83, 144); st["r2"] = own_cam(rbase_, "Fender Flares", True, "R", 83, 144)
    st["e1"] = part(eb, "Rear Spats", 0, False, "E"); st["e2"] = part(eb, "Rear Spats", 0, True, "E")
    ab = frameA(900)
    st["a1"] = part(ab, "Trunk Lip", 0, False, "A"); st["a2"] = part(ab, "Trunk Lip", 0, True, "A")
    st["a3"] = part(ab, "Rear Wing", 0, False, "A"); st["a4"] = part(ab, "Rear Wing", 0, True, "A")
    cash -= sum(p.values())

    # respray: first capture's option screen (camera M) cleared of its own block, second capture's swatch block as an overlay
    # Respray (v15; user: "change the colour swatch to Recommended and display all the OEM colours"): the game's Recommended tab,
    # with the car's ten factory colours as swatches (Epsilon-Site lookbook data for this car). The cursor runs through them,
    # the car previews each, and stops on Boost Blue. Built on the second capture's swatch block (frame 5160, Blue tab):
    # swatches repainted, selection frame, counter and scroll bar redrawn, tab highlight moved to RECOMMENDED.
    def respray_base():
        img = frameA(1700).copy(); clean = frameA(100)
        bx0, by0, bx1, by1 = box(20, 790, 1080, 1066); img[by0:by1, bx0:bx1] = clean[by0:by1, bx0:bx1]
        retitle(img, box(30, 30, 172, 62), "COSMETICS", OSW, None, OSW_SQ * 0.9, thr=14)
        retitle(img, box(30, 68, 420, 110), "RESPRAY", OSW, None, OSW_SQ)
        panel_from_A(img); car_tag(img, 555); wallet_clear(img)
        return img
    rbase = respray_base(); r0 = frameB(5160); plain = frameB(2300)
    SX = [48, 208, 368, 528, 688, 848]; SY, SS = 1088, 146                     # swatch slots (measured)

    def sprite(x0, y0, x1, y1, ref_rect):
        """An icon lifted off a swatch: alpha = distance from the swatch's own colour."""
        reg = r0[y0:y1, x0:x1].astype(np.float32); rx0, ry0, rx1, ry1 = ref_rect
        med = np.median(r0[ry0:ry1, rx0:rx1].reshape(-1, 3), 0)
        a = np.clip((np.abs(reg - med).max(2) - 70) / 40.0, 0, 1)        # hard threshold: no fringe of the source swatch's blue
        a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        return reg, a[..., None]
    tag = sprite(SX[1] + 96, SY + 92, SX[1] + 140, SY + 138, (SX[1] + 10, SY + 80, SX[1] + 80, SY + 135))
    chev = sprite(SX[5] + 8, SY + 96, SX[5] + 44, SY + 142, (SX[5] + 50, SY + 100, SX[5] + 90, SY + 135))
    hexbgr = lambda h: np.array([int(h[5:7], 16), int(h[3:5], 16), int(h[1:3], 16)], np.float32)

    def swatch(col):
        yy, xx = np.mgrid[0:SS, 0:SS].astype(np.float32)
        d = (xx + yy) / (2 * SS)
        sheen = 0.92 + 0.16 * d + 0.10 * np.exp(-((xx - yy * 0.6 - 60) / 16.0) ** 2)      # the game's diagonal highlight
        t = np.clip(hexbgr(col)[None, None] * sheen[..., None] + 6, 0, 255)
        t[:2] = t[:2] * 0.6 + 100; t[-2:] = t[-2:] * 0.6 + 100; t[:, :2] = t[:, :2] * 0.6 + 100; t[:, -2:] = t[:, -2:] * 0.6 + 100
        return t

    def respray(sel, done):
        r = r0.copy()
        r[1076:1270, 20:1030] = plain[1076:1270, 20:1030]                       # swatch row, arrows, scroll bar: start clean
        r[1024:1070, 840:1010] = plain[1024:1070, 840:1010]                     # counter
        force = np.zeros(r.shape[:2], np.float32)
        start = min(max(0, sel - 5), len(OEM) - 6)
        for k in range(6):
            x = SX[k]; name, fin, col = OEM[start + k]
            r[SY:SY + SS, x:x + SS] = swatch(col).astype(np.uint8); force[SY:SY + SS, x:x + SS] = 1
            reg, a = tag; ty, tx = SY + 92, x + 96
            r[ty:ty + reg.shape[0], tx:tx + reg.shape[1]] = (r[ty:ty + reg.shape[0], tx:tx + reg.shape[1]] * (1 - a) + reg * a).astype(np.uint8)
            if start + k == sel:
                cv2.rectangle(r, (x - 4, SY - 4), (x + SS + 3, SY + SS + 3), (245, 245, 245), 4); force[SY - 6:SY + SS + 6, x - 6:x + SS + 6] = 1
                reg, a = chev; ty, tx = SY + 96, x + 8
                r[ty:ty + reg.shape[0], tx:tx + reg.shape[1]] = (r[ty:ty + reg.shape[0], tx:tx + reg.shape[1]] * (1 - a) + reg * a).astype(np.uint8)
        if start > 0:
            r[1140:1182, 22:44] = r0[1140:1182, 22:44]
        if start + 6 < len(OEM):
            r[1140:1182, 998:1020] = r0[1140:1182, 998:1020]
        bx0, bx1 = 48, 994; tw = (bx1 - bx0) * 6 / len(OEM); tx = bx0 + (bx1 - bx0) * start / len(OEM)
        cv2.line(r, (int(tx), 1255), (int(tx + tw), 1255), (205, 205, 210), 6, cv2.LINE_AA); force[1250:1261, int(tx) - 3:int(tx + tw) + 3] = 1
        from PIL import ImageFont
        fnt = ImageFont.truetype(LEX, 36 * 4); tot = f"{len(OEM)}"; num = f"{sel + 1}"
        wt, ws, wn = fnt.getlength(tot) / 4, fnt.getlength(" / ") / 4, fnt.getlength(num) / 4
        draw(r, tot, (990 - wt, 1062), LEX, 36, (165, 165, 172)); draw(r, " / ", (990 - wt - ws, 1062), LEX, 36, (165, 165, 172))
        draw(r, num, (990 - wt - ws - wn, 1062), LEX, 36, (240, 240, 240))
        name, fin, col = OEM[sel]
        retitle(r, box(22, 718, 330, 760), name, OSW, 45.5, OSW_SQ, baseline=1007)
        erase(r, (100, 1020, 420, 1066), thr=40); draw(r, fin, (104, 1058), OSW, 36.5, (238, 238, 238), OSW_SQ)
        # tab row: BLUE back to an unselected tab, RECOMMENDED selected
        ty0, ty1 = 1282, 1329
        bx = (788, 894); g = cv2.cvtColor(r[ty0:ty1, bx[0]:bx[1]], cv2.COLOR_BGR2GRAY)
        dark = (g < 120).astype(np.float32); dark[:6] = 0; dark[-6:] = 0; dark[:, :14] = 0; dark[:, -14:] = 0      # lettering only, not the floor at the leaning corners
        txt = cv2.GaussianBlur(dark, (0, 0), 0.6)[..., None]
        ref = r0[ty0:ty1, 700:708].astype(np.float32).mean(1, keepdims=True)                 # inside the RED tab, left of its lettering
        boxb = np.repeat(ref, bx[1] - bx[0], 1); boxb[:, :2] = r0[ty0:ty1, 694:696]; boxb[:, -2:] = r0[ty0:ty1, 784:786]
        r[ty0 - 4:ty1 + 4, 776:906] = plain[ty0 - 4:ty1 + 4, 776:906]                         # the white box leans past the tab: clear around it
        r[ty0:ty1, bx[0] + 2:bx[1] - 2] = (boxb * (1 - txt) + np.array([232, 232, 236], np.float32) * txt).astype(np.uint8)[:, 2:-2]
        force[ty0:ty1, bx[0] + 2:bx[1] - 2] = 1
        rx = (106, 334); g = cv2.cvtColor(r[ty0:ty1, rx[0]:rx[1]], cv2.COLOR_BGR2GRAY); txt = cv2.GaussianBlur((g > 160).astype(np.float32), (0, 0), 0.6)[..., None]
        r[ty0:ty1, rx[0]:rx[1]] = (246 * (1 - txt) + np.array([34, 30, 30], np.float32) * txt).astype(np.uint8); force[ty0:ty1, rx[0]:rx[1]] = 1
        if done:
            applied(r)
        d = cv2.absdiff(r, plain).max(2).astype(np.float32)
        al = cv2.morphologyEx((d > 18).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)).astype(np.float32)
        al = np.maximum(al, np.clip((d - 8) / 24, 0, 1)); al = cv2.GaussianBlur(al, (0, 0), 0.8)
        keep = np.zeros_like(al); keep[900:1070, 0:560] = 1; keep[1020:1070, 840:1010] = 1; keep[1070:1420, 0:1030] = 1
        al = al * keep
        # counter: digits only (the closed mask drew the counter's box and rule over a light car)
        al[1020:1070, 840:1010] = 0; al[1028:1068, 846:1004] = np.clip((d[1028:1068, 846:1004] - 30) / 40.0, 0, 1)
        al = np.maximum(al, force)
        return {"img": rbase, "view": "P", "overlay": np.dstack([r, np.clip(al * 255, 0, 255).astype(np.uint8)])}
    for k_ in range(len(OEM)):
        st[f"c{k_}"] = respray(k_, False)
    st["cA"] = respray(len(OEM) - 1, True)

    def susp(done, c):
        img = frameB(2100).copy()
        # PERFORMANCE / SUSPENSION (user, v9 review: "Wheel Kits is not suspension"). The capture files its lowered kit
        # under Pro Builds / Wheel Kits; the reel puts it on the Performance tab, where a suspension part belongs.
        erase(img, box(22, 28, 262, 64), thr=16)
        draw(img, "PERFORMANCE /", (45, 83), OSW, 31, (150, 150, 158), OSW_SQ)
        retitle(img, box(30, 68, 420, 110), "SUSPENSION", OSW, None, OSW_SQ)
        applied(img) if done else clear_status(img)
        hx0, hy0, hx1, hy1 = box(815, 1008, 1105, 1052)                       # "Respray the Ganado" hint names the game's car
        m = np.zeros(img.shape[:2], np.uint8); m[hy0:hy1, hx0:hx1] = 255; img[:] = cv2.inpaint(img, m, 6, cv2.INPAINT_TELEA)
        car_tag(img, 555); wallet_clear(img)
        return {"img": img, "view": "S"}
    st["s1"] = susp(False, cash); cash -= GAME["Suspension"]; st["s2"] = susp(True, cash)

    def rims(done, c):
        img = frameB(20040).copy()
        retitle(img, box(30, 768, 420, 812), "CUSTOM 10-SPOKE RIMS", OSW, 51.5, OSW_SQ, dx=5, baseline=1075)
        applied(img) if done else clear_status(img)
        car_tag(img, 920); wallet_clear(img)
        return {"img": img, "view": "W"}
    st["w1"] = rims(False, cash); cash -= GAME["Wheels"]; st["w2"] = rims(True, cash)
    assert cash == 0, cash
    return st


if __name__ == "__main__":
    W = Path("/home/user/media/work/gta6-integra")
    ca, cb = cv2.VideoCapture(U.VID), cv2.VideoCapture(VID_B)
    def fa(f): ca.set(1, f); return ca.read()[1]
    def fb(f): cb.set(1, f); return cb.read()[1]
    st = build(fa, fb); (W / "ui4").mkdir(exist_ok=True)
    tiles = []
    for k in ("m0", "l3b", "n1a", "n2c", "n3c", "f1", "f2", "r1", "r2", "d2", "e2", "a2", "a4", "c0", "c5", "cA", "s2", "w2"):
        im = st[k]["img"].copy()
        if st[k].get("overlay") is not None:
            o = st[k]["overlay"]; a = o[..., 3:] / 255; im = (im * (1 - a) + o[..., :3] * a).astype(np.uint8)
        cv2.imwrite(str(W / "ui4" / f"{k}.png"), im); tiles.append(cv2.resize(im, (1280, 720)))
    cv2.imwrite(str(W / "ui4" / "sheet.jpg"), np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, 18, 3)]), [cv2.IMWRITE_JPEG_QUALITY, 86])
    print("total", TOTAL)
