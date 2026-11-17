"""v0.8: track hand-placed part polygons through a 1080x1920 clip by chained frame-to-frame homographies
(LK optical flow on corners inside a region of interest around the part, RANSAC). Wheels are excluded so their
spin does not drag the fit.

    track.py frames_glob key_index poly_json roi_pad out.npy
"""
import glob, json, sys
import cv2
import numpy as np


def homs(frames, roi_masks):
    """H[i] maps frame i -> frame i+1; roi_masks[i] is a uint8 mask of where to take features in frame i."""
    out = []
    for i in range(len(frames) - 1):
        a, b = frames[i], frames[i + 1]
        p0 = cv2.goodFeaturesToTrack(a, 600, 0.005, 6, mask=roi_masks[i])
        p1, st, _ = cv2.calcOpticalFlowPyrLK(a, b, p0, None, winSize=(31, 31), maxLevel=4)
        pb, st2, _ = cv2.calcOpticalFlowPyrLK(b, a, p1, None, winSize=(31, 31), maxLevel=4)
        ok = (st[:, 0] == 1) & (st2[:, 0] == 1) & (np.linalg.norm(pb - p0, axis=2)[:, 0] < 1.0)
        H, inl = cv2.findHomography(p0[ok], p1[ok], cv2.RANSAC, 2.0)
        out.append(H)
    return out


def warp_poly(poly, H):
    p = np.array(poly, np.float32).reshape(-1, 1, 2)
    return cv2.perspectiveTransform(p, H).reshape(-1, 2)


def _roi(shape, poly, pad):
    """pad = (left/right, up, down) px around the polygon's bbox."""
    m = np.zeros(shape, np.uint8)
    px, pu, pd = (pad[0], pad[1], pad[1]) if len(pad) == 2 else pad
    x0, y0 = poly.min(0) - (px, pu)
    x1, y1 = poly.max(0) + (px, pd)
    cv2.rectangle(m, (int(max(0, x0)), int(max(0, y0))), (int(min(shape[1], x1)), int(min(shape[0], y1))), 255, -1)
    return m


def track_poly(gray, key, poly, pad=(40, 180)):
    """Polygon placed by hand on frame `key`, carried to every frame. Each step fits a homography to LK features
    in a box around the polygon's current position (pad = extra px left/right, up/down), so the part's own
    surface and the body panel next to it drive the fit, not the background. Falls back to the whole frame when
    the part has left it (it is then off screen and its mask does not matter)."""
    n = len(gray)
    polys = [None] * n
    polys[key] = np.array(poly, np.float32)
    for step in (1, -1):
        i = key
        while 0 <= i + step < n:
            p = polys[i]
            m = _roi(gray[i].shape, p, pad)
            if (m > 0).sum() < 4000:
                m[:] = 255
            try:
                H = homs([gray[i], gray[i + step]], [m])[0]
            except Exception:
                H = None
            polys[i + step] = warp_poly(p, H) if H is not None else p.copy()
            i += step
    return polys


def track_anchor(gray, key, poly, anchor, model="sim"):
    """Carry `poly` (a part) by the motion of `anchor` (a polygon around a well-textured, rigid region near the
    part, e.g. the trunk with emblem, plate and lamps). model "sim" = 4-dof similarity (stable when the anchor
    is small), "hom" = homography. Returns per-frame part polygons."""
    n = len(gray)
    P = [None] * n
    A = [None] * n
    P[key] = np.array(poly, np.float32)
    A[key] = np.array(anchor, np.float32)
    for step in (1, -1):
        i = key
        while 0 <= i + step < n:
            m = np.zeros(gray[i].shape, np.uint8)
            cv2.fillPoly(m, [A[i].astype(np.int32)], 255)
            a, b = gray[i], gray[i + step]
            p0 = cv2.goodFeaturesToTrack(a, 400, 0.005, 6, mask=m)
            p1, st, _ = cv2.calcOpticalFlowPyrLK(a, b, p0, None, winSize=(31, 31), maxLevel=4)
            pb, st2, _ = cv2.calcOpticalFlowPyrLK(b, a, p1, None, winSize=(31, 31), maxLevel=4)
            ok = (st[:, 0] == 1) & (st2[:, 0] == 1) & (np.linalg.norm(pb - p0, axis=2)[:, 0] < 1.0)
            if model == "sim":
                M, _ = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
                H = np.vstack([M, [0, 0, 1]])
            else:
                H, _ = cv2.findHomography(p0[ok], p1[ok], cv2.RANSAC, 2.0)
            P[i + step] = warp_poly(P[i], H)
            A[i + step] = warp_poly(A[i], H)
            i += step
    return P
