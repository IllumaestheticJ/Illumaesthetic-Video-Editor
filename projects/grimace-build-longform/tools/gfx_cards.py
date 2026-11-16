"""Title cards, chapter cards, parts-map shots, watch-next, thank-you and end cards (same kit as the explainers).
usage: gfx_cards.py [still]
Writes <media>/gfx/: T_title.mp4, T_ch1..T_ch5.mp4, T_track.mp4 (title cards), L10 (parts map intro), L45, L46 (watch next),
L61 (recap orbit with partners), L67 (thank-you), L69 (Illumaesthetic), L70 (end screen).
Partner names are text until the official logos arrive."""
import sys, os, glob, math
from PIL import Image
from gfx import *
PM = f'{M}/gfx/partsmap2'      # v6: parts placed from the model's real wheel positions
CH = [('coilovers', '1', 'COILOVERS', 'MCS · Eibach springs'), ('bushings', '2', 'BUSHINGS', 'Whiteline · Good-Win Racing'),
      ('brakes', '3', 'BRAKES', 'Fast Brakes · Wilwood calipers · CSG'), ('bracing', '4', 'BRACING AND SWAY BARS', 'Good-Win Racing · Whiteline'),
      ('steering', '5', 'STEERING', 'SPL · SuperPro · Mike Kojima')]
PARTNERS = [('coilovers', 'COILOVERS', 'MCS'), ('bushings', 'BUSHINGS', 'Whiteline'), ('brakes', 'BRAKES', 'Fast Brakes · CSG'),
            ('bracing', 'BRACING', 'Good-Win Racing · Whiteline'), ('swaybars', 'SWAY BARS', 'Whiteline · Good-Win Racing'), ('steering', 'STEERING', 'SPL · SuperPro')]
_img = {}


def bg(c, path, dim=1.0, zoom=1.0, shift=0):
    """Paste a parts-map render as the background (optionally zoomed about the centre and dimmed)."""
    if path not in _img: _img[path] = Image.open(path).convert('RGB')
    im = _img[path]; w, h = im.size; cw, chh = w / zoom, h / zoom
    if zoom >= 1:
        im = im.crop((int((w - cw) / 2), int((h - chh) / 2), int((w + cw) / 2), int((h + chh) / 2))).resize((W * SS, H * SS), Image.BILINEAR)
    else:       # shrink and pad with the render's own background colour
        sm = im.resize((int(W * SS * zoom), int(H * SS * zoom)), Image.BILINEAR); im = Image.new('RGB', (W * SS, H * SS), im.getpixel((4, 4)))
        im.paste(sm, ((W * SS - sm.size[0]) // 2, (H * SS - sm.size[1]) // 2))
    if dim < 1: im = Image.blend(Image.new('RGB', im.size, BG), im, dim)
    if shift:
        full = Image.new('RGB', im.size, im.getpixel((4, 4))); full.paste(im, (int(shift * SS), 0)); im = full
    c.im.paste(im); from PIL import ImageDraw; c.d = ImageDraw.Draw(c.im)


def seq(name):
    f = sorted(glob.glob(f'{PM}/{name}/*.png')); return f if len(f) >= 96 else [f'{PM}/still_all.png']      # only use an orbit once it has fully rendered


def title(c, u, t):
    bg(c, f'{PM}/still_all.png', 0.35, 1.0 + 0.04 * u); a = ease(seg(u, 0.05, 0.35))
    c.text(640, 300, 'FROM EBAY COILOVERS', 52, fade(WHITE, a), 'mm'); c.text(640, 366, 'TO A REAL RACE SETUP', 52, fade(WHITE, a), 'mm')
    c.rect(640 - 170 * a, 410, 640 + 170 * a, 414, fill=PURPLE); c.text(640, 446, 'Rebuilding our Miata', 24, fade(DIM, ease(seg(u, 0.25, 0.5))), 'mm')


def chapter(k):
    grp, num, name, who = CH[k]
    def f(c, u, t):
        bg(c, f'{PM}/still_{grp}.png', 0.75, 1.0 + 0.05 * u); a = ease(seg(u, 0.05, 0.3)); col = COL[grp]
        c.rect(0, 470, W, H, fill=(8, 10, 20)); c.rect(60, 500, 66, 500 + 100 * a, fill=col)
        c.text(86, 498, f'PART {num}', 18, fade(col, a, (8, 10, 20))); c.text(86, 524, name, 50, fade(WHITE, a, (8, 10, 20)))
        c.text(88, 588, who, 20, fade(DIM, ease(seg(u, 0.2, 0.45)), (8, 10, 20)), bold=False)
    return f


def track(c, u, t):
    a = ease(seg(u, 0.05, 0.3)); c.text(640, 330, 'ON TRACK', 60, fade(WHITE, a), 'mm'); c.rect(640 - 120 * a, 380, 640 + 120 * a, 384, fill=PURPLE)
    c.text(640, 416, 'event names and dates to fill in', 20, fade(DIM, a), 'mm', False)


RB = (28, 30, 40)      # background colour of the parts-map renders (text fades in from it)


def legend(c, u, start=0.1, step=0.11, names=True):
    for i, (grp, part, who) in enumerate(PARTNERS):
        a = ease(seg(u, start + step * i, start + step * i + 0.1)); y = 150 + i * 72; col = COL[grp]
        c.rect(60, y, 64, y + 50, fill=fade(col, a, RB)); c.text(78, y - 2, part, 22, fade(WHITE, a, RB))
        if names: c.text(78, y + 28, who, 17, fade(DIM, a, RB), bold=False)


def L10(c, u, t):       # parts map, first run
    f = seq('intro'); bg(c, f[min(len(f) - 1, int(u * (len(f) - 1)))], zoom=0.86, shift=150)
    c.header('THE PLAN', 'One part at a time', 'coilovers', u); legend(c, u, 0.12, 0.1, names=False)


def L61(c, u, t):       # recap orbit: every partner on its part
    f = seq('recap'); bg(c, f[min(len(f) - 1, int(u * (len(f) - 1)))], zoom=0.86, shift=150)
    c.header('ALL OF IT', 'Everything on the car', 'bracing', u); legend(c, u, 0.05, 0.08)


def watch(c, u, t):
    bg(c, f'{PM}/still_bracing.png', 0.45); a = ease(seg(u, 0.04, 0.2))
    c.header('WATCH NEXT', 'The bracing test', 'bracing', u)
    c.rect(700, 210, 1180, 480, fill=fade(PANEL, a), outline=fade(COL['bracing'], a), width=2, r=14)
    c.poly([(915, 310), (915, 380), (975, 345)], fill=fade(WHITE, a)); c.text(940, 440, 'video title + link to fill in', 17, fade(DIM, a), 'mm', False)
    c.text(100, 300, 'Fender braces + strut tower brace', 26, fade(WHITE, a)); c.text(100, 340, 'on a stock NB Miata, 3D scanned', 22, fade(DIM, a), bold=False)
    c.chip('Good-Win Racing · Whiteline', 'bracing', u=u)


def thanks(c, u, t):
    bg(c, f'{PM}/still_all.png', 0.22); a = ease(seg(u, 0.03, 0.15)); c.text(640, 120, 'THANK YOU', 44, fade(WHITE, a), 'mm')
    c.text(640, 196, 'MotoIQ  ·  Mike Kojima', 34, fade(PURPLE, ease(seg(u, 0.1, 0.25))), 'mm'); c.text(640, 236, 'technology partners', 17, fade(DIM, ease(seg(u, 0.1, 0.25))), 'mm', False)
    names = ['Good-Win Racing', 'Whiteline', 'MCS', 'Fast Brakes', 'CSG', 'SPL', 'SuperPro']
    for i, n in enumerate(names):
        x = 250 + (i % 4) * 260 if i < 4 else 380 + (i - 4) * 260; y = 360 if i < 4 else 460; b = ease(seg(u, 0.3 + 0.07 * i, 0.4 + 0.07 * i))
        c.rect(x - 115, y - 34, x + 115, y + 34, fill=fade(PANEL, b), outline=fade(GRID, b), width=1.5, r=10); c.text(x, y, n, 22, fade(WHITE, b), 'mm')
    c.text(640, 600, 'official logos replace these names', 15, fade(DIM, a), 'mm', False)


def illum(c, u, t):
    p = f'{M}/model/test_hero.png'; bg(c, p if os.path.exists(p) else f'{PM}/still_all.png', 0.5, 1.0 + 0.05 * u); a = ease(seg(u, 0.05, 0.3))
    c.rect(0, 470, W, H, fill=(8, 10, 20)); c.text(86, 500, 'ILLUMAESTHETIC', 48, fade(WHITE, a, (8, 10, 20)))
    c.text(88, 566, '3D scanning + engineering consulting', 24, fade(PURPLE, ease(seg(u, 0.2, 0.45)), (8, 10, 20)), bold=False)


def endscreen(c, u, t):
    a = ease(seg(u, 0.05, 0.25)); c.text(100, 150, 'WANT MORE?', 44, fade(WHITE, a)); c.text(100, 210, 'Tell us what you want to see next.', 24, fade(DIM, a), bold=False)
    c.rect(700, 250, 1180, 520, fill=fade(PANEL, a), outline=fade(PURPLE, a), width=2, r=14); c.poly([(915, 350), (915, 420), (975, 385)], fill=fade(WHITE, a))
    c.text(940, 480, 'the bracing video', 18, fade(DIM, a), 'mm', False)


JOBS = [('T_title', title, 4.0), ('T_track', track, 3.0)] + [(f'T_ch{k + 1}', chapter(k), 3.0) for k in range(5)]
LINES = {10: L10, 45: watch, 46: watch, 61: L61, 67: thanks, 68: thanks, 69: illum, 70: endscreen}
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        os.makedirs(f'{M}/gfx/chk', exist_ok=True)
        for n, f, d in JOBS: still(f, 0.8, f'{M}/gfx/chk/{n}.png')
        for k, f in LINES.items(): still(f, 0.9, f'{M}/gfx/chk/L{k}.png')
    else:
        for n, f, d in JOBS: render(0, f, d, n)
        for k, f in LINES.items(): render(k, f, max(line_dur(k), 8.0) if k == 61 else None)
