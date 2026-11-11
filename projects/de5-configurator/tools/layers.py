"""Build every 1080x1920/30fps layer for the DE5 GT-wing configurator demo: PNG-sequence screen captures -> mp4 (exact frame counts from the
beat grid), shared-window photo layers, 9:16 crops of the Integra install clips, end card, music bed. usage: layers.py [names...]"""
import sys, subprocess, numpy as np, cv2
M = '/home/user/media/de5-configurator'; Wk = '/home/user/media/work/de5'; L = f'{Wk}/layers'; W, H, FPS = 1080, 1920, 30
only = set(sys.argv[1:])
X264 = ['-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS)]
def run(*a): subprocess.run(['ffmpeg', '-y', '-v', 'error', *map(str, a)], check=True)
def want(n): return not only or n in only
# beat grid: 110.0 BPM (0.54545 s); frame(k) = 393 + round((k-24)*16.3636); the drop (35.97 s of the track) = beat 24 = frame 393
fr = lambda k: 393 + round((k - 24) * 30 * 60 / 110)
CUTS = {'A': 0, 'B': 5, 'C': 9, 'D': 16, 'E': 24, 'F1': 29, 'F2': 30, 'F3': 31, 'F4': 32, 'F5': 33, 'F6': 34, 'F7': 35, 'F8': 35.5, 'F9': 36, 'F10': 36.5,
        'G1': 37, 'G2': 41, 'H': 46, 'END': 53}
names = list(CUTS); N = {a: fr(CUTS[b]) - fr(CUTS[a]) for a, b in zip(names, names[1:])}
if 'grid' in only: print({k: fr(v) for k, v in CUTS.items()}, N); sys.exit()
# --- screen captures (frame-stepped PNGs from tools/capWeb.cjs, capD.cjs, capEnd.cjs); last frame held if the capture is short
for n in 'ABCDH':
    if want(n): run('-framerate', FPS, '-pattern_type', 'glob', '-i', f'{Wk}/frames/{n}/0*.png', '-vf', f'scale={W}:{H}:flags=lanczos,tpad=stop_mode=clone:stop=60', '-frames:v', N[n], *X264, f'{L}/{n}.mp4')
# --- stills with a linear 9:16 window move (cx, cy, height in photo px). E uses the SAME window path the configurator camera ends on (capD.cjs WIN)
def kb(name, photo, s0, s1, n=None, dur=None):
    im = cv2.imread(photo); n = n or N[name]; dur = dur or n
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', *X264, f'{L}/{name}.mp4'], stdin=subprocess.PIPE)
    for i in range(n):
        u = i / dur; cx, cy, h = [a + (b - a) * u for a, b in zip(s0, s1)]; sc = H / h
        Mx = np.array([[sc, 0, W / 2 - cx * sc], [0, sc, H / 2 - cy * sc]])
        p.stdin.write(cv2.warpAffine(im, Mx, (W, H), flags=cv2.INTER_AREA if sc < 1 else cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
    p.stdin.close(); p.wait()
PH = f'{M}/photos/gt_acura-integra-de5-gt-wing-'
DR = f'{M}/drive/'   # v2: the user's Drive photos of the DE5 GT wing (v1 used the listing's driveway photos)
if want('E'): kb('E', DR + '_DSF3972 wing1.jpg', (2420, 2381.5, 4763), (2520, 2480, 4250), dur=82)
if want('G1'): kb('G1', DR + '_DSF3974 wing.jpg', (1500, 2367.5, 4735), (4300, 2367.5, 4735))
if want('G2'): kb('G2', DR + '_DSF3842 wing1.jpg', (2200, 2950, 4900), (2200, 2850, 4400))
# --- install snippets: Dropbox 'Integra Sport Wing Install Tutorial' (Sony 1080p 23.976, flat profile): 9:16 window (608 px of 1920) at cx, grade lift
T = f'{M}/tutorial'
GR = 'eq=contrast=1.32:gamma=1.18:saturation=1.35'
CL = {'F1': ('C0196', 5.0, 0.62), 'F2': ('C0202', 2.5, 0.40), 'F3': ('C0204', 1.5, 0.55), 'F4': ('C0213', 0.3, 0.35), 'F5': ('C0220', 4.4, 0.45), 'F6': ('C0194', 3.0, 0.50),
      'F7': ('C0198', 0.6, 0.60), 'F8': ('C0234', 5.6, 0.60), 'F9': ('C0220', 13.0, 0.50), 'F10': ('C0217', 3.8, 0.55)}
for n, (c, t, cx) in CL.items():
    if want(n):
        run('-ss', t, '-i', f'{T}/{c}.MP4', '-an', '-vf', f'crop=608:1080:{max(0, min(1312, int(1920 * cx - 304)))}:0,{GR},scale={W}:{H}:flags=lanczos,fps={FPS}', '-frames:v', N[n], *X264, f'{L}/{n}.mp4')
# --- music bed: 'Time Back' - Sinny & 7vvch from 22.87 s so the drop (35.97 s) lands on frame 393 (13.100 s)
if want('music'):
    run('-ss', 35.97 - 393 / 30, '-i', f'{M}/music/time_back.mp3', '-t', 30.0, '-af', 'afade=t=in:d=0.25', '-ar', 48000, f'{L}/music.wav')
