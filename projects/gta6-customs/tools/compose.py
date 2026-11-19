"""Mod-shop reel: the capture's frames with the game's car swapped for the Civic and the menus re-lettered.

    python projects/gta6-customs/tools/compose.py            -> $W/shop.mp4 (2560x1440, 30 fps) + $W/shop_segments.json

Per output frame: the capture frame; the re-lettered menu pasted where it differs from the original
(tools/ui.py); the game car's area replaced by the clean plate; our render (car + shadow) on top.
The whips between views are the capture's own eight frames with the game car smeared out along the pan and
our car rendered from orbit cameras in between (tools/whipcams.py), blurred the same way.
"""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from plate import fill_directional, fill_nearest

W = Path("/home/user/media/work/gta6-customs")
VID = "/home/user/media/gta6-customs/capture/gta6_customization_1440p.mp4"
FPS = 30
# (name, capture frames, view, menu state, car render)        capture is 60 fps with every frame doubled: step 2
SEGMENTS = [
    ("menu",      range(150, 278, 2),   "M", "menu2", "M_stock"),
    ("whip_in",   range(278, 294, 2),   "whip", "none", "whip:0"),
    ("wing_none", range(294, 398, 2),   "A", "none", "A_stock"),
    ("wing_on",   range(880, 1000, 2),  "A", "wing", "A_wing"),
    ("whip_out",  range(1165, 1181, 2), "whip", "menu2b", "whip:1"),
    ("menu_back", range(1181, 1276, 2), "M", "menu2b", "M_stock"),
    ("menu_next", range(1277, 1340, 2), "M", "menu3", "M_stock"),
    ("full_kit",  range(1510, 1640, 2), "M", "kit", "M_kit"),
]
A_POLY = [(505, 885), (488, 740), (518, 640), (572, 430), (588, 250), (612, 232), (962, 230), (988, 340), (1268, 545), (1332, 600),
          (1348, 762), (1342, 792), (1300, 835), (1000, 925), (965, 940), (560, 910)]     # game car outline, rear view, 1920-wide coords


def main():
    cap = cv2.VideoCapture(VID)

    def frame(f):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = cap.read(); assert ok, f
        return im

    H, Wd = 1440, 2560
    load = lambda n: cv2.resize(cv2.imread(str(W / "cars" / f"{n}.png"), cv2.IMREAD_UNCHANGED), (Wd, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    cars = {n: load(n) for n in ("M_stock", "M_kit", "A_stock", "A_wing")}
    whip = [load(f"whip/w_{i:02d}") for i in range(8)]
    # menu patches: where the re-lettered reference differs from its source
    ui = {}
    for st in ("menu2", "menu2b", "menu3", "none", "wing", "kit"):
        new, src = cv2.imread(str(W / "ui" / f"{st}.png")), cv2.imread(str(W / "ui" / f"{st}_src.png"))
        m = (cv2.absdiff(new, src).max(2) > 6).astype(np.uint8)
        ui[st] = (new, cv2.dilate(m, np.ones((7, 7), np.uint8)) > 0)
    # game-car masks
    ute = {"M": cv2.imread(str(W / "frames/M_utemask.png"), 0) > 0}
    a = np.zeros((H, Wd), np.uint8); cv2.fillPoly(a, [(np.array(A_POLY) * 4 / 3).astype(np.int32)], 1)
    ute["A"] = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) > 0
    # the menu's dark gradient lies over the car too: darken our car toward the left edge the same way (menu view)
    xs = np.arange(Wd, dtype=np.float32) / (620 * 4 / 3); t = np.clip(xs, 0, 1); grad_M = (0.35 + 0.65 * t * t * (3 - 2 * t))[None, :, None]

    plates = {}
    PX0, PY0, PX1, PY1 = int(1466 * 4 / 3), int(520 * 4 / 3), int(1894 * 4 / 3), int(996 * 4 / 3)     # stats panel (rear-view and kit screens)
    kit_extra = np.zeros((H, Wd), bool); kit_extra[int(H * 0.70):int(H * 0.84), int(Wd * 0.13):int(Wd * 0.40)] = True

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
            # tail side: the door's sun line runs toward the left vanishing point, so mirror outward along those lines
            vp0 = np.array([-1583.0, 396.0])
            ys, xs_ = np.nonzero(right)
            if len(xs_):
                far = np.array([xs_.mean(), ys.mean()]) * 2 - vp0 + (np.array([xs_.mean(), ys.mean()]) - vp0) * 40
                p = fill_directional(p, right, tuple(far))
            p = fill_directional(p, left, (900, 5000))
        else:
            p = fill_nearest(ref, hole, [(-30000, 1100), (33000, 900), (1280, 30000)], block=ute[view])
        plates[(view, key)] = (p, ute[view])
        cv2.imwrite(str(W / f"frames/plate_{view}_{key}.jpg"), cv2.resize(p, (1280, 720)))
        return plates[(view, key)]

    def over(base, rgba, grad=None):
        al = rgba[..., 3:] / 255.0
        col = rgba[..., :3] if grad is None else rgba[..., :3] * grad
        return base * (1 - al) + col * al

    def hblur(img, k):
        return cv2.blur(img, (k, 1))

    def static(F, view, state, car):
        """One frame of a held view: re-lettered menu, game car out, our car in."""
        new, um = ui[state]
        out = F.copy()
        out[um] = new[um]
        if state == "kit":
            # Same camera as the menu, but the capture's car here is the game's yellow kit car. Use the menu's
            # plate for the whole car area (and the floor in front of it, which mirrors the yellow), and the
            # stats panel from the rear-view screen, where nothing bright stands behind it: the game's own
            # numbers for this car, without the game kit's stat gains.
            p, region = plate("M", "M_stock", None)
            region = region | kit_extra
        else:
            p, region = plate(view, car, out if (view, car) not in plates else None)
        out = out.astype(np.float32)
        out[region] = p[region]
        out = over(out, cars[car], grad_M if view == "M" else None)
        if state == "kit":
            out[PY0:PY1, PX0:PX1] = ui["none"][0][PY0:PY1, PX0:PX1]
        return out

    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{Wd}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "1", "-pix_fmt", "yuv420p", str(W / "shop.mp4")], stdin=subprocess.PIPE)
    meta, n, menu_ref = [], 0, None
    yy, xx = np.mgrid[0:H, 0:Wd].astype(np.float32)
    centre = np.exp(-(((xx - Wd * 0.47) / (Wd * 0.50)) ** 4 + ((yy - H * 0.60) / (H * 0.40)) ** 4))[..., None]   # where the game car is in a whip
    for name, frames, view, state, car in SEGMENTS:
        frames = list(frames)
        new, um = ui[state]
        for i, f in enumerate(frames):
            F = frame(f)
            if view == "whip":
                out = F.astype(np.float32)
                out = out * (1 - centre) + hblur(out, 301) * centre          # smear the game car along the pan
                k = int(car.split(":")[1]); idx = i if k == 0 else len(whip) - 1 - i
                out = over(out, hblur(whip[idx], 61))
                tight = cv2.dilate((cv2.absdiff(new, cv2.imread(str(W / "ui" / f"{state}_src.png"))).max(2) > 40).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
                keep = np.zeros((H, Wd), bool)
                keep[:, :int(Wd * 0.30)] = True; keep[int(H * 0.50):, int(Wd * 0.75):] = True  # lettering and car tag only
                # put the capture's own panels back over the smear, then our lettering
                panel = np.zeros((H, Wd), bool); panel[int(H * 0.50):int(H * 0.93), int(Wd * 0.76):int(Wd * 0.99)] = not state.startswith("menu")
                panel[int(H * 0.84):int(H * 0.93), int(Wd * 0.76):int(Wd * 0.99)] |= state.startswith("menu")
                if state.startswith("menu"):
                    # Whip back to the menu. The list and the car's name come from the finished menu frame that follows
                    # (so what shows through the erased rows is our scene, not the game car), and the stats panel that
                    # is fading out in the capture, old car name and all, is streaked along the pan.
                    if menu_ref is None:
                        menu_ref = static(frame(frames[-1] + 2), "M", state, "M_stock")
                    y0_, y1_, x0_ = int(H * 0.48), int(H * 0.95), int(Wd * 0.74)
                    out[y0_:y1_, x0_:] = hblur(np.ascontiguousarray(out[y0_:y1_, x0_:]), 301)
                    tagm = np.zeros((H, Wd), bool); tagm[int(918 * 4 / 3):int(996 * 4 / 3), PX0:PX1] = True
                    out[tagm] = menu_ref[tagm]
                    # the list's corner of the frame (dark gradient, little of the scene shows) is held still through the
                    # whip: pasting only the new glyphs left the capture's old rows smeared underneath
                    ls = np.zeros((H, Wd), np.float32)
                    ls[:int(H * 0.47), :int(Wd * 0.28)] = 1; ls[:int(H * 0.70), :int(Wd * 0.17)] = 1
                    ls = cv2.GaussianBlur(ls, (0, 0), 18)[..., None]
                    out = out * (1 - ls) + menu_ref * ls
                else:
                    out[panel] = F[panel]
                    out[tight & keep] = new[tight & keep]
                    tag = np.zeros((H, Wd), bool); tag[PY0:int(PY0 + 110 * 4 / 3), PX0:PX1] = True     # car name in the stats panel
                    out[um & tag] = new[um & tag]
            else:
                out = static(F, view, state, car)
            ff.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes()); n += 1
        meta.append({"name": name, "src": [frames[0], frames[-1]], "out_start": n - len(frames), "frames": len(frames)})
        print(name, len(frames), "frames", flush=True)
    ff.stdin.close(); ff.wait()
    json.dump({"fps": FPS, "segments": meta, "frames": n}, open(W / "shop_segments.json", "w"), indent=1)
    print("frames", n, "seconds", round(n / FPS, 2))


if __name__ == "__main__":
    main()
