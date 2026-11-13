"""IS350 speed-run thumbnails. Design at 2560x1440, downscale to 1280x720 (+320x180 proofs)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

T = '/home/user/media/work/is350-long/thumb'
FR = T + '/frames'
SC = '/home/user/media/work/is350-long/renders/B5_stills'
W, H = 2560, 1440
BLUR_PLATE = False   # owner v2: plates are no longer blurred
OFF = (232, 236, 242)       # #e8ecf2
RED = (226, 37, 37)         # brand bar red (one use per thumbnail)
INTER = '/usr/share/fonts/opentype/inter/InterDisplay-%s.otf'
MONO = '/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-%s.ttf'


def font(path, size):
    return ImageFont.truetype(path, size)


def scan_img(name='B5_front34_hero_alpha.png', contrast=True):
    a = Image.open(f'{SC}/{name}').convert('RGBA')
    a = a.crop(a.getbbox())
    if contrast:
        arr = np.asarray(a).astype(np.float32)
        rgb = arr[..., :3] / 255.0
        rgb = np.clip((rgb - 0.06) / 0.94, 0, 1) ** 1.35          # deepen shadows, keep highlights
        rgb = np.clip(rgb * 1.08, 0, 1)
        arr[..., :3] = rgb * 255
        a = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    return a


def paste_scan(canvas, scan, x, y, width, glow=True):
    h = round(scan.height * width / scan.width)
    s = scan.resize((width, h), Image.LANCZOS)
    if glow:   # soft contact light behind the car so the silver separates from black
        g = Image.new('L', canvas.size, 0)
        d = ImageDraw.Draw(g)
        d.ellipse([x - width * .05, y + h * .08, x + width * 1.05, y + h * 1.0], fill=46)
        g = g.filter(ImageFilter.GaussianBlur(width * .06))
        canvas.paste(Image.new('RGB', canvas.size, (150, 160, 175)), (0, 0), g)
    canvas.paste(s, (x, y), s)


def irl(name, box, size):
    im = Image.open(f'{FR}/{name}').convert('RGB').crop(box)
    im = im.resize(size, Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
    return im


def text(d, xy, s, f, fill=OFF, anchor='la', stroke=0, stroke_fill=(0, 0, 0)):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)


def save(img, name):
    img = img.convert('RGB')
    big = img.resize((1280, 720), Image.LANCZOS)
    big.save(f'{T}/{name}.png', optimize=True)
    q = 95
    while True:
        big.save(f'{T}/{name}.jpg', quality=q, subsampling=0)
        if os.path.getsize(f'{T}/{name}.jpg') < 1_800_000 or q < 70:
            break
        q -= 5
    big.resize((320, 180), Image.LANCZOS).save(f'{T}/{name}_320x180.png')
    img.save(f'{T}/{name}_2560.png')


def plate_blur(im, rect):
    """rect in output coords; heavy pixelate + blur so the plate is illegible."""
    x0, y0, x1, y1 = rect
    reg = im.crop(rect)
    reg = reg.resize((max(2, (x1 - x0) // 38), max(2, (y1 - y0) // 38)), Image.BILINEAR).resize(reg.size, Image.NEAREST)
    reg = reg.filter(ImageFilter.GaussianBlur(10))
    m = Image.new('L', reg.size, 0)
    ImageDraw.Draw(m).rectangle([6, 6, reg.width - 7, reg.height - 7], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(6))
    im.paste(reg, (x0, y0), m)


# ---------------------------------------------------------------- A: split
def concept_A(scan_name='B5_front34_hero_alpha.png'):
    c = Image.new('RGB', (W, H), (0, 0, 0))
    # IRL: FX30554 @ 11.011 s (walk-out, solved match frame). crop 1080p, car on the left.
    s = 1440 / 1080
    full = irl('FX30554_11.011.png', (0, 0, 1920, 1080), (round(1920 * s), 1440))
    off = -640
    layer = Image.new('RGB', (W, H), (0, 0, 0))
    layer.paste(full, (off, 0))
    # plate: source px (745..922, 718..815) -> out
    px0, py0, px1, py1 = 735, 712, 932, 820
    if BLUR_PLATE:
        plate_blur(layer, (round(px0 * s + off), round(py0 * s), round(px1 * s + off), round(py1 * s)))
    # diagonal seam polygon (left = IRL)
    top_x, bot_x = 1330, 1060
    mask = Image.new('L', (W * 2, H * 2), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (top_x * 2, 0), (bot_x * 2, H * 2), (0, H * 2)], fill=255)
    mask = mask.resize((W, H), Image.LANCZOS)
    c.paste(layer, (0, 0), mask)
    d = ImageDraw.Draw(c, 'RGBA')
    # seam: off-white hairline (no red here, red is used on the number line)
    d.line([(top_x, 0), (bot_x, H)], fill=OFF + (255,), width=10)
    # scan on black, right side, front 3/4
    scan = scan_img(scan_name)
    paste_scan(c, scan, 1220, 790, 1250)
    d = ImageDraw.Draw(c)
    text(d, (2480, 90), '32 MIN', font(MONO % 'ExtraBold', 290), anchor='ra')
    # the single red element: the bet number
    fb = font(INTER % 'Black', 165); fn = font(MONO % 'ExtraBold', 250)
    wn = d.textlength('15', font=fn)
    text(d, (2480, 455), '15', fn, anchor='ra', fill=RED)
    text(d, (2480 - wn - 24, 455), 'BET WAS', fb, anchor='ra', fill=OFF)
    return c


def concept_A_finish(c):
    return c


# ---------------------------------------------------------------- B: clock story
def concept_B():
    c = Image.new('RGB', (W, H), (0, 0, 0))
    # host FX30541 @ 28 s, crop 975x1080 -> 1300x1440
    host = irl('c_FX30541_28.png', (690, 0, 1665, 1080), (1300, 1440))
    # darken the shop background a little so the face leads
    arr = np.asarray(host).astype(np.float32) * 0.92
    host = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    fade = Image.new('L', (1300, 1440), 255)
    fa = np.ones((1440, 1300), np.float32)
    ramp = np.linspace(1, 0, 260) ** 1.3
    fa[:, -260:] = ramp[None, :]
    fade = Image.fromarray((fa * 255).astype(np.uint8))
    c.paste(host, (0, 0), fade)
    d = ImageDraw.Draw(c)
    f1 = font(MONO % 'ExtraBold', 285)
    # struck bet
    x1, y1 = 1265, 100
    text(d, (x1, y1), '15 MIN?', f1, fill=(176, 182, 194))
    bb = d.textbbox((x1, y1), '15 MIN?', font=f1)
    ymid = (bb[1] + bb[3]) // 2 + 20
    d.line([(bb[0] - 30, ymid + 25), (bb[2] + 30, ymid - 25)], fill=RED, width=40)
    # real result
    f2 = font(MONO % 'ExtraBold', 390)
    text(d, (1285, 420), '32', f2)
    f3 = font(MONO % 'ExtraBold', 250)
    text(d, (1285 + d.textlength('32', font=f2) + 20, 420 + 125), 'MIN', f3)
    # scan = the reward, lower right-centre (clear of the duration badge)
    scan = scan_img()
    paste_scan(c, scan, 1300, 880, 1000)
    return c


# ---------------------------------------------------------------- C: scan hero
def concept_C(scan_name='B5_front34_hero_alpha.png'):
    c = Image.new('RGB', (W, H), (0, 0, 0))
    scan = scan_img(scan_name)
    paste_scan(c, scan, 300, 570, 1850)
    d = ImageDraw.Draw(c)
    f1 = font(MONO % 'ExtraBold', 325)
    text(d, (110, 80), '32 MIN', f1)
    f2 = font(INTER % 'Black', 215)
    text(d, (2440, 70), 'THEN IT', f2, anchor='ra')
    text(d, (2440, 70 + 215), 'CRASHED', f2, anchor='ra', fill=RED)
    return c



def contrast_arr(a):
    arr = np.asarray(a).astype(np.float32)
    rgb = np.clip((arr[..., :3] / 255.0 - 0.06) / 0.94, 0, 1) ** 1.35
    arr[..., :3] = np.clip(rgb * 1.08, 0, 1) * 255
    return Image.fromarray(arr.astype(np.uint8), 'RGBA')


def stopwatch(d, cx, cy, r, col=RED):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=int(r * .16))
    d.rounded_rectangle([cx - r * .16, cy - r * 1.32, cx + r * .16, cy - r * 1.02], radius=8, fill=col)
    d.rounded_rectangle([cx + r * .80, cy - r * 1.12, cx + r * 1.12, cy - r * .86], radius=8, fill=col)
    for k in range(12):
        import math
        a = math.radians(k * 30)
        d.line([(cx + math.sin(a) * r * .70, cy - math.cos(a) * r * .70), (cx + math.sin(a) * r * .84, cy - math.cos(a) * r * .84)],
               fill=OFF, width=int(r * .05))
    d.line([(cx, cy), (cx + r * .38, cy - r * .50)], fill=OFF, width=int(r * .09))
    d.ellipse([cx - r * .09, cy - r * .09, cx + r * .09, cy + r * .09], fill=OFF)


# ---------------------------------------------------------------- D: guess stack
def concept_D():
    c = Image.new('RGB', (W, H), (0, 0, 0))
    scan = scan_img()
    paste_scan(c, scan, 960, 560, 1580)
    d = ImageDraw.Draw(c)
    stopwatch(d, 1880, 290, 190)
    f = font(MONO % 'ExtraBold', 175)
    for i, t in enumerate(['2 HOURS?', '30 MIN?', '15 MIN?']):
        y = 90 + i * 330
        d.rounded_rectangle([70, y, 1010, y + 270], radius=60, outline=OFF, width=14)
        text(d, (540, y + 138), t, f, anchor='mm')
    return c


# ---------------------------------------------------------------- E: face + the claim
def concept_E():
    c = Image.new('RGB', (W, H), (0, 0, 0))
    host = irl('d_26.6.png', (590, 0, 1565, 1080), (1300, 1440))
    fa = np.ones((1440, 1300), np.float32)
    fa[:, :300] = (np.linspace(0, 1, 300) ** 1.3)[None, :]
    c.paste(host, (1260, 0), Image.fromarray((fa * 255).astype(np.uint8)))
    d = ImageDraw.Draw(c)
    fn = font(MONO % 'ExtraBold', 760)
    text(d, (60, 20), '15', fn)
    fm = font(MONO % 'ExtraBold', 400)
    text(d, (60, 700), 'MIN', fm)
    text(d, (60 + d.textlength('MIN', font=fm), 700), '?', fm, fill=RED)
    paste_scan(c, scan_img(), 80, 1130, 760, glow=False)
    return c


# ---------------------------------------------------------------- F: question over real | scan
def concept_F():
    c = Image.new('RGB', (W, H), (0, 0, 0))
    band = 360
    s = 1440 / 1080
    real = Image.open(f'{FR}/FX30554_11.011.png').convert('RGB').resize((W, H), Image.LANCZOS)
    real = real.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
    sc = Image.open(f'{SC}/B5_halfhalf_FX30554_alpha.png').convert('RGBA').resize((W, H), Image.LANCZOS)
    sc = contrast_arr(sc)
    right = Image.new('RGBA', (W, H), (0, 0, 0, 255)); right.alpha_composite(sc)
    top_x, bot_x = 1560, 1080
    m = Image.new('L', (W * 2, H * 2), 0)
    ImageDraw.Draw(m).polygon([(0, 0), (top_x * 2, 0), (bot_x * 2, H * 2), (0, H * 2)], fill=255)
    m = m.resize((W, H), Image.LANCZOS)
    comp = Image.composite(real, right.convert('RGB'), m)
    d = ImageDraw.Draw(comp)
    d.line([(top_x, 0), (bot_x, H)], fill=OFF, width=10)
    k = 1.2
    comp = comp.resize((round(W * k), round(H * k)), Image.LANCZOS)
    cx, cy = round(1230 * k), round(790 * k)
    win = comp.crop((cx - W // 2, cy - (H - band) // 2, cx + W // 2, cy + (H - band) // 2))
    c.paste(win, (0, band))
    d = ImageDraw.Draw(c)
    text(d, (80, 30), 'HOW LONG?', font(INTER % 'Black', 285))
    text(d, (2480, 70), '00:00', font(MONO % 'ExtraBold', 200), anchor='ra', fill=RED)
    text(d, (2480, 285), '2 HR · 30 MIN · 15 MIN', font(MONO % 'Bold', 50), anchor='ra', fill=(176, 182, 194))
    return c



# ================================================================ F v3 (F1/F2/F3): scanner + 3D scanning wording
def split_base(s, cx, band, top_dx=260, bot_dx=-220):
    """Real car (4K FX30554 @ 11.011) | scan (halfhalf still), registered 1:1, as a (W, H-band) window.
    s = scale vs 4K; cx = canvas x of the car centre. Left of the seam = real, right = scan on black."""
    wh = H - band
    real = Image.open(f'{FR}/car4k.png').convert('RGB')
    sc = contrast_arr(Image.open(f'{SC}/B5_halfhalf_FX30554_alpha.png').convert('RGBA'))
    right = Image.new('RGBA', real.size, (0, 0, 0, 255)); right.alpha_composite(sc)
    nw, nh = round(3840 * s), round(2160 * s)
    real = real.resize((nw, nh), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    right = right.convert('RGB').resize((nw, nh), Image.LANCZOS)
    ox = round(cx - 1815 * s); oy = round(wh / 2 - 1080 * s)
    assert ox <= 0 and ox + nw >= W and oy <= 0 and oy + nh >= wh, (ox, oy, nw, nh)
    sx0 = -ox
    m = Image.new('L', (W * 2, wh * 2), 0)
    ImageDraw.Draw(m).polygon([(0, 0), ((cx + top_dx) * 2, 0), ((cx + bot_dx) * 2, wh * 2), (0, wh * 2)], fill=255)
    m = m.resize((W, wh), Image.LANCZOS)
    box = (sx0, -oy, sx0 + W, -oy + wh)
    comp = Image.composite(real.crop(box), right.crop(box), m)
    d = ImageDraw.Draw(comp)
    d.line([(cx + top_dx, 0), (cx + bot_dx, wh)], fill=OFF, width=10)
    return comp


def scanner_cut(width, angle=0):
    a = Image.open(f'{FR}/scanner84_rgba.png')   # BGRA from cv2
    rgba = a.convert('RGBA')   # file written by cv2 as BGRA = correct RGBA on disk
    rgba = rgba.crop((0, 270, 3360, 2160))
    r = width / rgba.width
    rgba = rgba.resize((width, round(rgba.height * r)), Image.LANCZOS)
    al = rgba.getchannel('A').filter(ImageFilter.GaussianBlur(1.2))
    rgba.putalpha(al)
    # a touch more punch so the white body reads
    rgb = np.asarray(rgba.convert('RGB')).astype(np.float32)
    rgb = np.clip((rgb - 12) * 1.12, 0, 255)
    out = Image.fromarray(rgb.astype(np.uint8)); out.putalpha(al)
    return out.rotate(angle, expand=True, resample=Image.BICUBIC) if angle else out


def drop_shadow_paste(c, img, xy, blur=30, off=(18, 26), op=170):
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sh.putalpha(img.getchannel('A').point(lambda v: v * op // 255))
    big = Image.new('RGBA', c.size, (0, 0, 0, 0)); big.paste(sh, (xy[0] + off[0], xy[1] + off[1]))
    big = big.filter(ImageFilter.GaussianBlur(blur))
    c.paste(big, (0, 0), big)
    c.paste(img, xy, img)


def fit_text(d, lines, fpath, width, gap=0.04):
    size = 400
    while max(d.textlength(t, font=font(fpath, size)) for t in lines) > width:
        size -= 4
    return size


def band_text(c, lines, band, tag_sw=True, sw_text='00:00', width=1640):
    d = ImageDraw.Draw(c)
    size = fit_text(d, lines, INTER % 'Black', width)
    f = font(INTER % 'Black', size)
    lh = size * 0.96
    y0 = (band - lh * len(lines)) / 2 - size * 0.12
    for i, t in enumerate(lines):
        text(d, (80, y0 + i * lh), t, f)
    if tag_sw:
        text(d, (2480, band / 2 - 20), sw_text, font(MONO % 'ExtraBold', 215), anchor='rm', fill=RED)
    return size


def guess_tags(d, x, y, w, h, gap, f, labels=('2 HOURS?', '30 MIN?', '15 MIN?')):
    for i, t in enumerate(labels):
        yy = y + i * (h + gap)
        d.rounded_rectangle([x, yy, x + w, yy + h], radius=h // 4, outline=OFF, width=12, fill=(0, 0, 0))
        text(d, (x + w / 2, yy + h / 2 + 6), t, f, anchor='mm')


def concept_F1():
    band = 420
    c = Image.new('RGB', (W, H), (0, 0, 0))
    c.paste(split_base(0.74, 1343, band), (0, band))
    sc = scanner_cut(920)
    drop_shadow_paste(c, sc, (0, H - sc.height + 20))
    band_text(c, ['HOW LONG TO', '3D SCAN A CAR?'], band)
    return c


def concept_F2():
    band = 420
    c = Image.new('RGB', (W, H), (0, 0, 0))
    c.paste(split_base(0.74, 1210, band), (0, band))
    d = ImageDraw.Draw(c)
    guess_tags(d, 1880, 470, 620, 200, 40, font(MONO % 'ExtraBold', 114))
    sc = scanner_cut(660)
    drop_shadow_paste(c, sc, (0, H - sc.height + 12), blur=22, off=(12, 18))
    band_text(c, ['3D SCAN A CAR', 'IN ___ MIN?'], band, width=1640)
    return c


def concept_F3():
    band = 420
    c = Image.new('RGB', (W, H), (0, 0, 0))
    c.paste(split_base(0.74, 1300, band), (0, band))
    # picture-in-picture: the scanner's own screen building the car (FX30545 @ 104 s), top-left of the road
    pip = Image.open(f'{FR}/q45_104.png').convert('RGB').crop((0, 300, 3840, 2160)).resize((860, round(1860 * 860 / 3840)), Image.LANCZOS)
    pip = pip.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
    pw, ph = pip.size
    frame = Image.new('RGBA', (pw + 24, ph + 24), OFF + (255,)); frame.paste(pip, (12, 12))
    msk = Image.new('L', frame.size, 0); ImageDraw.Draw(msk).rounded_rectangle([0, 0, frame.width - 1, frame.height - 1], radius=36, fill=255)
    frame.putalpha(msk)
    frame = frame.rotate(3, expand=True, resample=Image.BICUBIC)
    drop_shadow_paste(c, frame, (50, band + 40), blur=26)
    band_text(c, ['HOW FAST CAN WE', '3D SCAN THIS?'], band)
    return c



# ================================================================ v4: whole scanner standing on its base (FX30542 4K frame f_010)
def leo_cut(width):
    """Whole Artec-style handheld on its base/stand, cut from the 4K FX30542 frame (scanner4k/f_010, ~5 s).
    Matte: hand polygon + grabCut refinement + threshold clean-up (see frames/poly10.py); rear end rounded where a spray gun hides it."""
    im = Image.open(f'{T}/frames/leo_f010.jpg').convert('RGB')
    m = Image.open(f'{T}/scanner_leo_mask.png').convert('L')
    box = m.getbbox()
    im, m = im.crop(box), m.crop(box)
    m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.6))    # 1px choke + feather (no bench halo)
    r = width / im.width
    sz = (width, round(im.height * r))
    im = im.resize(sz, Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=80, threshold=2))
    m = m.resize(sz, Image.LANCZOS)
    arr = np.asarray(im).astype(np.float32)
    arr = np.clip((arr - 10) * 1.16, 0, 255)          # source is flat/pale: restore white body contrast
    out = Image.fromarray(arr.astype(np.uint8)).convert('RGBA'); out.putalpha(m)
    return out


def stand_on_ground(c, sc, x, base_y, blur_k=0.05):
    """Paste cut-out with its bottom at base_y and a soft ground shadow so it sits on the road."""
    w, h = sc.size
    sh = Image.new('L', c.size, 0)
    ImageDraw.Draw(sh).ellipse([x - w * .02, base_y - h * .075, x + w * 1.06, base_y + h * .055], fill=170)
    sh = sh.filter(ImageFilter.GaussianBlur(w * blur_k))
    c.paste(Image.new('RGB', c.size, (0, 0, 0)), (0, 0), sh)
    c.paste(sc, (x, base_y - h), sc)


def concept_F2b():
    band = 420
    c = Image.new('RGB', (W, H), (0, 0, 0))
    c.paste(split_base(0.74, 1210, band), (0, band))
    d = ImageDraw.Draw(c)
    guess_tags(d, 1880, 462, 620, 172, 34, font(MONO % 'ExtraBold', 102), labels=('2 HOURS?', '30 MIN?', '15 MIN?', 'LONGER?'))
    sc = leo_cut(665)
    stand_on_ground(c, sc, 34, H - 70)
    band_text(c, ['3D SCAN A CAR', 'IN ___ MIN?'], band, width=1640)
    return c


def concept_F2c():
    band = 420
    c = Image.new('RGB', (W, H), (0, 0, 0))
    c.paste(split_base(0.74, 1210, band), (0, band))
    d = ImageDraw.Draw(c)
    guess_tags(d, 1880, 462, 620, 172, 34, font(MONO % 'ExtraBold', 102), labels=('2 HOURS?', '30 MIN?', '15 MIN?', 'LONGER?'))
    sc = leo_cut(790)
    stand_on_ground(c, sc, 0, H - 40)
    band_text(c, ['3D SCAN A CAR', 'IN ___ MIN?'], band, width=1640)
    return c


if __name__ == '__main__':
    which = sys.argv[1:] or ['F1', 'F2', 'F3']
    for w in which:
        {'A': lambda: save(concept_A(), 'thumb_A'),
         'B': lambda: save(concept_B(), 'thumb_B'),
         'C': lambda: save(concept_C(), 'thumb_C'),
         'D': lambda: save(concept_D(), 'thumb_D'),
         'E': lambda: save(concept_E(), 'thumb_E'),
         'F': lambda: save(concept_F(), 'thumb_F'),
         'F1': lambda: save(concept_F1(), 'thumb_F1'),
         'F2': lambda: save(concept_F2(), 'thumb_F2'),
         'F2b': lambda: save(concept_F2b(), 'thumb_F2b'),
         'F2c': lambda: save(concept_F2c(), 'thumb_F2c'),
         'F3': lambda: save(concept_F3(), 'thumb_F3')}[w]()
