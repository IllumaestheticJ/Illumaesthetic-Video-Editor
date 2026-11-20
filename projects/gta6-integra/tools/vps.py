"""Vanishing points of a capture frame -> focal length and camera rotation relative to the room.

    python projects/gta6-integra/tools/vps.py frame.png [--mask x0,y0,x1,y1 ...] [--debug out.jpg]

LSD line segments, RANSAC for the three dominant vanishing points, then the focal length from each
orthogonal pair (principal point assumed at the image centre, square pixels):  f^2 = -(v1-c).(v2-c).
"""
import argparse, json, sys
import cv2, numpy as np


def segments(img, masks, min_len):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lsd = cv2.createLineSegmentDetector(cv2.LSD_REFINE_ADV)
    L = lsd.detect(g)[0].reshape(-1, 4)
    keep = []
    for x0, y0, x1, y1 in L:
        if np.hypot(x1 - x0, y1 - y0) < min_len:
            continue
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        if any(a <= mx <= c and b <= my <= d for a, b, c, d in masks):
            continue
        keep.append((x0, y0, x1, y1))
    return np.array(keep, np.float64)


def line_h(S):
    p = np.c_[S[:, 0], S[:, 1], np.ones(len(S))]; q = np.c_[S[:, 2], S[:, 3], np.ones(len(S))]
    l = np.cross(p, q); return l / np.linalg.norm(l[:, :2], axis=1, keepdims=True)


def angle_to_vp(S, v):
    """Angle (deg) between each segment and the line from its midpoint to vanishing point v (homogeneous)."""
    m = np.c_[(S[:, 0] + S[:, 2]) / 2, (S[:, 1] + S[:, 3]) / 2]
    d = np.c_[S[:, 2] - S[:, 0], S[:, 3] - S[:, 1]]; d /= np.linalg.norm(d, axis=1, keepdims=True)
    if abs(v[2]) < 1e-12:
        t = np.tile(v[:2], (len(S), 1))
    else:
        t = v[:2] / v[2] - m
    t = t / (np.linalg.norm(t, axis=1, keepdims=True) + 1e-12)
    return np.degrees(np.arccos(np.clip(np.abs((d * t).sum(1)), 0, 1)))


def refine(S, idx):
    l = line_h(S[idx]); w = np.hypot(S[idx, 2] - S[idx, 0], S[idx, 3] - S[idx, 1])
    _, _, vt = np.linalg.svd(l * w[:, None]); return vt[-1]


def ransac_vp(S, rng, thr=1.2, iters=4000, weights=None):
    l = line_h(S); n = len(S); best = (0, None, None)
    w = np.hypot(S[:, 2] - S[:, 0], S[:, 3] - S[:, 1]) if weights is None else weights
    for _ in range(iters):
        i, j = rng.choice(n, 2, replace=False, p=w / w.sum())
        v = np.cross(l[i], l[j])
        if np.linalg.norm(v) < 1e-9:
            continue
        inl = angle_to_vp(S, v) < thr
        score = w[inl].sum()
        if score > best[0]:
            best = (score, v, inl)
    v = refine(S, np.where(best[2])[0]); inl = angle_to_vp(S, v) < thr
    v = refine(S, np.where(inl)[0]); inl = angle_to_vp(S, v) < thr
    return v, inl


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("frame"); ap.add_argument("--mask", action="append", default=[])
    ap.add_argument("--min-len", type=float, default=45); ap.add_argument("--debug"); ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    img = cv2.imread(a.frame); H, W = img.shape[:2]; c = np.array([W / 2, H / 2])
    masks = [tuple(float(v) for v in m.split(",")) for m in a.mask]
    S = segments(img, masks, a.min_len); rng = np.random.default_rng(a.seed)
    rest = np.ones(len(S), bool); vps = []; cols = [(0, 0, 255), (0, 255, 0), (255, 128, 0), (255, 0, 255)]
    dbg = (img * 0.45).astype(np.uint8)
    for k in range(4):
        idx = np.where(rest)[0]
        if len(idx) < 12: break
        v, inl = ransac_vp(S[idx], rng)
        vps.append((v, int(inl.sum()), float(np.hypot(S[idx][inl, 2] - S[idx][inl, 0], S[idx][inl, 3] - S[idx][inl, 1]).sum())))
        for x0, y0, x1, y1 in S[idx][inl]:
            cv2.line(dbg, (int(x0), int(y0)), (int(x1), int(y1)), cols[k], 3)
        rest[idx[inl]] = False
    out = []
    for v, n, ln in vps:
        p = (v[:2] / v[2]).tolist() if abs(v[2]) > 1e-9 else [float("inf")] * 2
        out.append({"vp": [round(p[0], 1), round(p[1], 1)], "segments": n, "length": round(ln)})
    print(json.dumps({"size": [W, H], "n_segments": len(S), "vps": out}))
    for i in range(len(vps)):
        for j in range(i + 1, len(vps)):
            vi, vj = vps[i][0], vps[j][0]
            if abs(vi[2]) < 1e-9 or abs(vj[2]) < 1e-9: continue
            f2 = -((vi[:2] / vi[2] - c) * (vj[:2] / vj[2] - c)).sum()
            print(f"  pair {i}-{j}: f = {np.sqrt(f2):.0f} px" if f2 > 0 else f"  pair {i}-{j}: not orthogonal (f^2 = {f2:.0f})")
    if a.debug:
        cv2.imwrite(a.debug, cv2.resize(dbg, (1600, int(1600 * H / W))))


if __name__ == "__main__":
    main()
