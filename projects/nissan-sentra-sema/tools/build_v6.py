"""Sentra SEMA reel v6 (47.5 s) - new structure and music (user 2026-11-13):
hook (Nissan-admits-AI post) -> IT WASN'T. -> scan day -> 3D scan -> concepts -> panels + livery -> 360 of the final render
-> 1:1 cut to the real car ON THE DROP with the headlines landing on it -> SEMA clips that show the whole car -> end card.
Music: Way Out West - Killa (user-supplied), music t = video t; 130 BPM, bar 1.846 s, drop at 29.873 s.
  build_v6.py [segment ...] [mux]"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import build as B
from build import D, W, SEG, FPS, WD, HT, ENC, F, RED, OFF, pipe, clip, wa, fade, ig_frames, render_seq, REC, S

# ---- brand text style (v9, user: "match the colour style of our brand and website") --------------------------------------
# illumaesthetic.com: headings Fjalla One, uppercase, off-white #f2f3f1 with ONE phrase in the accent green #619f73;
# kickers / small labels in JetBrains Mono caps, green; background #0b0c0b; buttons are green parallelograms.
GREEN = (97, 159, 115); WHITE = (242, 243, 241); INK = (11, 12, 11)
# v10 (user): all text in Helvetica Bold, except "IT WASN'T." in a brushstroke font. Helvetica itself is not on this box (proprietary):
# Liberation Sans Bold is the metric-compatible stand-in; drop a real Helvetica-Bold.ttf into media fonts/ and it is used instead.
import os
_HELV = D + '/fonts/Helvetica-Bold.ttf'
_HELV = _HELV if os.path.exists(_HELV) else '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FJ = lambda size: ImageFont.truetype(_HELV, int(size * 0.76))        # 0.76: Helvetica is wider than the condensed Fjalla sizes used in v9
MONO = lambda size: ImageFont.truetype(_HELV, size)
BRUSH = lambda size: ImageFont.truetype(D + '/fonts/PermanentMarker-Regular.ttf', size)   # v12 (user): generic brush-stroke (Permanent Marker)   # v11 (user): Road Rage for the punch line (@fontsource/road-rage, OFL)
mul = lambda c, a: tuple(int(v * a) for v in c)


def spaced(d, xy, text, font, fill, track=0.0, **kw):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, **kw); x += d.textlength(ch, font=font) + track
    return x


def slash(d, x, y, w=70, h=12, fill=GREEN):
    d.polygon([(x + 6, y), (x + w + 6, y), (x + w, y + h), (x, y + h)], fill=fill)        # the site's slanted button shape, as a rule


def label(d, y, title, sub, alpha):
    """Scan/CGI shots: green mono kicker over a Fjalla title (replaces build.label's Inter + red rule)."""
    spaced(d, (80, y - 44), sub, MONO(26), mul(GREEN, alpha), track=1.5)
    spaced(d, (78, y), title, FJ(92), mul(WHITE, alpha), track=2)


def section_label(im, text, y=430):
    d = ImageDraw.Draw(im); slash(d, 72, y - 26)
    spaced(d, (72, y + 3), text, FJ(96), (0, 0, 0), track=2); spaced(d, (70, y), text, FJ(96), WHITE, track=2)


B.label = label; B.section_label = section_label

MUSIC = '/home/user/media/work/music/killa.m4a'
BAR = 1.8462; DROP = 29.873
fr = lambda t: int(round(t * FPS))
CUT = {k: fr(DROP + b * BAR) for k, b in dict(wasnt=-14, spray=-13, scanner=-12, tl=-11, scan=-10, concepts=-9, livery=-7, turn=-3, reveal=0, sema=4, end=8).items()}   # v9: scan 1 bar, bumper swap 4 bars, 360 3 bars
CUT['sema'] = fr(DROP + 7 * BAR / 4)   # v17: cut to the SEMA videos at 0:33 (7th base beat after the drop) so they get more time (user)
END = fr(47.5)


def seg_hook():
    """motor1com post 'NISSAN ADMITS IT USED AI IN ITS SENTRA SPEC V PICTURES' from the Instagram recording (t=171), slow 3 % push,
    with the user's blurb 'THE WORLD THOUGHT IT WAS AI' boxed over the top of the post (v8)."""
    im = ig_frames(171.0, 1)[0]; n = CUT['wasnt']; f1 = FJ(98)   # v13: two rows, in the band between car (y~780) and headline (y~1040)
    lines = [[('THE WORLD THOUGHT', WHITE)], [('IT WAS ', WHITE), ('AI', GREEN)]]
    def gen():
        for f in range(n):
            fr_ = B.punch(im, f, n, 1.03); d = ImageDraw.Draw(fr_)
            u = min(1.0, max(0.0, (f - 4) / 5))
            if u > 0:
                y0 = 806 - int((1 - u) * 40); h = 84
                ws = [sum(d.textlength(t, font=f1) for t, _ in ln) for ln in lines]; w = max(ws)
                box = [(WD - int(w)) // 2 - 44, y0 - 20, (WD + int(w)) // 2 + 44, y0 + h * len(lines) + 30]
                ov = Image.new('RGBA', fr_.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle(box, radius=34, fill=INK + (int(70 * u),))   # v11: softer (~27 % black), rounded corners
                fr_ = Image.alpha_composite(fr_.convert('RGBA'), ov).convert('RGB'); d = ImageDraw.Draw(fr_)
                for k, ln in enumerate(lines):
                    x = (WD - ws[k]) // 2
                    for t, c in ln:
                        d.text((x, y0 + k * h), t, font=f1, fill=c, stroke_width=3, stroke_fill=INK); x += d.textlength(t, font=f1)
            yield fr_
    pipe('v6_a_hook', gen())


def seg_wasnt():
    n = CUT['spray'] - CUT['wasnt']; f1 = BRUSH(185)
    def gen():
        for f in range(n):
            im = Image.new('RGB', (WD, HT), INK); d = ImageDraw.Draw(im)
            if f >= 2:
                for k, (t, c) in enumerate((('IT', WHITE), ("WASN'T.", GREEN))):
                    d.text(((WD - d.textlength(t, font=f1)) // 2, 720 + k * 230), t, font=f1, fill=c)
            yield im
    pipe('v6_b_wasnt', gen())


def frames_sel(name, src, idx):
    sel = '+'.join(f'eq(n\\,{i})' for i in idx)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', f"select='{sel}',setpts=N/{FPS}/TB,scale={WD}:{HT}", '-frames:v', str(len(idx))] + ENC + [f'{SEG}/{name}.mp4'], check=True)
    print(name, len(idx), 'frames')


def seg_scan():
    n = CUT['concepts'] - CUT['scan']; frs = render_seq('s7_scan', 111)
    def gen():
        for f in range(n):
            im = Image.fromarray(frs[min(f, len(frs) - 1)]); d = ImageDraw.Draw(im)
            if fade(f, 6, n - 6) > 0: label(d, 330, '3D SCAN', '24,996,032 TRIANGLES', fade(f, 6, n - 6))
            yield im
    pipe('v6_d1_scan', gen())


def seg_concepts():
    # v18: 32 concept renders in chronological order (grey CAD -> red renders -> white livery studies), one per 16th note
    # (BAR/16 = 0.115 s) over the 2 bars, so the flipbook runs twice as fast and every change lands on the grid (user)
    nums = [3053, 3054, 3092, 3099, 3123, 3122, 3127, 3135, 3143, 3144, 3156, 3192, 3197, 3206, 3219, 3245,
            3283, 3285, 3475, 3504, 3527, 3536, 3543, 3572, 3591, 3606, 3956, 3964, 4067, 4143, 4184, 4506]
    n = CUT['livery'] - CUT['concepts']
    edges = np.array([int(round((DROP - 9 * BAR + k * BAR / 16) * FPS)) - CUT['concepts'] for k in range(len(nums))] + [n])
    edges[0] = 0
    def gen():
        for j, num in enumerate(nums):
            src = Image.open(wa(num)).convert('RGB'); a = src.width / src.height
            pw = int(WD * 1.5); ph = int(pw / a); p = src.resize((pw, ph), Image.LANCZOS)
            im = Image.new('RGB', (WD, HT), tuple(int(v) for v in np.asarray(src)[4, 4])); im.paste(p, ((WD - pw) // 2, (HT - ph) // 2))
            section_label(im, 'CONCEPTS', 430)
            for _ in range(edges[j + 1] - edges[j]): yield im
    pipe('v6_e_concepts', gen())


def seg_livery():
    """v9 bumper swap: real 30 fps renders (parts move, so no interpolation): stock bumper off -> scanned structure -> new bumper on
    -> ducts, sides, wheels -> rear: diffuser, wing -> paint wipe -> stripes."""
    import glob
    n = CUT['turn'] - CUT['livery']; fs = sorted(glob.glob(f'{W}/renders/s16_swap/f_*.png')); print('s16 frames', len(fs), 'need', n)
    def gen():
        for f in range(n):
            im = Image.open(fs[min(f, len(fs) - 1)]).convert('RGB').resize((WD, HT), Image.LANCZOS); d = ImageDraw.Draw(im)
            if fade(f, 6, 54) > 0: label(d, 330, 'OLD BUMPER OFF', 'SCANNED WITH THE BUMPER REMOVED', fade(f, 6, 54))
            if fade(f, 58, 176) > 0: label(d, 330, 'NEW BODY PANELS', 'BOMEX WIDEBODY / NISSAN x MOTOIQ', fade(f, 58, 176))
            if fade(f, 180, n - 3) > 0: label(d, 330, 'LIVERY', 'APPLIED IN 3D FIRST', fade(f, 180, n - 3))
            yield im
    pipe('v6_d2_livery', gen())


def seg_turn():
    """360 rendered at 30 fps: 4.2 s constant-speed orbit, 1 s ease into the reveal camera, hold on it."""
    n = CUT['reveal'] - CUT['turn']; frs = render_seq('s16_turn', n, direct=True)   # v12: 30 fps render, no minterpolate (it wobbled the car)
    def gen():
        for f in range(n):
            im = Image.fromarray(frs[min(f, len(frs) - 1)]); d = ImageDraw.Draw(im)
            if fade(f, 6, 110) > 0: label(d, 330, 'FINAL RENDER', 'SCAN + NEW PANELS + LIVERY', fade(f, 6, 110))
            yield im
    pipe('v6_d3_turn', gen())


def seg_reveal():
    """The real car (Nov 5 booth photo, the frame the 360 ends on) with eight real headlines landing on it, one per beat from beat 2."""
    A = lambda name, y0, y1, x0=0, x1=1080: Image.open(f'{D}/press/{name}.png').convert('RGB').crop((x0, y0, x1, y1))
    mt = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '141', '-i', REC, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    mt = Image.fromarray(np.frombuffer(mt, np.uint8).reshape(2622, 1206, 3)).crop((60, 1465, 1140, 1615))
    top = [('CARSCOOPS', A('carscoops', 215, 500)), ('MOTORTREND', mt), ('MOTORWEEK', A('motorweek', 520, 700)), ('MOTORING RESEARCH', A('motoringresearch', 235, 510)), ('AUTO123', A('auto123', 460, 580))]
    bot = [('TOP GEAR PHILIPPINES', A('topgear_ph', 310, 610, 80, 1080)), ('TFLCAR', A('tflcar', 245, 460)), ('MOTOR ILLUSTRATED', A('motorillustrated', 255, 460))]
    CW = 620; tagf = MONO(22); cards = []
    def lay(lst, y, xs):
        for k, (tag, im) in enumerate(lst):
            h = int(im.height * CW / im.width); cards.append([tag, im.resize((CW, h), Image.LANCZOS), xs[k % 2], y + 34]); y += h + 34 + 14
        return y
    print('top stack ends y', lay(top, 44, (50, 410))); print('bottom stack ends y', lay(bot, 1330, (410, 50)))   # v17: back to staggered left/right (user preferred it to one column)
    order = [0, 5, 1, 6, 2, 7, 3, 4]                      # alternate top / bottom so the car stays clear in the middle
    beat_s = BAR / 4                                                          # base beat grid (0.4615 s), from the drop
    appear = {c: int(round((k * beat_s) * FPS)) for k, c in enumerate(order)}   # v14: one headline per base beat, starting on the drop
    base = Image.open(f'{W}/match/reveal.png').convert('RGB'); n = CUT['sema'] - CUT['reveal']
    def gen():
        for f in range(n):
            im = base.copy(); d = ImageDraw.Draw(im)
            for c, (tag, card, x, y) in enumerate(cards):
                if f < appear[c]: continue
                u = min(1.0, (f - appear[c] + 1) / 4); dy = int((1 - u) * 50)
                d.rectangle([x - 6, y - 36 + dy, x + CW + 6, y + card.height + 6 + dy], fill=INK)
                spaced(d, (x + 2, y - 31 + dy), tag, tagf, GREEN, track=2)
                im.paste(card, (x, y + dy))
            yield im
    pipe('v6_r_reveal', gen())


def seg_end():
    """v18: Illumaesthetic / motoiq lockup / Bomex stacked, centred, with equal gaps, the stack centred on the frame (user)."""
    logo = Image.open(f'{D}/logo/v2complete.png').convert('RGBA'); lw = 700; logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    mq = Image.open(f'{D}/logo/motoiq_lockup_white.png').convert('RGBA'); mq = mq.resize((560, int(mq.height * 560 / mq.width)), Image.LANCZOS)
    bx = Image.open(f'{D}/logo/bomex_white.png').convert('RGBA'); bx = bx.resize((560, int(bx.height * 560 / bx.width * 1.2)), Image.LANCZOS)   # v19: source badge art is squashed; +20% height (user)
    def ink(im):                                     # visible box (alpha bbox), so spacing is between the marks, not the canvases
        return im.crop(im.getchannel('A').getbbox())
    logo, mq, bx = ink(logo), ink(mq), ink(bx)
    gap = 170; total = logo.height + mq.height + bx.height + 2 * gap; y0 = (HT - total) // 2
    ys = [y0, y0 + logo.height + gap, y0 + logo.height + gap + mq.height + gap]
    n = END - CUT['end']
    def gen():
        for f in range(n):
            im = Image.new('RGB', (WD, HT), (0, 0, 0))
            for k, (lg, yy) in enumerate(zip((logo, mq, bx), ys)):
                al = min(1.0, f / 8) if k == 0 else max(0.0, min(1.0, (f - 14) / 8))
                if al <= 0: continue
                lg2 = lg.copy(); lg2.putalpha(lg.getchannel('A').point(lambda v: int(v * al)))
                im.paste(lg2, ((WD - lg.width) // 2, yy), lg2)
            yield im
    pipe('v6_z_end', gen())


def seg_sema():
    """Four clips where the whole car stays in frame (user: earlier end shots cropped the car or cut too soon), one bar each."""
    n = (CUT['end'] - CUT['sema']); e = np.round(np.linspace(0, n, 5)).astype(int); L = [e[i + 1] - e[i] for i in range(4)]
    def gen():
        yield from ig_frames(151.4, L[0])                                  # motoiq: door lifts, car revealed
        yield from ig_frames(72.0, L[1])                                   # caranddriver: on track
        yield from ig_frames(88.0, L[2])                                   # eddiex616: whole car from the front
    pipe('v6_s1_reels', gen())                                             # (own IMG_3228 booth wide dropped: nose leaves the frame)
    clip('v6_s3_rear', S + 'IMG_3235.mov', 0.0, L[3])                      # rear wide, wing + diffuser


SEGS = {
    'v6_a_hook': seg_hook, 'v6_b_wasnt': seg_wasnt,
    'v6_c1_spray': lambda: frames_sel('v6_c1_spray', D + '/dropbox/may11_1135.mov', np.round(np.linspace(10, 280, CUT['scanner'] - CUT['spray'])).astype(int)),
    'v6_c2_scanner': lambda: clip('v6_c2_scanner', S + 'may11_1145.mov', 7.0, CUT['tl'] - CUT['scanner'], hdr=False),
    'v6_c3_timelapse': lambda: frames_sel('v6_c3_timelapse', D + '/dropbox/may11_1140.mov', np.round(np.linspace(540, 780, CUT['scan'] - CUT['tl'])).astype(int)),
    'v6_d1_scan': seg_scan, 'v6_e_concepts': seg_concepts, 'v6_d2_livery': seg_livery, 'v6_d3_turn': seg_turn,
    'v6_r_reveal': seg_reveal, 'v6_s': seg_sema, 'v6_z_end': seg_end,
}
ORDER = ['v6_a_hook', 'v6_b_wasnt', 'v6_c1_spray', 'v6_c2_scanner', 'v6_c3_timelapse', 'v6_d1_scan', 'v6_e_concepts', 'v6_d2_livery', 'v6_d3_turn',
         'v6_r_reveal', 'v6_s1_reels', 'v6_s3_rear', 'v6_z_end']
if __name__ == '__main__':
    print('cut frames', CUT, 'end', END)
    for k in [a for a in sys.argv[1:] if a != 'mux']: SEGS[k]()
    if 'mux' in sys.argv:
        lst = SEG + '/list_v6.txt'; open(lst, 'w').write(''.join(f"file '{SEG}/{k}.mp4'\n" for k in ORDER)); out = W + '/out/sentra_sema_v19.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', MUSIC, '-filter_complex', f'[1:a]afade=t=out:st={END / FPS - 1.2}:d=1.2[a]',
                        '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-t', str(END / FPS), '-movflags', '+faststart', out], check=True)
        print(out)
