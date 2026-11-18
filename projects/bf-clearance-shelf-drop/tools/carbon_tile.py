"""2x2 twill carbon tile (tileable): colour + height maps for the carbon material in shots_v0.py.
Each tow has a cylindrical sheen across its width and fine fibre lines along it; warp and weft tows alternate
in the 2-over-2 twill so the weave reads as diagonal steps, like real 3k carbon."""
import sys, numpy as np
from PIL import Image
out = sys.argv[1]
N, T = 8, 64                        # 8x8 tows per tile, 64 px per tow (tile = 2 twill repeats)
S = N * T
y, x = np.mgrid[0:S, 0:S]
i, j = x // T, y // T               # tow column / row
u, v = (x % T) / T, (y % T) / T     # position inside the tow cell
warp = ((i + j) // 2) % 2 == 0      # 2/2 twill: run of 2, shifted by one each row
across = np.where(warp, u, v)       # coordinate across the tow width
along = np.where(warp, v, u)
prof = np.sin(np.pi * across) ** 0.6                      # rounded tow cross-section
fib = 0.88 + 0.12 * np.sin(2 * np.pi * across * 22 + 3 * np.sin(2 * np.pi * along)) # fibre striations
gap = np.clip(np.minimum(across, 1 - across) / 0.06, 0, 1) ** 0.5                    # dark resin gap between tows
lin = np.where(warp, 0.045, 0.012) * (0.30 + 0.70 * prof) * fib * gap + 0.002         # linear albedo, warp/weft differ
srgb = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
Image.fromarray((np.clip(srgb, 0, 1) * 255).astype(np.uint8)).save(f"{out}/carbon_col.png")
h = prof * gap
Image.fromarray((h * 255).astype(np.uint8)).save(f"{out}/carbon_h.png")
print("ok", S)
