"""Plate / screen blur tracking for assemble_long.py.

    python track_blur.py grid <event> [frames...]          # graded frames with a 100 px grid -> build/blur/<event>_grid_*.jpg
    python track_blur.py track <event> <obj> f:x,y,w,h ...   # track the box from each keyframe (template match, both ways)
    python track_blur.py sheet <event>                       # every 4th frame with the boxes drawn -> build/blur/<event>_check.jpg
    python track_blur.py clear <event>

Coordinates are pre-crop source pixels (1920x1080; 1080x1920 for the rotated 545). Boxes are stored per source
frame in tools/blur_tracks.json, which assemble_long.py reads (and re-renders the segment when it changes).
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, str(Path(__file__).parent))
import assemble_long as al

TR = al.P / "tools/blur_tracks.json"
OUTD = al.B / "blur"


def ev(eid):
    d = json.load(open(al.B / "plan_internal.json"))
    return next(e for e in d["events"] if e["id"] == eid)


def frames(e, start=None, n=None):
    w, h = al.probe_wh(e["source"])
    vf = (["scale=1920:1080:flags=lanczos"] if (w, h) != (1920, 1080) else []) + ["format=rgb48le", f"lut3d=file={al.LUT}:interp=tetrahedral"]
    if e.get("rotate"):
        vf.append(f"transpose={e['rotate']}")
    vf.append("format=rgb24")
    ow, oh = (1080, 1920) if e.get("rotate") else (1920, 1080)
    s = e["src_start_f"] if start is None else start
    n = e["n"] if n is None else n
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{(s - 0.5) / al.FPS:.4f}", "-i", e["source"], "-frames:v", str(n), "-vf", ",".join(vf),
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    return [f.copy() for f in al.reader(cmd, ow, oh)]


def load():
    return json.load(open(TR)) if TR.exists() else {}


def save(d):
    al.atomic_json(TR, d)


def grid(eid, fl):
    e = ev(eid)
    fr = frames(e)
    idx = [int(x) - e["src_start_f"] for x in fl] if fl else [0, len(fr) // 2, len(fr) - 1]
    for i in idx:
        im = cv2.cvtColor(fr[i], cv2.COLOR_RGB2BGR)
        H, W = im.shape[:2]
        for x in range(0, W, 100):
            cv2.line(im, (x, 0), (x, H), (0, 255, 255) if x % 500 else (0, 0, 255), 1)
            cv2.putText(im, str(x), (x + 2, 20), 0, 0.6, (0, 255, 255), 2)
        for y in range(0, H, 100):
            cv2.line(im, (0, y), (W, y), (0, 255, 255) if y % 500 else (0, 0, 255), 1)
            cv2.putText(im, str(y), (2, y - 3), 0, 0.6, (0, 255, 255), 2)
        cv2.putText(im, f"{eid} src f{e['src_start_f'] + i}", (40, 60), 0, 1.4, (0, 255, 0), 3)
        cv2.imwrite(str(OUTD / f"{eid}_grid_{e['src_start_f'] + i}.jpg"), im, [cv2.IMWRITE_JPEG_QUALITY, 80])
        print(OUTD / f"{eid}_grid_{e['src_start_f'] + i}.jpg")


def track_from(gray, k, box, step):
    x, y, w, h = box
    out = {k: (x, y, w, h)}
    tpl = gray[k][int(y):int(y + h), int(x):int(x + w)].copy()
    i = k
    while 0 <= i + step < len(gray):
        i += step
        g = gray[i]
        R = 70
        x0, y0 = max(0, int(x - R)), max(0, int(y - R))
        x1, y1 = min(g.shape[1], int(x + w + R)), min(g.shape[0], int(y + h + R))
        win = g[y0:y1, x0:x1]
        if win.shape[0] <= tpl.shape[0] or win.shape[1] <= tpl.shape[1]:
            out[i] = (x, y, w, h); continue
        r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(r)
        if mx > 0.35:
            x, y = x0 + loc[0], y0 + loc[1]
            new = g[int(y):int(y + h), int(x):int(x + w)]
            if new.shape == tpl.shape:
                tpl = (0.7 * tpl + 0.3 * new).astype(np.uint8)
        out[i] = (x, y, w, h)
    return out


def track(eid, obj, keys):
    e = ev(eid)
    fr = frames(e)
    gray = [cv2.GaussianBlur(cv2.cvtColor(f, cv2.COLOR_RGB2GRAY), (3, 3), 0) for f in fr]
    kf = []
    for s in keys:
        f, b = s.split(":")
        kf.append((int(f) - e["src_start_f"], tuple(float(v) for v in b.split(","))))
    kf.sort()
    tracks = [(k, track_from(gray, k, b, +1), track_from(gray, k, b, -1)) for k, b in kf]
    boxes = []
    for i in range(len(fr)):
        left = [t for t in tracks if t[0] <= i]
        right = [t for t in tracks if t[0] >= i]
        cand = []
        if left:
            k, fw, _ = left[-1]; cand.append((i - k, fw[i]))
        if right:
            k, _, bw = right[0]; cand.append((k - i, bw[i]))
        if len(cand) == 2 and cand[0][0] + cand[1][0] > 0:
            (da, A), (db, Bb) = cand
            u = da / (da + db)
            b = tuple(A[j] * (1 - u) + Bb[j] * u for j in range(4))
        else:
            b = cand[0][1]
        boxes.append([e["src_start_f"] + i, round(b[0], 1), round(b[1], 1), round(b[2], 1), round(b[3], 1), obj])
    d = load()
    ent = d.setdefault(eid, {"boxes": [], "keys": {}})
    ent["boxes"] = [b for b in ent["boxes"] if b[5] != obj] + boxes
    ent["keys"][str(obj)] = keys
    save(d)
    sheet(eid, fr)


def sheet(eid, fr=None, a=None, b=None, step=4, div=4, cols=8):
    e = ev(eid)
    fr = fr or frames(e)
    bx = load().get(eid, {}).get("boxes", [])
    tiles = []
    lo = 0 if a is None else a - e["src_start_f"]
    hi = len(fr) if b is None else b - e["src_start_f"] + 1
    for i in range(lo, hi, step):
        im = fr[i].copy()
        for x, y, w, h in al.boxes_for(bx, e["src_start_f"] + i):
            im = al.apply_blur(im, [[x, y, w, h]])
            cv2.rectangle(im, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 2)
        im = cv2.resize(im, (im.shape[1] // div, im.shape[0] // div))
        cv2.putText(im, str(e["src_start_f"] + i), (5, 20), 0, 0.6, (0, 255, 0), 2)
        tiles.append(im)
    while len(tiles) % cols:
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[r:r + cols]) for r in range(0, len(tiles), cols)]
    out = OUTD / (f"{eid}_check.jpg" if a is None else f"{eid}_zoom_{a}_{b}.jpg")
    cv2.imwrite(str(out), cv2.cvtColor(np.vstack(rows), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 82])
    print(out)


if __name__ == "__main__":
    OUTD.mkdir(parents=True, exist_ok=True)
    cmd, eid = sys.argv[1], sys.argv[2]
    if cmd == "grid":
        grid(eid, sys.argv[3:])
    elif cmd == "track":
        track(eid, int(sys.argv[3]), sys.argv[4:])
    elif cmd == "sheet":
        sheet(eid)
    elif cmd == "zoom":  # zoom <event> a b step
        sheet(eid, None, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), 2, 3)
    elif cmd == "limit":  # limit <event> <obj> first last : keep boxes only in [first, last]
        d = load(); ob, a, b = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        d[eid]["boxes"] = [x for x in d[eid]["boxes"] if x[5] != ob or a <= x[0] <= b]
        d[eid].setdefault("limits", {})[str(ob)] = [a, b]; save(d)
    elif cmd == "clear":
        d = load(); d.pop(eid, None); save(d)
