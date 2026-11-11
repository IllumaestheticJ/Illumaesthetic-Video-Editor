"""Track the car-lot turntable through a capture: per frame, how far the rest-position turntable has
slid (the game swaps cars by sliding the whole turntable out to the left and the next one in from the
right, about 2980 px apart on one conveyor, while the menu stays put).

    python projects/nfs-carlot/tools/track.py <a60.mp4> <E.png> <f0> <f1> <out.json>

E.png is the frame with the empty turntable at rest. Output: per frame {r: [dx, score], l: [dx, score]}
for the turntable's right and left rim tips (template matches along x), plus the list of transitions
(first moving frame, first frame back at rest).
"""
import json, sys
import cv2, numpy as np

Y0, Y1, XR0, XL0 = 870, 965, 1700, 170


def tracker(E):
    Eg = cv2.cvtColor(E, cv2.COLOR_BGR2GRAY)
    TR, TL = Eg[Y0:Y1, XR0:XR0 + 270], Eg[Y0:Y1, XL0:XL0 + 250]

    def track(F):
        Fg = cv2.cvtColor(F, cv2.COLOR_BGR2GRAY)[Y0:Y1]
        out = []
        for T, x0 in ((TR, XR0), (TL, XL0)):
            res = cv2.matchTemplate(Fg, T, cv2.TM_CCOEFF_NORMED)[0]
            i = int(np.argmax(res))
            out.append((i - x0, float(res[i])))
        return out
    return track


if __name__ == "__main__":
    vid, epath, f0, f1, outp = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    cap = cv2.VideoCapture(vid)
    track = tracker(cv2.imread(epath))
    cap.set(cv2.CAP_PROP_POS_FRAMES, f0)
    rows = {}
    for f in range(f0, f1):
        ok, F = cap.read()
        if not ok:
            break
        (dr, sr), (dl, sl) = track(F)
        rows[f] = {"r": [dr, round(sr, 3)], "l": [dl, round(sl, 3)]}
    rest = {f: (abs(v["r"][0]) < 14 and abs(v["l"][0]) < 14 and v["r"][1] > 0.9 and v["l"][1] > 0.9) for f, v in rows.items()}
    trans, cur = [], None
    for f in sorted(rows):
        if not rest[f] and cur is None:
            cur = f
        elif rest[f] and cur is not None:
            trans.append([cur, f]); cur = None
    json.dump({"frames": rows, "transitions": trans}, open(outp, "w"))
    for a, b in trans:
        first = next((rows[k]["r"][0] for k in range(a, b) if rows[k]["r"][1] > 0.55), 0)
        print(f"transition f{a}-{b}  t={a/60:.3f}-{b/60:.3f}  {b-a} frames  dir={'left' if first < 0 else 'right'}")
