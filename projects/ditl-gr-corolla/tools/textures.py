"""Low-res 'video game' textures (numpy/PIL), 128 px, meant for Closest filtering. python textures.py <outdir>"""
import sys, numpy as np
from PIL import Image, ImageDraw
rng = np.random.default_rng(11); N = 128
def fn(n=N, octs=5, seed=None):
    r = np.random.default_rng(seed) if seed is not None else rng; out = np.zeros((n, n)); amp = 1.0; tot = 0
    for o in range(octs):
        k = 2 ** (o + 2); g = r.random((k, k)); g = np.kron(g, np.ones((n // k + 1, n // k + 1)))[:n, :n]
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((n, n), Image.BILINEAR if o < 3 else Image.NEAREST); out += np.asarray(im) / 255 * amp; tot += amp; amp *= 0.55
    return out / tot
def rgb(a): return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
def col(c, v): return np.stack([np.clip(v * c[i], 0, 1) for i in range(3)], -1)
def speck(p, n=N): return (rng.random((n, n)) < p).astype(float)
def asphalt():
    v = 0.16 + 0.1 * fn() + 0.12 * speck(0.12) - 0.06 * speck(0.1); a = col((1, 1, 1.05), v); im = rgb(a); d = ImageDraw.Draw(im)
    for _ in range(3):
        x, y = rng.integers(0, N, 2); pts = [(x, y)]
        for _ in range(8): x += rng.integers(-12, 13); y += rng.integers(4, 14); pts.append((x, y))
        d.line(pts, fill=(18, 18, 20), width=1)
    return im
def grass():
    v = 0.5 + 0.5 * fn(); a = np.stack([0.13 + 0.12 * v, 0.34 + 0.3 * v, 0.08 + 0.06 * v], -1); s = speck(0.2)[..., None]; a = a * (1 - 0.35 * s); s2 = speck(0.06)[..., None]; a = a + s2 * np.array([0.12, 0.2, 0.02]); return rgb(a)
def brick():
    a = np.zeros((N, N, 3)); a[:] = (0.62, 0.6, 0.55); bh, bw = 16, 32
    for r in range(N // bh):
        off = (bw // 2) * (r % 2)
        for c in range(-1, N // bw + 1):
            x0, y0 = c * bw + off, r * bh; t = rng.random(); cc = np.array((0.5 + 0.2 * t, 0.2 + 0.1 * t, 0.13 + 0.07 * t))
            a[y0 + 1:y0 + bh - 1, max(0, x0 + 1):max(0, min(N, x0 + bw - 1))] = cc
    return rgb(a * (0.8 + 0.4 * fn()[..., None]))
def wood():
    y, x = np.mgrid[0:N, 0:N]; g = np.sin((y + 6 * fn(octs=3) * 20) * 0.9) * 0.5 + 0.5; v = 0.55 + 0.3 * g + 0.15 * fn(); a = col((0.62, 0.36, 0.17), v)
    a[:, ::32] *= 0.45; a[::64, :] *= 0.6; return rgb(a)
def detail(kind):
    y, x = np.mgrid[0:N, 0:N]
    if kind == "plaster": v = 0.82 + 0.16 * fn() - 0.08 * speck(0.03)
    elif kind == "carpet": v = 0.6 + 0.25 * rng.random((N, N)) + 0.15 * fn()
    elif kind == "siding": v = 0.9 - 0.35 * ((y % 16) < 2) - 0.12 * ((y % 16) / 16) + 0.08 * fn()
    elif kind == "shingle": v = 0.75 - 0.4 * ((y % 12) < 2) - 0.3 * (((x + 8 * ((y // 12) % 2)) % 16) < 1) + 0.2 * rng.random((N, N))
    elif kind == "concrete": v = 0.8 + 0.15 * fn() + 0.06 * rng.random((N, N)); v[:2] = 0.45; v[:, :2] = 0.45
    elif kind == "fabric": v = 0.75 + 0.2 * (((x + y) % 4) < 2) * 0.5 + 0.1 * rng.random((N, N))
    elif kind == "metal": v = 0.85 + 0.1 * fn() - 0.1 * speck(0.02)
    return rgb(col((1, 1, 1), v))
def cardboard():
    y, x = np.mgrid[0:N, 0:N]; v = 0.8 + 0.12 * np.sin(x * 1.6) + 0.1 * fn(); a = col((0.72, 0.53, 0.32), v); a[60:68, :] = (0.78, 0.72, 0.6); return rgb(a)
def plaid():
    y, x = np.mgrid[0:N, 0:N]; a = np.zeros((N, N, 3)); a[:] = (0.15, 0.22, 0.13); a[(x % 32) < 10] += (0.08, 0.1, 0.02); a[(y % 32) < 10] += (0.08, 0.1, 0.02); a[(x % 32) == 20] = (0.5, 0.45, 0.2); a[(y % 32) == 20] = (0.5, 0.45, 0.2)
    return rgb(a * (0.85 + 0.3 * rng.random((N, N, 1))))
def camo():
    f1, f2 = fn(octs=3, seed=3), fn(octs=3, seed=5); a = np.zeros((N, N, 3)); a[:] = (0.36, 0.38, 0.24); a[f1 > 0.55] = (0.2, 0.25, 0.14); a[f2 > 0.6] = (0.42, 0.33, 0.2); a[(f1 < 0.38)] = (0.1, 0.11, 0.08)
    return rgb(a * (0.9 + 0.2 * rng.random((N, N, 1))))
def tile():
    y, x = np.mgrid[0:N, 0:N]; chk = ((x // 32 + y // 32) % 2); a = np.where(chk[..., None], np.array((0.75, 0.72, 0.62)), np.array((0.5, 0.5, 0.46))); a = a * (0.85 + 0.3 * fn()[..., None]); a[::32] *= 0.6; a[:, ::32] *= 0.6; return rgb(a)
def sky(dawn=False):
    W, H = 1024, 512; y = np.linspace(0, 1, H)[:, None]; top, hor = ((0.18, 0.4, 0.86), (0.72, 0.84, 0.97)) if not dawn else ((0.25, 0.38, 0.75), (0.98, 0.78, 0.62))
    t = np.clip(y * 2, 0, 1) ** 0.8; a = np.stack([np.repeat(top[i] + (hor[i] - top[i]) * t, W, 1) for i in range(3)], -1)
    r = np.random.default_rng(2); c = np.zeros((H, W)); amp = 1; tot = 0
    for o in range(6):
        kx, ky = 2 ** (o + 2), 2 ** (o + 1); g = np.asarray(Image.fromarray((r.random((ky, kx)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)) / 255; c += g * amp; tot += amp; amp *= 0.55
    c = np.clip((c / tot - 0.5) * 5, 0, 1) * np.clip(1.15 - np.abs(y - 0.33) * 3.2, 0, 1); c = np.round(c * 4) / 4
    cl = np.array((1.0, 0.99, 0.97)) if not dawn else np.array((1.0, 0.88, 0.8)); a = a * (1 - c[..., None]) + cl * c[..., None]; a[H // 2:] = a[H // 2 - 1:H // 2]
    return rgb(a)
if __name__ == "__main__":
    out = sys.argv[1]
    for n, f in (("asphalt", asphalt), ("grass", grass), ("brick", brick), ("wood", wood), ("cardboard", cardboard), ("plaid", plaid), ("camo", camo), ("tile", tile)): f().save(f"{out}/tx_{n}.png")
    for kd in ("plaster", "carpet", "siding", "shingle", "concrete", "fabric", "metal"): detail(kd).save(f"{out}/tx_{kd}.png")
    sky().save(f"{out}/sky_day.png"); sky(True).save(f"{out}/sky_dawn.png")
