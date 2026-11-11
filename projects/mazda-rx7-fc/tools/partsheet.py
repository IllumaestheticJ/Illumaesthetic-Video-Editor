"""Side + top density plots of part STLs (red) over the full car (grey), levelled mm frame.
    python projects/mazda-rx7-fc/tools/partsheet.py car.stl out.png part1.stl [...]"""
import sys, numpy as np
from PIL import Image
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84)["v"].mean(1)
def img(p, a, b, rng, bins):
    H, _, _ = np.histogram2d(p[:, a], p[:, b], bins=bins, range=rng); return H.T[::-1]
rows = []
for f in sys.argv[3:]:
    p = np.fromfile(f, dtype=TRI, offset=84)["v"].mean(1)
    tiles = []
    for a, b, rng, bins in [(1, 2, [[-2300, 2300], [-250, 1100]], [460, 135]), (0, 1, [[-1550, 350], [-2300, 2300]], [190, 460]),
                            (0, 2, [[-1550, 350], [-250, 1100]], [190, 135])]:
        bg = img(car, a, b, rng, bins); fg = img(p, a, b, rng, bins)
        rgb = np.zeros(bg.shape + (3,), np.uint8); rgb[...] = np.minimum(bg * 8, 120)[..., None]
        rgb[..., 0] = np.maximum(rgb[..., 0], np.minimum(fg * 30, 255)); tiles.append(Image.fromarray(rgb))
    t = Image.new("RGB", (650, 460)); t.paste(tiles[0], (0, 0)); t.paste(tiles[1], (460, 0)); t.paste(tiles[2], (0, 200)); rows.append(t)
o = Image.new("RGB", (650, 460 * len(rows))); [o.paste(r, (0, i * 460)) for i, r in enumerate(rows)]; o.save(sys.argv[2])
