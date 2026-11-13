"""Search the camera that matches a website photo: each round renders 16 candidate cameras as 16 frames of ONE Blender run
(keys one frame apart, ease lin -> each frame is exactly one candidate), scores silhouette IoU against the photo mask,
keeps the best and shrinks the steps. Camera = target T + (azimuth, elevation, distance) + focal (36 mm sensor, width).

    python3 projects/ferrari-296/tools/photo_search.py <mask.png> <tag> Tx,Ty,Tz az el dist focal [--rounds 6] [--pct 15] [--photo photo.jpg (score gradient NCC, not IoU)]
"""
import json
import math
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots_v5 import BASE, PARTS, part  # noqa: E402
from shots import Z3, _k  # noqa: E402

OUTD = "/home/user/media/work/f296/web/fit"
N = 16


def cam(p):
    tx, ty, tz, az, el, dist, f = p
    a, e = math.radians(az), math.radians(el)
    loc = [tx + dist * math.cos(e) * math.cos(a), ty + dist * math.cos(e) * math.sin(a), tz + dist * math.sin(e)]
    return loc, [tx, ty, tz], f


def biggest(m):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
    return lab == 1 + np.argmax(st[1:, 4]) if n > 1 else m


def render(cands, tag, W, H, pct):
    keys = []
    for i, p in enumerate(cands):
        loc, tgt, f = cam(p)
        keys.append({"t": round(i / 15, 5), "loc": loc, "target": tgt, "focal": f, "ease": "lin"})
    out = f"{OUTD}/{tag}"
    for old in (os.path.join(out, x) for x in (os.listdir(out) if os.path.isdir(out) else [])):
        os.remove(old)
    sp = {"base": BASE, "parts": [part(n, [_k(0, Z3, Z3)], pv) for n, (pv, _) in PARTS.items()],
          "camera": {"sensor": 36.0, "keys": keys}, "seconds": len(cands) / 15, "fps": 15, "res": f"{W}x{H}",
          "res_pct": pct, "samples": 2, "out": out}
    p = f"{OUTD}/{tag}.json"
    json.dump(sp, open(p, "w"))
    subprocess.run(["blender", "-b", "-P", "projects/ferrari-296/tools/shot.py", "--", p], capture_output=True)
    return [f"{out}/f_{i + 1:04d}.png" for i in range(len(cands))]


def main():
    mask, tag = sys.argv[1:3]
    p0 = [float(v) for v in sys.argv[3].split(",")] + [float(v) for v in sys.argv[4:8]]
    rounds = int(sys.argv[sys.argv.index("--rounds") + 1]) if "--rounds" in sys.argv else 6
    pct = int(sys.argv[sys.argv.index("--pct") + 1]) if "--pct" in sys.argv else 15
    tm_full = cv2.imread(mask, 0) > 127
    H, W = tm_full.shape
    w, h = round(W * pct / 100), round(H * pct / 100)
    tm = cv2.resize(tm_full.astype(np.uint8), (w, h), interpolation=cv2.INTER_AREA) > 0

    photo = sys.argv[sys.argv.index("--photo") + 1] if "--photo" in sys.argv else None
    if photo:  # lesson (Sera, here too): IoU slid the car 40 px to trade off silhouette differences -> gradient NCC
        def grad(g):
            g = cv2.GaussianBlur(g.astype(np.float32), (0, 0), 1.2)
            m = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
            return cv2.GaussianBlur(m, (0, 0), 1.5)
        pg = grad(cv2.resize(cv2.imread(photo, 0), (w, h), interpolation=cv2.INTER_AREA))
        roi = cv2.dilate(tm.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        pv = pg[roi] - pg[roi].mean()

    def score(f):
        r = cv2.imread(f, 0)
        if r is None:
            return 0.0
        if photo:
            rg = grad(cv2.resize(r, (w, h), interpolation=cv2.INTER_AREA))[roi]
            rv = rg - rg.mean()
            return float((rv * pv).sum() / np.sqrt((rv * rv).sum() * (pv * pv).sum()))
        rm = biggest(cv2.resize(r, (w, h)) > 40)
        return (rm & tm).sum() / max(1, (rm | tm).sum())

    step = np.array([float(v) for v in os.environ.get("STEP", "0.08,0.08,0.06,3.0,2.5,0.5,6.0").split(",")])
    best, bs = np.array(p0), None
    rng = np.random.default_rng(1)
    for rd in range(rounds):
        cands = [best.copy()]
        for i in range(N - 1):
            d = np.zeros(7)
            if i < 14:  # +- each parameter
                d[i // 2] = step[i // 2] * (1 if i % 2 == 0 else -1)
            else:
                d = rng.normal(0, 0.5, 7) * step
            c = best + d
            if i // 2 == 6 and i < 14:  # focal change: keep the car the same size (dist scales with focal)
                c[5] = best[5] * c[6] / best[6]
            cands.append(c)
        files = render(cands, f"{tag}_r{rd}", W, H, pct)
        sc = [score(f) for f in files]
        k = int(np.argmax(sc))
        bs, best = sc[k], cands[k]
        print(f"round {rd}: base {sc[0]:.4f} best {bs:.4f} cand {k} ->", ",".join(f"{v:.3f}" for v in best), flush=True)
        step = step * (0.6 if k == 0 else 0.85)
    loc, tgt, f = cam(best)
    res = {"loc": loc, "target": tgt, "focal": f, "sensor": 36.0, "iou": bs, "params": best.tolist()}
    json.dump(res, open(f"{OUTD}/{tag}_best.json", "w"), indent=1)
    print(json.dumps(res))


if __name__ == "__main__":
    main()
