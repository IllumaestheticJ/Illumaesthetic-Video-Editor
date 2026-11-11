"""Swap the game's cars for Epsilon kit cars in the NFSU2 car-lot menu capture, frame by frame.

    python projects/nfs-carlot/tools/composite.py            # writes $W/menu.mp4 + $W/menu_segments.json

How it works (all coordinates are in the cropped 2144x1206 capture, `a60.mp4`):
  * E = the frame where the menu is up and the turntable is empty and at rest (the clean plate).
  * The game changes cars by sliding the turntable (car on it) out to the left while the next one slides
    in from the right; the menu and the room do not move. `track.py` measures that slide per frame.
  * For every output frame we start from the REAL capture frame, repaint the zone where the game's car
    is with the empty plate (turntable pixels follow the slide, room pixels stay), then lay the Epsilon
    car render (same slide offset) on top. Everything else - menu, stat bars, cursor, room - is the capture.
  * The name plate is repainted with a plate lifted from the capture (Toyota Corolla, Honda Civic, Mazda
    Miata) or, for the car the game never had (Acura Integra), one drawn in the same greys.
  * The timeline is five scrolls of the capture, each range starting on the first frame of a scroll; how long
    each runs is set by the real-time capture's audio so its scroll sounds land on the car changes.
"""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

W = Path("/home/user/media/work/nfs-carlot")
VID, EPATH = W / "a60.mp4", W / "match/E.png"
D_CONVEYOR = 2980                       # px between the outgoing and the incoming turntable
PANEL = (490, 144, 1700, 332)           # x0,y0,x1,y1 of the name plate interior (logo box + wordmark)
BOX = (320, 1078, 696, 1206)            # profile-name / bank box, bottom left
BAR_ROWS = (1026, 1054)                 # the stat bars themselves: never repainted
ZONE_Y = (480, 1076)

# segment = (first source frame, last source frame, car shown after the scroll, plate)
# The capture's garage section plays at DOUBLE speed (a scroll takes 14 frames at 60 fps here, 0.47 s in a
# second, real-time capture), so the menu is written at 30 fps with every source frame: that is real time.
# Segment lengths are the gaps between scrolls in the real-time capture's audio (b.wav), see assemble.py.
SEGMENTS = [
    (3829, 3919, "corolla", "corolla"),      # menu opens: empty turntable slides out, car 1 slides in
    (4041, 4112, "civic_fe", "civic"),
    (4631, 4682, "integra", "integra"),
    (4732, 4785, "nc", "miata"),
    (5089, 5143, "ep3", "civic"),
]
OUT_FPS = 30
CARS_DIR = "cars2"                       # renders with the wheel-fitted camera and the game-matched rig
PLATE_SRC = {"corolla": 4280, "civic": 4610, "miata": 4430}     # rest frames showing each real plate
BOX_SRC = 3996


def shift_x(img, dx, fill=0):
    """img moved right by dx px (dx may be negative); returns moved image and a validity mask."""
    h, w = img.shape[:2]
    out = np.full_like(img, fill)
    ok = np.zeros((h, w), bool)
    dx = int(round(dx))
    if dx >= w or dx <= -w:
        return out, ok
    if dx >= 0:
        out[:, dx:] = img[:, :w - dx]; ok[:, dx:] = True
    else:
        out[:, :w + dx] = img[:, -dx:]; ok[:, :w + dx] = True
    return out, ok


def turntable_mask(h, w):
    """Pixels that belong to the turntable at rest (they move during a slide)."""
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy, a, b = 1060, 925, 900, 130
    far = ((xx - cx) / a) ** 2 + ((yy - cy) / b) ** 2 <= 1
    near = (yy >= cy) & (np.abs(xx - cx) <= a)
    return far | near


def build_zone(cap, E):
    """Soft mask of where any game car (and its shadow on the turntable) differs from the empty plate."""
    U = np.zeros(E.shape[:2], np.float32)
    for f in (3990, 4100, 4160, 4215, 4280, 4360, 4430, 4490, 4550, 4610, 4700, 4850, 4980, 5025, 5070, 5150):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, F = cap.read()
        U = np.maximum(U, cv2.absdiff(F, E).max(2).astype(np.float32))
    m = (U > 22).astype(np.uint8)
    m[:ZONE_Y[0]] = 0; m[ZONE_Y[1]:] = 0; m[:, :560] = 0; m[:, 1760:] = 0
    m[BAR_ROWS[0]:BAR_ROWS[1]] = 0
    upper = m.copy(); upper[985:] = 0                       # car + shadow above the stat band: one generous blob
    upper = cv2.morphologyEx(upper, cv2.MORPH_CLOSE, np.ones((61, 61), np.uint8))
    upper = cv2.dilate(upper, np.ones((33, 33), np.uint8)); upper[985:] = 0
    lower = m.copy(); lower[:985] = 0                       # faint shadow seen through the band: only where it is
    lower = cv2.dilate(cv2.morphologyEx(lower, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)), np.ones((15, 15), np.uint8))
    lower[:985] = 0; lower[BAR_ROWS[0] - 2:BAR_ROWS[1] + 2] = 0
    z = np.maximum(upper, lower).astype(np.float32)
    return cv2.GaussianBlur(z, (0, 0), 5)


def slide(rows, a, b):
    """s(k) for k in [a, b): how far the conveyor has moved (0 .. D). Uses the right rim tip of the outgoing
    turntable early, the left rim tip of the incoming one late, and a straight line in between."""
    r0, l1 = rows[str(a - 1)]["r"][0], rows[str(b)]["l"][0]
    known = {a - 1: 0.0, b: float(D_CONVEYOR)}
    last = 0.0
    for k in range(a, b):
        dr, sr = rows[str(k)]["r"]
        s = -(dr - r0)
        if sr > 0.5 and s > last and s < 1400:
            known[k] = float(s); last = s
        else:
            break
    prev = 0.0
    for k in range(b - 1, a - 1, -1):
        dl, sl = rows[str(k)]["l"]
        x = dl - l1
        if sl > 0.68 and x > prev and x < 1400:
            known[k] = float(D_CONVEYOR - x); prev = x
        else:
            break
    ks = sorted(known)
    return {k: float(np.interp(k, ks, [known[i] for i in ks])) for k in range(a, b)}


def rest_offset(rows, f):
    v = rows[str(f)]
    return 0.5 * (v["r"][0] + v["l"][0])


def font(name, size):
    for p in (f"/usr/share/fonts/truetype/inter/{name}.ttf", f"/usr/share/fonts/opentype/inter/{name}.otf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    out = subprocess.run(["fc-match", "-f", "%{file}", name.replace("-", ":style=")], capture_output=True, text=True).stdout
    return ImageFont.truetype(out, size)


def integra_plate(plates):
    """A plate the game never had. Background = per-pixel median of the real plates (their wordmarks sit in
    different places, so the median is the bare plate); logo box flattened; then logo + wordmark in the
    capture's own greys (measured from the Honda Civic plate)."""
    # wordmarks are darker than the plate and sit in different places on each car's plate, so a high
    # percentile across many plates is the bare plate (a plain median left ghost lettering)
    stack = np.stack(list(plates.values())).astype(np.float32)
    bg = cv2.GaussianBlur(np.percentile(stack, 88, 0).astype(np.float32), (0, 0), 2.0)
    x0, y0, x1, y1 = PANEL
    lx0, ly0, lx1, ly1 = 2 * 257 - x0 + 6, 2 * 78 - y0 + 6, 2 * 420 - x0 - 6, 2 * 160 - y0 - 6      # logo box interior
    # logo box: the Honda plate's own box (unselected state, with the room showing through it), badge inpainted out
    civ8 = plates["civic"]
    bx = civ8[:, :lx1 + 14].copy()
    g = cv2.cvtColor(bx, cv2.COLOR_BGR2GRAY)
    inner = np.zeros_like(g); inner[ly0 + 8:ly1 - 8, lx0 + 8:lx1 - 8] = 1
    badge = ((g.astype(np.int16) > int(np.median(g[ly0:ly1, lx0:lx1])) + 22) & (inner > 0)).astype(np.uint8)
    badge = cv2.dilate(badge, np.ones((9, 9), np.uint8))
    bg[:, :lx1 + 14] = cv2.inpaint(bx, badge, 7, cv2.INPAINT_TELEA).astype(np.float32)
    civ = plates["civic"].astype(np.float32)
    txt = civ[2 * 132 - y0:2 * 160 - y0, 2 * 560 - x0:2 * 780 - x0].reshape(-1, 3)
    ink = np.percentile(txt, 8, 0)                                         # wordmark grey
    logo = np.percentile(civ[ly0:ly1, lx0:lx1].reshape(-1, 3), 97, 0)      # logo highlight grey
    S = 4
    h, w = bg.shape[:2]
    lay = Image.new("L", (w * S, h * S), 0); d = ImageDraw.Draw(lay)
    # wordmark: small maker name over a wide heavy italic model name, like the Honda / CIVIC plate
    d.text(((2 * 551 - x0) * S, (2 * 101 - y0) * S), "Acura", font=font("Inter-SemiBold", 46 * S), fill=255)
    big = Image.new("L", (900 * S, 90 * S), 0)
    ImageDraw.Draw(big).text((10 * S, 0), "INTEGRA", font=font("Inter-Black", 64 * S), fill=255)
    big = big.resize((int(big.width * 1.32), big.height))                                   # wide
    big = big.transform(big.size, Image.AFFINE, (1, 0.22, -0.22 * big.height, 0, 1, 0))     # italic
    lay.paste(big, ((2 * 540 - x0) * S, (2 * 128 - y0) * S), big)
    a = np.asarray(lay.resize((w, h), Image.LANCZOS)).astype(np.float32)[..., None] / 255
    out = bg * (1 - a * 0.92) + ink * a * 0.92
    # logo: the calipers in an oval
    lg = Image.new("L", (w * S, h * S), 0); d = ImageDraw.Draw(lg)
    cx, cy = (lx0 + lx1) / 2 * S, (ly0 + ly1) / 2 * S
    rx, ry = 62 * S, 50 * S
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=255, width=9 * S)
    d.line((cx - 30 * S, cy + 40 * S, cx - 5 * S, cy - 40 * S), fill=255, width=9 * S)
    d.line((cx + 30 * S, cy + 40 * S, cx + 5 * S, cy - 40 * S), fill=255, width=9 * S)
    d.line((cx - 5 * S, cy - 40 * S, cx + 5 * S, cy - 40 * S), fill=255, width=9 * S)
    d.line((cx - 17 * S, cy + 6 * S, cx + 17 * S, cy + 6 * S), fill=255, width=7 * S)
    a = np.asarray(lg.resize((w, h), Image.LANCZOS)).astype(np.float32)[..., None] / 255
    out = out * (1 - a) + logo * a
    return np.clip(out, 0, 255).astype(np.uint8)


def main():
    cap = cv2.VideoCapture(str(VID))
    E = cv2.imread(str(EPATH))
    H, Wd = E.shape[:2]
    rows = json.load(open(W / "track.json"))
    trans = {a: b for a, b in rows["transitions"]}
    rows = rows["frames"]

    def frame(f):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, F = cap.read(); return F

    T = turntable_mask(H, Wd)
    zone = build_zone(cap, E)
    cv2.imwrite(str(W / "match/zone.png"), (zone * 255).astype(np.uint8))
    Ef = E.astype(np.float32)
    x0, y0, x1, y1 = PANEL
    plates = {k: frame(f)[y0:y1, x0:x1].copy() for k, f in PLATE_SRC.items()}
    more = {f"x{f}": frame(f)[y0:y1, x0:x1].copy() for f in (3990, 4100, 4360, 4700, 4850)}   # 206, Focus, 240SX, 106, Corsa
    plates["integra"] = integra_plate({**plates, **more})
    cv2.imwrite(str(W / "match/plate_integra.png"), plates["integra"])
    bx0, by0, bx1, by1 = BOX
    box_ref = frame(BOX_SRC)[by0:by1, bx0:bx1].copy()
    cars = {}
    for name in {s[2] for s in SEGMENTS}:
        im = cv2.imread(str(W / CARS_DIR / f"{name}.png"), cv2.IMREAD_UNCHANGED).astype(np.float32)
        if im.shape[:2] != (H, Wd):
            im = cv2.resize(im, (Wd, H), interpolation=cv2.INTER_LINEAR)
        cars[name] = im

    above_band = np.clip((986 - np.arange(H, dtype=np.float32)) / 6.0, 0, 1)[:, None, None]

    def paint(F, car, dx):
        """Repaint the game-car zone (moved by dx) with the empty plate and put `car` there."""
        out = F.astype(np.float32)
        z, _ = shift_x(zone, dx)
        if z.max() <= 0:
            return out
        Es, ok = shift_x(Ef, dx)
        Ts, _ = shift_x(T, dx, False)
        # turntable pixels ride the slide; room pixels come from the plate, except where the plate shows
        # the turntable at rest (it has slid away from there): keep the capture's own floor
        fill = np.where((Ts & ok)[..., None], Es, np.where(T[..., None], out, Ef))
        # Under the stat band the menu is drawn over the turntable and cannot be separated from it: at rest
        # take the plate unshifted there (a shifted fill doubled the "HANDLING" label), mid-slide leave it alone.
        if abs(dx) < 20:
            fill[985:] = Ef[985:]
        else:
            z = z.copy(); z[985:] = 0
        z3 = z[..., None]
        out = out * (1 - z3) + fill * z3
        if car is not None:
            c, okc = shift_x(cars[car], dx)
            a = (c[..., 3:] / 255.0) * okc[..., None] * above_band        # the menu's stat band stays on top
            out = out * (1 - a) + c[..., :3] * a
        return out

    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{Wd}x{H}", "-r", str(OUT_FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "1", "-pix_fmt", "yuv420p", str(W / "menu.mp4")], stdin=subprocess.PIPE)
    meta, n_out, prev_car = [], 0, None
    for si, (f0, f1, car, plate) in enumerate(SEGMENTS):
        # the transition inside this segment
        ta = next(a for a in sorted(trans) if f0 <= a <= f1)
        tb = trans[ta]
        s = slide(rows, ta, tb)
        ob, oa = rest_offset(rows, ta - 1), rest_offset(rows, tb)
        hold = list(range(tb, f1 + 1))
        med = np.median(np.stack([frame(f) for f in hold[::max(1, len(hold) // 9)]]), 0).astype(np.uint8)
        for f in range(f0, f1 + 1):
            F = frame(f)
            if f < ta:                       # before the scroll: previous car at rest
                out = paint(F, prev_car, ob)
            elif f < tb:                     # sliding
                out = paint(F, prev_car, -s[f] + ob)
                out = paint(out, car, D_CONVEYOR - s[f] + oa)
            else:
                out = paint(F, car, oa)
            cur_plate = plate if f >= ta else (SEGMENTS[si - 1][3] if si else plate)
            out[y0:y1, x0:x1] = plates[cur_plate]
            out[by0:by1, bx0:bx1] = box_ref
            if f >= tb:                      # put the mouse cursor back where it crossed anything we repainted
                d = cv2.absdiff(F, med).max(2)
                m = (d > 46).astype(np.uint8)
                keep = np.zeros_like(m); keep[y0:y1, x0:x1] = 1
                keep |= (zone > 0.02).astype(np.uint8)
                m = cv2.morphologyEx(m & keep, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                n, lab, st, _ = cv2.connectedComponentsWithStats(m)
                cm = np.zeros_like(m)
                for i in range(1, n):
                    if 60 < st[i, cv2.CC_STAT_AREA] < 2600 and st[i, cv2.CC_STAT_WIDTH] < 80 and st[i, cv2.CC_STAT_HEIGHT] < 90:
                        cm[lab == i] = 1
                cm = cv2.dilate(cm, np.ones((3, 3), np.uint8)).astype(bool)
                out[cm] = F[cm]
            ff.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
            n_out += 1
        meta.append({"car": car, "plate": plate, "src": [f0, f1], "transition": [ta, tb], "out_start": n_out - (f1 - f0 + 1), "frames": f1 - f0 + 1})
        prev_car = car
        print(f"segment {si + 1}: {car:9s} src f{f0}-{f1} scroll f{ta}-{tb} rest offsets {ob:+.1f}/{oa:+.1f}", flush=True)
    ff.stdin.close(); ff.wait()
    json.dump({"fps": OUT_FPS, "segments": meta, "frames": n_out}, open(W / "menu_segments.json", "w"), indent=1)
    print("frames", n_out, "seconds", round(n_out / OUT_FPS, 2))


if __name__ == "__main__":
    main()
