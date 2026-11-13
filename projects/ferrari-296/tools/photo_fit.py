"""Fit the locked (assembled) car to a website photo by eye + silhouette IoU: render one low-res still at the photo's
aspect from a candidate camera, score the silhouette against the photo mask, write an edge overlay.

    python3 projects/ferrari-296/tools/photo_fit.py <photo.jpg> <mask.png> <tag> lx,ly,lz tx,ty,tz focal [--pct 20]

Lesson (silfit.py on this car): the point-projection chamfer fit wandered off (noisy projected silhouette, ground slab in
car_6mm). A real Blender still of the exact end-of-drop scene (comp_v5 + all 9 parts home) is the honest judge.
Sensor 36 mm across the WIDTH (HORIZONTAL fit), so focal transfers to any output width at the same horizontal FOV.
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots_v5 import BASE, PARTS, part  # noqa: E402
from shots import Z3, _k  # noqa: E402

OUTD = "/home/user/media/work/f296/web/fit"


def main():
    photo, mask, tag, loc, tgt, focal = sys.argv[1:7]
    pct = int(sys.argv[sys.argv.index("--pct") + 1]) if "--pct" in sys.argv else 20
    im = cv2.imread(photo)
    H, W = im.shape[:2]
    os.makedirs(OUTD, exist_ok=True)
    sp = {"base": BASE, "parts": [part(n, [_k(0, Z3, Z3)], pv) for n, (pv, _) in PARTS.items()],
          "camera": {"sensor": 36.0, "keys": [{"t": 0, "loc": [float(v) for v in loc.split(",")],
                                                "target": [float(v) for v in tgt.split(",")], "focal": float(focal), "ease": "lin"}]},
          "seconds": 1 / 15, "fps": 15, "res": f"{W}x{H}", "res_pct": pct, "samples": 4, "out": f"{OUTD}/{tag}"}
    p = f"{OUTD}/{tag}.json"
    json.dump(sp, open(p, "w"), indent=1)
    subprocess.run(["blender", "-b", "-P", "projects/ferrari-296/tools/shot.py", "--", p], capture_output=True)
    r = cv2.imread(f"{OUTD}/{tag}/f_0001.png", 0)
    r = cv2.resize(r, (W, H))
    rm = r > 25
    tm = cv2.imread(mask, 0) > 127
    iou = (rm & tm).sum() / max(1, (rm | tm).sum())
    ov = im.copy()
    for m, col in ((tm, (0, 140, 255)), (rm, (255, 255, 0))):
        e = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)) > 0
        ov[e] = col
    cv2.imwrite(f"{OUTD}/{tag}_ov.jpg", cv2.resize(ov, (W // 3, H // 3)))
    ys, xs = np.nonzero(rm)
    print(f"{tag} IoU {iou:.3f} render bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} | photo mask bbox",
          cv2.boundingRect(tm.astype(np.uint8)))


if __name__ == "__main__":
    main()
