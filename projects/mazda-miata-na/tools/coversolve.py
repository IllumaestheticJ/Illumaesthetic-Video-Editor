"""Solve the Blender camera that reproduces the listing cover photo (a grey render of the full-car scan) by silhouette fit.
    python coversolve.py cover.jpg car4_np.stl out.json [--init x,y,z,tx,ty,tz,focal]
Prepped coords (m) = levelled mm * 0.001 + root_location (prep/frame.json). Blender sensor 36 mm fit to image width."""
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage, optimize
cover, stl, out = sys.argv[1:4]
init = [float(v) for v in sys.argv[5].split(",")] if len(sys.argv) > 5 else [2.6, -3.9, 2.9, 0.0, -0.3, 0.35, 50]
ROOT = np.array([0.09076634049415588, 0.1967344880104065, -0.0060896193608641624])
T = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
tri = np.fromfile(stl, dtype=T, offset=84)
rng = np.random.default_rng(0)
P = tri["v"][rng.choice(len(tri), 400_000, replace=False)].mean(1) * 0.001 + ROOT
img = Image.open(cover).convert("L"); W0, H0 = img.size

def target(w):
    h = round(w * H0 / W0); a = np.asarray(img.resize((w, h)), float)
    m = ndimage.median_filter(a, 3) > 60
    m[int(h * .9):, :int(w * .2)] = False; m[int(h * .88):, int(w * .9):] = False  # watermarks
    lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1)); m = lab == (np.argmax(sz) + 1)
    return ndimage.binary_fill_holes(m), h

def cam_basis(p):
    c, t = np.array(p[:3]), np.array(p[3:6]); fwd = t - c; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
    return c, fwd, right, up

def render(p, w, h):
    c, fwd, right, up = cam_basis(p); f = p[6] / 36 * w
    d = P - c; z = d @ fwd; ok = z > 0.1
    u = w / 2 + f * (d[ok] @ right) / z[ok]; v = h / 2 - f * (d[ok] @ up) / z[ok]
    m = np.zeros((h, w), bool); ui, vi = u.astype(int), v.astype(int); k = (ui >= 0) & (ui < w) & (vi >= 0) & (vi < h)
    m[vi[k], ui[k]] = True
    m = ndimage.binary_closing(m, iterations=2, border_value=0)
    return ndimage.binary_fill_holes(m)

def solve(p0, w, it):
    tm, h = target(w)
    def cost(p):
        m = render(p, w, h); return 1 - (m & tm).sum() / max(1, (m | tm).sum())
    r = optimize.minimize(cost, p0, method="Nelder-Mead", options={"maxiter": it, "xatol": 1e-4, "fatol": 1e-5, "initial_simplex": None})
    return r.x, 1 - r.fun

p, iou = solve(np.array(init), 216, 600); print("216px IoU %.3f" % iou, np.round(p, 3))
p, iou = solve(p, 433, 600); print("433px IoU %.3f" % iou, np.round(p, 3))
p, iou = solve(p, 866, 400); print("866px IoU %.3f" % iou, np.round(p, 3))
json.dump({"loc": list(p[:3]), "target": list(p[3:6]), "focal": p[6], "iou_866": iou, "img": [W0, H0]}, open(out, "w"), indent=1)
w = 866; h = round(w * H0 / W0); tm, _ = target(w); m = render(p, w, h)
ov = np.zeros((h, w, 3), np.uint8); ov[..., 0] = tm * 255; ov[..., 1] = m * 255; ov[..., 2] = (np.asarray(img.resize((w, h)))*0.5).astype(np.uint8)
Image.fromarray(ov).save(out.replace(".json", "_overlay.png"))
