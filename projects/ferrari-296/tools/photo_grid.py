"""Coarse grid for the website-photo camera when local search sticks (here: wheels 150 px off at a good IoU = yaw error
traded against framing). For each (azimuth, elevation, focal) the target/distance are corrected so the render's bbox
centre and width equal the photo's (pass 1 measures, pass 2 renders corrected), then candidates are ranked by
gradient NCC inside the car. Every pass is ONE Blender run (one candidate per frame).

    python3 projects/ferrari-296/tools/photo_grid.py <photo.jpg> <mask.png> <tag> Tx,Ty,Tz dist
"""
import itertools
import json
import math
import sys

import cv2
import numpy as np

from photo_search import OUTD, cam, render, biggest

import os
_g = lambda k, d: [float(v) for v in os.environ.get(k, d).split(",")]
AZ, EL, FOC = _g("AZ", "-58,-54,-50,-46,-42"), _g("EL", "22,26,30"), _g("FOC", "40,52")


def main():
    photo, mask, tag, T, dist = sys.argv[1:6]
    T = [float(v) for v in T.split(",")]
    dist = float(dist)
    tm_full = cv2.imread(mask, 0) > 127
    H, W = tm_full.shape
    pct = 25
    w, h = round(W * pct / 100), round(H * pct / 100)
    tm = cv2.resize(tm_full.astype(np.uint8), (w, h), interpolation=cv2.INTER_AREA) > 0
    ys, xs = np.nonzero(tm)
    pc, pw = np.array([(xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2]), xs.max() - xs.min()

    def grad(g):
        g = cv2.GaussianBlur(g.astype(np.float32), (0, 0), 1.2)
        m = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
        return cv2.GaussianBlur(m, (0, 0), 1.5)
    pg = grad(cv2.resize(cv2.imread(photo, 0), (w, h), interpolation=cv2.INTER_AREA))
    roi = cv2.dilate(tm.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    pv = pg[roi] - pg[roi].mean()

    grid = list(itertools.product(AZ, EL, FOC))
    cands = [np.array(T + [az, el, dist * f / 46.0, f]) for az, el, f in grid]
    for ps in range(2):
        files = render(cands, f"{tag}_g{ps}", W, H, pct)
        out = []
        for c, f in zip(cands, files):
            r = cv2.resize(cv2.imread(f, 0), (w, h), interpolation=cv2.INTER_AREA)
            m = biggest(r > 40)
            ys, xs = np.nonzero(m)
            rc, rw = np.array([(xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2]), xs.max() - xs.min()
            rg = grad(r)[roi]
            rv = rg - rg.mean()
            ncc = float((rv * pv).sum() / np.sqrt((rv * rv).sum() * (pv * pv).sum()))
            iou = (m & tm).sum() / (m | tm).sum()
            out.append((ncc, iou, c.copy()))
            # correction: move the target so the bbox centre lands on the photo's, scale distance by the width ratio
            loc, tgt, foc = cam(c)
            fwd = np.array(tgt) - np.array(loc)
            d = np.linalg.norm(fwd)
            fwd /= d
            right = np.cross(fwd, [0, 0, 1])
            right /= np.linalg.norm(right)
            up = np.cross(right, fwd)
            fx = foc / 36.0 * w
            dx, dy = (rc - pc) * d / fx  # render is right/down of the photo by (dx, dy) m at the target
            c[:3] = c[:3] + right * dx - up * dy
            c[5] = c[5] * rw / pw
        out.sort(key=lambda o: -o[0])
        print(f"pass {ps}:")
        for ncc, iou, c in out[:6]:
            print(f"  ncc {ncc:.4f} iou {iou:.3f} ->", ",".join(f"{v:.3f}" for v in c))
    best = out[0][2]
    loc, tgt, f = cam(best)
    json.dump({"loc": loc, "target": tgt, "focal": f, "sensor": 36.0, "ncc": out[0][0], "iou": out[0][1], "params": best.tolist()},
              open(f"{OUTD}/{tag}_best.json", "w"), indent=1)


if __name__ == "__main__":
    main()
