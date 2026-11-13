"""YouTube thumbnail: the real car on the jack (rough-cut frame) against the 3D heat map from the scans.
usage: python thumb.py <media_dir> <out.jpg> [--yaws]     writes 1920x1080 and a 1280x720 copy next to it"""
import sys, os, math, subprocess, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
M, OUT = sys.argv[1], sys.argv[2]; HERE = os.path.dirname(os.path.abspath(__file__)); W, H = 1920, 1080
sp = importlib.util.spec_from_file_location('h', f'{HERE}/heat3d.py'); h = importlib.util.module_from_spec(sp); sp.loader.exec_module(h)
def F(sz, wt='Black'):
    return ImageFont.truetype(subprocess.run(['fc-match', '-f', '%{file}', f'Inter Display:style={wt}'], capture_output=True, text=True).stdout, sz)
def heat(yaw, pitch, w, hh, scale, state='jacked'):
    a = h.render(f'{M}/heat3d', state, math.radians(yaw), math.radians(pitch), w, hh, scale, splat=7); bg = np.array(h.BGC, np.uint8)
    al = (np.abs(a.astype(int) - bg).sum(2) > 6).astype(np.uint8)*255; return Image.fromarray(np.dstack([a, al]))
if '--yaws' in sys.argv:
    sh = Image.new('RGB', (1920, 1080), '#111')
    for i, y in enumerate((20, 60, 120, 160, 200, 240, 300, 340)): sh.paste(heat(y, 16, 480, 540, 0.105), (480*(i % 4), 540*(i//4)))
    sh.save(OUT); sys.exit()
T = float(sys.argv[sys.argv.index('--t') + 1]) if '--t' in sys.argv else 192.5
raw = f'{M}/work/fr/thumb_src.png'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(T), '-i', f'{M}/dl/MiataScan_RoughCut_1.mp4', '-frames:v', '1', raw], check=True)
src = Image.open(raw).convert('RGB'); s = H/src.height*0.80; src = src.resize((int(src.width*s), int(src.height*s)), Image.LANCZOS)
im = Image.new('RGB', (W, H), '#0d0f12'); from PIL import ImageEnhance
src = ImageEnhance.Contrast(ImageEnhance.Brightness(src).enhance(1.3)).enhance(1.08); src = ImageEnhance.Color(src).enhance(1.15); im.paste(src, (int(os.environ.get('SX', -40)), H - src.height))
fade = Image.new('L', (W, H), 0); fd = ImageDraw.Draw(fade)
for j in range(140): fd.line([(0, H - src.height + j), (W, H - src.height + j)], fill=int(255*(1 - j/140)))
fd.rectangle([0, 0, W, H - src.height], fill=255); im = Image.composite(Image.new('RGB', (W, H), '#0d0f12'), im, fade)
# right side: dark panel behind a diagonal, heat-map car on it
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).polygon([(1010, 0), (W, 0), (W, H), (840, H)], fill=255)
panel = Image.new('RGB', (W, H), '#0d0f12'); pd = ImageDraw.Draw(panel)
for i in range(60): pd.ellipse([1400 - 14*i, 640 - 9*i, 1400 + 14*i, 640 + 9*i], outline=None, fill=(13 + (60 - i)//3, 15 + (60 - i)//3, 18 + (60 - i)//2)) if False else None
glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([980, 330, 1900, 1010], fill=70); glow = glow.filter(ImageFilter.GaussianBlur(120)); panel = Image.composite(Image.new('RGB', (W, H), '#3a4658'), panel, glow)
car = heat(float(os.environ.get('YAW', 300)), 16, 1200, 800, 0.275); panel.paste(car, (800, 250), car)
im.paste(panel, (0, 0), mask); d = ImageDraw.Draw(im)
d.line([(1010, 0), (840, H)], fill='#d6a419', width=10)
# darken the top left for the headline
sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rectangle([0, 0, 1000, 420], fill=150); sh = sh.filter(ImageFilter.GaussianBlur(90)); im = Image.composite(Image.new('RGB', (W, H), '#000'), im, sh); d = ImageDraw.Draw(im)
def txt(xy, s, f, fill): d.text(xy, s, font=f, fill=fill, stroke_width=10, stroke_fill='#000')
txt((56, 36), 'DOES BRACING', F(132), '#ffffff'); txt((56, 176), 'ACTUALLY WORK?', F(132), '#ffd21f')
# labels
def pill(x, y, s, f, bg, fg):
    w = d.textlength(s, font=f); bb = f.getbbox(s); d.rounded_rectangle([x, y, x + w + 56, y + bb[3] + 30], radius=(bb[3] + 30)//2, fill=bg); d.text((x + 28, y + 15 - bb[1]/2), s, font=f, fill=fg)
pill(1130, 60, 'WE 3D SCANNED IT', F(64), '#d6a419', '#111')
# colour ramp under the heat map: the scale the video uses
v = np.linspace(-h.SC, h.SC, 520); ramp = Image.fromarray(np.repeat(h.cmap(v)[None].astype(np.uint8), 26, 0)); im.paste(ramp, (1180, 990)); d = ImageDraw.Draw(im)
d.text((1170, 1003), 'IN', font=F(30, 'Bold'), fill='#e8ecf2', anchor='rm'); d.text((1712, 1003), 'OUT', font=F(30, 'Bold'), fill='#e8ecf2', anchor='lm')
im.save(OUT, quality=93); im.resize((1280, 720), Image.LANCZOS).save(OUT.replace('.jpg', '_1280.jpg'), quality=90); print(OUT)
