"""IS350 speed-run thumbnails. Design at 2560x1440, downscale to 1280x720 (+320x180 proofs)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

T = '/home/user/media/work/is350-long/thumb'
FR = T + '/frames'
SC = '/home/user/media/work/is350-long/renders/B5_stills'
W, H = 2560, 1440
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


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for w in which:
        {'A': lambda: save(concept_A(), 'thumb_A'),
         'B': lambda: save(concept_B(), 'thumb_B'),
         'C': lambda: save(concept_C(), 'thumb_C')}[w]()
