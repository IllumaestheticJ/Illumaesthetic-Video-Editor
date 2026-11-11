"""Zoomed crosshair tiles for landmark picking.
    python tools/zoom.py IMAGE OUT.jpg "name:x,y;name2:x,y" [--r 40] [--scale 4]
Each tile shows a (2r x 2r) window around (x,y) upscaled, with a red crosshair at (x,y) and
a tick every 10 px; the tile title is the name and the centre pixel."""
import argparse, cv2, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("img"); ap.add_argument("out"); ap.add_argument("pts")
ap.add_argument("--r", type=int, default=40); ap.add_argument("--scale", type=int, default=4)
a = ap.parse_args(); im = cv2.imread(a.img); r, s = a.r, a.scale
tiles = []
for item in a.pts.split(";"):
    n, xy = item.split(":"); x, y = (int(round(float(v))) for v in xy.split(","))
    pad = cv2.copyMakeBorder(im, r, r, r, r, cv2.BORDER_CONSTANT)
    c = pad[y:y + 2 * r, x:x + 2 * r]; c = cv2.resize(c, (2 * r * s, 2 * r * s), interpolation=cv2.INTER_NEAREST)
    for k in range(-r, r + 1, 10):
        p = (k + r) * s
        cv2.line(c, (p, 0), (p, 6), (0, 255, 255), 1); cv2.line(c, (0, p), (6, p), (0, 255, 255), 1)
    m = r * s; cv2.line(c, (m - 12, m), (m + 12, m), (0, 0, 255), 1); cv2.line(c, (m, m - 12), (m, m + 12), (0, 0, 255), 1)
    cv2.putText(c, f"{n} {x},{y}", (4, 2 * r * s - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    tiles.append(c)
cols = 5; rows = (len(tiles) + cols - 1) // cols
blank = np.zeros_like(tiles[0]); tiles += [blank] * (rows * cols - len(tiles))
cv2.imwrite(a.out, np.vstack([np.hstack(tiles[i * cols:(i + 1) * cols]) for i in range(rows)]))
