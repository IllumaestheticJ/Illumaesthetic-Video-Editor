"""kb_zoomout.py CAR ANGLE OUTNAME dur [start]. Shared zoom-out for one angle on an extended canvas (photo + blurred fill / scan / CGI) -> three 1080x1920 30fps mp4s.
usage: kb_zoomout.py PLANNAME OUTNAME dur_s [start 'cx,cy,h' override]
Window height grows geometrically (constant perceived zoom speed, soft ease at both ends); the same window is
applied to all three layers so the car stays pixel-locked across cuts."""
import sys, json, subprocess, numpy as np, cv2
car, pn, outn, dur = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]); sys.argv = sys.argv[1:]
M = f'/home/user/media/cars/{car}/match'; L = f'/home/user/media/cars/{car}/layers'; W, H, FPS = 1080, 1920, 30
pl = json.load(open(f'{M}/plan_{pn}.json')); rs = pl['render_scale']; ox, oy = pl['origin_photo_px']
s0 = [float(v) for v in sys.argv[4].split(',')] if len(sys.argv) > 4 else pl['win_start']; s1 = pl['win_end']
scan = cv2.imread(f'{L}/{pn}_scan_canvas.png'); cgi = cv2.imread(f'{L}/{pn}_cgi_canvas.png'); Hc, Wc = scan.shape[:2]
assert cgi.shape[:2] == (Hc, Wc)
# photo canvas: blurred, darkened cover-fill of the same photo + the real photo with a feathered edge
ph = cv2.imread(pl['photo']); pw, phh = round(pl['photo_size'][0] * rs), round(pl['photo_size'][1] * rs)
ph = cv2.resize(ph, (pw, phh), interpolation=cv2.INTER_AREA)
k = max(Wc / pw, Hc / phh) * 1.08
bg = cv2.resize(ph, (int(pw * k), int(phh * k)), interpolation=cv2.INTER_LINEAR)
by, bx = (bg.shape[0] - Hc) // 2, (bg.shape[1] - Wc) // 2; bg = bg[by:by + Hc, bx:bx + Wc]
bg = (cv2.GaussianBlur(bg, (0, 0), Wc * 0.025).astype(np.float32) * 0.45)
px, py = round(-ox * rs), round(-oy * rs)
a = np.zeros((Hc, Wc), np.float32); a[py:py + phh, px:px + pw] = 1
f = max(3, int(pw * 0.004)) | 1; a = cv2.GaussianBlur(cv2.erode(a, np.ones((f, f))), (0, 0), f / 2)[..., None]
fg = np.zeros((Hc, Wc, 3), np.float32); fg[py:py + phh, px:px + pw] = ph
photo = (fg * a + bg * (1 - a)).clip(0, 255).astype(np.uint8)
cv2.imwrite(f'{L}/{outn}_photo_canvas.jpg', photo, [cv2.IMWRITE_JPEG_QUALITY, 92])
layers = {'photo': photo, 'scan': scan, 'cgi': cgi}
pyr = {kk: [im] for kk, im in layers.items()}
for kk in pyr:
    for _ in range(3): pyr[kk].append(cv2.pyrDown(pyr[kk][-1]))
tc = lambda c: ((c[0] - ox) * rs, (c[1] - oy) * rs, c[2] * rs)
c0, c1 = tc(s0), tc(s1); n = int(round(dur * FPS))
ease = lambda u: 0.7 * u + 0.3 * (3 * u * u - 2 * u ** 3)
procs = {kk: subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
         '-c:v', 'libx264', '-crf', '10', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{L}/{outn}_{kk}.mp4'], stdin=subprocess.PIPE) for kk in layers}
for i in range(n):
    u = ease(i / max(1, n - 1)); h = c0[2] * (c1[2] / c0[2]) ** u
    t = (h - c0[2]) / (c1[2] - c0[2]) if c1[2] != c0[2] else u  # centre follows the zoom so framing grows evenly
    cx, cy = c0[0] + (c1[0] - c0[0]) * t, c0[1] + (c1[1] - c0[1]) * t
    sc = H / h; lv = int(min(3, max(0, np.floor(np.log2(1 / sc))))) if sc < 1 else 0; f2 = 2 ** lv
    Mx = np.array([[sc * f2, 0, W / 2 - cx * sc], [0, sc * f2, H / 2 - cy * sc]])
    for kk in layers:
        procs[kk].stdin.write(cv2.warpAffine(pyr[kk][lv], Mx, (W, H), flags=cv2.INTER_CUBIC if sc * f2 > 1 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT).tobytes())
for p in procs.values(): p.stdin.close(); p.wait()
print('KB', outn, n, 'frames, zoom', round(c1[2] / c0[2], 2))
