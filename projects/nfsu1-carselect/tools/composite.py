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
NATIVE_W = 0.92


class Comp:
    def __init__(self):
        # per menu state: the stat bars are different for every car, so the menu colour map is too
        self.AB = {k: (np.load(f"{WORK}/ui/A_{k}.npy"), np.load(f"{WORK}/ui/B_{k}.npy")[..., None]) for k in ("mazda", "dodge")}
        self.P = json.load(open(f"{WORK}/track/poses.json")); self.f = self.P["focal_px"]
        self.V, self.F, _ = sil.load_mesh(f"{WORK}/track/nb.npz")
        self.cap = cv2.VideoCapture(f"{WORK}/a60.mp4")
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

    def compose(self, src, car, kit_src, plates, strip, glare=True):
        """src: capture frame for the background; kit_src: which render of `car`;
        plates: [(name, weight)]; strip: [(make, x_centre, mix 0=side..1=centre, opacity)]."""
        obs = self.frame(src)
        A, B = self.AB["mazda" if src < FLIP_SRC else "dodge"]
        s = (obs - A) / B
        changed = np.zeros((H, W), bool)
        # 2a. native plate off
        r0, r1, c0, c1 = PL
        nat = self.a("plate_mazda" if src < FLIP_SRC else "plate_dodge_native")
        pre = nat[..., :3] * NATIVE_W; al = nat[..., 3:] / 255 * NATIVE_W
        s[r0:r1, c0:c1] = (s[r0:r1, c0:c1] - pre) / np.clip(1 - al, 0.3, 1)
        changed[r0:r1, c0:c1] |= al[..., 0] > 0.01
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
        K = self.kit(car, kit_src); Ka = K[..., 3:] / 255
        pose = self.P["frames"][str(src)] if str(src) in self.P["frames"] else self.P["hold"]
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
        return np.clip(out, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    c = Comp()
    car, src, ksrc, dst = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    makes = {"na": "mazda", "corolla": "toyota", "delsol": "honda", "frs": "scion"}
    plate = {"na": "plate_mazda", "corolla": "plate_corolla", "delsol": "plate_delsol", "frs": "plate_frs"}[car]
    im = c.compose(src, car, ksrc, [(plate, 1.0)], [("toyota", SLOT["L"], 0, 1), (makes[car], SLOT["C"], 1, 1), ("honda", SLOT["R"], 0, 1)])
    cv2.imwrite(dst, im)
