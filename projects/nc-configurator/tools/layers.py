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
if want('G2s'): kb('G2s', f'{PH}/nc-06.jpg', 50, (1400, 1600, 3200), (1600, 1250, 2300))
if want('G3s'): kb('G3s', f'{PH}/nc-01.jpg', 50, (1000, 900, 1800), (860, 720, 1300))
if want('G4'): kb('G4', f'{PH}/nc-04.jpg', 50, (1200, 1550, 3200), (1200, 1250, 2300))
# --- install snippets: the NC's own shoot, Dropbox '/1. Epsilon Plus Videos/2. Long Form/TC Wing Tutorial' (iPhone 4K HLG, landscape):
# tonemap to SDR, 9:16 window (1215 px of 3840, no upscale) centred at cx. (v1 used the Integra tutorial by mistake - user feedback.)
T = f'{M}/tutorial/nc'
TM = 'zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p'
CL = {'F1': ('1837', 57.0, 0.50), 'F2': ('1839b', 46.0, 0.55), 'F3': ('1846', 65.0, 0.45), 'F4': ('1923b', 17.0, 0.45), 'F5': ('1924', 14.0, 0.50), 'F6': ('1929', 40.0, 0.60),
      'F7': ('1844b', 5.5, 0.45), 'F8': ('1848', 12.5, 0.50), 'F9': ('1929', 3.5, 0.50), 'F10': ('1923b', 45.5, 0.60),
      'G1': ('1932a', 0.8, 0.50), 'G2': ('1933', 7.4, 0.55), 'G3': ('1932b', 2.2, 0.50)}
for n, (c, t, cx) in CL.items():
    if want(n):
        run('-ss', t, '-i', f'{T}/{c}.mov', '-t', 1.75, '-an', '-vf', f'crop=1216:2160:{int(3840 * cx - 608)}:0,{TM},scale={W}:{H}:flags=lanczos,fps={FPS}', *X264, f'{L}/{n}.mp4')
# --- music bed: 'Take Me (To The Moon)' from 12.405 s so the drop kick (24.915 s) lands on frame 375
if want('music'):
    run('-ss', 12.405, '-i', f'{M}/music/take_me.mp3', '-t', 30.5, '-af', 'afade=t=in:d=0.04', '-ar', 48000, f'{L}/music.wav')
