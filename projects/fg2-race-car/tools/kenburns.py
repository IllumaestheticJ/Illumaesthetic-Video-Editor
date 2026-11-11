"""Shared Ken Burns push for the three layers of one angle (photo / cgi / scan) -> three 1080x1920 30fps mp4s.
The SAME window path is applied to every layer, so on any frame the car is pixel-locked across layers.
usage: kenburns.py ANGLE photo.jpg dur_s 'cx,cy,h' 'cx,cy,h' [ease]   (window centre + height in photo px, start -> end)"""
import sys, subprocess, numpy as np, cv2
name, photo, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
s0 = [float(v) for v in sys.argv[4].split(',')]; s1 = [float(v) for v in sys.argv[5].split(',')]
L = '/home/user/media/work/fg2/layers'; W, H, FPS = 1080, 1920, 30
layers = {'photo': cv2.imread(photo), 'cgi': cv2.imread(f'{L}/{name}_cgi.png'), 'scan': cv2.imread(f'{L}/{name}_scan.png')}
ph = layers['photo'].shape[:2]
for k, im in layers.items():
    assert im is not None, k
    if im.shape[:2] != ph: layers[k] = cv2.resize(im, (ph[1], ph[0]), interpolation=cv2.INTER_LANCZOS4)
n = int(round(dur * FPS))
def ease(u):  # gentle: mostly linear with soft ends so it reads as a constant slow push
    return 0.85 * u + 0.15 * (3 * u * u - 2 * u ** 3)
procs = {k: subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-crf', '10', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{L}/{name}_{k}.mp4'], stdin=subprocess.PIPE) for k in layers}
for i in range(n):
    u = ease(i / max(1, n - 1)); cx, cy, h = [a + (b - a) * u for a, b in zip(s0, s1)]
    sc = H / h; M = np.array([[sc, 0, W / 2 - cx * sc], [0, sc, H / 2 - cy * sc]])
    for k, im in layers.items():
        procs[k].stdin.write(cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
for p in procs.values(): p.stdin.close(); p.wait()
print('KB', name, n, 'frames')
