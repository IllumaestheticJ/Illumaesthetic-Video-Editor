"""Arrow + label that follows Grimace (purple/green #558 Miata) through the paddock pan, rough cut 83.92-89.67 s.
usage: callout.py <rough_cut.mp4> <t0> <t1> <out.mp4> [--frames dir]   Tracks the purple livery (HSV), smooths, draws with PIL."""
import sys, subprocess, colorsys, numpy as np
from PIL import Image, ImageDraw, ImageFont
src, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]; W, H = 1920, 1080; FPS = 24000/1001; n = int(round((t1-t0)*FPS))
def F(sz, wt): return ImageFont.truetype(subprocess.run(['fc-match', '-f', '%{file}', f'Inter Display:style={wt}'], capture_output=True, text=True).stdout, sz)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', f'{(t1-t0):.3f}', '-i', src, '-vf', f'scale={W}:{H}', '-r', '24000/1001', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3); n = min(n, len(fr)); box = []
for f in fr[:n]:
    s = f[::4, ::4].astype(np.float32)/255; mx, mn = s.max(2), s.min(2); d = mx-mn+1e-6; r, g, b = s[..., 0], s[..., 1], s[..., 2]
    hue = np.where(mx == b, 4 + (r-g)/d, np.where(mx == r, ((g-b)/d) % 6, 2 + (b-r)/d))*60
    m = (hue > 232) & (hue < 300) & (d/(mx+1e-6) > .38) & (mx > .2); m[:m.shape[0]//4] = False        # purple livery, not the sky
    ys, xs = np.nonzero(m)
    if len(xs) < 150: box.append(box[-1] if box else (W/2, H/2, 300)); continue
    cx = np.median(xs); k = np.abs(xs-cx) < 110; box.append((np.median(xs[k])*4, np.quantile(ys[k], .04)*4, (np.quantile(xs[k], .95)-np.quantile(xs[k], .05))*4))
b = np.array(box); k = 9; pad = np.pad(b, ((k, k), (0, 0)), mode='edge'); sm = np.stack([np.convolve(pad[:, i], np.ones(2*k+1)/(2*k+1), 'valid') for i in range(3)], 1)
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24000/1001', '-i', '-', '-ss', str(t0), '-t', f'{(t1-t0):.3f}', '-i', src,
                       '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '24000/1001', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2',
                       '-video_track_timescale', '24000', '-t', f'{(t1-t0):.3f}', out], stdin=subprocess.PIPE)
f1, f2 = F(58, 'Black'), F(36, 'Bold')
for i in range(n):
    im = Image.fromarray(fr[i]); a = min(1, max(0, (i-6)/8)) * min(1, (n-1-i)/6)            # fade in after the cut, out before the next
    if a > 0:
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); cx, top, _ = sm[i]; tip = (cx, max(top-45, 330)); lx = min(max(cx, 330), W-330); ly = tip[1]-250
        for wd, col in ((16, (0, 0, 0, 255)), (8, (255, 255, 255, 255))):
            d.line([(lx, ly+118), (tip[0], tip[1]-34)], fill=col, width=wd); h = 46 if wd == 8 else 54
            d.polygon([(tip[0], tip[1]+(4 if wd == 16 else 0)), (tip[0]-h*.55, tip[1]-h), (tip[0]+h*.55, tip[1]-h)], fill=col)
        d.text((lx, ly), 'GRIMACE', font=f1, fill='white', anchor='mm', stroke_width=5, stroke_fill='black')
        d.text((lx, ly+62), '@epsilon_motorsports car', font=f2, fill='white', anchor='mm', stroke_width=4, stroke_fill='black')
        ov.putalpha(ov.getchannel('A').point(lambda v: int(v*a))); im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    if '--frames' in sys.argv and i in (12, n//2, n-12): im.resize((640, 360)).save(f"{sys.argv[sys.argv.index('--frames')+1]}/callout_{i}.jpg")
    ff.stdin.write(im.tobytes())
ff.stdin.close(); ff.wait(); print(out, n)
