"""GTA 6 mod-shop reel for the MR2 Spyder (ZZW30) kit: the Civic reel's v19 structure (projects/gta6-customs, tools/compose4.py) with
eight parts, each entered from the list, bought on a camera that shows it, and left back to the list.
    python projects/gta6-mr2-spyder/tools/compose4.py   -> $W/shop4.mp4 + $W/shop4_segments.json   (START / END / OUTNAME / WRITE_JSON for partial renders)
"""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from plate import fill_directional, fill_nearest, fill_from_above, fill_wall_floor
import ui as U, ui4 as ui3

W = Path("/home/user/media/work/gta6-mr2-spyder"); CARS = W / "cars3"
FPS = 30; H, Wd = 1440, 2560; S = 4 / 3
R = ui3.R
TITLE, BLOCK, HINT = R(0, 0, 640, 130), R(0, 760, 640, 1066), R(815, 1008, 1105, 1052)
PRE = {"F": [TITLE, BLOCK], "H": [TITLE, BLOCK, HINT], "T": [TITLE, BLOCK, HINT], "D": [TITLE, R(0, 600, 640, 1066), HINT], "M": [R(0, 150, 640, 760), R(0, 70, 955, 120)],
       "A": [TITLE, R(0, 840, 640, 1066)], "E": [TITLE, R(0, 840, 640, 1066)],
       "P": [TITLE, R(0, 790, 1080, 1066)], "S": [TITLE, R(0, 795, 470, 1066), HINT],
       "W": [TITLE, R(0, 655, 760, 1066)], "X": []}        # W: the whole block (price, name, thumbnails) from the state
PANEL, TAG, WALLET = R(1466, 553, 1894, 996), R(1466, 915, 1894, 998), R(1730, 20, 1905, 80)    # panel only: the strip above it is scene
POST = {v: [PANEL, WALLET] for v in "FHDTAEPS"}; POST.update({"M": [TAG, WALLET], "W": [TAG], "X": []})
# W: the wallet sits over the car's body there, so it is laid on as glyphs (anything in its box that is not the game car's yellow)
TOAST = {v: (2270, 535) for v in "FHDTAEPS"}; TOAST.update({"M": (2270, 1025), "W": (2270, 1025)})
LINE = "Need anything else, or is that everything?"


def fw(a, b, n):
    """n capture frames from a held view: forward, then the last frame held. Never back and forth (lesson: anything that moves runs backwards)."""
    f = list(range(a, b + 1, 2))
    return [f[min(i, len(f) - 1)] for i in range(n)]


def timeline():
    T, ev, seg = [], [], []

    def add(name, cap, src, view, fn):
        g0 = len(T)
        for i, f in enumerate(src):
            ui, car = fn(i)
            T.append({"cap": cap, "src": f, "view": view, "ui": ui, "car": car, "toast": 0.0, "sub": 0.0})
        seg.append({"name": name, "out_start": g0, "frames": len(src)})
        return g0

    def whip(key):
        g0 = len(T)
        for i in range(8):
            T.append({"view": "whip", "key": key, "i": i, "uid": g0})
        seg.append({"name": "whip_" + key, "out_start": g0, "frames": 8})

    fade = lambda i, c, a, b: (a, b, float(np.clip((i - (c + 2)) / 4.0, 0, 1)))

    def buy(g):
        ev.append([g, "purchase"])
        for k in range(9, 41):
            if g + k < len(T) and T[g + k]["view"] != "whip":
                T[g + k]["toast"] = float(min(1, (k - 8) / 4.0, (41 - k) / 6.0))

    def simple(name, cap, src, view, s1, s2, car1, car2, c):
        g = add(name, cap, src, view, lambda i: (s1 if i < c + 4 else s2, fade(i, c, car1, car2)))
        buy(g + c); last["g"] = g + c; return g

    last = {}; spends = []

    def spend(amount):                          # the wallet counts down over 0.4 s, starting as the part appears
        spends.append((last["g"] + 3, amount))

    P_ = ui3.PRICES; G_ = ui3.GAME
    # v12 (user, v11 review: the navigation for the aero parts skipped steps): every part is entered from the list and left
    # back to it: select, camera to the part, buy, back, camera to the list (row now marked), down one, select ...
    def nav(name, steps, car, sounds):
        """steps: [(state, frames), ...] on the menu camera; sounds: [(frame offset, name), ...]"""
        keys = [k for k, n_ in steps for _ in range(n_)]
        # forward frames only: a ping-pong of the capture made whatever moves in the background run back and forth (user, v14 review)
        g_ = add(name, "A", range(100, 100 + 2 * len(keys), 2), "M", lambda i: (keys[i], (car, car, 1.0)))
        ev.extend([g_ + o, nm] for o, nm in sounds)

    def back_to(key):
        ev.append([len(T) - 3, "back"]); whip(key)

    PART = 54; step = [(7, "row"), (14, "select")]
    SRC = {"F": ("B", lambda n: fw(14706, 14748, n)), "H": ("B", lambda n: fw(11916, 11952, n)), "D": ("B", lambda n: fw(2083, 2151, n)),
           "E": ("B", lambda n: fw(17951, 17970, n)), "T": ("B", lambda n: fw(16582, 16695, n)), "A": ("A", lambda n: list(range(880, 880 + 2 * n, 2)))}
    g = add("menu", "A", range(10, 70, 2), "M", lambda i: ("m0", ("M_s0", "M_s0", 1.0)))
    PL = ui3.PARTS
    ev.append([g + 27, "select"]); whip("M_" + PL[0][2])
    for k, (name, pr, view, slot) in enumerate(PL, 1):
        cap, src = SRC[view]
        simple(slot, cap, src(PART), view, f"p{k}a", f"p{k}b", f"{view}_s{k - 1}", f"{view}_s{k}", 12); spend(pr)
        back_to(view + "_M")
        if k < len(PL):
            nav(f"list_{k}", [(f"l{k}", 7), (f"l{k}b", 9)], f"M_s{k}", step); whip("M_" + PL[k][2])
    # between sections: back on the list, shoulder button to the tab, the tab's own rows, select (v9)
    nav("nav_paint", [("n1a", 10), ("n1b", 14)], "M_s8", [(10, "tab"), (22, "select")])
    # respray: Recommended tab with the car's OEM colours; the cursor runs through all eleven (3 frames each, a tick each),
    # the car previews each colour, and Boost Blue is bought
    NC = len(ui3.OEM); cbuy = 6 + 3 * (NC - 1) + 6
    ckey = lambda k: "M_s8" if k == 0 else "M_ky" if k == NC - 1 else f"M_c{k}"
    def rs(i):
        k = int(np.clip((i - 6) // 3 + 1, 0, NC - 1)) if i >= 6 else 0
        return ("cA" if i >= cbuy + 4 else f"c{k}"), (ckey(k), ckey(k), 1.0)
    g = add("respray", "A", range(1510, 1510 + 2 * (cbuy + 46), 2), "P", rs)
    ev.extend([g + 6 + 3 * k, "step"] for k in range(NC - 1)); buy(g + cbuy)
    # Cosmetics -> Bodywork -> Performance (two presses, as the tab order requires), down to Suspension, select
    nav("nav_susp", [("n2a", 10), ("n2x", 7), ("n2b", 9), ("n2c", 10)], "M_ky", [(-2, "back"), (10, "tab"), (17, "tab"), (26, "row"), (34, "select")])
    whip("M_S")
    simple("suspension", "B", fw(2083, 2151, 64), "S", "s1", "s2", "S_ky", "S_low", 16); spend(G_["Suspension"])
    back_to("S_M")
    nav("nav_wheels", [("n3a", 12), ("n3b", 12), ("n3c", 12)], "M_low", [(12, "tab"), (24, "row"), (34, "select")])
    whip("M_W")
    simple("wheels", "B", fw(20258, 20398, 64), "W", "w1", "w2", "W_low", "W_fin", 16); spend(G_["Wheels"])
    back_to("W_M")
    # one frozen frame: the UI-free stretch is ten frames long, and looping it made the background run back and forth
    g = add("exit", "A", [4096] * 68, "X", lambda i: (None, ("M_fin", "M_fin", 1.0)))
    for k in range(12, 64):
        T[g + k]["sub"] = float(min(1, (k - 11) / 3.0, (64 - k) / 4.0))
    ev.append([g + 12, "line"])
    total = sum(a for _, a in spends)
    for n, e in enumerate(T):
        cash = total
        for g0, a in spends:
            u = float(np.clip((n - g0) / 12.0, 0, 1)); cash -= a * u * u * (3 - 2 * u)
        e["cash"] = cash
    assert total == ui3.TOTAL, (total, ui3.TOTAL)
    return T, ev, seg


def main():
    caps = {"A": cv2.VideoCapture(U.VID), "B": cv2.VideoCapture(ui3.VID_B)}

    def frame(cap, f):
        caps[cap].set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = caps[cap].read(); assert ok, (cap, f)
        return im

    load = lambda p: cv2.resize(cv2.imread(str(CARS / p), cv2.IMREAD_UNCHANGED), (Wd, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    cars = {}
    car = lambda n: cars.setdefault(n, load(n + ".png"))
    whips = {}
    states = ui3.build(lambda f: frame("A", f), lambda f: frame("B", f))
    toast = cv2.imread(str(W / "sfx/toast.png"), cv2.IMREAD_UNCHANGED).astype(np.float32)
    z = np.load(str(W / "frames/masks0.npz")); ute = {}
    for k in z.files:                                  # the game car's outline per view (tools: camsearch.py notes), grown 20 px
        ute[k] = cv2.dilate(z[k], cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) > 0
    ute["D"] = ute["S"]                               # the side-skirt shot uses the low front-quarter screen's frames
    kit_extra = np.zeros((H, Wd), bool); kit_extra[int(H * 0.70):int(H * 0.84), int(Wd * 0.13):int(Wd * 0.40)] = True
    ute["P"] = ute["M"] | kit_extra; ute["X"] = ute["M"]
    xs = np.arange(Wd, dtype=np.float32) / (620 * S); t = np.clip(xs, 0, 1); grad_M = (0.35 + 0.65 * t * t * (3 - 2 * t))[None, :, None]
    A100 = frame("A", 100)
    plates = {}

    def plate(view, key, ref):
        if (view, key) in plates:
            return plates[(view, key)]
        covered = cv2.erode((car(key)[..., 3] > 200).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        if view in ("M", "P", "X"):                   # one camera; plate always from the list screen's frame (dark car, no kit block)
            hole = ute["M"] & ~covered
            p = A100.copy()
            right = hole.copy(); right[:, :1500] = False
            left = hole.copy(); left[:, 1500:] = False
            vp0 = np.array([-1583.0, 396.0]); ys, xs_ = np.nonzero(right)
            if len(xs_):
                c = np.array([xs_.mean(), ys.mean()]); p = fill_directional(p, right, tuple(c * 2 - vp0 + (c - vp0) * 40))
            p = fill_directional(p, left, (900, 5000))
        else:
            hole = ute[view] & ~covered
            if view in ("D", "S"):                    # low front-quarter views: the game car's bed sticks out behind our tail,
                # in front of the open door. Mirror the doorway in from the right and the floor up from below; never sample
                # the stats panel. (Filling from above streaked the bunting down the frame; blurring it read as a smear.)
                blockm = ute[view].copy(); blockm[int(H * 0.46):int(H * 0.93), int(Wd * 0.755):] = True
                p = fill_nearest(ref, hole, [(33000, 500), (1280, 30000)], block=blockm)
            else:
                p = fill_nearest(ref, hole, [(-30000, 1100), (33000, 900), (1280, 30000)], block=ute[view])
            if view == "W":                    # close-ups: what the game's car hid is far background, out of focus
                soft_ = cv2.GaussianBlur(p, (0, 0), 14); wgt = cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 6)[..., None]
                p = (p * (1 - wgt) + soft_ * wgt).astype(np.uint8)
        plates[(view, key)] = p
        cv2.imwrite(str(W / f"v3/plate4_{view}_{key}.jpg"), cv2.resize(p, (1280, 720)))
        print("plate", view, key, "uncovered px", int(hole.sum()), f"{100 * hole.sum() / hole.size:.1f} % of frame", flush=True)
        return p

    def over(base, rgba, grad=None):
        al = rgba[..., 3:] / 255.0
        return base * (1 - al) + (rgba[..., :3] if grad is None else rgba[..., :3] * grad) * al

    def with_car(base, view, key):
        p = plate(view, key, base)
        out = base.astype(np.float32); out[ute[view]] = p[ute[view]]
        return over(out, car(key), grad_M if view == "M" else None)

    # Second capture: the uploader's watermark sits bottom right over the floor and over the game's own button hints
    # (user, v11 review: "remove the watermark on the bottom right"). The corner is covered with floor from the same frame
    # (the patch up and to the left of it) and the first capture's clean "BACK" hint is put back.
    WM = (1950, 1352, 2560, 1436)
    a340 = frame("A", 340); hx0, hy0, hx1, hy1 = 2370, 1358, 2530, 1416
    hreg = a340[hy0:hy1, hx0:hx1].astype(np.float32); hmed = cv2.medianBlur(a340[hy0:hy1, hx0:hx1], 31).astype(np.float32)
    halpha = np.clip((np.abs(hreg - hmed).max(2) - 30) / 30.0, 0, 1)
    halpha = cv2.GaussianBlur(cv2.dilate(halpha, np.ones((3, 3), np.uint8)), (0, 0), 0.6)[..., None]
    wy0, wy1 = WM[1], WM[3]; wx0, wx1 = WM[0], WM[2]
    feather = np.ones((wy1 - wy0, wx1 - wx0), np.float32); feather[:10] = np.linspace(0, 1, 10)[:, None]; feather[:, :14] *= np.linspace(0, 1, 14)[None, :]
    feather = feather[..., None]

    def dewatermark(F):
        out = F.astype(np.float32)
        src = out[wy0 - (wy1 - wy0) - 2:wy0 - 2, wx0 - (wx1 - wx0):wx0][:, ::-1]        # floor beside the corner, mirrored so the seam matches
        out[wy0:wy1, wx0:wx1] = out[wy0:wy1, wx0:wx1] * (1 - feather) + src * feather
        out[hy0:hy1, hx0:hx1] = out[hy0:hy1, hx0:hx1] * (1 - halpha) + hreg * halpha
        return np.clip(out, 0, 255).astype(np.uint8)

    def static(e):
        F = frame(e["cap"], e["src"]); view = e["view"]; st = states.get(e["ui"]) if e["ui"] else None
        if e["cap"] == "B":
            F = dewatermark(F)
        out = F.copy()
        if view == "X":                               # leaving: the capture still shows its wallet and the "Leave when ready" prompt
            U.erase(out, (1100, 1350, 1460, 1410), thr=25); ui3.wallet_clear(out)
        if st is not None:
            for x0, y0, x1, y1 in PRE[view]:
                out[y0:y1, x0:x1] = st["img"][y0:y1, x0:x1]
        a_, b_, t_ = e["car"]
        res = with_car(out, view, b_)
        if t_ < 1:
            res = with_car(out, view, a_) * (1 - t_) + res * t_
        if st is not None:
            for x0, y0, x1, y1 in POST[view]:
                res[y0:y1, x0:x1] = st["img"][y0:y1, x0:x1]
            if st.get("overlay") is not None:
                res = over(res, st["overlay"])
            if view == "W":                           # wallet icon as glyphs: it sits over the car's body here
                x0, y0, x1, y1 = WALLET; reg = st["img"][y0:y1, x0:x1].astype(np.float32)
                med = np.median(reg.reshape(-1, 3), 0)
                al = np.clip((np.abs(reg - med).max(2) - 28) / 30.0, 0, 1)
                al = cv2.GaussianBlur(cv2.morphologyEx(al, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)), (0, 0), 0.7)[..., None]
                res[y0:y1, x0:x1] = res[y0:y1, x0:x1] * (1 - al) + reg * al
        if st is not None or view == "X":             # live wallet figure
            u8 = np.clip(res, 0, 255).astype(np.uint8); ui3.wallet_text(u8, e["cash"]); res = u8.astype(np.float32)
        if e["toast"] > 0:
            x0, y0 = TOAST[view]; h, w = toast.shape[:2]; al = toast[..., 3:] / 255.0 * e["toast"]
            res[y0:y0 + h, x0:x0 + w] = res[y0:y0 + h, x0:x0 + w] * (1 - al) + toast[..., :3] * al
        if e["sub"] > 0:
            img = np.clip(res, 0, 255).astype(np.uint8); lay = img.copy()
            from PIL import ImageFont
            wtxt = ImageFont.truetype(U.LEX, 46 * 4).getlength(LINE) / 4
            x = Wd / 2 - wtxt / 2; y = 1392
            for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2), (-2, -2), (2, -2), (-2, 2), (0, 4)):
                U.draw(lay, LINE, (x + ox, y + oy), U.LEX, 46, (20, 20, 22))
            U.draw(lay, LINE, (x, y), U.LEX, 46, (245, 245, 245))
            res = res * (1 - e["sub"]) + lay.astype(np.float32) * e["sub"]
        return res

    hblur = lambda img, k: cv2.blur(img, (k, 1))

    def shift(img, dx):
        M_ = np.float32([[1, 0, dx], [0, 1, 0]])
        return cv2.warpAffine(img, M_, (Wd, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    def soft(rects, sigma=14):
        m = np.zeros((H, Wd), np.float32)
        for x0, y0, x1, y1 in rects:
            m[y0:y1, x0:x1] = 1
        return cv2.GaussianBlur(m, (0, 0), sigma)[..., None]

    T, events, segs = timeline()
    import os
    if os.environ.get("ONLY"):                       # test: first N frames only
        T = T[:int(os.environ["ONLY"])]
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{Wd}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "1", "-pix_fmt", "yuv420p", str(W / os.environ.get("OUTNAME", "shop4.mp4"))], stdin=subprocess.PIPE)
    prev = None; nxt_cache = {}
    START, END = int(os.environ.get("START", 0)), int(os.environ.get("END", len(T)))     # partial render of frames START..END-1
    for n, e in enumerate(T):
        if n < START - 1 or n >= END:
            continue
        if n == START - 1:                            # only needed as the frame a whip leaves from
            if e["view"] != "whip":
                prev = static(e); prev_cash = e["cash"]; prev_e = e
            continue
        if e["view"] == "whip":
            key, i = e["key"], e["i"]; uid = e["uid"]
            if uid not in nxt_cache:
                ne = next(x for x in T[n:] if x["view"] != "whip"); ne = dict(ne); ne["toast"] = 0.0; ne["sub"] = 0.0; ne["cash"] = prev_cash
                # What gets blurred must not carry sharp bright UI (user, v15 review: "screen tear" at 17 s): the list's white
                # highlight bar smeared into a hard band, and the option block held sharp showed a rectangle of the next
                # shot's car. So the list is taken out of both blurred frames, and only the lettering corners are held.
                nb = static(dict(ne, ui="m_blank")) if ne["view"] == "M" else None
                nxt_cache[uid] = (static(ne), ne["view"], nb)
                a_, b_ = key.split("_")                # a return whip without frames of its own plays the outward one backwards
                whips[key] = ([load(f"whip_{key}/w_{k:02d}.png") for k in range(8)] if (CARS / f"whip_{key}").exists()
                              else [load(f"whip_{b_}_{a_}/w_{7 - k:02d}.png") for k in range(8)])
                hold_from = static(dict(prev_e, ui="m_blank", toast=0.0, sub=0.0)) if prev_e["view"] == "M" else prev.copy()
            nxt, nview, nblank = nxt_cache[uid]
            t = (i + 1) / 9.0
            bg = shift(hold_from, -t * Wd * 0.7) * (1 - t) + shift(nxt if nblank is None else nblank, (1 - t) * Wd * 0.7) * t
            out = hblur(bg, 301)
            out = over(out, hblur(whips[key][i], 61))
            if nblank is not None:
                # list screen: hold exactly what the list adds to the blank screen (rows, highlight bar, tab highlight), nothing
                # of the scene behind it (a sharp scrap of shelf sat beside the list in v16's first pass)
                hm = np.clip(np.abs(nxt - nblank).max(2) / 24.0, 0, 1)
                hm = cv2.GaussianBlur(cv2.dilate(hm, np.ones((5, 5), np.uint8)), (0, 0), 1.2)[..., None]
                hm = np.maximum(hm, soft([R(0, 74, 760, 116)], 6) * 0.9)          # the tab bar's lettering
                out = out * (1 - hm) + nxt * hm
            elif PRE[nview]:
                # the title's lettering only (titles here run to 620 px: a held box that wide would be a sharp rectangle of scenery)
                x0, y0, x1, y1 = R(0, 22, 640, 112); tg = cv2.cvtColor(np.clip(nxt[y0:y1, x0:x1], 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
                tm = cv2.GaussianBlur(cv2.dilate((tg > 150).astype(np.float32), np.ones((5, 5), np.uint8)), (0, 0), 1.2)
                tm[:, 900:] = 0; hm = np.zeros((H, Wd, 1), np.float32); hm[y0:y1, x0:x1, 0] = tm
                out = out * (1 - hm) + nxt * hm
            for rect in POST[nview]:
                if rect is WALLET:                    # a pasted wallet box shows against a blurred frame: figure only
                    continue
                x0, y0, x1, y1 = rect
                out[y0:y1, x0:x1] = nxt[y0:y1, x0:x1]
            u8 = np.clip(out, 0, 255).astype(np.uint8); ui3.wallet_text(u8, prev_cash); out = u8.astype(np.float32)
        else:
            out = static(e); prev = out; prev_cash = e["cash"]; prev_e = e
        ff.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
        if n % 60 == 0:
            print("frame", n, "/", len(T), flush=True)
    ff.stdin.close(); ff.wait()
    if os.environ.get("WRITE_JSON") or not (os.environ.get("ONLY") or os.environ.get("START") or os.environ.get("END")):                   # a partial render (ONLY/OUTNAME, to splice a changed opening in) leaves the timeline file alone
        json.dump({"fps": FPS, "segments": segs, "events": events, "frames": len(T)}, open(W / "shop4_segments.json", "w"), indent=1)
    print("frames", len(T), "seconds", round(len(T) / FPS, 2))


if __name__ == "__main__":
    main()
