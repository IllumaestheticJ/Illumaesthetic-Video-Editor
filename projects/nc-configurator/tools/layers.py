"""Build every 1080x1920/30fps layer for the NC configurator demo: PNG-sequence screen captures -> mp4, shared-push photo layers,
9:16 crops of the install tutorial clips, the end card and the trimmed music bed. usage: layers.py [names...]"""
import sys, subprocess, numpy as np, cv2
M = '/home/user/media/nc-configurator'; Wk = '/home/user/media/work/nc'; L = f'{Wk}/layers'; W, H, FPS = 1080, 1920, 30
only = set(sys.argv[1:])
X264 = ['-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS)]
def run(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *map(str, a)], check=True)
def want(n): return not only or n in only
# --- screen captures (frame-stepped PNGs from tools/capWeb.cjs, capD.cjs)
for n in 'ABCD':
    if want(n): run('-framerate', FPS, '-pattern_type', 'glob', '-i', f'{Wk}/frames/{n}/0*.png', '-vf', f'scale={W}:{H}:flags=lanczos', *X264, f'{L}/{n}.mp4')
# --- stills with a linear push; nc-05 uses the SAME window path the configurator camera ends on (capD.cjs WIN)
def kb(name, photo, n, s0, s1):
    im = cv2.imread(photo)
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', *X264, f'{L}/{name}.mp4'], stdin=subprocess.PIPE)
    for i in range(n):
        u = i / 83; cx, cy, h = [a + (b - a) * u for a, b in zip(s0, s1)]; sc = H / h
        Mx = np.array([[sc, 0, W / 2 - cx * sc], [0, sc, H / 2 - cy * sc]])
        p.stdin.write(cv2.warpAffine(im, Mx, (W, H), flags=cv2.INTER_AREA if sc < 1 else cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
    p.stdin.close(); p.wait()
PH = f'{M}/photos'
if want('E'): kb('E', f'{PH}/nc-05.jpg', 90, (1300, 1560, 3000), (1480, 1380, 2400))
if want('G2'): kb('G2', f'{PH}/nc-06.jpg', 50, (1400, 1600, 3200), (1600, 1250, 2300))
if want('G3'): kb('G3', f'{PH}/nc-01.jpg', 50, (1000, 900, 1800), (860, 720, 1300))
if want('G4'): kb('G4', f'{PH}/nc-04.jpg', 50, (1200, 1550, 3200), (1200, 1250, 2300))
# --- install tutorial snippets (Sony 1080p24 flat profile): 9:16 window at cx, mild contrast/saturation lift
T = f'{M}/tutorial/integra'; GRADE = 'eq=contrast=1.2:saturation=1.35:gamma=1.3'
CL = {'F1': ('C0198', 0.6, 0.52), 'F2': ('C0202', 2.3, 0.40), 'F3': ('C0203', 3.3, 0.50), 'F4': ('C0194', 2.3, 0.50), 'F5': ('C0234', 3.3, 0.50), 'F6': ('C0217', 4.3, 0.50),
      'F7': ('C0204', 3.8, 0.45), 'F8': ('C0193', 1.0, 0.50), 'F9': ('C0199', 1.6, 0.50), 'F10': ('C0219', 16.6, 0.62), 'G1': ('C0222', 0.75, 0.50)}
for n, (c, t, cx) in CL.items():
    if want(n):
        g = GRADE if n != 'G1' else 'eq=contrast=1.08:saturation=1.2'
        run('-ss', t, '-i', f'{T}/{c}.MP4', '-t', 1.75, '-an', '-vf', f'crop=608:1080:{int(1920 * cx - 304)}:0,scale={W}:{H}:flags=lanczos,{g},fps={FPS}', *X264, f'{L}/{n}.mp4')
# --- music bed: 'Take Me (To The Moon)' from 12.405 s so the drop kick (24.915 s) lands on frame 375
if want('music'):
    run('-ss', 12.405, '-i', f'{M}/music/take_me.mp3', '-t', 30.5, '-af', 'afade=t=in:d=0.04', '-ar', 48000, f'{L}/music.wav')
