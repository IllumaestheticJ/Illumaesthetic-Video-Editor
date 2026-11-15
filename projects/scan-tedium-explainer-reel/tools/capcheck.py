"""Caption placement check: Part A frames + the overlay, at each caption page's first and last frame (full words shown).
    python capcheck.py <gfx.mov> <out.jpg> [video.mp4]   (video defaults to partA_v5.mp4)"""
import sys, subprocess, numpy as np, cv2
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import full_build as fb

def grab(path, frames, fmt, ch):
    sel = '+'.join(f'eq(n\\,{f})' for f in frames)
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'select={sel}', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', fmt, '-'],
                       capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, 1920, 1080, ch)

pg = fb.pages()
frames = sorted({f for p in pg for f in (round(p['t0'] * 30) + 2, round(p['t1'] * 30) - 1)})
vid = sys.argv[3] if len(sys.argv) > 3 else str(fb.OUT / 'partA_v5.mp4')
V = grab(vid, frames, 'rgb24', 3)
if len(sys.argv) > 3:
    C = V.astype(np.float32)
else:
    G = grab(sys.argv[1], frames, 'rgba', 4).astype(np.float32)
    a = G[..., 3:4] / 255
    C = V * (1 - a) + G[..., :3] * a
tiles = []
for f, im in zip(frames, C):
    t = cv2.resize(im.astype(np.uint8), (270, 480), interpolation=cv2.INTER_AREA)
    cv2.rectangle(t, (15, 55), (235, 375), (255, 0, 0), 1)   # safe area x 60-940, y 220-1500
    cv2.putText(t, str(f), (5, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    tiles.append(t)
while len(tiles) % 9:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + 9]) for i in range(0, len(tiles), 9)]
cv2.imwrite(sys.argv[2], cv2.cvtColor(np.vstack(rows), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(frames)
