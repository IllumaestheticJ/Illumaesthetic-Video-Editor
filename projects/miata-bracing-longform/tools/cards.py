"""Data cards for the Miata bracing long-form (1920x1080 PNG), built from the engineering-Drive PDFs.
usage: python cards.py <data_dir> <out_dir>   Numbers come from Strut Spread.xlsx / the PDFs only."""
import sys, subprocess, glob, os
from PIL import Image, ImageDraw, ImageFont
D, O = sys.argv[1], sys.argv[2]; os.makedirs(O, exist_ok=True)
W, H = 1920, 1080
def F(sz, wt='Bold'):
    for p in (f'/usr/share/fonts/truetype/inter/InterDisplay-{wt}.ttf', f'/usr/share/fonts/truetype/inter/Inter-{wt}.ttf'):
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    c = subprocess.run(['fc-match', '-f', '%{file}', f'Inter Display:style={wt}'], capture_output=True, text=True).stdout
    return ImageFont.truetype(c, sz)
EXT = {'jacked': 'NB Miata Scan Jacked Exterior_Heatmap.pdf', 'fender': 'NB Miata Scan Fender Brace Only Jacked_Heatmap.pdf',
       'strut': 'NB Miata Scan Strut Tower Jacked Exterior_Heatmap.pdf', 'both': 'NB Miata Scan Fender and Strut Jacked Up Exterior_Heatmap.pdf'}
BAY = {'jacked': 'NB Miata Scan Jacked Up Engine Bay.pdf', 'fender': 'NB Miata Scan Fender Brace Jacked Engine Bay.pdf',
       'strut': 'NB Miata Scan Strut Brace Jacked Up.pdf', 'both': 'NB Miata Scan Fender + Strut Jacked Up.pdf'}
TITLE = {'jacked': 'Stock, Jacked (No Bracing)', 'fender': 'Fender Braces Only', 'strut': 'Strut Tower Brace Only', 'both': 'Fender Braces + Strut Tower Brace'}
# engine-bay width, mm (Strut Spread.xlsx)
WID = {'control': 960.948, 'jacked': 962.643, 'fender': 961.185, 'strut': 961.679, 'both': 961.384}
ROWS = [('control', 'Control (stock, on the ground)'), ('jacked', 'Stock, jacked (no bracing)'), ('fender', 'Fender braces only, jacked'),
        ('strut', 'Strut tower brace only, jacked'), ('both', 'Fender braces + strut tower brace, jacked')]
_cache = {}
def page(pdf, p, r=220):
    k = (pdf, p, r)
    if k not in _cache:
        pre = os.path.join(O, '_tmp'); subprocess.run(['pdftoppm', '-r', str(r), '-f', str(p), '-l', str(p), '-png', os.path.join(D, pdf), pre], check=True)
        f = glob.glob(pre + '*.png')[0]; im = Image.open(f).convert('RGB'); im.load(); os.remove(f); _cache[k] = im
    return _cache[k]
def frac(im, x0, y0, x1, y1):
    # crop, wipe the report's frame lines (long straight dark runs), trim to content
    import numpy as np
    w, h = im.size; a = np.array(im.crop((int(w*x0), int(h*y0), int(w*x1), int(h*y1)))); dark = a.max(axis=2) < 90
    a[dark.mean(axis=1) > .5, :, :] = 255; a[:, dark.mean(axis=0) > .5, :] = 255
    ink = a.min(axis=2) < 235; ys = np.where(ink.any(axis=1))[0]; xs = np.where(ink.any(axis=0))[0]
    return Image.fromarray(a[max(ys[0]-12, 0):ys[-1]+12, max(xs[0]-12, 0):xs[-1]+12])
def fit(im, w, h):
    s = min(w/im.width, h/im.height); return im.resize((int(im.width*s), int(im.height*s)), Image.LANCZOS)
def white(title, sub=None):
    c = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(c)
    d.text((W/2, 70), title, font=F(58), fill='#111', anchor='mm')
    if sub: d.text((W/2, 128), sub, font=F(30, 'Medium'), fill='#666', anchor='mm')
    return c, d
def pair(title, a, b, name, sub=None, la=None, lb=None):
    c, d = white(title, sub); y0 = 170; bw, bh = 900, 840
    for i, (im, lab) in enumerate(((a, la), (b, lb))):
        im = fit(im, bw, bh - (50 if lab else 0)); x = 40 + i*940 + (bw-im.width)//2; c.paste(im, (x, y0 + (50 if lab else 0) + (bh-(50 if lab else 0)-im.height)//2))
        if lab: d.text((40 + i*940 + bw/2, y0 + 20), lab, font=F(32, 'SemiBold'), fill='#333', anchor='mm')
    c.save(os.path.join(O, name)); return c
# --- engine-bay width cards (page 2: upper = reference, lower = state)
def width(k):
    p = page(BAY[k], 2); return frac(p, .08, .05, .92, .47), frac(p, .08, .47, .92, .9)
ctrl, _ = width('jacked')
c, d = white('Control: Stock, On The Ground', 'Engine bay width between the strut towers (mm)'); im = fit(ctrl, 1300, 860); c.paste(im, ((W-im.width)//2, 180)); c.save(os.path.join(O, 'w_control.png'))
for k in ('jacked', 'fender', 'strut', 'both'):
    a, b = width(k); pair(TITLE[k], a, b, f'w_{k}.png', 'Engine bay width between the strut towers (mm)')
# --- cumulative table, new order
def table(n, name, hl=None):
    c = Image.new('RGB', (W, H), '#262626'); d = ImageDraw.Draw(c)
    d.text((110, 150), 'ENGINE BAY WIDTH BETWEEN STRUT TOWERS', font=F(30, 'SemiBold'), fill='#9aa0a6')
    xs = (110, 1010, 1420); y = 250
    for x, t in zip(xs, ('Configuration', 'Width', 'Delta vs control')): d.text((x, y), t, font=F(34, 'SemiBold'), fill='#e8ecf2')
    y += 70
    for i, (k, lab) in enumerate(ROWS[:n]):
        d.line((110, y-18, W-110, y-18), fill='#444', width=2); col = '#ffffff' if (hl is None or i == n-1) else '#aab0b8'
        d.text((xs[0], y), lab, font=F(38, 'Medium'), fill=col); d.text((xs[1], y), f'{WID[k]:.3f} mm', font=F(38, 'Medium'), fill=col)
        dl = WID[k]-WID['control']; d.text((xs[2], y), '—' if k == 'control' else f'+{dl:.3f} mm wider', font=F(38, 'Medium'), fill=col); y += 96
    c.save(os.path.join(O, name))
for n in range(1, 6): table(n, f'table_{n}.png', hl=True)
# --- exterior heat maps (each view keeps its own colour scale from the report)
def views(pdf, p): pg = page(pdf, p); return frac(pg, .05, .045, .975, .475), frac(pg, .05, .475, .975, .905)
for k in EXT:
    sc = 'Deviation vs control ground scan, mm.  Colour scale ±8 mm on this report' if k == 'both' else 'Deviation vs control ground scan, mm.  Colour scale ±15 mm'
    for p, nm in ((2, 'side'), (3, 'ends'), (4, 'top')):
        a, b = views(EXT[k], p); pair(TITLE[k], a, b, f'h_{k}_{nm}.png', sc)
# --- strut-tower close-ups (bay reports page 3, lower view), unbraced vs each
def tower(k): return frac(page(BAY[k], 3), .03, .50, .985, .86)
for k in ('fender', 'strut', 'both'):
    pair('Strut Tower Top, Jacked', tower('jacked'), tower(k), f'tower_{k}.png', 'Deviation vs engine-bay control scan, mm (scale about ±3 mm)', 'No bracing', TITLE[k])
# --- conclusion bar chart
c = Image.new('RGB', (W, H), '#262626'); d = ImageDraw.Draw(c)
d.text((110, 90), 'HOW MUCH THE STRUT TOWERS SPREAD WITH ONE CORNER JACKED', font=F(34, 'SemiBold'), fill='#9aa0a6')
d.text((110, 140), 'Engine bay width minus control (960.948 mm)', font=F(30, 'Medium'), fill='#777')
base = WID['jacked']-WID['control']; y = 250; x0 = 640; full = 900
for k, lab, colr in (('jacked', 'No bracing', '#e5484d'), ('fender', 'Fender braces only', '#3fb950'), ('strut', 'Strut tower brace only', '#4c9aff'), ('both', 'Fender + strut', '#d6a419')):
    dl = WID[k]-WID['control']; w = full*dl/base
    d.text((110, y+38), lab, font=F(42, 'SemiBold'), fill='#e8ecf2', anchor='lm'); d.rectangle((x0, y, x0+w, y+76), fill=colr)
    d.text((x0+w+24, y+38), f'+{dl:.3f} mm', font=F(42, 'Bold'), fill='#fff', anchor='lm')
    if k != 'jacked': d.text((x0+w+330, y+38), f'{100*(1-dl/base):.0f}% less than unbraced', font=F(34, 'Medium'), fill='#9aa0a6', anchor='lm')
    y += 170
d.text((110, 980), 'One car, one scan per setup, static load from a jack. Percentages calculated from the widths above.', font=F(28, 'Medium'), fill='#777')
c.save(os.path.join(O, 'chart.png'))
# --- takeaways + end card
def bullets(name, head, items):
    c = Image.new('RGB', (W, H), '#262626'); d = ImageDraw.Draw(c); d.text((110, 120), head, font=F(34, 'SemiBold'), fill='#9aa0a6'); y = 250
    for i, t in enumerate(items):
        d.text((110, y), f'{i+1}', font=F(64), fill='#d6a419'); 
        for j, ln in enumerate(t.split('\n')): d.text((210, y+6+j*58), ln, font=F(46, 'SemiBold' if j == 0 else 'Medium'), fill='#fff' if j == 0 else '#aab0b8')
        y += 250
    c.save(os.path.join(O, name))
bullets('takeaways.png', 'WHAT THE DATA SAYS', ['Every setup cut the tower spread by more than half', 'Fender braces alone did the most at the towers\n86% less spread, vs 57% for the strut tower brace alone',
        'The braces did not simply add up\nBoth together: 74% less, about the same as fender braces alone'])
bullets('caveats.png', 'KEEP IT IN CONTEXT', ['One car, one scan per setup', 'Static load: one corner on a jack, not a corner on track', 'Largest movement measured at the towers: 1.695 mm'])
c = Image.new('RGB', (W, H), 'black'); d = ImageDraw.Draw(c)
d.text((W/2, 470), 'DOES CHASSIS BRACING\nACTUALLY DO ANYTHING?', font=F(72, 'Black'), fill='white', anchor='mm', align='center')
d.text((W/2, 660), 'YES. AND YOU CAN MEASURE IT.', font=F(44, 'Bold'), fill='white', anchor='mm'); c.save(os.path.join(O, 'end.png'))
print('cards ->', O, len(os.listdir(O)))
