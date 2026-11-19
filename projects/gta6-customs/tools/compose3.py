"""v3 of the mod-shop reel (user, v2 review):

  stock car -> Front Lip, Side Skirts (list screen) -> Rear Lip (camera to the second capture's exhaust angle) ->
  Sport Wing (rear view) -> Respray, everything painted -> Suspension (car drops, the game's handling gain) ->
  Rims -> out of the menu, the mechanic's line as a subtitle.

    python projects/gta6-customs/tools/compose3.py     -> $W/shop3.mp4 + $W/shop3_segments.json

Held views are capture frames with the game's car replaced (clean plate + our render) and the state's panels
from tools/ui3.py. The capture has whips for only two of the six view changes, so all six are built the same
way: the two held frames slide and cross-fade under a long horizontal blur, with our car rendered from orbit
cameras between the two views (tools/whipcams.py) and the destination's panels already up, as in the game.
Every change happens at a purchase, timed as the second capture's one purchase: sound, part 0.1 s later,
"Applied" with it, "Purchased" pop-up 0.3 s later.
"""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from plate import fill_directional, fill_nearest, fill_from_above
import ui as U, ui3

W = Path("/home/user/media/work/gta6-customs"); CARS = W / "cars3"
FPS = 30; H, Wd = 1440, 2560; S = 4 / 3
P16 = lambda pts: (np.array(pts) * 1.6).astype(np.int32)
POLY = {
    "A": (np.array([(505, 885), (488, 740), (518, 640), (572, 430), (588, 250), (612, 232), (962, 230), (988, 340), (1268, 545), (1332, 600),
                    (1348, 762), (1342, 792), (1300, 835), (1000, 925), (965, 940), (560, 910)]) * S).astype(np.int32),
    "E": P16([(175, 95), (690, 45), (1050, 45), (1365, 90), (1375, 410), (1340, 445), (1150, 495), (1010, 550), (930, 550), (510, 530),
              (490, 485), (230, 440), (175, 395)]),
    "S": P16([(40, 380), (210, 270), (700, 270), (930, 205), (1090, 212), (1170, 340), (1460, 385), (1460, 470), (1225, 470), (1225, 540),
              (760, 590), (740, 640), (640, 705), (520, 705), (430, 640), (400, 560), (130, 540), (40, 480)]),
    "W": P16([(150, 140), (300, 0), (1600, 0), (1600, 550), (1300, 550), (1250, 620), (1150, 720), (940, 765), (730, 720), (640, 600),
              (600, 480), (350, 370), (180, 370)]),
}
R = ui3.R
PRE = {"M": [R(0, 150, 640, 760)], "A": [R(0, 0, 640, 130), R(0, 840, 640, 1066)], "E": [R(0, 0, 640, 130), R(0, 840, 640, 1066)],
       "P": [R(0, 0, 640, 130), R(0, 790, 1080, 1066)], "S": [R(0, 0, 640, 130), R(0, 795, 470, 1066), R(815, 1008, 1105, 1052)],
       "W": [R(0, 0, 640, 130), R(0, 655, 760, 1066)], "X": []}        # W: the whole block (price, name, thumbnails) from the state
PANEL, TAG, WALLET = R(1466, 553, 1894, 996), R(1466, 915, 1894, 998), R(1730, 20, 1905, 80)    # panel only: the strip above it is scene
POST = {"M": [TAG, WALLET], "A": [PANEL, WALLET], "E": [PANEL, WALLET], "P": [PANEL, WALLET], "S": [PANEL, WALLET], "W": [TAG], "X": []}
# W: the wallet sits over the car's body there, so it is laid on as glyphs (anything in its box that is not the game car's yellow)
TOAST = {"M": (2270, 1025), "W": (2270, 1025), "A": (2270, 535), "E": (2270, 535), "P": (2270, 535), "S": (2270, 535)}
LINE = "Need anything else, or is that everything?"


def pp(a, b, n):
    """n capture frames from a held view that is shorter than needed: forward, back, forward ..."""
    f = list(range(a, b + 1, 2)); f = f + f[-2:0:-1]
    return [f[i % len(f)] for i in range(n)]


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
            T.append({"view": "whip", "key": key, "i": i})
        seg.append({"name": "whip_" + key, "out_start": g0, "frames": 8})

    fade = lambda i, c, a, b: (a, b, float(np.clip((i - (c + 2)) / 4.0, 0, 1)))

    def buy(g):
        ev.append([g, "purchase"])
        for k in range(9, 45):
            if g + k < len(T) and T[g + k]["view"] != "whip":
                T[g + k]["toast"] = float(min(1, (k - 8) / 4.0, (45 - k) / 6.0))

    def simple(name, cap, src, view, s1, s2, car1, car2, c):
        g = add(name, cap, src, view, lambda i: (s1 if i < c + 4 else s2, fade(i, c, car1, car2)))
        buy(g + c); return g

    c1, r1, c2, r2 = 21, 62, 74, 119
    def m(i):
        ui = "m0" if i < c1 + 4 else "m1" if i < r1 else "m2" if i < c2 + 4 else "m3" if i < r2 else "m4"
        return ui, (fade(i, c1, "M_stock", "M_lip") if i < c2 else fade(i, c2, "M_lip", "M_ls"))
    g = add("menu", "A", range(10, 278, 2), "M", m)
    ev += [[g + r1, "row"], [g + r2, "row"], [g + 131, "select"]]; buy(g + c1); buy(g + c2)
    whip("M_E")
    # the capture's camera creeps in over this screen: only the half second around the frame the menu was built on is used
    simple("rear_lip", "B", pp(17946, 17976, 70), "E", "e1", "e2", "E_ls", "E_lsr", 14)
    ev.append([len(T) - 3, "back"]); whip("E_A")
    simple("wing", "A", range(880, 1040, 2), "A", "a1", "a2", "A_lsr", "A_kit", 14)
    ev.append([len(T) - 3, "back"]); whip("A_M")
    simple("respray", "A", range(1510, 1690, 2), "P", "p1", "p2", "M_kit_grey", "M_kit_blue", 24)
    ev.append([len(T) - 3, "back"]); whip("M_S")
    simple("suspension", "B", pp(2072, 2150, 80), "S", "s1", "s2", "S_kit", "S_low", 20)
    ev.append([len(T) - 3, "back"]); whip("S_W")
    simple("wheels", "B", pp(20258, 20398, 80), "W", "w1", "w2", "W_low", "W_te", 20)
    ev.append([len(T) - 3, "back"]); whip("W_M")
    g = add("exit", "A", pp(4086, 4104, 78), "X", lambda i: (None, ("M_final", "M_final", 1.0)))
    for k in range(12, 74):
        T[g + k]["sub"] = float(min(1, (k - 11) / 3.0, (74 - k) / 4.0))
    ev.append([g + 12, "line"])
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
    ute = {"M": cv2.imread(str(W / "frames/M_utemask.png"), 0) > 0}
    for k, poly in POLY.items():
        a = np.zeros((H, Wd), np.uint8); cv2.fillPoly(a, [poly], 1)
        ute[k] = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) > 0
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
            if view == "S":
                p = fill_from_above(ref, hole, ute[view], sigma=11)
            else:
                p = fill_nearest(ref, hole, [(-30000, 1100), (33000, 900), (1280, 30000)], block=ute[view])
            if view == "W":                    # close-ups: what the game's car hid is far background, out of focus
                soft_ = cv2.GaussianBlur(p, (0, 0), 14); wgt = cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 6)[..., None]
                p = (p * (1 - wgt) + soft_ * wgt).astype(np.uint8)
        plates[(view, key)] = p
        cv2.imwrite(str(W / f"v3/plate_{view}_{key}.jpg"), cv2.resize(p, (1280, 720)))
        return p

    def over(base, rgba, grad=None):
        al = rgba[..., 3:] / 255.0
        return base * (1 - al) + (rgba[..., :3] if grad is None else rgba[..., :3] * grad) * al

    def with_car(base, view, key):
        p = plate(view, key, base)
        out = base.astype(np.float32); out[ute[view]] = p[ute[view]]
        return over(out, car(key), grad_M if view == "M" else None)

    def static(e):
        F = frame(e["cap"], e["src"]); view = e["view"]; st = states.get(e["ui"]) if e["ui"] else None
        out = F.copy()
        if view == "X":                               # leaving: the capture still shows its wallet and the "Leave when ready" prompt
            U.erase(out, (1100, 1350, 1460, 1410), thr=25); U.wallet(out, 0)
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
            if view == "W":
                x0, y0, x1, y1 = WALLET; reg = st["img"][y0:y1, x0:x1].astype(np.float32)
                med = np.median(reg.reshape(-1, 3), 0)
                al = np.clip((np.abs(reg - med).max(2) - 28) / 30.0, 0, 1)
                al = cv2.GaussianBlur(cv2.morphologyEx(al, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)), (0, 0), 0.7)[..., None]
                res[y0:y1, x0:x1] = res[y0:y1, x0:x1] * (1 - al) + reg * al
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
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "1", "-pix_fmt", "yuv420p", str(W / "shop3.mp4")], stdin=subprocess.PIPE)
    prev = None; nxt_cache = {}
    for n, e in enumerate(T):
        if e["view"] == "whip":
            key, i = e["key"], e["i"]
            if key not in nxt_cache:
                ne = next(x for x in T[n:] if x["view"] != "whip"); ne = dict(ne); ne["toast"] = 0.0; ne["sub"] = 0.0
                nxt_cache[key] = (static(ne), ne["view"])
                whips[key] = [load(f"whip_{key}/w_{k:02d}.png") for k in range(8)]
                hold_from = prev.copy()
            nxt, nview = nxt_cache[key]
            t = (i + 1) / 9.0
            bg = shift(hold_from, -t * Wd * 0.7) * (1 - t) + shift(nxt, (1 - t) * Wd * 0.7) * t
            out = hblur(bg, 301)
            out = over(out, hblur(whips[key][i], 61))
            if PRE[nview]:
                hm = soft([r for r in PRE[nview] if r[2] < Wd * 0.5]); out = out * (1 - hm) + nxt * hm
            for x0, y0, x1, y1 in POST[nview]:
                out[y0:y1, x0:x1] = nxt[y0:y1, x0:x1]
        else:
            out = static(e); prev = out
        ff.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
        if n % 60 == 0:
            print("frame", n, "/", len(T), flush=True)
    ff.stdin.close(); ff.wait()
    json.dump({"fps": FPS, "segments": segs, "events": events, "frames": len(T)}, open(W / "shop3_segments.json", "w"), indent=1)
    print("frames", len(T), "seconds", round(len(T) / FPS, 2))


if __name__ == "__main__":
    main()
