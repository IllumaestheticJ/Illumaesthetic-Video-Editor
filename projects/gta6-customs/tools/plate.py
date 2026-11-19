"""Clean plate helpers: fill the parts of the game's car that our car does not cover.

fill_directional(img, hole, vp): each hole pixel takes the pixel found by walking from it toward a vanishing
point until it leaves the hole, and then as far again (a mirror about the hole's edge, along the scene's own
perspective lines). Floor joints, the door's sun line and kerbs run toward the room's vanishing points, so
they carry on straight through the fill; ordinary inpainting smeared them (tried: Telea, FSR).
"""
import cv2, numpy as np


def fill_directional(img, hole, vp, margin=6, max_steps=900):
    H, W = hole.shape
    out = img.astype(np.float32).copy()
    ys, xs = np.nonzero(hole)
    px = np.stack([xs, ys], 1).astype(np.float32)
    d = np.array(vp, np.float32)[None] - px
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    s = np.zeros(len(px), np.float32); done = np.zeros(len(px), bool)
    grown = cv2.dilate(hole.astype(np.uint8), np.ones((2 * margin + 1, 2 * margin + 1), np.uint8)) > 0
    for step in range(1, max_steps):
        q = px + d * step
        qi = np.round(q).astype(int)
        inside = (qi[:, 0] >= 0) & (qi[:, 0] < W) & (qi[:, 1] >= 0) & (qi[:, 1] < H)
        free = np.zeros(len(px), bool)
        free[inside] = ~grown[qi[inside, 1], qi[inside, 0]]
        new = free & ~done
        s[new] = step; done |= new
        if done.all():
            break
    src = px + d * (2 * s[:, None] + 1)
    sx = np.clip(src[:, 0], 0, W - 1); sy = np.clip(src[:, 1], 0, H - 1)
    xi, yi = np.round(sx).astype(int), np.round(sy).astype(int)
    samp = img.astype(np.float32)[yi, xi]
    ok = done & ~grown[np.round(sy).astype(int), np.round(sx).astype(int)]
    out[ys[ok], xs[ok]] = samp[ok]
    left = np.zeros((H, W), np.uint8); left[ys[~ok], xs[~ok]] = 255
    res = np.clip(out, 0, 255).astype(np.uint8)
    if left.any():
        res = cv2.inpaint(res, left, 5, cv2.INPAINT_TELEA)
    # soften the seam
    edge = cv2.dilate(hole.astype(np.uint8), np.ones((5, 5), np.uint8)) - cv2.erode(hole.astype(np.uint8), np.ones((5, 5), np.uint8))
    blur = cv2.GaussianBlur(res, (0, 0), 1.5)
    res[edge > 0] = blur[edge > 0]
    return res


def fill_nearest(img, hole, vps, margin=6, block=None):
    """Like fill_directional, but each hole pixel uses whichever of several directions leaves the hole soonest.
    For a car seen from behind: left of it take the floor from the left, right from the right, under its
    bumper from in front of the camera."""
    H, W = hole.shape
    ys, xs = np.nonzero(hole)
    px = np.stack([xs, ys], 1).astype(np.float32)
    # block: everything that must not be sampled (the whole game car, also where our car will hide it); a walk
    # only ends, and only samples, outside it. Without it the fill mirrored the game car's own tailgate.
    grown = cv2.dilate((hole if block is None else (block | hole)).astype(np.uint8), np.ones((2 * margin + 1, 2 * margin + 1), np.uint8)) > 0
    best_s = np.full(len(px), 1e9, np.float32); best_src = np.zeros((len(px), 2), np.float32)
    for vp in vps:
        d = np.array(vp, np.float32)[None] - px
        d /= np.linalg.norm(d, axis=1, keepdims=True)
        s = np.full(len(px), 1e9, np.float32); done = np.zeros(len(px), bool)
        for step in range(1, 1200):
            qi = np.round(px + d * step).astype(int)
            inside = (qi[:, 0] >= 0) & (qi[:, 0] < W) & (qi[:, 1] >= 0) & (qi[:, 1] < H)
            free = np.zeros(len(px), bool); free[inside] = ~grown[qi[inside, 1], qi[inside, 0]]
            new = free & ~done; s[new] = step; done |= new
            if done.all(): break
        src = px + d * (2 * s[:, None] + 1)
        ok = done & (src[:, 0] >= 0) & (src[:, 0] < W - 1) & (src[:, 1] >= 0) & (src[:, 1] < H - 1)
        ok[ok] &= ~grown[np.round(src[ok, 1]).astype(int), np.round(src[ok, 0]).astype(int)]
        better = ok & (s < best_s)
        best_s[better] = s[better]; best_src[better] = src[better]
    out = img.copy()
    got = best_s < 1e8
    out[ys[got], xs[got]] = img[np.round(best_src[got, 1]).astype(int), np.round(best_src[got, 0]).astype(int)]
    left = np.zeros((H, W), np.uint8); left[ys[~got], xs[~got]] = 255
    if left.any():
        out = cv2.inpaint(out, left, 5, cv2.INPAINT_TELEA)
    soft = cv2.GaussianBlur(out, (0, 0), 2.0)                     # take the mirrored grain down a little and hide the seams
    w = cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 3)[..., None] * 0.6
    return (out * (1 - w) + soft * w).astype(np.uint8)
