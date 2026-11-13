"""v3 panel cuts for the Cappuccino exploded view - seams come from the scan, not from margins (reviewer: "the lines
where the front bumper and the trunk were cut are not correct"). Replaces lids.py --clip and composite.py's trims.

  panels.py LEVDIR OUTDIR [--hood-only]        (levelled+cropped mm frame; writes hood.stl trunk.stl base.stl fb_nolights.stl + check PNGs)

How each seam is found
  trunk lid   sides + front edge: least-cost path along the shut-line GROOVE in a top-down height map (2 mm px, groove
              depth = grey closing - height), through a few waypoints read off the map. The edge that drops over the
              tail cannot be seen from above -> same trace in the REAR view (over the tail-lamp tops, along the seam).
  hood        side shut lines + head-lamp inner outlines: groove trace top-down. Rear edge: the cowl groove (flood
              fill stops there). Front edge: the nose seam = the upper outline of the Front Bumper PART scan.
  bumpers     body-side cut = car skin that the bumper-OFF state scan does not have (> ABSENT mm from it), limited to
              NEAR mm around the bumper part scan. The state decides the seam; the part scan only limits the zone.
"""
import struct, sys
import numpy as np
from matplotlib.path import Path as MPath
from PIL import Image
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from skimage.graph import route_through_array

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
PX = 2.0
ABSENT, NEAR, ADD = 6.0, 25.0, 6.0
CORRIDOR = 14   # px
NEAR_LOW = 70.0
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
def cen(t): return t["v"].mean(1)
def save(p, r): open(p, "wb").write(b"ive cappuccino panels v3".ljust(80) + struct.pack("<I", len(r)) + r.tobytes()); print(p, len(r))

def hmap(p, ax, rng, depth, sign=1):
    (a0, a1), (b0, b1) = rng; a, b = ax
    q = p[(p[:, a] > a0) & (p[:, a] < a1) & (p[:, b] > b0) & (p[:, b] < b1)]
    W, H = int((a1 - a0) / PX), int((b1 - b0) / PX)
    i = ((q[:, a] - a0) / PX).astype(int).clip(0, W - 1); j = ((q[:, b] - b0) / PX).astype(int).clip(0, H - 1)
    h = np.full((H, W), -1e9); np.maximum.at(h, (j, i), sign * q[:, depth]); return h
def groove(h):
    hh = ndi.grey_closing(np.where(h > -1e8, h, -1e4), size=(3, 3))      # pinholes
    return np.clip(ndi.grey_closing(hh, size=(13, 13)) - hh, 0, 50), hh
def shade(h):
    hh = np.where(h > -1e8, h, np.nan); gy, gx = np.gradient(hh)
    return (255 * np.nan_to_num(1 / np.sqrt(1 + gx ** 2 + gy ** 2))).astype(np.uint8)
def trace(h, rng, wps_mm):
    """least-cost path along grooves through waypoints given in mm (axis a, axis b) -> polyline in mm"""
    (a0, _), (b0, _) = rng; gd, _ = groove(h); cost = 1 + 40 * np.exp(-gd / 0.8)
    pts = [(int((b - b0) / PX), int((a - a0) / PX)) for a, b in wps_mm]; path = []
    jj, ii = np.mgrid[0:h.shape[0], 0:h.shape[1]]
    for p, q in zip(pts, pts[1:]):      # stay within a corridor around the straight segment (no shortcuts along other grooves)
        v = np.array(q, float) - p; t = np.clip(((jj - p[0]) * v[0] + (ii - p[1]) * v[1]) / max(1e-9, v @ v), 0, 1)
        dist = np.hypot(jj - p[0] - t * v[0], ii - p[1] - t * v[1])
        path += route_through_array(cost + 8 * np.clip(dist - CORRIDOR, 0, None), p, q, fully_connected=True, geometric=True)[0]
    path = np.array(path); return np.stack([a0 + (path[:, 1] + 0.5) * PX, b0 + (path[:, 0] + 0.5) * PX], 1)
def check(name, h, rng, polys, od):
    (a0, _), (b0, _) = rng; im = np.stack([shade(h)] * 3, -1); H, W = h.shape
    for poly, col in polys:
        i = ((poly[:, 0] - a0) / PX).astype(int).clip(0, W - 1); j = ((poly[:, 1] - b0) / PX).astype(int).clip(0, H - 1)
        for dj in (0, 1): im[np.clip(j + dj, 0, H - 1), i] = col
    Image.fromarray(im[::-1]).save(f"{od}/check_{name}.png")

# waypoints (mm, levelled frame: nose -Y, x centre ~ -120), read off the groove maps
TRUNK_TOP = [(-634, 1720), (-638, 1540), (-600, 1390), (-120, 1414), (360, 1388), (390, 1540), (382, 1720)]
TRUNK_REAR = [(-630, 785), (-520, 778), (-430, 715), (-415, 660), (-120, 658), (175, 660), (190, 715), (280, 778), (385, 785)]
HOOD_L = [(-712, -116), (-711, -250), (-708, -400), (-704, -550), (-700, -700), (-694, -850), (-686, -1000), (-676, -1136), (-436, -1326)]
HOOD_R = [(156, -1326), (396, -1136), (408, -1000), (416, -850), (420, -700), (426, -550), (430, -400), (434, -250), (436, -116)]
# v5 (reviewer: "the hood is cut a little funny when the front bumper comes off"): the nose edge between the lamps came out
# ragged (+-6 mm waves and 10-45 mm tabs where the bumper-top outline dipped). Its real edge is a smooth arc: a quadratic fitted
# to the 28 mm upper envelope of the v4 edge (z mm over x mm). Hood tris below it are dropped (also kept off the body, so no lip).
NOSE_EDGE = (-8.7237e-05, -2.9107e-02, 493.62); NOSE_X = (-436.0, 162.0)
TRUNK_YT = 1720.0     # behind this the lid edge is taken from the rear view

class Cuts:
    def __init__(self, car_c, fb_c, li_c, od):
        skin = car_c[car_c[:, 2] > 450]
        # --- trunk
        self.rt = ((-900, 660), (1150, 1900)); ht = hmap(skin, (0, 1), self.rt, 2)
        top = trace(ht, self.rt, TRUNK_TOP)
        self.trunk_poly = MPath(np.vstack([top, [top[-1, 0], 1910], [top[0, 0], 1910]]))
        self.rr = ((-720, 480), (500, 950)); hr = hmap(car_c[car_c[:, 1] > 1500], (0, 2), self.rr, 1)
        rear = trace(hr, self.rr, TRUNK_REAR); o = np.argsort(rear[:, 0])
        xs, i = np.unique(rear[o, 0], return_index=True); self.seam_x, self.seam_z = xs, np.maximum.reduceat(rear[o, 1], i)
        self.ht = ht
        check("trunk_top", ht, self.rt, [(top, (255, 40, 40))], od); check("trunk_rear", hr, self.rr, [(rear, (255, 40, 40))], od)
        # --- hood
        self.rh = ((-900, 660), (-1400, -60)); hh = hmap(skin, (0, 1), self.rh, 2)   # side shut lines run back to the screen corners (y ~ -110)
        L, R = trace(hh, self.rh, HOOD_L), trace(hh, self.rh, HOOD_R)
        poly = np.vstack([L, [L[-1, 0], -1410], [R[0, 0], -1410], R])
        H, W = hh.shape; yy, xx = np.mgrid[0:H, 0:W]
        inside = MPath(poly).contains_points(np.stack([-900 + (xx.ravel() + .5) * PX, -1400 + (yy.ravel() + .5) * PX], 1)).reshape(H, W)
        gd, _ = groove(hh); bar = ndi.binary_dilation((gd > 1.5) | (hh < -1e8), iterations=1)
        lab, _ = ndi.label(inside & ~bar); seed = lab[int((-800 + 1400) / PX), int((-120 + 900) / PX)]
        m = ndi.binary_fill_holes(ndi.binary_closing(lab == seed, iterations=6)) & inside
        self.hood_mask, self.hh = m, hh
        # nose seam: upper outline of the bumper part scan between the lamps
        f = np.vstack([fb_c, li_c]); f = f[f[:, 1] < -1150]
        bx = np.floor((f[:, 0] + 900) / 4).astype(int); self.fb_top = np.full(400, -1e9); np.maximum.at(self.fb_top, bx.clip(0, 399), f[:, 2])
        self.fb_top = ndi.median_filter(ndi.maximum_filter1d(self.fb_top, 3), 9)
        self.fb_tree = cKDTree(f)
        check("hood_top", hh, self.rh, [(L, (255, 40, 40)), (R, (255, 40, 40))], od)
        Image.fromarray((np.stack([shade(hh)] * 3, -1) * np.where(m, 1.0, 0.45)[..., None]).astype(np.uint8)[::-1]).save(f"{od}/check_hood_mask.png")

    def _px(self, c, rng, h):
        i = ((c[:, 0] - rng[0][0]) / PX).astype(int); j = ((c[:, 1] - rng[1][0]) / PX).astype(int)
        ok = (i >= 0) & (i < h.shape[1]) & (j >= 0) & (j < h.shape[0]); return i.clip(0, h.shape[1] - 1), j.clip(0, h.shape[0] - 1), ok

    def trunk(self, c):
        i, j, ok = self._px(c, self.rt, self.ht)
        m = ok & (c[:, 2] > 450) & self.trunk_poly.contains_points(c[:, :2]) & (c[:, 2] > self.ht[j, i] - 60)
        seam = np.interp(c[:, 0], self.seam_x, self.seam_z, left=1e9, right=1e9)
        return m & ((c[:, 1] < TRUNK_YT) | (c[:, 2] > seam))

    def hood(self, c, smooth_nose=True):
        i, j, ok = self._px(c, self.rh, self.hh)
        m = ok & (c[:, 2] > 450) & self.hood_mask[j, i] & (c[:, 2] > self.hh[j, i] - 60)
        nose = c[:, 1] < -1150
        top = self.fb_top[np.floor((c[:, 0] + 900) / 4).astype(int).clip(0, 399)]
        d, _ = self.fb_tree.query(c[m & nose], distance_upper_bound=5); near = np.zeros(len(c), bool); near[np.where(m & nose)[0]] = d <= 4
        m &= ~(nose & ((c[:, 2] < top + 2) | near))
        if smooth_nose:
            band = nose & (c[:, 0] > NOSE_X[0]) & (c[:, 0] < NOSE_X[1]) & (c[:, 2] < np.polyval(NOSE_EDGE, c[:, 0]))
            m &= ~band
        return m

def main(lev, od):
    g = lambda n: load(f"{lev}/{n}")
    fb, rb, li = g("Front_Bumper_2mm_c.stl"), g("Rear_Bumper_2mm_c.stl"), g("Front_Bumper_Lights_2mm_c.stl")
    fbo, rear = g("Front_Bumper_Off_Hood_Open_2mm_c.stl"), g("Rear_End_All_Removed_2mm_c.stl")
    car2 = g("Full_Car_2mm_c.stl"); c2 = cen(car2)
    cuts = Cuts(c2, cen(fb), cen(li), od)
    save(f"{od}/hood.stl", car2[cuts.hood(c2)]); save(f"{od}/trunk.stl", car2[cuts.trunk(c2)])
    if "--hood-only" in sys.argv: return
    car = g("Full_Car_3mm_c.stl"); cc = cen(car)
    rm = cuts.hood(cc, smooth_nose=False) | cuts.trunk(cc)   # the trimmed nose strip goes with neither hood nor body
    for state, parts in ((fbo, (fb, li)), (rear, (rb,))):
        dn = cKDTree(np.vstack([cen(p) for p in parts])).query(cc, distance_upper_bound=NEAR_LOW + 1)[0]
        near = (dn <= NEAR) | ((dn <= NEAR_LOW) & (cc[:, 2] < 350))   # lower lip / undertray edge: the part scans are thin there
        d, _ = cKDTree(cen(state)).query(cc[near], distance_upper_bound=ABSENT + 1)
        rm[np.where(near)[0][d > ABSENT]] = True
    kc = car[~rm]; print("car trimmed", int(rm.sum()), "of", len(car))
    # states' propped-open lids are dropped (our hinged lid parts replace them): state points > 30 mm above the car roofline
    cell = 40.0
    key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
    u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
    def roof(p):
        k = key(p[:, :2]); i = np.clip(np.searchsorted(u, k), 0, len(u) - 1); return np.where(u[i] == k, top[i], -1e9)
    T = cKDTree(cen(kc)[::2]); adds = []
    for name, st in (("fboho", fbo), ("rear", rear)):
        sc = cen(st); d, _ = T.query(sc, distance_upper_bound=ADD + 1); up = sc[:, 2] > roof(sc) + 30
        a = (d > ADD) & ~up; print(name, "added", int(a.sum()), "dropped open lid", int(up.sum())); adds.append(st[a])
    save(f"{od}/base.stl", np.concatenate([kc] + adds))
    d, _ = cKDTree(cen(li)).query(cen(fb), distance_upper_bound=7); save(f"{od}/fb_nolights.stl", fb[d > 6])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
