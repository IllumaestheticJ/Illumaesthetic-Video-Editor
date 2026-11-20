"""Move the camera until the MR2 covers the game's car (knowledge doc §2), keeping the part in frame and clear of the menu blocks.
    python tools/camsearch.py VIEW x y z heading pitch [free_pitch]   -> prints the best camera, writes test/cs_VIEW.jpg
Random local search on position (and heading +-10, pitch +-3 unless free) minimising the game car's uncovered pixels.
"""
import sys, json, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from silh import Geo, mancam, STOCK_HIDE, overlay
W = "/home/user/media/work/gta6-mr2-spyder/"
REF = {"M": "M", "H": "H", "T": "T2", "A": "A", "E": "E", "F": "F", "S": "S", "D": "S", "W": "W"}
PARTS = {"F": ["part_front_bumper", "part_eyelids"], "H": ["part_hood_vents"], "D": ["part_side_skirts"], "E": ["part_rear_spats", "part_diffuser"],
         "T": ["part_hardtop"], "A": ["part_duckbill"], "M": [], "S": ["wheel_FL"], "W": ["wheel_FL"]}
SAFE = (60, 185, 1930, 1040)          # where a part must sit: right of nothing, above the option block, left of the stats panel


def cost(g, mask, p, view, sc=0.125):
    cam = mancam(*p); s = g.mask(cam, [h for h in STOCK_HIDE if h not in PARTS[view]], sc) > 0
    m = mask; unc = (m & ~s).sum() / m.sum()
    LAM = float(__import__("os").environ.get("LAM", 0.25))
    pen = LAM * (s & ~m).sum() / m.sum()            # do not zoom in further than needed: car pixels outside the game car cost too
    edge = s[0].sum() + s[-1].sum() + s[:, 0].sum() + s[:, -1].sum()
    pen += 0.0 if view in ("W", "S", "D") else edge / 300.0        # whole car in frame for the full views
    for n in PARTS[view]:
        b = g.bbox(cam, n)
        if view == "W":                              # wheel close-up: our wheel on the game's wheel (centre 2027,1080, radius 267 px)
            t = (1760, 813, 2294, 1347); pen += sum(abs(a - c) for a, c in zip(b, t)) / 300.0
            continue
        over = max(0, SAFE[0] - b[0]) + max(0, SAFE[1] - b[1]) + max(0, b[2] - SAFE[2]) + max(0, b[3] - SAFE[3])
        pen += over / 400.0
    return unc + pen, unc


def main():
    view = sys.argv[1]; p0 = np.array(list(map(float, sys.argv[2:7]))); freep = len(sys.argv) > 7
    g = Geo(); z = np.load(W + "frames/masks0.npz"); mk = "S" if view == "D" else view
    mask = cv2.resize(z[mk], (320, 180), interpolation=cv2.INTER_NEAREST) > 0
    rng = np.random.default_rng(1); best = p0.copy(); bc, bu = cost(g, mask, best, view)
    sig = np.array([0.5, 0.5, 0.3, 5.0, 4.0 if freep else 1.0])
    lo = p0 - np.array([9, 9, 9, 12, 12 if freep else 3]); hi = p0 + np.array([9, 9, 9, 12, 12 if freep else 3]); lo[2] = max(lo[2], 0.25)
    for it in range(500):
        q = np.clip(best + rng.standard_normal(5) * sig * (0.25 + 0.75 * (1 - it / 500)), lo, hi)
        c, u = cost(g, mask, q, view)
        if c < bc:
            best, bc, bu = q, c, u
    print(view, "best", best.round(3).tolist(), "cost", round(bc, 4), "uncovered", round(bu, 4), "start", cost(g, mask, p0, view))
    cam = mancam(*best); fr = cv2.imread(W + f"frames/ref_{REF[view]}.png")
    o = overlay(fr, g.mask(cam, [h for h in STOCK_HIDE if h not in PARTS[view]], 0.5))
    cnt, _ = cv2.findContours(z[mk], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(o, cnt, -1, (0, 0, 255), 4)
    for n in PARTS[view]:
        b = list(map(int, g.bbox(cam, n))); cv2.rectangle(o, (b[0], b[1]), (b[2], b[3]), (255, 0, 255), 3)
    cv2.imwrite(W + f"test/cs_{view}.jpg", cv2.resize(o, (1280, 720)), [1, 80])
    json.dump(cam, open(Path(__file__).resolve().parents[1] / f"cam_{view}.json", "w"), indent=1)


if __name__ == "__main__":
    main()
