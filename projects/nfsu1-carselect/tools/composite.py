"""NFSU1 car-select: put an Epsilon car where the game's Miata is, under the game's menu, with our name plate and logos.

Every output frame starts from a real capture frame of the Miata's cycle (drive-in f1653-1745, hold f1746-1836,
drive-out f1838-1972) and changes as little as possible:
  1. take the menu off:   scene = (frame - A) / B      (A = menu colour, B = how much scene shows through; ui/A.npy, B.npy)
  2. take the game's name plate off (it is a 50 % white layer: scene = (x - w*plate) / (1 - w*alpha)), blur-fill the logo strip
  3. erase what is left of the Miata around the kit car (tracked NB silhouette + blue pixels), filled from the surroundings
  4. kit car render over it; the Miata's headlight flare is laid back on top during the approach
  5. menu back on:        frame = A + B * scene, then our plate and logo strip
Pixels nothing touched are the capture's own.
"""
import sys, os, json
import cv2, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import sil

WORK = "/home/user/media/work/nfsu1-carselect"
W, H = sil.W, sil.H
PL = (230, 410, 1150, 1850)
SLOT = {"L": 750, "C": 1086, "R": 1392}; SW = 322; SY0, SY1 = 20, 205
STRIP = (22, 200, 560, 1630)                  # logo strip zone that is blur-filled
FLIP_SRC = 1821                               # native plate: Mazda before, Dodge from here
NATIVE_W = 1.0


# wheel centres (x, y, z) and tyre radius in each car's own GLB frame, and the shift that parks the car on the NB
# (tools: wheels measured from the GLB wheel_* nodes; shift = wheelbase midpoint minus the NB's, as in cams_30_<car>.json)
WHEELS = {"na": ([(0.734, -1.178), (-0.733, -1.178), (0.733, 1.097), (-0.727, 1.097)], 0.289, (0.0, -0.009)),
          "corolla": ([(0.802, -1.276), (-0.805, -1.276), (0.810, 1.383), (-0.811, 1.383)], 0.322, (0.0, 0.085)),
          "delsol": ([(0.815, -1.147), (-0.764, -1.148), (0.779, 1.231), (-0.745, 1.230)], 0.313, (0.021, 0.0735)),
          "frs": ([(0.749, -1.245), (-0.753, -1.245), (0.755, 1.304), (-0.751, 1.304)], 0.313, (0.0, 0.061))}


def spin_wheels(K, car, pose, f, deg):
    """The game's cars roll while they are shown; the render's wheels stand still. Smear each camera-facing wheel
    around its axle: unwrap the wheel disc with the homography of its plane, blur along the angle, wrap it back."""
    if deg <= 0 or car not in WHEELS:
        return K
    pts, r, (sx, sy) = WHEELS[car]
    R, _ = cv2.Rodrigues(np.asarray(pose[:3], float)); t = np.asarray(pose[3:6], float)
    cam = -R.T @ t
    N = 160
    for (x, y) in pts:
        if (cam[0] - (x - sx)) * x <= 0.3 * abs(x):          # wheel face turned away from the camera
            continue
        xo = x + (0.11 if x > 0 else -0.11) - sx                  # outer face of the wheel, NB frame
        yc = y - sy; rr = r * 0.98
        P3 = np.array([[xo, yc - rr, r - rr], [xo, yc + rr, r - rr], [xo, yc + rr, r + rr], [xo, yc - rr, r + rr]])
        Pc = P3 @ R.T + t
        if Pc[:, 2].min() < 0.3:
            continue
        uv = np.stack([f * Pc[:, 0] / Pc[:, 2] + W / 2, f * Pc[:, 1] / Pc[:, 2] + H / 2], 1).astype(np.float32)
        if uv[:, 0].max() < 0 or uv[:, 0].min() > W or uv[:, 1].max() < 0 or uv[:, 1].min() > H:
            continue
        if cv2.contourArea(uv) < 900:
            continue
        sq = np.array([[0, N], [N, N], [N, 0], [0, 0]], np.float32)
        Hm = cv2.getPerspectiveTransform(uv, sq)
        patch = cv2.warpPerspective(K, Hm, (N, N), flags=cv2.INTER_LINEAR)
        pol = cv2.warpPolar(patch, (N // 2, 360), (N / 2, N / 2), N / 2, cv2.WARP_POLAR_LINEAR)
        k = max(3, int(deg) | 1)
        pol_b = cv2.blur(np.vstack([pol[-k:], pol, pol[:k]]), (1, k))[k:-k]
        back = cv2.warpPolar(pol_b, (N, N), (N / 2, N / 2), N / 2, cv2.WARP_POLAR_LINEAR | cv2.WARP_INVERSE_MAP)
        yy, xx = np.mgrid[0:N, 0:N]; rad = np.hypot(xx - N / 2, yy - N / 2) / (N / 2)
        m = np.clip((0.9 - rad) / 0.08, 0, 1).astype(np.float32)   # rim and sidewall, not the tyre's outline
        full = cv2.warpPerspective(np.dstack([back, m]), np.linalg.inv(Hm), (W, H), flags=cv2.INTER_LINEAR)
        full = np.nan_to_num(full)
        mm = full[..., 4:5] * (K[..., 3:4] > 250)
        K = K * (1 - mm) + full[..., :4] * mm
    return K


class Comp:
    def __init__(self):
        # per menu state: the stat bars are different for every car, so the menu colour map is too
        self.AB = {k: (np.load(f"{WORK}/ui/A_{k}.npy"), np.load(f"{WORK}/ui/B_{k}.npy")[..., None]) for k in ("mazda", "dodge")}
        self.P = json.load(open(f"{WORK}/track/poses.json")); self.f = self.P["focal_px"]
        sp = f"{WORK}/track/shift.json"; self.shift = json.load(open(sp)) if os.path.exists(sp) else {}
        self.V, self.F, _ = sil.load_mesh(f"{WORK}/track/nb.npz")
        self.cap = cv2.VideoCapture(f"{WORK}/a60.mp4")
        self.name = {k: np.load(f"{WORK}/ui/name_{k}.npz") for k in ("mazda", "dodge")}   # player name -> "Epsilon" (name_patch.py)
        self.asset = {}
        self.kit_cache = {}

    def a(self, name):
        if name not in self.asset:
            self.asset[name] = np.load(f"{WORK}/ui/assets/{name}.npy")
        return self.asset[name]

    def frame(self, i):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(i))
        return self.cap.read()[1].astype(np.float32)

    def kit(self, car, src):
        p = f"{WORK}/renders/{car}/f_{src:04d}.png"
        if p not in self.kit_cache:
            k = cv2.imread(p, cv2.IMREAD_UNCHANGED)
            if k is None:
                raise FileNotFoundError(p)
            self.kit_cache = {p: cv2.resize(k, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)}
        return self.kit_cache[p]

    def compose(self, src, car, kit_src, plates, strip, glare=True, spin=28):
        """src: capture frame for the background; kit_src: which render of `car`;
        plates: [(name, weight)]; strip: [(make, x_centre, mix 0=side..1=centre, opacity)]."""
        obs = self.frame(src)
        A, B = self.AB["mazda" if src < FLIP_SRC else "dodge"]
        s = (obs - A) / B
        changed = np.zeros((H, W), bool)
        # 2a. native plate off
        r0, r1, c0, c1 = PL
        nat = self.a("plate_mazda" if src < FLIP_SRC else "plate_dodge_native")
        # how strongly the plate sits in this frame, fitted per text line (the make line is more solid than the
        # model wordmark, and the lifted artwork is a low percentile, so a fixed weight leaves a ghost)
        g = nat[..., 0]; rows_ink = np.nonzero((g > 25).sum(1) > 3)[0]
        wmap = np.full(g.shape, NATIVE_W, np.float32)
        if len(rows_ink):
            gaps = np.nonzero(np.diff(rows_ink) > 3)[0]
            cut = (rows_ink[gaps[0]] + rows_ink[gaps[0] + 1]) // 2 if len(gaps) else g.shape[0]
            zg = s[r0:r1, c0:c1].mean(2); hp = lambda q: q - cv2.blur(q, (31, 31))
            hz, hg = hp(zg), hp(g)
            for ya, yb in ((0, cut), (cut, g.shape[0])):
                den = float((hg[ya:yb] ** 2).sum())
                if den > 1e4:
                    wmap[ya:yb] = np.clip(float((hz[ya:yb] * hg[ya:yb]).sum()) / den, 0.7, 1.5)
        pre = nat[..., :3] * wmap[..., None]; al = np.clip(nat[..., 3:] / 255 * wmap[..., None], 0, 0.75)
        z = np.clip((s[r0:r1, c0:c1] - pre) / np.clip(1 - al, 0.3, 1), 0, 255)
        # the letter edges never subtract cleanly (the lifted plate is a little softer than the live one):
        # repaint a thin band along every edge from its neighbours
        a1 = al[..., 0]
        edge = (cv2.dilate((a1 > 0.04).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0) & ~(cv2.erode((a1 > 0.36).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0)
        z = cv2.inpaint(z.astype(np.uint8), edge.astype(np.uint8), 4, cv2.INPAINT_TELEA).astype(np.float32)
        # and what still shows inside the strokes is mostly painted out (the new plate goes over the same spot)
        ink = cv2.dilate((a1 > 0.04).astype(np.uint8), np.ones((9, 9), np.uint8))
        flat = cv2.inpaint(z.astype(np.uint8), ink, 6, cv2.INPAINT_TELEA).astype(np.float32)
        wi = cv2.GaussianBlur(ink.astype(np.float32), (0, 0), 2)[..., None] * 0.8
        z = z * (1 - wi) + flat * wi
        s[r0:r1, c0:c1] = z
        changed[r0:r1, c0:c1] |= cv2.dilate((a1 > 0.01).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        # 2b. logo strip: fill from its surroundings (it sits inside the top band, B ~ 0.3)
        y0, y1, x0, x1 = STRIP
        pad = 60
        reg = s[y0 - 20:y1 + pad, x0 - pad:x1 + pad]
        m = np.ones(reg.shape[:2], np.float32); m[20:20 + (y1 - y0), pad:pad + (x1 - x0)] = 0
        num = cv2.GaussianBlur(reg * m[..., None], (0, 0), 28); den = cv2.GaussianBlur(m, (0, 0), 28)[..., None]
        fill = num / np.maximum(den, 1e-3)
        s[y0:y1, x0:x1] = fill[20:20 + (y1 - y0), pad:pad + (x1 - x0)]
        changed[y0:y1, x0:x1] = True
        # 3. what is left of the game's car
        pose = self.P["frames"][str(src)] if str(src) in self.P["frames"] else self.P["hold"]
        kpose = self.P["frames"][str(kit_src)]
        K = spin_wheels(self.kit(car, kit_src), car, kpose, self.f, spin)
        dx, dy = self.shift.get(str(kit_src), (0.0, 0.0))            # steady.py: steadied screen path, render only
        if abs(dx) + abs(dy) > 1e-3:
            K = cv2.warpAffine(K, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        Ka = K[..., 3:] / 255
        G = cv2.resize(sil.car_mask(self.V, self.F, pose, self.f, 0.5), (W, H), interpolation=cv2.INTER_NEAREST)
        G = cv2.dilate(G, np.ones((15, 15), np.uint8))
        near = cv2.dilate(G, np.ones((61, 61), np.uint8))
        blue = cv2.dilate(sil.blue_mask(np.clip(s, 0, 255).astype(np.uint8)), np.ones((7, 7), np.uint8)) & near
        left = ((G | blue) > 0) & (Ka[..., 0] < 0.6)
        if left.any():
            q = 4
            small = cv2.resize(np.clip(s, 0, 255).astype(np.uint8), (W // q, H // q), interpolation=cv2.INTER_AREA)
            hole = ((G | blue) > 0) | (Ka[..., 0] > 0.05)
            hole = cv2.dilate(cv2.resize(hole.astype(np.uint8), (W // q, H // q), interpolation=cv2.INTER_NEAREST), np.ones((3, 3), np.uint8))
            inp = cv2.inpaint(small, hole, 4, cv2.INPAINT_TELEA)
            inp = cv2.resize(inp, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
            wgt = cv2.GaussianBlur(left.astype(np.float32), (0, 0), 3)[..., None]
            wgt = np.clip(wgt * 2.2, 0, 1)
            s = s * (1 - wgt) + inp * wgt
            changed |= wgt[..., 0] > 0.01
        # 4. kit car
        s = s * (1 - Ka) + K[..., :3] * Ka
        changed |= Ka[..., 0] > 0.003
        if glare and src < 1700:                       # the game's headlight flare, kept on top
            sc = np.clip((obs - A) / B, 0, 255)
            g = ((sc.min(2) > 185) & (near > 0)).astype(np.float32)
            g = cv2.GaussianBlur(cv2.dilate(g, np.ones((5, 5), np.uint8)), (0, 0), 6)[..., None]
            s = s * (1 - g) + np.maximum(s, sc) * g
            changed |= g[..., 0] > 0.01
        out = A + B * s
        # 4b. player name: the box is rebuilt from the patched menu maps over a blur-filled scene (the scene estimate
        # under the old, nearly opaque letters is noise)
        nm = self.name["mazda" if src < FLIP_SRC else "dodge"]; n0, n1, m0, m1 = [int(v) for v in nm["box"]]
        sr = s[n0:n1, m0:m1]; keep = (1 - nm["old"]).astype(np.float32)
        fill = cv2.GaussianBlur(sr * keep[..., None], (0, 0), 6) / np.maximum(cv2.GaussianBlur(keep, (0, 0), 6), 1e-3)[..., None]
        sr = np.where(nm["old"][..., None] > 0, fill, sr)
        out[n0:n1, m0:m1] = nm["A"] + nm["B"][..., None] * sr
        changed[n0:n1, m0:m1] = True
        # 5. our plate and strip
        acc_pre = np.zeros((r1 - r0, c1 - c0, 3), np.float32); acc_a = np.zeros((r1 - r0, c1 - c0, 1), np.float32)
        for name, wt in plates:
            p = self.a(name); acc_pre += p[..., :3] * wt; acc_a += p[..., 3:] / 255 * wt
        out[r0:r1, c0:c1] = out[r0:r1, c0:c1] * (1 - acc_a) + acc_pre
        changed[r0:r1, c0:c1] |= acc_a[..., 0] > 0.01
        for make, xc, mix, op in strip:
            spr = self.a(f"strip_{make}_S") * (1 - mix) + self.a(f"strip_{make}_C") * mix
            xa = int(round(xc - SW / 2)); xs0, xs1 = max(xa, x0), min(xa + SW, x1)
            if xs1 <= xs0 or op <= 0:
                continue
            sp = spr[:, xs0 - xa:xs1 - xa] * op
            out[SY0:SY1, xs0:xs1] = out[SY0:SY1, xs0:xs1] * (1 - sp[..., 3:] / 255) + sp[..., :3]
        out = np.where(changed[..., None], out, obs)
        return np.clip(np.nan_to_num(out), 0, 255).astype(np.uint8)


if __name__ == "__main__":
    c = Comp()
    car, src, ksrc, dst = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    makes = {"na": "mazda", "corolla": "toyota", "delsol": "honda", "frs": "scion"}
    plate = {"na": "plate_mazda", "corolla": "plate_corolla", "delsol": "plate_delsol", "frs": "plate_frs"}[car]
    im = c.compose(src, car, ksrc, [(plate, 1.0)], [("toyota", SLOT["L"], 0, 1), (makes[car], SLOT["C"], 1, 1), ("honda", SLOT["R"], 0, 1)])
    cv2.imwrite(dst, im)
