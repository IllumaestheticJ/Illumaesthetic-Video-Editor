"""Mod-shop reel: the capture's frames with the game's car swapped for the Civic and the menus rebuilt.

    python projects/gta6-customs/tools/compose.py            -> $W/shop.mp4 (2560x1440, 30 fps) + $W/shop_segments.json

v2 (user, v1 review): the four parts are installed one after another and stay on the car. Front lip and side
skirts go on in the menu view, the list's cursor moves to Rear Lip, select, whip to the rear view, rear lip
and wing go on there, whip back to the menu with everything fitted. Each install follows the capture that
shows a purchase (second capture, 3:33): sound starts, the part and the "Applied" state follow 0.1 s later,
the "Purchased" pop-up 0.3 s later; here the wallet also pays the catalogue price.

Per output frame: the capture frame; the menu state's panels pasted in (tools/ui.py); the game car's area
replaced by the clean plate; our render (car + shadow) on top; the pop-up. The whips between views are the
capture's own eight frames with the game car smeared along the pan and our car from orbit cameras.
"""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from plate import fill_directional, fill_nearest
import ui as UI

W = Path("/home/user/media/work/gta6-customs")
VID = "/home/user/media/gta6-customs/capture/gta6_customization_1440p.mp4"
FPS = 30; H, Wd = 1440, 2560; S = 4 / 3
A_POLY = [(505, 885), (488, 740), (518, 640), (572, 430), (588, 250), (612, 232), (962, 230), (988, 340), (1268, 545), (1332, 600),
          (1348, 762), (1342, 792), (1300, 835), (1000, 925), (965, 940), (560, 910)]     # game car outline, rear view, 1920-wide coords
R = lambda x0, y0, x1, y1: tuple(int(round(v * S)) for v in (x0, y0, x1, y1))
RECTS = {"M": [R(0, 150, 640, 760), R(1466, 915, 1894, 998), R(1730, 20, 1905, 80)],            # list, car tag, wallet
         "A": [R(0, 0, 640, 130), R(0, 840, 640, 1066), R(1466, 520, 1894, 996), R(1730, 20, 1905, 80)]}   # title, option block, stats panel, wallet
TOAST_BOX = (2270, 535)                       # "Purchased" pop-up, where the second capture shows it (option screens)
TOAST_DY_MENU = 490                           # the same distance above the view dots on the list screen


def timeline():
    """One entry per output frame: capture frame, view, menu state, car before/after and blend, pop-up strength.
    Returns (frames, sound events, segments)."""
    T, ev, seg = [], [], []

    def add(name, src, view, fn, audio_from=None):
        src = list(src); g0 = len(T)
        for i, f in enumerate(src):
            ui, car = fn(i)
            T.append({"src": f, "view": view, "ui": ui, "car": car, "toast": 0.0})
        seg.append({"name": name, "src": [src[0], src[-1]], "out_start": g0, "frames": len(src), "audio_from": audio_from if audio_from is not None else src[0]})
        return g0

    def car_at(i, c, a, b):
        t = float(np.clip((i - (c + 2)) / 4.0, 0, 1))
        return (a, b, t)

    def pop(g):
        for k in range(9, 45):
            if g + k < len(T):
                T[g + k]["toast"] = float(min(1, (k - 8) / 4.0, (45 - k) / 6.0))

    # menu view, part 1: stock -> front lip -> side skirts -> cursor on Rear Lip -> select (the capture's own, at frame 275)
    c1, r1, c2, r2 = 21, 62, 74, 119
    def m1(i):
        ui = "m0" if i < c1 + 4 else "m1" if i < r1 else "m2" if i < c2 + 4 else "m3" if i < r2 else "m4"
        car = car_at(i, c1, "M_stock", "M_lip") if i < c2 else car_at(i, c2, "M_lip", "M_ls")
        return ui, car
    g = add("menu", range(10, 278, 2), "M", m1)
    ev += [[g + c1, "purchase"], [g + r1, "row"], [g + c2, "purchase"], [g + r2, "row"]]; pop(g + c1); pop(g + c2)
    add("whip_in", range(278, 294, 2), "whip", lambda i: ("a1", ("whip_ls", i)))
    c3 = 14
    g = add("rear_lip", range(294, 400, 2), "A", lambda i: ("a1" if i < c3 + 4 else "a2", car_at(i, c3, "A_ls", "A_lsr")))
    ev.append([g + c3, "purchase"]); pop(g + c3)
    c4 = 17
    g = add("wing", range(880, 1040, 2), "A", lambda i: ("a3" if i < c4 + 4 else "a4", car_at(i, c4, "A_lsr", "A_kit")))
    ev += [[g, "option"], [g + c4, "purchase"]]; pop(g + c4)
    g = add("whip_out", range(1165, 1181, 2), "whip", lambda i: ("mF", ("whip_kit", 7 - i)))
    ev.append([g - 2, "back"])
    add("menu_done", range(1181, 1341, 2), "M", lambda i: ("mF", ("M_kit", "M_kit", 1.0)), audio_from=100)
    return T, ev, seg


def main():
    cap = cv2.VideoCapture(VID)

    def frame(f):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = cap.read(); assert ok, f
        return im

    load = lambda n: cv2.resize(cv2.imread(str(W / "cars" / f"{n}.png"), cv2.IMREAD_UNCHANGED), (Wd, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    cars = {n: load(n) for n in ("M_stock", "M_lip", "M_ls", "M_kit", "A_ls", "A_lsr", "A_kit")}
    whips = {k: [load(f"{k}/w_{i:02d}") for i in range(8)] for k in ("whip_ls", "whip_kit")}
    states = UI.build(frame)
    toast = cv2.imread(str(W / "sfx/toast.png"), cv2.IMREAD_UNCHANGED).astype(np.float32)
    ute = {"M": cv2.imread(str(W / "frames/M_utemask.png"), 0) > 0}
    a = np.zeros((H, Wd), np.uint8); cv2.fillPoly(a, [(np.array(A_POLY) * S).astype(np.int32)], 1)
    ute["A"] = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) > 0
    xs = np.arange(Wd, dtype=np.float32) / (620 * S); t = np.clip(xs, 0, 1); grad_M = (0.35 + 0.65 * t * t * (3 - 2 * t))[None, :, None]
    plates = {}

    def plate(view, key, ref):
        """Clean plate for a view and a car render: the reference frame with the uncovered game car filled in."""
        if (view, key) in plates:
            return plates[(view, key)]
        covered = cv2.erode((cars[key][..., 3] > 200).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        hole = ute[view] & ~covered
        if view == "M":
            p = ref.copy()
            right = hole.copy(); right[:, :1500] = False
            left = hole.copy(); left[:, 1500:] = False
            vp0 = np.array([-1583.0, 396.0])          # tail side: the door's sun line runs toward the left vanishing point
            ys, xs_ = np.nonzero(right)
            if len(xs_):
                c = np.array([xs_.mean(), ys.mean()]); p = fill_directional(p, right, tuple(c * 2 - vp0 + (c - vp0) * 40))
            p = fill_directional(p, left, (900, 5000))
        else:
            p = fill_nearest(ref, hole, [(-30000, 1100), (33000, 900), (1280, 30000)], block=ute[view])
        plates[(view, key)] = p
        return p

    def over(base, rgba, grad=None):
        al = rgba[..., 3:] / 255.0
        return base * (1 - al) + (rgba[..., :3] if grad is None else rgba[..., :3] * grad) * al

    def with_car(base, view, key):
        p = plate(view, key, base)
        out = base.astype(np.float32); out[ute[view]] = p[ute[view]]
        return over(out, cars[key], grad_M if view == "M" else None)

    def static(F, view, ui, car):
        """One frame of a held view: the state's panels, game car out, our car in (blended while a part fades in)."""
        out = F.copy(); st = states[ui]
        for x0, y0, x1, y1 in RECTS[view]:
            out[y0:y1, x0:x1] = st[y0:y1, x0:x1]
        a_, b_, t_ = car
        res = with_car(out, view, b_)
        if t_ < 1:
            res = with_car(out, view, a_) * (1 - t_) + res * t_
        return res

    def put_toast(out, strength, view):
        if strength <= 0:
            return
        x0, y0 = TOAST_BOX; y0 += TOAST_DY_MENU if view == "M" else 0
        h, w = toast.shape[:2]; al = toast[..., 3:] / 255.0 * strength
        out[y0:y0 + h, x0:x0 + w] = out[y0:y0 + h, x0:x0 + w] * (1 - al) + toast[..., :3] * al

    hblur = lambda img, k: cv2.blur(img, (k, 1))
    yy, xx = np.mgrid[0:H, 0:Wd].astype(np.float32)
    centre = np.exp(-(((xx - Wd * 0.47) / (Wd * 0.50)) ** 4 + ((yy - H * 0.60) / (H * 0.40)) ** 4))[..., None]   # where the game car is in a whip

    def soft(rects, sigma=18):
        m = np.zeros((H, Wd), np.float32)
        for x0, y0, x1, y1 in rects:
            m[y0:y1, x0:x1] = 1
        return cv2.GaussianBlur(m, (0, 0), sigma)[..., None]

    hold_A = soft([R(0, 0, 440, 118), R(0, 845, 470, 1062)], 12); hold_M = soft([R(0, 0, 540, 510), R(0, 0, 330, 760)])
    T, events, segs = timeline()
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{Wd}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "1", "-pix_fmt", "yuv420p", str(W / "shop.mp4")], stdin=subprocess.PIPE)
    refs = {}
    for n, e in enumerate(T):
        F = frame(e["src"])
        if e["view"] == "whip":
            ui = e["ui"]; key, idx = e["car"]
            out = F.astype(np.float32)
            out = out * (1 - centre) + hblur(out, 301) * centre                   # smear the game car along the pan
            out = over(out, hblur(whips[key][idx], 61))
            if ui not in refs:                                                    # the held frame this whip leads to (or leaves)
                nxt = next(x for x in T[n:] if x["view"] != "whip") if ui.startswith("a") else next(x for x in T[n:] if x["view"] == "M")
                refs[ui] = static(frame(nxt["src"]), nxt["view"], ui, (nxt["car"][1], nxt["car"][1], 1.0))
            ref = refs[ui]
            # the screen's corners with lettering are held still through the whip (dark gradient, little scene shows);
            # opaque panels are pasted; the stats panel that is fading out on the way back is streaked
            if ui.startswith("a"):
                out = out * (1 - hold_A) + ref * hold_A
                for x0, y0, x1, y1 in RECTS["A"][2:]:
                    out[y0:y1, x0:x1] = ref[y0:y1, x0:x1]
            else:
                y0_, y1_, x0_ = int(H * 0.48), int(H * 0.95), int(Wd * 0.74)
                out[y0_:y1_, x0_:] = hblur(np.ascontiguousarray(out[y0_:y1_, x0_:]), 301)
                out = out * (1 - hold_M) + ref * hold_M
                for x0, y0, x1, y1 in RECTS["M"][1:]:
                    out[y0:y1, x0:x1] = ref[y0:y1, x0:x1]
        else:
            out = static(F, e["view"], e["ui"], e["car"])
            put_toast(out, e["toast"], e["view"])
        ff.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
        if n % 60 == 0:
            print("frame", n, "/", len(T), flush=True)
    ff.stdin.close(); ff.wait()
    json.dump({"fps": FPS, "segments": segs, "events": events, "frames": len(T)}, open(W / "shop_segments.json", "w"), indent=1)
    print("frames", len(T), "seconds", round(len(T) / FPS, 2))


if __name__ == "__main__":
    main()
