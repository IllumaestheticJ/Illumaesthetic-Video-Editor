"""Reverse-engineer a reference edit: shot boundaries, shot lengths, motion, brightness,
and a labelled thumbnail board an agent can look at.

This is how the system "learns" a house style: every reference reel we are told is good
gets analyzed, its numbers land in training/references/<name>.json, and a human/agent
writes the qualitative notes next to it (training/references/<name>.md).
"""
from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np


def _hist(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = cv2.calcHist([hsv], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
    return cv2.normalize(h, h).flatten()


def analyze(video: str, out_dir: str, threshold: float = 0.45, min_shot: float = 0.25) -> dict:
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    prev_h = prev_g = None
    cuts = [0]
    motion, bright = [], []
    frames_mid = {}
    i = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        small = cv2.resize(f, (160, int(160 * f.shape[0] / f.shape[1])))
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        h = _hist(small)
        bright.append(float(g.mean()))
        if prev_h is not None:
            d = cv2.compareHist(prev_h, h, cv2.HISTCMP_BHATTACHARYYA)
            m = float(np.mean(cv2.absdiff(g, prev_g)))
            motion.append(m)
            if d > threshold and (i - cuts[-1]) / fps >= min_shot:
                cuts.append(i)
        prev_h, prev_g = h, g
        frames_mid[i] = small
        i += 1
    cap.release()
    n = i
    cuts.append(n)
    shots = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        if b <= a:
            continue
        mid = (a + b) // 2
        shots.append({
            "start": round(a / fps, 3), "end": round(b / fps, 3), "dur": round((b - a) / fps, 3),
            "motion": round(float(np.mean(motion[a:b - 1] or [0])), 2),
            "brightness": round(float(np.mean(bright[a:b])), 1),
            "thumb_frame": mid,
        })
    durs = [s["dur"] for s in shots]
    stats = {
        "video": video, "fps": fps, "frames": n, "duration": round(n / fps, 2), "shots": len(shots),
        "avg_shot_s": round(float(np.mean(durs)), 2) if durs else 0,
        "median_shot_s": round(float(np.median(durs)), 2) if durs else 0,
        "shortest_s": min(durs) if durs else 0, "longest_s": max(durs) if durs else 0,
        "cuts_per_10s": round(10 * len(shots) / max(n / fps, 1e-6), 2),
        "mean_brightness": round(float(np.mean(bright)), 1),
        "shot_list": shots,
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for k, s in enumerate(shots):
        t = frames_mid[s["thumb_frame"]].copy()
        cv2.rectangle(t, (0, 0), (t.shape[1], 16), (0, 0, 0), -1)
        cv2.putText(t, f"{k+1} {s['start']:.1f}s {s['dur']:.2f}s", (2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
        tiles.append(t)
    if tiles:
        cols = 8
        h, w = tiles[0].shape[:2]
        rows = (len(tiles) + cols - 1) // cols
        board = np.zeros((rows * h, cols * w, 3), np.uint8)
        for k, t in enumerate(tiles):
            t = cv2.resize(t, (w, h))
            r, c = divmod(k, cols)
            board[r * h:(r + 1) * h, c * w:(c + 1) * w] = t
        stem = Path(video).stem
        cv2.imwrite(str(out / f"{stem}.shots.jpg"), board)
        stats["board"] = str(out / f"{stem}.shots.jpg")
    (out / f"{Path(video).stem}.json").write_text(json.dumps(stats, indent=2))
    return stats
