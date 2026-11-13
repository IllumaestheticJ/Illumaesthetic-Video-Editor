"""Motion-graphics layer for the Miata bracing long-form (everything after 3:04) + the 0:51 caption fix.
Called per frame by final.py:  frame = Fx(rows, vo, t_new, total).apply(frame_rgb_uint8, t)
All numbers shown are the rounded (0.1 mm) report widths or the body shares computed in clips.md."""
import math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
GOLD, WHITE, INK, BG = (214, 164, 25), (255, 255, 255), (17, 17, 17), (38, 38, 38)
_fonts = {}
def F(sz, wt='Bold'):
    k = (sz, wt)
    if k not in _fonts:
        p = subprocess.run(['fc-match', '-f', '%{file}', f'Inter Display:style={wt}'], capture_output=True, text=True).stdout
        _fonts[k] = ImageFont.truetype(p, sz)
    return _fonts[k]
def ease(x): x = min(max(x, 0.0), 1.0); return 1 - (1 - x)**3
def spring(x):
    x = min(max(x, 0.0), 1.0); return 1 - math.cos(x*math.pi*2.2)*math.exp(-5*x) if x < 1 else 1.0
def a8(c, a): return (*c, int(255*min(max(a, 0), 1)))

SCAN = ['CONTROL', 'NO BRACING', 'FENDER BRACES', 'STRUT TOWER BRACE', 'BOTH BRACES']
BADGE = {184.27: (1, 'CONTROL', 'car on the ground, stock'), 189.19: (2, 'NO BRACING', 'one front corner on the jack'),
         298.59: (3, 'FENDER BRACES', 'Goodwin Racing'), 372.33: (3, 'FENDER BRACES', 'engine-bay scan'),
         248.0: (4, 'STRUT TOWER BRACE', 'on its own'), 320.32: (5, 'BOTH BRACES', 'final scan')}
DELTA = {'w_jacked': 1.7, 'w_fender': 0.2, 'w_strut': 0.7, 'w_both': 0.4}
# heat-map callouts: (start as a fraction of the line, kind, x, y, text)
CALL = {
 'h_jacked_side': [(.28, 'ring', 274, 533, 'moved inward'), (.55, 'ring', 1728, 590, 'moved outward, around 10 mm')],
 'h_jacked_top': [(.03, 'ring', 432, 438, 'out'), (.10, 'ring', 432, 706, 'in'), (.70, 'badge', 960, 905, 'just under 60% of the body within 2.5 mm')],
 'h_fender_side': [(.35, 'ring', 1734, 562, 'rear still moving')],
 'h_fender_top': [(.12, 'ring', 200, 576, 'trunk lid: a hinged panel'), (.72, 'badge', 960, 905, 'about 60% of the body within 2.5 mm')],
 'h_strut_side': [(.55, 'badge', 960, 905, 'about 90% of the body within 2.5 mm')],
 'h_strut_top': [(.55, 'badge', 960, 905, 'one scan: we cannot explain this yet')],
 'h_both_side': [(.04, 'badge', 960, 205, 'this map: 8 mm scale, not 15'), (.48, 'ring', 452, 605, 'door'), (.56, 'ring', 620, 640, 'fender, refitted')],
 'h_both_top': [(.45, 'badge', 960, 905, 'about three quarters of the body within 2.5 mm')],
}
REVEAL = {'legend': [(.18, 540, 540, 1900, 700), (.42, 540, 280, 1900, 440), (.55, 540, 830, 1900, 985)],
          'takeaways': [(.02, 100, 230, 1900, 430), (.30, 100, 480, 1900, 680), (.55, 100, 730, 1900, 930)],
          'chart': [(.42, 630, 240, 1900, 340), (.62, 630, 410, 1900, 510), (.74, 630, 580, 1900, 680), (.88, 630, 750, 1900, 850)],
          'caveats': [(.04, 100, 230, 1900, 430), (.22, 100, 480, 1900, 680), (.40, 100, 730, 1900, 930)]}
MARK = {'legend': [(.18, 600), (.42, 330), (.55, 890)]}          # colour-bar pointer positions (y) per reveal

LBL = {'control': 'CONTROL, ON THE GROUND', 'jacked': 'NO BRACING', 'fender': 'FENDER BRACES', 'strut': 'STRUT TOWER BRACE', 'both': 'BOTH BRACES'}
HB = {('control>jacked', 'top'): (.70, 'just under 60% of the body within 2.5 mm'), ('jacked>fender', 'top'): (.78, 'about 60% of the body within 2.5 mm'),
      ('jacked>strut', 'sides'): (.62, 'about 90% of the body within 2.5 mm'), ('jacked>strut', 'top'): (.30, 'hypothesis: better against this kind of twist'),
      ('jacked>both', 'top'): (.03, 'about three quarters of the body within 2.5 mm')}
def _ramp():
    st = np.array([[-1, 0, 0, 255], [-.6, 0, 0, 255], [-.35, 0, 140, 255], [-.001, 0, 255, 255], [.001, 0, 255, 0], [.35, 255, 255, 0], [.65, 255, 150, 0], [1, 255, 0, 0]], float)
    v = np.linspace(-1, 1, 420); bar = np.stack([np.interp(v, st[:, 0], st[:, i]) for i in (1, 2, 3)], 1).astype(np.uint8); return Image.fromarray(np.repeat(bar[None], 14, 0)).convert('RGBA')
RAMP = _ramp()
def _logo(p, w):
    im = Image.open(p).convert('RGBA'); return im.resize((w, int(im.height*w/im.width)), Image.LANCZOS)
LOGO = {}

class Fx:
    def __init__(self, rows, vo, t_new, total):
        self.rows, self.t_new, self.total = rows, t_new, total
        self.line = {nar: (s, len(x)/48000) for s, x, nar, i in vo}
        self.i = 0
    def row(self, t):
        while self.i + 1 < len(self.rows) and t >= self.rows[self.i + 1][0] - 1e-6: self.i += 1
        while self.i > 0 and t < self.rows[self.i][0] - 1e-6: self.i -= 1
        return self.rows[self.i]
    # ---------- 0:51 caption: "Thank you. Good one." -> "Thank you, Goodwin."
    def caption(self, f, t):
        if not 50.9 < t < 52.7: return f
        band = f[940:1060]; m = band.min(2) > 235; cols = np.where(m.sum(0) > 2)[0]
        if len(cols) == 0 or not 595 < cols[-1] - cols[0] < 630: return f
        import cv2
        x0, x1 = cols[0] - 16, cols[-1] + 16; reg = np.ascontiguousarray(f[956:1056, x0:x1]); txt = (reg.min(2) > 200) | (reg.max(2) < 45)
        mask = cv2.dilate(txt.astype(np.uint8)*255, np.ones((9, 9), np.uint8)); fixed = cv2.inpaint(reg, mask, 6, cv2.INPAINT_TELEA)
        out = f.copy(); out[956:1056, x0:x1] = cv2.GaussianBlur(fixed, (0, 0), 1.2)
        im = Image.fromarray(out); d = ImageDraw.Draw(im)
        d.text((W/2, 1037), 'Thank you, Goodwin.', font=F(66, 'Bold'), fill='white', anchor='ms', stroke_width=5, stroke_fill='black')
        return np.asarray(im)
    # ---------- helpers
    def chip(self, d, x, y, small, big, sub, p):
        """left-anchored info chip sliding in from the left; p = 0..1 visibility"""
        if p <= 0: return
        w = int(max(d.textlength(big, font=F(44, 'Black')), d.textlength(sub, font=F(26, 'Medium'))) + 70); dx = int((1 - ease(p))*-(w + x + 20))
        d.rounded_rectangle((x + dx, y, x + dx + w, y + 132), 14, fill=(12, 12, 12, 215)); d.rectangle((x + dx, y + 14, x + dx + 7, y + 118), fill=a8(GOLD, 1))
        d.text((x + dx + 28, y + 12), small, font=F(22, 'Bold'), fill=a8(GOLD, 1)); d.text((x + dx + 28, y + 38), big, font=F(44, 'Black'), fill=a8(WHITE, 1))
        d.text((x + dx + 28, y + 92), sub, font=F(26, 'Medium'), fill=(200, 205, 212, 255))
    def tracker(self, d, t, idx, dark):
        p = ease((t - self.t_new)/0.6); y = int(-60 + 84*p); x = W - 40; pulse = .55 + .45*math.sin(t*4)
        items = []
        for i in range(4, -1, -1):
            if i == idx:
                w = int(d.textlength(SCAN[i], font=F(20, 'Bold'))) + 58; items.append((x - w, x, i)); x -= w + 10
            else: items.append((x - 22, x, i)); x -= 32
        d.rounded_rectangle((x - 6, y - 10, W - 26, y + 32), 21, fill=(0, 0, 0, 170))
        for x0, x1, i in items:
            if i == idx:
                d.rounded_rectangle((x0, y, x1, y + 22), 11, fill=a8(GOLD, 1)); d.ellipse((x0 + 6, y + 5, x0 + 18, y + 17), fill=(20, 20, 20, int(255*pulse)))
                d.text((x0 + 26, y + 11), f'{i+1}/5  ' + SCAN[i] if False else SCAN[i], font=F(20, 'Bold'), fill=(20, 20, 20, 255), anchor='lm')
            elif i < idx: d.ellipse((x0, y, x1, y + 22), fill=(235, 238, 242, 255))
            else: d.ellipse((x0 + 2, y + 2, x1 - 2, y + 20), outline=(150, 155, 162, 255), width=3)
    def ring(self, d, x, y, text, u):
        """pulsing ring with a label; u = seconds since it appeared"""
        if u < 0: return
        p = spring(u/0.5); r = 58*p
        for k in range(2):
            ph = (u*0.9 + k*.5) % 1; d.ellipse((x - r - 40*ph, y - r - 40*ph, x + r + 40*ph, y + r + 40*ph), outline=a8(GOLD, .7*(1 - ph)), width=4)
        d.ellipse((x - r, y - r, x + r, y + r), outline=(20, 20, 20, 255), width=9); d.ellipse((x - r, y - r, x + r, y + r), outline=a8(GOLD, 1), width=5)
        q = ease((u - .25)/.35)
        if q > 0:
            tw = d.textlength(text, font=F(28, 'Bold')); lx = min(max(x, tw/2 + 40), W - tw/2 - 40); ly = y - 58 - 62
            d.line((x, y - r, lx, ly + 22), fill=a8(GOLD, q), width=4)
            d.rounded_rectangle((lx - tw/2 - 18, ly - 22, lx + tw/2 + 18, ly + 22), 10, fill=(12, 12, 12, int(225*q))); d.text((lx, ly), text, font=F(28, 'Bold'), fill=a8(WHITE, q), anchor='mm')
    def badge(self, d, x, y, text, u, gold=True):
        if u < 0: return
        p = spring(u/0.55); tw = d.textlength(text, font=F(34, 'Bold')); w = (tw/2 + 34)*p; h = 34*min(p, 1.05)
        d.rounded_rectangle((x - w, y - h, x + w, y + h), 16, fill=a8(GOLD if gold else (12, 12, 12), .96))
        if p > .6: d.text((x, y), text, font=F(34, 'Bold'), fill=(20, 20, 20, 255) if gold else a8(WHITE, 1), anchor='mm')
    def end(self, im, d, u, dur):
        if not LOGO:
            LOGO['m'] = _logo('/home/user/media/miata-bracing/logos/motoiq_white.png', 520); LOGO['i'] = _logo('/home/user/media/miata-bracing/logos/IllumaestheticLogoColor-01.png', 760)
        d.rectangle((0, 0, W, H), fill=(0, 0, 0, 120))
        for j in range(140): d.line((0, 880 + j, W, 880 + j), fill=(0, 0, 0, int(255*min(1, j/90))))          # hides the rough cut's burned-in subtitle band
        d.rectangle((0, 1020, W, H), fill=(0, 0, 0, 255))
        for key, y, small, t0 in (('m', 250, 'PARTS BROUGHT TO YOU BY', .4), ('i', 560, 'SCANNING BY', 2.2)):
            p = ease((u - t0)/.6)
            if p <= 0: continue
            d.text((W/2, y - 12*(1 - p)), small, font=F(34, 'Bold'), fill=a8(GOLD, p), anchor='mm'); lg = LOGO[key].copy(); lg.putalpha(lg.getchannel('A').point(lambda v: int(v*p)))
            d._image.alpha_composite(lg, (int(W/2 - lg.width/2), int(y + 50 - 12*(1 - p))))
    # ---------- per frame
    def apply(self, f, t):
        f = self.caption(f, t)
        if t < self.t_new: return f
        tt, dur, (k, a, c, sec, pic, nar) = self.row(t); u = t - tt; ls, ld = self.line.get(nar, (tt, dur)) if nar else (tt, dur); lu = t - ls
        heat = k == 'heat'; name = a if k == 'card' else None; dark = k == 'card' and name in ('legend', 'chart', 'takeaways', 'caveats') or (name or '').startswith(('table', 'title', 'end'))
        im = Image.fromarray(f)
        if name and name.startswith('h_'):                                  # slow push-in on the heat maps
            z = 1 + .045*ease(u/dur); cw, ch = W/z, H/z; im = im.resize((W, H), Image.BICUBIC, box=((W - cw)/2, (H - ch)/2, (W + cw)/2, (H + ch)/2))
            Z = lambda x, y: ((x - W/2)*z + W/2, (y - H/2)*z + H/2)
        else: Z = lambda x, y: (x, y)
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        idx = 5 if sec.startswith('5') else int(sec[0]) if not sec.startswith('1') else (0 if 'jacked' not in sec else 1)
        if name and name.startswith('title'):                               # section title: gold rule grows, ticks count in
            p = ease(u/.7); d.rectangle((W/2 - 420*p, 652, W/2 + 420*p, 658), fill=a8(GOLD, 1))
            for j in range(5):
                q = ease((u - .15*j)/.3); x = W/2 - 80 + 40*j; d.ellipse((x - 9*q, 700 - 9*q, x + 9*q, 700 + 9*q), fill=a8(GOLD if j <= idx else (90, 90, 90), 1))
        elif name == 'end': pass
        elif k == 'end': self.end(im, d, u, dur)
        else: self.tracker(d, t, idx, dark)
        if k == 'src':                                                      # shop footage: chip with the scan number
            b = BADGE.get(round(a, 2)) if isinstance(a, float) or isinstance(a, int) else None
            if b:
                hold = min(dur - .8, 7.5); p = min(u/.45, 1) if u < hold else 1 - (u - hold)/.4
                self.chip(d, 56, 770, f'SCAN {b[0]} OF 5', b[1], b[2], p)
                if round(a, 2) == 189.19:                                   # tape-measure beat
                    v = u - 8.5; p2 = min(v/.45, 1) if v < 6 else 1 - (v - 6)/.4
                    if v > 0: self.chip(d, 56, 770, 'JACK HEIGHT', 'SAME EVERY RUN', 'checked with a tape measure', p2)
        if name in DELTA:                                                   # count-up delta between the two scans
            v = lu - ld*.42
            if v > 0:
                p = ease(v/.9); val = DELTA[name]*p; s = spring(v/.6); d.line((860, 640, 860 + 200*ease(v/.5), 640), fill=a8(GOLD, 1), width=8)
                if v > .35: d.polygon([(1075, 640), (1045, 622), (1045, 658)], fill=a8(GOLD, 1))
                d.rounded_rectangle((960 - 165*s, 540 - 62*s, 960 + 165*s, 540 + 62*s), 18, fill=a8(GOLD, .97))
                if s > .6: d.text((960, 526), f'+{val:.1f} mm', font=F(54, 'Black'), fill=(20, 20, 20, 255), anchor='mm'); d.text((960, 578), 'wider than control', font=F(24, 'Bold'), fill=(20, 20, 20, 255), anchor='mm')
        if name == 'w_control': self.badge(d, 960, 930, 'BASELINE: 960.9 mm', lu - ld*.45)
        if name and name.startswith('table'):                               # newest row: sweep + marker
            n = int(name[-1]); y = 320 + 96*(n - 1); p = ease((u - .3)/.7)
            d.rectangle((110, y + 58, 110 + 1700*p, y + 62), fill=a8(GOLD, 1)); d.rectangle((84, y + 4, 92, y + 4 + 44*p), fill=a8(GOLD, 1))
        if name in REVEAL:                                                  # staged reveals on the text / chart cards
            for frac, x0, y0, x1, y1 in REVEAL[name]:
                v = lu - ld*frac
                if v < .5: d.rectangle((x0 + (x1 - x0)*ease(max(v, 0)/.5), y0, x1, y1), fill=(*BG, 255))
            if name in MARK:
                ys = [y for frac, y in MARK[name] if lu >= ld*frac]
                if ys:
                    y = ys[-1] + 6*math.sin(t*5); d.polygon([(132, y), (104, y - 16), (104, y + 16)], fill=a8(GOLD, 1))
        if name in CALL:
            sw = u/.8                                                       # scanner sweep as the map comes up
            if sw < 1:
                x = int(W*ease(sw))
                for j in range(60): d.line((x - j*3, 160, x - j*3, 1020), fill=(0, 220, 255, int(150*(1 - j/60)*(1 - sw))), width=3)
            for frac, kind, x, y, text in CALL[name]:
                v = lu - ld*frac; x, y = Z(x, y) if kind == 'ring' else (x, y)
                (self.ring if kind == 'ring' else self.badge)(d, x, y, text, v)
        if heat:                                                            # 3D before/after: labels, scale, divider, badge
            l, r = a.split('>'); p = ease(u/.5); q = ease((u - .25)/.5)
            for x, key, tag, colr in ((485, l, 'REFERENCE' if l == 'control' else 'BEFORE', (225, 228, 232)), (1435, r, 'JACKED' if l == 'control' else 'AFTER', GOLD)):
                d.text((x, 96 - 20*(1 - p)), tag, font=F(22, 'Bold'), fill=a8(colr, p), anchor='mm'); d.text((x, 138 - 20*(1 - p)), LBL[key], font=F(46, 'Black'), fill=a8(WHITE, p), anchor='mm')
            d.rectangle((958, 540 - 380*q, 962, 540 + 380*q), fill=(90, 92, 98, 255))
            ov.alpha_composite(RAMP, (750, 34)); d.text((740, 41), '15 mm inward', font=F(20, 'Bold'), fill=(200, 205, 212, 255), anchor='rm'); d.text((1180, 41), '15 mm outward', font=F(20, 'Bold'), fill=(200, 205, 212, 255), anchor='lm')
            d.rectangle((959, 30, 961, 52), fill=(20, 20, 20, 255))
            if u < .9:
                x = int(W*ease(u/.9))
                for j in range(50): d.line((x - j*3, 170, x - j*3, 1000), fill=(0, 220, 255, int(140*(1 - j/50)*(1 - u/.9))), width=3)
            hb = HB.get((a, c))
            if hb: self.badge(d, 960, 925, hb[1], lu - ld*hb[0])
        if (k == 'card' and not (name or '').startswith(('title', 'end'))) or heat:   # progress rule along the bottom of every data card
            d.rectangle((0, H - 6, W*(t - self.t_new)/(self.total - self.t_new), H), fill=a8(GOLD, .9))
        return np.asarray(Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'))
