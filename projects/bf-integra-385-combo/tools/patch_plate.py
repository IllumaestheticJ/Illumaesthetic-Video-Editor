"""v1.2 plate move: paste the re-rendered plate region (shots.py --plate-border, cropped) into the existing v1.1 HQ
frames, with a feathered edge. usage: python patch_plate.py SHOT  (render_hq/sN + render_hq12_plate/sN -> render_hq12/sN)"""
import sys, os, json, glob, numpy as np
from PIL import Image
W = '/home/user/media/bf-integra-385-combo/work'
s = sys.argv[1]
src, crp, out = f'{W}/render_hq/s{s}', f'{W}/render_hq12_plate/s{s}', f'{W}/render_hq12/s{s}'
os.makedirs(out, exist_ok=True)
b = json.load(open(f'{crp}/border.json'))['border']
frames = sorted(glob.glob(f'{src}/f*.png'))
off = None
for f in frames:
    nm = os.path.basename(f); cf = f'{crp}/{nm}'
    if not os.path.exists(cf) or os.path.getsize(cf) == 0: sys.exit(f'missing crop {cf}')
    A = np.asarray(Image.open(f).convert('RGB')).astype(np.float32); C = np.asarray(Image.open(cf).convert('RGB')).astype(np.float32)
    H, Wd = A.shape[:2]; h, w = C.shape[:2]
    if off is None:  # find the paste position: border estimate +-3 px, best match on the crop's outer ring
        ex, ey = int(b[0] * Wd), H - int(b[1] * H) - h
        ring = np.ones((h, w), bool); ring[12:-12, 12:-12] = False
        best = min(((np.abs(A[ey + dy:ey + dy + h, ex + dx:ex + dx + w] - C)[ring].mean(), dx, dy)
                    for dx in range(-3, 4) for dy in range(-3, 4) if 0 <= ey + dy and ey + dy + h <= H and 0 <= ex + dx and ex + dx + w <= Wd))
        off = (ex + best[1], ey + best[2]); print(f'shot {s}: crop {w}x{h} at {off}, ring diff {best[0]:.2f}')
        yy, xx = np.mgrid[0:h, 0:w]; e = np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]).astype(np.float32)
        M = np.clip((e - 4) / 10, 0, 1)[..., None]   # 4 px untouched, 10 px ramp
    x, y = off
    A[y:y + h, x:x + w] = A[y:y + h, x:x + w] * (1 - M) + C * M
    Image.fromarray(A.round().astype(np.uint8)).save(f'{out}/{nm}', compress_level=3)
print('done', len(frames))
