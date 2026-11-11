"""Onion overlay: real frame + scan render (cyan edges of the render, 50/50 blend).
    python tools/onion.py frame.png render.png out.jpg [--width 1600]"""
import argparse, cv2, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("frame"); ap.add_argument("render"); ap.add_argument("out")
ap.add_argument("--width", type=int, default=1600); a = ap.parse_args()
f = cv2.imread(a.frame); r = cv2.imread(a.render)
r = cv2.resize(r, (f.shape[1], f.shape[0]))
s = a.width / f.shape[1]; f = cv2.resize(f, None, fx=s, fy=s); r = cv2.resize(r, None, fx=s, fy=s)
g = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY); e = cv2.Canny(g, 40, 120)
blend = cv2.addWeighted(f, 0.55, r, 0.45, 0); edge = f.copy(); edge[e > 0] = (255, 255, 0)
cv2.imwrite(a.out, np.hstack([blend, edge]) if f.shape[1] < f.shape[0] else np.vstack([blend, edge]))
