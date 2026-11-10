"""QA for the 1:1 match cut: does the scan render line up with the IRL frame?

Produces an onion-skin + edge overlay image and a numeric score (median distance in px
from the render's silhouette/feature edges to the nearest IRL edge). Agents must run
this before committing a match cut and record the score in the edit log.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def _edges(img: np.ndarray) -> np.ndarray:
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    g = cv2.GaussianBlur(g, (5, 5), 0)
    v = np.median(g)
    return cv2.Canny(g, int(max(0, 0.66 * v)), int(min(255, 1.33 * v + 40)))


def check(frame_path: str, render_path: str, out_path: str) -> dict:
    irl = cv2.imread(frame_path)
    ren = cv2.imread(render_path, cv2.IMREAD_UNCHANGED)
    if irl is None or ren is None:
        raise FileNotFoundError("could not read frame or render")
    h, w = irl.shape[:2]
    if ren.shape[:2] != (h, w):
        ren = cv2.resize(ren, (w, h), interpolation=cv2.INTER_AREA)
    if ren.shape[2] == 4:
        alpha = ren[:, :, 3]
        ren_bgr = ren[:, :, :3]
    else:
        ren_bgr = ren
        # opaque render: background = median of the four corners (scan looks use a dark grey bg)
        g = cv2.cvtColor(ren, cv2.COLOR_BGR2GRAY).astype(np.int16)
        bg = np.median([g[:8, :8], g[:8, -8:], g[-8:, :8], g[-8:, -8:]])
        alpha = (np.abs(g - bg) > 14).astype(np.uint8) * 255

    # Score on the render's outer silhouette only: interior scan edges (panel gaps, cracks)
    # and IRL background clutter both make interior-edge scores meaningless.
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 0).astype(np.uint8))
    if n > 1:
        biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        alpha = np.where(lab == biggest, 255, 0).astype(np.uint8)
    sil = cv2.morphologyEx(alpha, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    ren_e = (sil > 0).astype(np.uint8) * 255
    irl_e = _edges(irl)

    dist = cv2.distanceTransform(255 - irl_e, cv2.DIST_L2, 3)
    ys, xs = np.nonzero(ren_e)
    if len(xs) == 0:
        raise ValueError("render has no visible edges - is the scan in frame?")
    d = dist[ys, xs]
    scale = 1920 / max(w, h)  # report in px of a 1920-long-side frame
    med = float(np.median(d)) * scale
    p90 = float(np.percentile(d, 90)) * scale

    onion = cv2.addWeighted(irl, 0.5, ren_bgr, 0.5, 0)
    onion[irl_e > 0] = (0, 200, 255)   # IRL edges: orange
    onion[ren_e > 0] = (255, 255, 0)   # scan edges: cyan
    label = f"silhouette median {med:.1f}px p90 {p90:.1f}px (@1920 long side)  {verdict(med)}"
    cv2.putText(onion, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, max(0.6, w / 1920), (255, 255, 255), 2)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(out_path, onion)
    return {"median_edge_px_1080p": med, "p90_edge_px_1080p": p90, "verdict": verdict(med), "overlay": out_path}


def verdict(med: float) -> str:
    if med < 2.5:
        return "PASS: 1:1"
    if med < 6:
        return "SOFT: acceptable with a flash/scanline transition to hide it"
    return "FAIL: re-solve camera (add points spread across the frame and depth)"
