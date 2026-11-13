"""Customer-car photo clips for the ending: 9:16 crop of each photo (centre cx/cy as fractions, zoom >= 1 crops
tighter than the full-height 9:16 window), slow push-in, N frames at 30 fps.
Photos: real customer cars from the epsilon.plus TC-wing product galleries (see clips.md).
  python photos.py [--sheet]"""
import subprocess, sys
from PIL import Image
P = '/home/user/media/epsilon-wing-configurator/photos/full/'
OUT = '/home/user/media/epsilon-wing-configurator/clips/'
# name: (file, cx, cy, zoom)   frames come from assemble.py
SPEC = {'ph1': ('c216.jpg', 0.47, 0.56, 1.0), 'ph2': ('c017.jpg', 0.45, 0.42, 1.0),
        'ph3': ('c163.jpg', 0.47, 0.62, 1.0), 'ph4': ('c065.jpg', 0.53, 0.58, 1.0),
        # v5: three more customer cars (landscape: whole photo fitted to width)
        'ph5': ('c005.jpg', 0.46, 0.5, 1.3), 'ph6': ('c043.jpg', 0.5, 0.48, 1.08), 'ph7': ('c268.jpg', 0.57, 0.55, 1.25)}
PUSH = 0.04

def window(im, cx, cy, z, s=1.0):
    W, H = im.size
    h = min(H, W * 16 / 9) / (z * s); w = h * 9 / 16
    x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
    return (x0, y0, x0 + w, y0 + h)

def frame_fit(im, s, bg, cx=0.5, cy=0.5, z=1.0):
    """photo (cropped by zoom z around cx/cy, car kept whole) fitted to the frame width, on a blurred fill of itself"""
    W, H = im.size; fw = 1080; fh = round(H * fw / W)
    w, h = W / (s * z), H / (s * z)
    x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h); box = (x0, y0, x0 + w, y0 + h)
    fg = im.resize((fw, fh), Image.LANCZOS, box=box)
    out = bg.copy(); out.paste(fg, (0, (1920 - fh) // 2)); return out

def make_bg(im):
    from PIL import ImageFilter, ImageEnhance
    b = im.resize((1080, 1920), Image.LANCZOS, box=window(im, 0.5, 0.5, 1.0))
    return ImageEnhance.Brightness(b.filter(ImageFilter.GaussianBlur(40))).enhance(0.45)

def clip(name, n):
    f, cx, cy, z = SPEC[name]; im = Image.open(P + f).convert('RGB')
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30', '-i', '-',
                           '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', OUT + name + '.mp4'], stdin=subprocess.PIPE)
    bg = make_bg(im)
    for i in range(n):
        s = 1 + PUSH * i / max(1, n - 1)
        ff.stdin.write(frame_fit(im, s, bg, cx, cy, z).tobytes())
    ff.stdin.close(); ff.wait(); print(OUT + name + '.mp4', n)

if __name__ == '__main__':
    if '--sheet' in sys.argv:
        S = Image.new('RGB', (len(SPEC) * 280, 480), 'white')
        for k, name in enumerate(SPEC):
            f, cx, cy, z = SPEC[name]; im = Image.open(P + f).convert('RGB')
            S.paste(frame_fit(im, 1.0, make_bg(im), cx, cy, z).resize((270, 480), Image.LANCZOS), (k * 280, 0))
        S.save(OUT + 'photos_sheet.jpg'); print('sheet')
    else:
        for name in SPEC: clip(name, int(sys.argv[1]) if len(sys.argv) > 1 else 33)
