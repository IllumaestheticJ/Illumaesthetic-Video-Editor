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
  * The timeline is five scrolls of the capture, one per car, each range starting on the first frame of a
    scroll; how long each runs is set by the real-time capture's audio so its scroll sounds land on the car
    changes. The last car is the one that gets bought: Continue, then the purchase prompt with our car
    behind it and the game's car name replaced in the question.
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
SEGMENTS = [                                                   # (source frames, car, plate)
    (range(3829, 3920), "corolla", "corolla"),                 # menu opens: empty turntable slides out, car 1 slides in
    (range(4041, 4113), "civic_fe", "civic"),
    (range(4631, 4683), "integra", "integra"),
    (range(4732, 4786), "nc", "miata"),
    # The last car is bought (user, v10 review: buy the EP3, no wrap back to the Corolla). Its scroll, a rest
    # with the capture's cursor on the left arrow (pasted over with the name bar's end), then the last frames
    # before the player clicks Continue. 42 frames: Continue is clicked 0.6 s after the voice line ends.
    (list(range(5089, 5122)) + list(range(5204, 5213)), "ep3", "civic"),
]
# "Do you want this stock 240SX?": fade-in (5213-5218), the cursor's trip from Continue up to the buttons
# (5224-5233), three frames of it hovering, then across to Yes and the click (5247-5263). 36 frames = the
# 1.2 s the prompt is up in the real-time capture; the frames left out are ones where the cursor sits still.
# Cursor (user, v6 review: "the cursor arrow freaks out"). The capture's cursor is in a different place in
# every range the menu is cut from, so it jumped at each cut, and the clean plate had a copy of it baked in
# that blinked on and off around slides. Now the capture's cursor is removed from the menu and one cursor
# (sprite from tools/cursor.py) is drawn on a continuous path: where the capture has it when the menu opens,
# over to the "next" arrow, there for every scroll, then down to Continue once the last car has settled. From
# Continue on, the capture's own cursor is kept: the prompt frames are chosen so its path is unbroken.
CUR_START, CUR_HOME, CUR_CONTINUE = (1046, 1032), (1730, 242), (1611, 1087)    # top-left of the sprite box, capture px
CUR_CLEAN_SRC = 4035                    # first car at rest with the cursor elsewhere: clean pixels under CUR_START
STRIP_L, STRIP_R = (300, 144, 490, 332), (1700, 144, 1842, 332)   # the name bar's ends with the arrow buttons
STRIP_SRC = {"L": 4050, "R": 4110}      # frames with the cursor on the other arrow
DIALOG = {"frames": list(range(5213, 5219)) + list(range(5224, 5234)) + [5238, 5240, 5243] + list(range(5247, 5264)), "rest": 5212, "steady": 5240, "scene": 5264,
          "text": "Do you want this Epsilon EP3?", "text_box": (773, 577, 1382, 620)}
OUT_FPS = 30
CARS_DIR = "cars3"                       # wheel-fitted camera, game-matched rig, front wheels steered 25 deg
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
    # Wordmark, set the way the game sets its plates: maker name in a condensed grotesque (cf. "Honda", "Mazda"),
    # model name as the car's own badge lettering - the real INTEGRA badge is upright, wide and squared
    # (Microgramma style). v1-v3 used Inter with a fake italic and the user asked for the typeface to be fixed.
    # Positions copy the Honda / CIVIC plate: maker cap-top at y 40, model at y 102, both starting near x 612.
    S = 4
    h, w = bg.shape[:2]
    FONTS = Path("/home/user/media/nfs-carlot/fonts")           # tools/fetch_fonts.sh
    lay = Image.new("L", (w * S, h * S), 0); d = ImageDraw.Draw(lay)
    fm = ImageFont.truetype(str(FONTS / "roboto-condensed-latin-500-normal.ttf"), 52 * S)
    l, t, r, b_ = fm.getbbox("Acura")
    d.text((612 * S - l, 40 * S - t), "Acura", font=fm, fill=255)
    fb = ImageFont.truetype(str(FONTS / "michroma-latin-400-normal.ttf"), 52 * S)
    sw = int(3.4 * S)                                           # Michroma is a regular weight; the game's wordmarks are heavy
    x = 616 * S + sw
    for ch in "INTEGRA":                                        # letter by letter: the added weight needs air
        l, t, r, b_ = fb.getbbox(ch)
        d.text((x - l, 106 * S - fb.getbbox("I")[1]), ch, font=fb, fill=255, stroke_width=sw, stroke_fill=255)
        x += (r - l) + int(10.5 * S)
    a = cv2.GaussianBlur(np.asarray(lay.resize((w, h), Image.LANCZOS)).astype(np.float32), (0, 0), 0.8)[..., None] / 255
    out = bg * (1 - a * 0.95) + ink * 0.88 * a * 0.95
    # badge: the real emblem, lifted front-on from the Integra GLB's own grille (tools/badge_from_glb.py);
    # v1/v2 drew one by hand and the user called it wrong
    bm = cv2.imread(str(W / "match/acura_badge.png"), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    bh = int((ly1 - ly0) * 0.86); bw = int(bm.shape[1] * bh / bm.shape[0])
    bm = cv2.resize(bm, (bw, bh), interpolation=cv2.INTER_AREA)
    by, bx = (ly0 + ly1 - bh) // 2, (lx0 + lx1 - bw) // 2
    shade = np.linspace(1.08, 0.82, bh, dtype=np.float32)[:, None, None]          # chrome: lighter on top, like the game's badges
    a = bm[..., None]
    out[by:by + bh, bx:bx + bw] = out[by:by + bh, bx:bx + bw] * (1 - a) + np.clip(logo * shade, 0, 255) * a
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

    # cursor sprite, and the plate cleaned of the cursor that was in the capture when it was grabbed
    spr = cv2.imread(str(W / "cursor/sprite.png"), cv2.IMREAD_UNCHANGED).astype(np.float32)
    sh, sw = spr.shape[:2]
    cx0, cy0 = CUR_START
    cur_hole = cv2.dilate((spr[..., 3] > 5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(bool)   # the capture's cursor is a little larger and softer than the sprite
    PADC = 14
    cur_clean = frame(CUR_CLEAN_SRC)[cy0 - PADC:cy0 + sh + PADC, cx0 - PADC:cx0 + sw + PADC]
    hole_pad = cv2.copyMakeBorder(cur_hole.astype(np.uint8) * 255, PADC, PADC, PADC, PADC, cv2.BORDER_CONSTANT, value=0)

    def lift_start_cursor(img):
        """Take the capture's cursor out at CUR_START. The clean pixels come from a later frame of the same car,
        but the floor there is darker or lighter depending on what stands on the turntable, so they are blended
        in by gradient (Poisson) rather than pasted: a plain paste left a visible cursor-shaped patch."""
        y, x = cy0 - PADC, cx0 - PADC
        reg = np.clip(img[y:y + cur_clean.shape[0], x:x + cur_clean.shape[1]], 0, 255).astype(np.uint8)
        c = (reg.shape[1] // 2, reg.shape[0] // 2)
        img[y:y + reg.shape[0], x:x + reg.shape[1]] = cv2.seamlessClone(cur_clean, reg, hole_pad, c, cv2.NORMAL_CLONE)

    lift_start_cursor(E)
    strips = {k: frame(STRIP_SRC[k])[b[1]:b[3], b[0]:b[2]].copy() for k, b in (("L", STRIP_L), ("R", STRIP_R))}
    cur_track = json.load(open(W / "cursor/track.json"))["track"]

    def draw_cursor(out, pos):
        """Alpha-composite the sprite with its box's top-left at pos (sub-pixel)."""
        x, y = pos; xi, yi = int(np.floor(x)), int(np.floor(y))
        M = np.float32([[1, 0, x - xi + 1], [0, 1, y - yi + 1]])
        sp = cv2.warpAffine(spr, M, (sw + 3, sh + 3), flags=cv2.INTER_LINEAR, borderValue=0)
        ya, xa = max(0, yi - 1), max(0, xi - 1); yb, xb = min(H, yi - 1 + sh + 3), min(Wd, xi - 1 + sw + 3)
        sp = sp[ya - (yi - 1):yb - (yi - 1), xa - (xi - 1):xb - (xi - 1)]
        a = sp[..., 3:] / 255.0
        out[ya:yb, xa:xb] = out[ya:yb, xa:xb] * (1 - a) + sp[..., :3] * a

    def glide(p, q, t):
        """Point t (0..1) of the way from p to q: eased, with a slight bow like a hand-moved mouse."""
        t = float(np.clip(t, 0, 1)); e = t * t * (3 - 2 * t)
        dx, dy = q[0] - p[0], q[1] - p[1]
        bow = 0.045 * np.sin(np.pi * e)
        return p[0] + dx * e - dy * bow, p[1] + dy * e + dx * bow

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
    for name in {s[1] for s in SEGMENTS}:
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
    meta, n_out, prev_car, last_out = [], 0, None, None
    for si, (frames, car, plate) in enumerate(SEGMENTS):
        frames = list(frames); fset = set(frames)
        ta = next(a for a in sorted(trans) if a in fset)      # the scroll inside this segment
        tb = trans[ta]
        s = slide(rows, ta, tb)
        ob, oa = rest_offset(rows, ta - 1), rest_offset(rows, tb)
        last_seg = si == len(SEGMENTS) - 1
        k_real = next((i for i, f_ in enumerate(frames) if f_ >= 5204), len(frames))   # from here the capture's cursor is on Continue
        for f in frames:
            F = frame(f)
            if f < ta:                       # before the scroll: previous car at rest
                out = paint(F, prev_car, ob)
            elif f < tb:                     # sliding
                out = paint(F, prev_car, -s[f] + ob)
                out = paint(out, car, D_CONVEYOR - s[f] + oa)
            else:
                out = paint(F, car, oa)
            cur_plate = plate if f >= ta else (SEGMENTS[si - 1][2] if si else plate)
            out[y0:y1, x0:x1] = plates[cur_plate]
            out[by0:by1, bx0:bx1] = box_ref
            # cursor: take the capture's out, draw ours
            out[STRIP_L[1]:STRIP_L[3], STRIP_L[0]:STRIP_L[2]] = strips["L"]
            out[STRIP_R[1]:STRIP_R[3], STRIP_R[0]:STRIP_R[2]] = strips["R"]
            k = frames.index(f)
            if si == 0 and ta <= f < tb:     # opening slide: the capture's cursor is at CUR_START and nothing under it is repainted
                pos = None
            elif si == 0:                    # ... and it stays there for the whole first range: take it out, draw ours
                lift_start_cursor(out)
                k0 = frames.index(tb) + 12   # a beat after the first car has settled, go to the "next" arrow
                pos = glide(CUR_START, CUR_HOME, (k - k0) / 16.0)
            elif not last_seg:
                pos = CUR_HOME
            elif k < k_real:                 # last car: once it has settled, travel to Continue, arriving as the capture's cursor takes over
                pos = glide(CUR_HOME, CUR_CONTINUE, (k - (k_real - 13)) / 13.0)
            else:
                pos = None                   # the capture's own cursor is on Continue from here
            if pos is not None:
                draw_cursor(out, pos)
            last_out = np.clip(out, 0, 255)
            ff.stdin.write(last_out.astype(np.uint8).tobytes())
            n_out += 1
        meta.append({"car": car, "plate": plate, "src": [frames[0], frames[-1]], "transition": [ta, tb], "out_start": n_out - len(frames),
                     "scroll_at": n_out - len(frames) + frames.index(ta), "frames": len(frames)})
        prev_car, last_oa = car, oa
        print(f"segment {si + 1}: {car:9s} src f{frames[0]}-{frames[-1]} ({len(frames)} frames) scroll f{ta}-{tb} rest offsets {ob:+.1f}/{oa:+.1f}", flush=True)

    # ---- the purchase prompt -------------------------------------------------------------------------
    # The prompt dims the room, hides the menu and lays a translucent panel over the car. Where the capture
    # shows the game's car through all that, ours must show instead:  F' = F + T * (our scene - game scene),
    # with T = how much of the scene reaches each pixel. T is constant per part of the prompt; the values are
    # robust fits of prompt frames against the one clean frame the game shows right after the click (room and
    # car, no menu, full brightness): prompt = T * scene + c, same T to 0.001 on four different frames.
    dg = DIALOG
    R = frame(dg["rest"]).astype(np.float32)                    # last menu frame as captured
    Rp = last_out.astype(np.float32)                            # ... and as we just wrote it
    car_a, _ = shift_x(cars[prev_car][..., 3] / 255.0, last_oa)
    zmask = np.maximum(shift_x(zone, last_oa)[0], car_a); zmask[985:] = 0
    dS = (Rp - R) * cv2.GaussianBlur((zmask > 0.01).astype(np.float32), (0, 0), 2)[..., None]
    T_OUT, T_FRAME, T_PANEL, T_BTN, T_BTN_HOT = 0.361, 0.125, 0.067, 0.055, 0.031
    BTN = {"yes": (359, 738, 1034, 840), "no": (1115, 738, 1788, 840)}

    def t_map(F):
        t = np.full((H, Wd), T_OUT, np.float32)
        t[366:883, 322:1828] = 0                                 # the prompt's outline is opaque
        t[377:872, 332:1816] = T_FRAME                           # dark band inside the outline
        t[481:850, 346:1800] = T_PANEL                           # grey panel
        for bx0_, by0_, bx1_, by1_ in BTN.values():              # the button under the cursor is darker and more opaque
            hot = float(np.median(F[by0_ + 8:by1_ - 8, bx0_ + 8:bx1_ - 8])) < 68
            t[by0_:by1_, bx0_:bx1_] = T_BTN_HOT if hot else T_BTN
        return cv2.GaussianBlur(t, (0, 0), 1.2)[..., None]
    tx0, ty0, tx1, ty1 = dg["text_box"]
    FONTS = Path("/home/user/media/nfs-carlot/fonts")
    S_ = 4
    fnt = ImageFont.truetype(str(FONTS / "roboto-condensed-latin-400-italic.ttf"), 49 * S_)   # near-exact match for the game's prompt type
    track_px = 0.85 * S_
    width = sum(fnt.getlength(ch) + track_px for ch in dg["text"]) - track_px
    lay = Image.new("L", (Wd * S_, 90 * S_), 0); dr = ImageDraw.Draw(lay)
    xx = ((tx0 + tx1) / 2) * S_ - width / 2
    top = fnt.getbbox("D")[1]
    for ch in dg["text"]:
        dr.text((xx, 20 * S_ - top), ch, font=fnt, fill=255); xx += fnt.getlength(ch) + track_px
    text_a = cv2.GaussianBlur(np.asarray(lay.resize((Wd, 90), Image.LANCZOS)).astype(np.float32), (0, 0), 0.7)[..., None] / 255
    pad = 22

    def prompt(F):
        """A steady prompt frame with our car behind it and the reworded question."""
        out = F.astype(np.float32) + t_map(F) * dS
        reg = np.clip(out[ty0 - pad:ty1 + pad, tx0 - pad:tx1 + pad], 0, 255).astype(np.uint8)
        g = cv2.cvtColor(F[ty0 - pad:ty1 + pad, tx0 - pad:tx1 + pad], cv2.COLOR_BGR2GRAY)
        ink = (g > int(np.median(g)) + 38).astype(np.uint8)
        ink = cv2.dilate(ink, np.ones((5, 5), np.uint8))
        white = np.percentile(F[ty0:ty1, tx0:tx1].reshape(-1, 3), 99.5, 0)
        out[ty0 - pad:ty1 + pad, tx0 - pad:tx1 + pad] = cv2.inpaint(reg, ink, 5, cv2.INPAINT_TELEA)
        a = text_a[:, :, :]
        out[ty0 - 20:ty0 + 70] = out[ty0 - 20:ty0 + 70] * (1 - a) + white * a
        return np.clip(out, 0, 255)

    D0 = frame(5218).astype(np.float32); D0p = prompt(frame(5218))
    for f in dg["frames"]:
        F = frame(f)
        if f < 5218:                                            # fading in: a mix of the menu and the steady prompt
            Ff = F.astype(np.float32)
            u = float(np.clip(((Ff - R) * (D0 - R)).sum() / (((D0 - R) ** 2).sum() + 1e-6), 0, 1))
            out = (1 - u) * Rp + u * D0p
        else:
            out = prompt(F)
            t = cur_track.get(str(f))
            if t and t["score"] > 0.85:                         # the cursor is on top of everything: no car showing through it
                tx, ty = t["x"], t["y"]
                m = cv2.dilate((spr[..., 3] > 40).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
                out[ty:ty + sh, tx:tx + sw][m] = F[ty:ty + sh, tx:tx + sw][m]
        ff.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes()); n_out += 1
    print(f"prompt: {len(dg['frames'])} frames, text '{dg['text']}'", flush=True)
    ff.stdin.close(); ff.wait()
    json.dump({"fps": OUT_FPS, "segments": meta, "dialog": {"out_start": n_out - len(dg["frames"]), "frames": len(dg["frames"])}, "frames": n_out},
              open(W / "menu_segments.json", "w"), indent=1)
    print("frames", n_out, "seconds", round(n_out / OUT_FPS, 2))


if __name__ == "__main__":
    main()
