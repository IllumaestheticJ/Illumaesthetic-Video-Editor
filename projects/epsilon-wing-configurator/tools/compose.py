"""Compose captured frames into 1080x1920 clips using meta.json panes (see capture.js).
  python compose.py <shot> [--sheet]     -> /home/user/media/epsilon-wing-configurator/clips/<shot>.mp4 (or sheet.jpg)"""
import json, os, subprocess, sys
from PIL import Image
CAP = '/home/user/media/epsilon-wing-configurator/cap/'
OUT = '/home/user/media/epsilon-wing-configurator/clips/'
BG = (236, 236, 236)

def frame(meta, path):
    im = Image.open(path).convert('RGB'); d = meta['dpr']
    sx = im.width / meta['clip']['width']; sy = im.height / meta['clip']['height']
    out = Image.new('RGB', (1080, 1920), BG)
    for p in meta['panes']:
        x, y, w, h = p['src']; X, Y, W, H = p['dst']
        box = (round(x * sx), round(y * sy), round((x + w) * sx), round((y + h) * sy))
        out.paste(im.crop(box).resize((W, H), Image.LANCZOS), (X, Y))
    return out

def main(shot, sheet=False):
    d = CAP + shot + '/'; meta = json.load(open(d + 'meta.json'))
    files = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))
    os.makedirs(OUT, exist_ok=True)
    if sheet:
        ims = [frame(meta, d + f).resize((270, 480)) for f in files]
        s = Image.new('RGB', (270 * len(ims) + 10 * (len(ims) - 1), 480), (255, 0, 255))
        for i, im in enumerate(ims): s.paste(im, (i * 280, 0))
        s.save(OUT + shot + '_sheet.jpg', quality=88); print(OUT + shot + '_sheet.jpg', files); return
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30', '-i', '-',
                           '-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', OUT + shot + '.mp4'], stdin=subprocess.PIPE)
    for f in files: ff.stdin.write(frame(meta, d + f).tobytes())
    ff.stdin.close(); ff.wait(); print(OUT + shot + '.mp4', len(files), 'frames')

if __name__ == '__main__':
    main(sys.argv[1], '--sheet' in sys.argv)
