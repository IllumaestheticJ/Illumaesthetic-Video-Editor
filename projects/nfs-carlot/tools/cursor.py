"""Find the mouse cursor in every capture frame the reel uses, and build a cursor sprite.

    python projects/nfs-carlot/tools/cursor.py        -> $W/cursor/track.json, $W/cursor/sprite.png

The capture's own cursor cannot stay in the reel: the menu is cut from several ranges of the capture, so
the cursor jumps at every cut (user, v6 review: "the cursor arrow freaks out"). composite.py removes it
using this track and draws one cursor of its own on a continuous path.
"""
import json, sys
from pathlib import Path
import cv2, numpy as np

W = Path("/home/user/media/work/nfs-carlot")
OUT = W / "cursor"
REF = (5247, 1262, 766, 5236)           # cursor over a flat dark button: frame, x, y, and a frame with the same place empty
BOX = (46, 70)
OUTLINE_PX, OUTLINE_SOFT, OUTLINE_GREY = 7, 1.0, 22.0    # set by eye against real cursors over light backgrounds


def sprite(frame):
    """Cursor as BGRA: the white arrow measured from the capture, the dark outline rebuilt around it.

    Over a dark, flat background the white arrow's soft alpha is exact (p = a * white + (1 - a) * bg), but
    the dark-grey outline cannot be told from the background there. Solving both from two instances over
    different backgrounds was tried and failed on sub-pixel misalignment between them. So the outline is the
    arrow's shape grown by 3 px with a soft edge, which is what it is in the game."""
    f, x, y, fb = REF; w, h = BOX
    p = frame(f)[y:y + h, x:x + w].astype(np.float32).mean(2)
    b = frame(fb)[y:y + h, x:x + w].astype(np.float32).mean(2)
    af = np.clip((p - b) / (250.0 - b), 0, 1)
    af = np.where(af < 0.06, 0, af)
    n, lab, st, _ = cv2.connectedComponentsWithStats((af > 0.3).astype(np.uint8))
    big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    af *= cv2.dilate((lab == big).astype(np.uint8), np.ones((5, 5), np.uint8))
    grown = cv2.dilate((af > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (OUTLINE_PX, OUTLINE_PX)))
    ao = cv2.GaussianBlur(grown.astype(np.float32), (0, 0), OUTLINE_SOFT)
    alpha = np.maximum(ao, af)
    grey = 252.0 * af + OUTLINE_GREY * (1 - af)
    return np.dstack([grey, grey, grey, alpha * 255]).astype(np.uint8)


def main():
    OUT.mkdir(exist_ok=True)
    sys.path.insert(0, str(Path(__file__).parent))
    import composite as C
    cap = cv2.VideoCapture(str(W / C.VID))

    def frame(f):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = cap.read(); assert ok, f
        return im

    sp = sprite(frame)
    cv2.imwrite(str(OUT / "sprite.png"), sp)
    tmpl = cv2.cvtColor(sp[..., :3], cv2.COLOR_BGR2GRAY)
    mask = (sp[..., 3] > 128).astype(np.uint8) * 255
    frames = sorted({f for seg in C.SEGMENTS for f in seg[0]} | set(range(5204, 5266)))
    track, prev = {}, None
    for f in frames:
        g = cv2.cvtColor(frame(f), cv2.COLOR_BGR2GRAY)
        r = cv2.matchTemplate(g, tmpl, cv2.TM_CCOEFF_NORMED, mask=mask)
        r[~np.isfinite(r)] = -1
        _, s, _, (x, y) = cv2.minMaxLoc(r)
        # second-best away from the best: how unambiguous the find is
        r2 = r.copy(); r2[max(0, y - 30):y + 30, max(0, x - 30):x + 30] = -1
        track[f] = {"x": int(x), "y": int(y), "score": round(float(s), 3), "next": round(float(r2.max()), 3)}
    json.dump({"box": [sp.shape[1], sp.shape[0]], "track": track}, open(OUT / "track.json", "w"))
    last = None
    for f in frames:
        t = track[f]
        key = (t["x"] // 6, t["y"] // 6)
        if key != last or t["score"] < 0.8:
            print(f, t)
        last = key


if __name__ == "__main__":
    main()
