"""Green-screen meme cats -> keyed full-frame RGBA overlays (ProRes 4444 .mov in build/) + their audio on a separate stem.

    python projects/smart-450-hellkitten/tools/memes.py [--check]    # --check writes keyed 3-frame sheets to out/meme_check_<id>.png

Each clip is keyed with its OWN measured background colour (median of the frame border): distance in the CbCr plane + a luma term,
soft ramp -> alpha, 1 px erode + 1 px blur, despill (green capped at max(R, B) inside the matte fringe), then cropped to the union
bounding box, scaled to the target width and placed in a 1080x1920 transparent frame at (x, y) for the chosen time window.
"""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SM, FPS

SRC = Path(SM) / "memes" / "src"; BUILD = Path(SM) / "build"; OUT = Path(SM) / "out"
W, H = 1080, 1920
# id: dict(file, t0 (s into the clip), dur, width px on screen, x, y (top-left of the cropped cat), start_frame on the timeline, tol (key tolerance), audio_db or None)
# pos = (side, bottom y). Timeline frames: huh enters on m-3 and leaves on the drop (frame 45); oiia's spin starts (clip t 1.5 s) exactly on the
# body-off swap, frame 406; yapapa's first yell (audio onset 0.9 s into the clip) lands on the choir meow, T(44.5) = frame 547; clap runs m62..m64.
MEMES = {
    "huh": dict(file="huh_cat.mp4", t0=0.5, dur=1.1, width=340, pos=("right", 1690), start=12, tol=(26, 62), why="a confused cat next to the opening question 'THIS IS A SMART CAR?'"),
    "oiia": dict(file="oiiaoiia_cat.mp4", t0=1.2, dur=1.5, width=330, pos=("left", 1690), start=397, tol=(30, 70), why="the spin on the body-off swap (beat 32): the spin starts on the swap frame"),
    "yapapa": dict(file="yapapa_cat.mp4", t0=0.5, dur=1.7, width=400, pos=("left", 1690), start=535, tol=(30, 70), why="mouth open on the choir meow of the Hellkitten reveal (beat 44.5)"),
    "clap": dict(file="clapping_cat.mp4", t0=0.0, dur=101 / 30, width=440, pos=("right", 1690), start=744, tol=(30, 70), rim=True, retime=(3.5, 1.109, 79, 50),
                 why="approval clap after the long unimpressed meow, carried over the cut onto the logo card; claps retimed (x1.109, 2 beats per clap) so one lands on the logo downbeat (frame 767) and the next ones on beats 66, 68, 70; exit on beat 71 (frame 845)"),
}


def probe_wh(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip().split(",")
    return int(r[0]), int(r[1])


def gen_frames(path, t0, dur, scale_w=None):
    """stream frames (BGR) at 30 fps; one at a time (memory)."""
    sw, sh = probe_wh(path)
    vf = f"fps={FPS}" + (f",scale={scale_w}:-2" if scale_w else "")
    ow = scale_w or sw; oh = (int(round(sh * scale_w / sw)) // 2 * 2) if scale_w else sh
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-t", f"{dur:.4f}", "-i", str(path), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = ow * oh * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n: break
        yield np.frombuffer(buf, np.uint8).reshape(oh, ow, 3).copy()
    p.kill(); p.wait()


def one_frame(path, t):
    g = gen_frames(path, t, 0.1); f = next(g); g.close(); return f


def bg_colour(fr):
    b = np.concatenate([fr[:8].reshape(-1, 3), fr[-8:].reshape(-1, 3), fr[:, :8].reshape(-1, 3), fr[:, -8:].reshape(-1, 3)])
    return np.median(b, axis=0)


def key(fr, bg, tol):
    """returns BGRA float-free uint8 frame; alpha from CbCr distance to the measured background colour."""
    ycc = cv2.cvtColor(fr, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    bgy = cv2.cvtColor(np.uint8([[bg]]), cv2.COLOR_BGR2YCrCb).astype(np.float32)[0, 0]
    d = np.sqrt((ycc[..., 1] - bgy[1]) ** 2 + (ycc[..., 2] - bgy[2]) ** 2) + 0.15 * np.abs(ycc[..., 0] - bgy[0])
    a = np.clip((d - tol[0]) / (tol[1] - tol[0]), 0, 1)
    a = (a ** 1.0)
    a = cv2.erode(a, np.ones((3, 3), np.uint8)); a = cv2.GaussianBlur(a, (3, 3), 0.8)
    # despill: where the matte is partial or green dominates, cap G at max(R, B) (+ a little)
    b, g, r = [fr[..., i].astype(np.float32) for i in range(3)]
    lim = np.maximum(r, b)
    spill = np.clip(g - lim, 0, None)
    fringe = np.clip(1.5 - a * 1.5 + 0.0, 0, 1) * 0 + (a < 0.999)
    g2 = g - spill * np.clip(0.35 + 0.65 * (a < 0.98) + 0.35 * (spill > 18), 0, 1)
    out = np.dstack([b, g2, r]).clip(0, 255).astype(np.uint8)
    return np.dstack([out, (a * 255).astype(np.uint8)])


def build_overlay(mid, cfg):
    out = BUILD / f"meme_{mid}.mov"
    path = SRC / cfg["file"]; n = int(round(cfg["dur"] * FPS))
    bg = bg_colour(one_frame(path, cfg["t0"]))   # v6: measured at the clip in-point (the YouTube huh clip opens on a black frame)
    boxes = []
    sw, sh = probe_wh(path)
    for f in gen_frames(path, cfg["t0"], cfg["dur"], scale_w=240):
        k = key(f, bg, cfg["tol"]); ys, xs = np.where(k[..., 3] > 40)
        if len(xs): boxes.append((xs.min(), ys.min(), xs.max(), ys.max()))
    b = np.array(boxes); sc = sw / 240.0
    x0, y0 = int(max(b[:, 0].min() * sc - 6, 0)), int(max(b[:, 1].min() * sc - 6, 0)); x1, y1 = int(min(b[:, 2].max() * sc + 6, sw)), int(min(b[:, 3].max() * sc + 6, sh))
    cw, ch = x1 - x0, y1 - y0; tw = cfg["width"]; th = int(round(ch * tw / cw))
    px = 30 if cfg["pos"][0] == "left" else W - tw - 30; py = cfg["pos"][1] - th
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", str(out)], stdin=subprocess.PIPE)
    i = 0
    def prep(f):
        k = key(f, bg, cfg["tol"])[y0:y1, x0:x1]
        a = k[..., 3:4].astype(np.float32) / 255.0; rgb = k[..., :3].astype(np.float32) * a
        rgb = cv2.resize(rgb, (tw, th), interpolation=cv2.INTER_AREA); al = cv2.resize(a[..., 0], (tw, th), interpolation=cv2.INTER_AREA)
        col = np.where(al[..., None] > 1e-3, rgb / np.maximum(al[..., None], 1e-3), 0)
        if cfg.get("rim"):   # faint cool-grey outer glow so dark fur stays visible on a black card
            glow = np.clip(cv2.GaussianBlur(al, (0, 0), 4.0) * 1.8 - al * 1.0, 0, 1) * 0.95
            col = np.clip(col * 1.35 + 6, 0, 255)           # lift the black fur a little so it separates from the black card
            rc = np.array([225, 210, 205], np.float32)           # BGR
            col = (col * al[..., None] + rc * glow[..., None] * (1 - al[..., None])) / np.maximum(al + glow * (1 - al), 1e-3)[..., None]
            al = al + glow * (1 - al)
        return col.astype(np.float32), al.astype(np.float32)
    if cfg.get("retime"):
        base0, rate, wrap_at, wrap_by = cfg["retime"]
        cache = [prep(f) for j, f in zip(range(int(wrap_at) + 2), gen_frames(path, 0.0, (wrap_at + 2) / FPS))]
        for i in range(n):
            pos = base0 + rate * i
            while pos >= wrap_at: pos -= wrap_by
            j = int(np.floor(pos)); fr_ = pos - j
            c0, a0 = cache[j]; c1, a1 = cache[min(j + 1, len(cache) - 1)]
            col = c0 * (1 - fr_) + c1 * fr_; al = a0 * (1 - fr_) + a1 * fr_
            ramp = min(1.0, (i + 1) / 3.0, (n - i) / 3.0)
            frame = np.zeros((H, W, 4), np.uint8)
            frame[py:py + th, px:px + tw, :3] = col.clip(0, 255).astype(np.uint8); frame[py:py + th, px:px + tw, 3] = (al * 255 * ramp).clip(0, 255).astype(np.uint8)
            p.stdin.write(frame.tobytes())
        p.stdin.close(); p.wait()
        return dict(id=mid, file=cfg["file"], start_frame=cfg["start"], frames=n, crop=[x0, y0, x1, y1], screen=[px, py, tw, th], bg_bgr=bg.tolist(), why=cfg["why"])
    for f in gen_frames(path, cfg["t0"], cfg["dur"]):
        if i >= n: break
        k = key(f, bg, cfg["tol"])[y0:y1, x0:x1]
        # premultiplied resize to avoid green/dark halos
        a = k[..., 3:4].astype(np.float32) / 255.0; rgb = k[..., :3].astype(np.float32) * a
        rgb = cv2.resize(rgb, (tw, th), interpolation=cv2.INTER_AREA); al = cv2.resize(a[..., 0], (tw, th), interpolation=cv2.INTER_AREA)
        col = np.where(al[..., None] > 1e-3, rgb / np.maximum(al[..., None], 1e-3), 0)
        ramp = min(1.0, (i + 1) / 3.0, (n - i) / 3.0)         # 2-frame pop in / out on the beat
        frame = np.zeros((H, W, 4), np.uint8)
        frame[py:py + th, px:px + tw, :3] = col.clip(0, 255).astype(np.uint8); frame[py:py + th, px:px + tw, 3] = (al * 255 * ramp).clip(0, 255).astype(np.uint8)
        p.stdin.write(frame.tobytes()); i += 1
    p.stdin.close(); p.wait()
    return dict(id=mid, file=cfg["file"], start_frame=cfg["start"], frames=n, crop=[x0, y0, x1, y1], screen=[px, py, tw, th], bg_bgr=bg.tolist(), why=cfg["why"])


if __name__ == "__main__" and "--build" in sys.argv:
    info = [build_overlay(m, c) for m, c in MEMES.items() if (SRC / c["file"]).exists()]   # v6: clips the owner has not re-supplied yet are skipped
    print("memes missing:", [m for m, c in MEMES.items() if not (SRC / c["file"]).exists()])
    (BUILD / "memes.json").write_text(json.dumps(info, indent=1)); print(json.dumps(info))
    sys.exit(0)

if __name__ == "__main__":
    for mid, cfg in MEMES.items():
        path = SRC / cfg["file"]
        if not path.exists(): continue
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout)
        bg = bg_colour(one_frame(path, cfg["t0"]))
        tiles = []
        for q in (0.18, 0.5, 0.8):
            f = one_frame(path, dur * q); k = key(f, bg, cfg["tol"]); al = k[..., 3:4] / 255.0
            comp = (k[..., :3] * al + np.array([40, 0, 120]) * (1 - al)).astype(np.uint8)
            ys, xs = np.where(k[..., 3] > 20)
            if len(xs): comp = comp[max(ys.min() - 10, 0):ys.max() + 10, max(xs.min() - 10, 0):xs.max() + 10]
            tiles.append(cv2.resize(comp, (360, int(360 * comp.shape[0] / comp.shape[1]))))
        hh = max(t.shape[0] for t in tiles); sheet = np.zeros((hh, 360 * 3, 3), np.uint8)
        for j, t in enumerate(tiles): sheet[:t.shape[0], j * 360:(j + 1) * 360] = t
        cv2.imwrite(str(OUT / f"meme_check_{mid}.png"), sheet); print(mid, "bg BGR", bg, "->", OUT / f"meme_check_{mid}.png")
