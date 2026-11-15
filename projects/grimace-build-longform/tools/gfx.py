"""Shared 2D explainer kit for the Grimace build video (PIL, supersampled). One visual system for every explainer:
dark navy field, purple accent (matches the x-ray parts map), white text, one accent colour per part group.

A graphic is keyed by the script line it plays under: render(line, draw_fn) writes <media>/gfx/L<line>.mp4 with the
duration of that line's processed take (+0.6 s), so tools/build_review.py can drop it in place of the blue card.

draw_fn(c, u, t): c = Canvas, u = 0..1 progress through the line, t = seconds. Coordinates are in a 1280x720 space.
"""
import os, sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = os.environ.get('GRIMACE_MEDIA', '/home/user/media/grimace-build')
W, H, SS, FPS = 1280, 720, 2, 24
BG, PANEL, GRID = (10, 13, 24), (20, 26, 46), (30, 38, 64)
WHITE, DIM, PURPLE = (240, 242, 250), (140, 148, 172), (150, 110, 255)
COL = dict(coilovers=(255, 110, 70), bushings=(80, 235, 130), brakes=(255, 190, 40), bracing=(235, 235, 255),
           swaybars=(240, 110, 240), steering=(80, 195, 255), bad=(255, 90, 90), good=(90, 230, 140))
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
_fonts = {}


def font(size, bold=True):
    k = (size, bold)
    if k not in _fonts: _fonts[k] = ImageFont.truetype(FB if bold else FR, int(size * SS))
    return _fonts[k]


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def seg(u, a, b): return clamp((u - a) / (b - a)) if b > a else float(u >= b)      # 0..1 inside the window a..b
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, x): return tuple(int(lerp(a, b, clamp(x))) for a, b in zip(c1, c2))
def fade(col, x, bg=BG): return mix(bg, col, x)


class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W * SS, H * SS), BG); self.d = ImageDraw.Draw(self.im)

    def _p(self, *v): return [x * SS for x in v]
    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=2, r=0):
        self.d.rounded_rectangle(self._p(x0, y0, x1, y1), radius=r * SS, fill=fill, outline=outline, width=int(width * SS))
    def line(self, pts, fill=WHITE, width=3):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=fill, width=int(width * SS), joint='curve')
    def circle(self, x, y, r, fill=None, outline=None, width=2):
        self.d.ellipse(self._p(x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=int(width * SS))
    def poly(self, pts, fill=None, outline=None):
        self.d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill, outline=outline)
    def arc(self, x, y, r, a0, a1, fill=WHITE, width=3):
        self.d.arc(self._p(x - r, y - r, x + r, y + r), a0, a1, fill=fill, width=int(width * SS))
    def text(self, x, y, s, size=24, fill=WHITE, anchor='la', bold=True):
        self.d.text((x * SS, y * SS), s, font=font(size, bold), fill=fill, anchor=anchor)
    def arrow(self, x0, y0, x1, y1, fill=WHITE, width=4, head=12):
        a = math.atan2(y1 - y0, x1 - x0); self.line([(x0, y0), (x1 - head * 0.6 * math.cos(a), y1 - head * 0.6 * math.sin(a))], fill, width)
        self.poly([(x1, y1), (x1 - head * math.cos(a - 0.45), y1 - head * math.sin(a - 0.45)), (x1 - head * math.cos(a + 0.45), y1 - head * math.sin(a + 0.45))], fill=fill)
    def spring(self, x, y0, y1, coils=7, w=26, fill=WHITE, width=4):
        pts = [(x, y0)] + [(x + (w if i % 2 else -w), lerp(y0, y1, (i + 0.5) / (coils * 2))) for i in range(coils * 2)] + [(x, y1)]
        self.line(pts, fill, width)
    def glow(self, radius=10, amount=0.55):
        """Soft bloom over everything drawn so far (use once, after the bright shapes, before small text)."""
        b = self.im.filter(ImageFilter.GaussianBlur(radius * SS)); self.im = Image.blend(self.im, Image.composite(b, self.im, b.convert('L')), amount)
        self.d = ImageDraw.Draw(self.im)
    def header(self, kicker, title, group, u=1.0):
        """Top-left: small kicker ('HOW IT WORKS'), big title, accent bar in the part group's colour. Same on every explainer."""
        a = ease(seg(u, 0, 0.08)); col = COL[group]
        self.rect(60, 54, 66, 54 + 62 * a, fill=col)
        self.text(82, 52, kicker, 15, fade(DIM, a)); self.text(82, 74, title, 34, fade(WHITE, a))
    def chip(self, s, group, x=60, y=648, u=1.0):
        """Bottom-left partner chip: text only (official logos replace it later)."""
        a = ease(seg(u, 0.04, 0.14)); w = self.d.textlength(s, font=font(17)) / SS + 34
        self.rect(x, y, x + w, y + 34, fill=fade(PANEL, a), outline=fade(COL[group], a), width=1.5, r=17)
        self.text(x + 17, y + 17, s, 17, fade(WHITE, a), 'lm')
    def label(self, x, y, s, size=20, fill=WHITE, a=1.0, anchor='mm'):
        self.text(x, y, s, size, fade(fill, a), anchor)
    def bar(self, x, y, w, h, frac, col, label=None, a=1.0):
        self.rect(x, y, x + w, y + h, fill=fade(GRID, a), r=h / 2)
        if frac > 0.01: self.rect(x, y, x + max(h, w * frac), y + h, fill=fade(col, a), r=h / 2)
        if label: self.text(x, y - 12, label, 16, fade(DIM, a), 'lb')
    def knob(self, x, y, r, ang, col, a=1.0, label=None):
        self.circle(x, y, r, fill=fade(PANEL, a), outline=fade(col, a), width=3)
        for k in range(12):
            t = math.radians(k * 30); self.line([(x + (r + 5) * math.cos(t), y + (r + 5) * math.sin(t)), (x + (r + 11) * math.cos(t), y + (r + 11) * math.sin(t))], fade(DIM, a), 2)
        t = math.radians(ang - 90); self.line([(x, y), (x + (r - 6) * math.cos(t), y + (r - 6) * math.sin(t))], fade(WHITE, a), 4)
        if label: self.text(x, y + r + 30, label, 17, fade(WHITE, a), 'mm')
    def out(self): return self.im.resize((W, H), Image.LANCZOS)


def line_dur(line):
    """Seconds this script line occupies in the cut: processed take + 0.6 s (same rule as build_review.py)."""
    p = f'{M}/vo/p/L{line:02d}.wav'
    if not os.path.exists(p): return 5.0
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout) + 0.6


def render(line, draw, dur=None, name=None):
    """Render draw(c, u, t) for the duration of script line `line` to <media>/gfx/L<line>.mp4 (or <name>.mp4)."""
    dur = dur or line_dur(line); n = max(2, round(dur * FPS)); os.makedirs(f'{M}/gfx', exist_ok=True)
    out = f"{M}/gfx/{name or 'L%02d' % line}.mp4"
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24000/1001', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        c = Canvas(); draw(c, i / (n - 1), i / FPS); ff.stdin.write(c.out().tobytes())
    ff.stdin.close(); ff.wait(); print('wrote', out, f'{dur:.2f}s', flush=True); return out


def still(draw, u, path):
    c = Canvas(); draw(c, u, 0); c.out().save(path); return path
