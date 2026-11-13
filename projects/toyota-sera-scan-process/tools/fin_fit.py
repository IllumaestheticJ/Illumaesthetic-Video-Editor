"""Hand-fit the finished-car camera on the FULL phone frame and write a close-up comparison.
    python tools/fin_fit.py NAME angle dist height focal shift_x shift_y [target_fwd]
Level camera `angle` deg off the nose toward car-left at `dist` m; sensor 20.25 mm (full frame of the short).
Writes $W/cam_NAME.json, renders clay at 50 %, and $W/qa/NAME_cmp.jpg (photo | photo + cyan render edges)."""
import json, math, subprocess, sys, numpy as np, cv2
W = '/home/user/media/work/sera'
n = sys.argv[1]; a, d, h, foc, sx, sy = [float(x) for x in sys.argv[2:8]]; tf = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0
f = np.array([0.258, 0.966]); l = np.array([-0.966, 0.258]); ar = math.radians(a)
v = f * math.cos(ar) + l * math.sin(ar); loc = v * d + f * tf
out = f'{W}/cam_{n}.json'
subprocess.run(['python', '-m', 'ive', 'lookat', out, f'--loc={loc[0]:.4f},{loc[1]:.4f},{h}', f'--target={tf*f[0]:.4f},{tf*f[1]:.4f},{h}',
                '--focal', str(foc), '--sensor', '20.25', '--size', '1080x1920'], check=True, capture_output=True)
c = json.load(open(out)); c['shift_x'] = sx; c['shift_y'] = sy; json.dump(c, open(out, 'w'), indent=1)
if '--no-render' in sys.argv: sys.exit()
kit = open(f'{W}/kit_all.txt').read().split()
subprocess.run(['python', '-m', 'ive', 'render', '--', '--scene', f'{W}/kitbase.blend', '--camera', out, '--out', f'{W}/prev/{n}.png',
                '--look', 'clay', '--res-pct', '50', '--samples', '4'] + kit, check=True, capture_output=True)
p = cv2.imread(f'{W}/match_fin_full.png'); r = cv2.resize(cv2.imread(f'{W}/prev/{n}.png'), (1080, 1920))
e = cv2.dilate(cv2.Canny(cv2.cvtColor(r, cv2.COLOR_BGR2GRAY), 40, 120), np.ones((2, 2), np.uint8)); o = p.copy(); o[e > 0] = (255, 255, 0)
cv2.imwrite(f'{W}/qa/{n}_cmp.jpg', np.hstack([p[820:1560, 0:1000], o[820:1560, 0:1000]]))
