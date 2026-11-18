"""Pip & Gus Ep 6 (SeamForged) full build: cartoon (rendered frames; real slicer clips pinned on the laptop screen in S1/S2,
the SeamForged capture pinned on the phone screen in S7), the SeamForged screen capture with Gus's and Pip's voice-over
(B1 cut, B2 numbers, B3 plates, B4 the printed piece), the "SEAMFORGED / COMING SOON" app card, the logo card with Pip's
voice-only line 10, captions (word by word, cartoon only), music and dialogue mix. Adapted from Ep 7's tools/ep7_build.py.

    python projects/pip-gus-ep6-seamforge/tools/ep6_build.py [--name pip_gus_ep6_v1]

Resumable: cached steps in BUILD (clips, gfx_<hash>.mov, cartoon.mp4, video.mp4, mix). Delete a file to redo that step.

Timeline (frames, 30 fps): cartoon 0-576 (S7's last frame = phone screen full frame) | B1 577 (music lift = bass entry,
bar 8 downbeat) 4 beats | B2 5 beats | B3 5 beats | B4 6 beats | app card 6 beats | logo (Pip's line 10 voice-only; final
chord bar 16 = 108 frames in; 1.2 s ring-out). Beat = 18 frames (100 BPM).
Music: the series bed (pilot's ElevenLabs Music v2.5 job 077bbd23 = "inquisitive_A"), intro stretched with the pilot's
measured seamless 2-bar back-jumps (beats 10->2, 14->6, 30->22) so the lift lands on frame 577; no jump after the lift (the
32 beats from lift to final chord = Part B + card + 6 beats of logo exactly).
Screen capture: SeamForge v1.46.0 (a807c0a) on the GR86 rear bumper, recorded under Xvfb with software GL (slow: Auto-Slice
and engraving take minutes there), so long waits are shown as visible time-lapse (sped-up orbit), never as a hidden cut.
The capture's viewport is cropped 1080x1920 at (289, 52): no window title, no printer-brand panel, no file name.
"""
import argparse, hashlib, json, subprocess, sys, wave
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
W_ = Path("/home/user/media/work/ep6")
MEDIA = Path("/home/user/media/pip-gus-ep6-seamforge")
DROP = MEDIA / "dropbox"
CAP = MEDIA / "capture/run4"
BUILD = W_ / "build"
FRAMES = W_ / "frames"
OUTD = W_ / "out"
PROC = W_ / "voice/proc"
W, H, FPS, SR = 1080, 1920, 30, 48000
TL = json.loads((PROJ / "ep6_timeline.json").read_text())
A_N = TL["total_frames"]
BEATF = 18
SEG_BEATS = [("B1", 4), ("B2", 5), ("B3", 5), ("B4", 6), ("card", 6)]
CUTS, _f = {}, A_N
for _k, _b in SEG_BEATS:
    CUTS[_k] = _f
    _f += _b * BEATF
CUTS["logo"] = _f
CUTS["end"] = _f + 6 * BEATF + 36            # final chord 6 beats into the logo card, 1.2 s ring-out
VO_LEAD = 5                                  # frames from a Part B segment start to its voice-over line
VO10_AT = CUTS["logo"] + 8
CROP = (1080, 1904, 289, 80)                 # SeamForge viewport inside the 1640x2040 capture (27 px Xvfb menu bar + 48 px app bar above)
LAPTOP_CLIP = dict(src=DROP / "laptop_A_manualcut.mp4", t0=0.0)   # S1 bumper over the bed + error toast, S2 manual cut
B4_SRC = MEDIA / "printed_piece.mp4"         # owner's GR86 printed piece (pending); fallback: exploded close-up
WIN = dict(x=110, y=700, w=860, h=645, r=30, border=5)
BRAND = dict(accent="#619f73", onAccent="#0b0c0b", ink="#ecefec", bg="#0b0c0b", sub="#c8ccc8", sub2="#aeb3ae", label="#aeb3ae")
CAPC = dict(PIP="#619f73", GUS="#ecefec")
TRACK = W_ / "music/inquisitive_A.mp3"
BEAT0, BEAT = 0.0203, 0.60001
LIFT_BEAT, JUMPS, XF = 32, [(10, 2), (14, 6), (30, 22)], 0.008
FINAL_BEAT = 64


def bt(k):
    return BEAT0 + k * BEAT


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def nframes(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def frames_of(path, w, h):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE,
                         bufsize=10 ** 8)
    while True:
        b = p.stdout.read(w * h * 3)
        if len(b) < w * h * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.stdout.close(); p.wait()


ENC = ["-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-colorspace", "bt709", "-an"]


# ------------------------------------------------------------------ Part B clips from the screen capture
def ev():
    return {e["name"]: e for e in json.loads((CAP / "events.json").read_text())}


def vf_crop(zoom=1.0, cy=0.5, cx=0.5):
    """Viewport crop, optional centred zoom (cy = vertical centre as a fraction), to 1080x1920 (1904 -> 1920 by a 0.8 % scale)."""
    w, h, x, y = CROP
    zw, zh = int(w / zoom) // 2 * 2, int(h / zoom) // 2 * 2
    zx, zy = x + int(min(max(w * cx - zw / 2, 0), w - zw)), y + int(min(max(h * cy - zh / 2, 0), h - zh))
    return f"crop={zw}:{zh}:{zx}:{zy},scale=1090:1920:flags=lanczos,crop=1080:1920:5:0"


def capture_piece(out, pieces, n_total, zoom=1.0, cy=0.5, cx=0.5):
    """pieces: [(t_src0, t_src1, n_frames)] from session.mp4, each retimed to n_frames (setpts), concatenated, cropped."""
    if out.exists() and nframes(out) == n_total:
        return out
    parts = []
    for i, (a, b, n) in enumerate(pieces):
        pp = BUILD / f"_{out.stem}_{i}.mp4"
        speed = (b - a) / (n / FPS)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(CAP / "session.mp4"), "-vf",
             f"{vf_crop(zoom, cy, cx)},setpts=PTS/{speed:.5f},fps={FPS}", "-frames:v", str(n)] + ENC + [str(pp)])
        parts.append(pp)
    lst = BUILD / f"_{out.stem}.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-frames:v", str(n_total)] + ENC + [str(out)])
    for p in parts:
        p.unlink()
    lst.unlink()
    assert nframes(out) == n_total, (out, nframes(out), n_total)
    return out


def clips():
    BUILD.mkdir(parents=True, exist_ok=True)
    e = ev()
    n = {k: CUTS[nx] - CUTS[k] for k, nx in (("B1", "B2"), ("B2", "B3"), ("B3", "B4"), ("B4", "card"))}
    out = {}
    s7 = [s for s in TL["shots"] if s["id"] == "S7"][0]
    n_phone = A_N - s7["f0"]
    # B1 (incl. the phone part of S7): the uncut bumper orbiting at real speed, then the slicing as a visible time-lapse
    # (planes appear, pieces colour up), then the cut result at real speed
    c = e["autoslice_click"]["t"]
    s = e["sliced"]["t"]
    nb1 = n_phone + n["B1"]
    tl_n = 45                                 # time-lapse frames for the minutes of slicing
    pre = 50
    post = nb1 - pre - tl_n
    out["B1"] = capture_piece(BUILD / "b1.mp4", [(c - pre / FPS, c, pre), (c, s, tl_n), (s, s + post / FPS, post)], nb1,
                              zoom=1.3, cy=0.42, cx=0.42)
    out["phone_frames"] = n_phone
    # B2: numbers: the explode slider pulling the pieces apart (time-lapse of the engraving first)
    x0, x1, xe = e["explode_start"]["t"], e["explode_end"]["t"], e["explode_hold_end"]["t"]
    out["B2"] = capture_piece(BUILD / "b2.mp4", [(e["engrave_click"]["t"], e["engraved"]["t"], 14), (x0, x1, n["B2"] - 14 - 40),
                                                  (x1, x1 + 40 / FPS, 40)], n["B2"], zoom=1.35, cy=0.5)
    # B3: plates: Plan plates (time-lapse of the planning), then the beds orbiting
    p0, p1, pe = e["plan_click"]["t"], e["planned"]["t"], e["plates_hold_end"]["t"]
    out["B3"] = capture_piece(BUILD / "b3.mp4", [(p1 + 22.5, p1 + 22.5 + n["B3"] / FPS, n["B3"])], n["B3"], zoom=1.5, cy=0.53, cx=0.47)
    # (the plates view renders black for ~22 s after planning on this machine: the clip starts when the beds are drawn)
    # B4: the owner's printed piece when it arrives; until then the exploded pieces, held (numbers on the mating faces)
    if B4_SRC.exists():
        p = BUILD / "b4.mp4"
        if not (p.exists() and nframes(p) == n["B4"]):
            run(["ffmpeg", "-v", "error", "-y", "-i", str(B4_SRC), "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                 "-frames:v", str(n["B4"])] + ENC + [str(p)])
        out["B4"], out["B4_kind"] = p, "printed piece"
    else:
        out["B4"] = capture_piece(BUILD / "b4_fallback.mp4", [(xe - n["B4"] / FPS, xe, n["B4"])], n["B4"], zoom=2.0, cy=0.5)
        out["B4_kind"] = "fallback: exploded pieces held (owner footage pending)"
    # app card window: exploded pieces
    p = BUILD / "card_win.mp4"
    nc = CUTS["logo"] - CUTS["card"]
    if not (p.exists() and nframes(p) == nc):
        w, h, x, y = CROP
        cw = 760
        ch = int(cw * WIN["h"] / WIN["w"]) // 2 * 2
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{x1:.3f}", "-i", str(CAP / "session.mp4"), "-vf",
             f"crop={cw}:{ch}:{x + (w - cw) // 2}:{y + (h - ch) // 2},scale={WIN['w']}:{WIN['h']}:flags=lanczos,fps={FPS},format=yuv444p",
             "-frames:v", str(nc)] + [e if e != "yuv420p" else "yuv444p" for e in ENC] + [str(p)])
    out["card"] = p
    # laptop insert (S1+S2), 1200x800 -> fills the 0.42x0.27 screen (corner-pinned)
    out["laptop"] = LAPTOP_CLIP["src"]
    return out


# ------------------------------------------------------------------ cartoon (rendered frames + screen composites)
def key_comp(img, foot, quad):
    fh, fw = foot.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [fw, 0], [fw, fh], [0, fh]]), np.float32(quad))
    warp = cv2.warpPerspective(foot, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    f = img.astype(np.float32)
    mag = np.minimum(f[..., 0], f[..., 2]) - f[..., 1]
    m = np.clip((mag - 40) / 80, 0, 1)[..., None]
    spill = mag > 15
    f[spill, 0] = np.minimum(f[spill, 0], f[spill, 1] + 8)
    f[spill, 2] = np.minimum(f[spill, 2], f[spill, 1] + 8)
    return (f * (1 - m) + warp * m).clip(0, 255).astype(np.uint8)


def cartoon(cl):
    p = BUILD / "cartoon.mp4"
    if p.exists() and nframes(p) == A_N:
        return p
    corn = json.loads((FRAMES / "screen_corners.json").read_text())["shots"]
    lap = frames_of(cl["laptop"], 1200, 800)
    lap_last = None
    b1 = frames_of(cl["B1"], W, H)
    tmp = BUILD / "cartoon_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r",
                            str(FPS), "-i", "-"] + ENC + [str(tmp)], stdin=subprocess.PIPE)
    for s in TL["shots"]:
        for fr in range(s["f0"], s["f1"]):
            im = cv2.imread(str(FRAMES / s["id"] / f"{fr:04d}.png"), cv2.IMREAD_COLOR)
            assert im is not None, (s["id"], fr)
            img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            if s["id"] in ("S1", "S2"):
                lap_last = next(lap, lap_last)
                q = corn.get(s["id"], {}).get("per_frame", {}).get(str(fr))
                if q:
                    img = key_comp(img, lap_last, q)
            if s["id"] == "S7":
                foot = next(b1)
                q = corn["S7"]["per_frame"].get(str(fr))
                if fr == A_N - 1:
                    img = foot
                elif q:
                    img = key_comp(img, foot, q)
            enc.stdin.write(np.ascontiguousarray(img).tobytes())
    enc.stdin.close(); enc.wait()
    assert nframes(tmp) == A_N
    tmp.rename(p)
    return p


# ------------------------------------------------------------------ captions + cards (Remotion ExplainerGfx)
def caption_tokens(L):
    toks = L["text"].split()
    ws = L["words"]
    if len(toks) != len(ws):
        toks = [L["text"]]
        ws = ws[:1]
    return [dict(w=t.lstrip("."), t0=round(w["t0"], 3)) for t, w in zip(toks, ws)]


def screen_rect(fr):
    corn = json.loads((FRAMES / "screen_corners.json").read_text())["shots"]
    for sid in ("S1", "S2", "S7"):
        c = corn.get(sid, {}).get("per_frame", {}).get(str(fr))
        if c:
            xs, ys = [p[0] for p in c], [p[1] for p in c]
            return min(xs), min(ys), max(xs), max(ys)
    return None


SIZE = 80
Y_RANGE = (300, 1500)


def box_of(p, y):
    n = max(len(" ".join(w["w"] for w in ln)) for ln in p["lines"])
    w = n * SIZE * 0.42 + 2 * SIZE * 0.3 + 52
    h = len(p["lines"]) * SIZE * 1.12 + 22
    return int(540 - w / 2), int(y - h / 2), int(540 + w / 2), int(y + h / 2)


def pages():
    out = []
    lines = TL["lines"]
    for i, L in enumerate(lines):
        toks = caption_tokens(L)
        sents, cur = [], []
        for t in toks:
            cur.append(t)
            if t["w"].endswith((".", "?", "!")):
                sents.append(cur); cur = []
        if cur:
            sents.append(cur)
        merged = []
        for s in sents:
            if merged and len(merged[-1]) + len(s) <= 4 and len(merged[-1]) <= 1:
                merged[-1] = merged[-1] + s
            else:
                merged.append(s)
        nxt = lines[i + 1]["t0"] if i + 1 < len(lines) else A_N / FPS
        for k, s in enumerate(merged):
            t0 = s[0]["t0"]
            t1 = merged[k + 1][0]["t0"] if k + 1 < len(merged) else min(L["t1"] + 0.3, nxt - 0.02)
            ln = [s[:(len(s) + 1) // 2], s[(len(s) + 1) // 2:]] if len(s) > 3 else [s]
            out.append(dict(t0=round(t0, 3), t1=round(t1, 3), color=CAPC[L["speaker"]], y=1330, cx=540, lines=ln))
    place(out)
    return out


def place(pages_):
    """One caption height per shot where the rendered frames are quietest (fewest edges); never over a screen."""
    shots = TL["shots"]
    cache = {}

    def dark(fr):
        if fr not in cache:
            sid = [s["id"] for s in shots if s["f0"] <= fr < s["f1"]][0]
            im = cv2.imread(str(FRAMES / sid / f"{fr:04d}.png"), cv2.IMREAD_GRAYSCALE)
            e = cv2.Canny(cv2.GaussianBlur(im, (5, 5), 0), 40, 110)
            cache[fr] = cv2.dilate(e, np.ones((9, 9), np.uint8)).astype(np.float32) / 255.0
        return cache[fr]

    for s in shots:
        ps = [p for p in pages_ if s["f0"] <= int(round(p["t0"] * FPS)) < s["f1"]]
        if not ps:
            continue
        best = None
        for y in range(Y_RANGE[0], Y_RANGE[1] + 1, 20):
            sc, bad = 0.0, False
            for p in ps:
                x0, y0, x1, y1 = box_of(p, y)
                if y0 < Y_RANGE[0] - 80 or y1 > Y_RANGE[1] + 80:
                    bad = True
                    break
                for fr in range(int(round(p["t0"] * FPS)), min(int(round(p["t1"] * FPS)), A_N), 3):
                    sc += float(dark(fr)[y0:y1, max(0, x0):min(W, x1)].mean())
                    r = screen_rect(fr)
                    if r and not (y0 > r[3] + 12 or y1 < r[1] - 12) and fr != A_N - 1:
                        bad = True
            if bad:
                continue
            sc += 0.00002 * abs(y - 1330)
            if best is None or sc < best[0]:
                best = (sc, y)
        assert best, ("no clear caption height", s["id"])
        for p in ps:
            p["y"] = best[1]
        print(f"[captions] {s['id']}: y {best[1]} (dark {best[0]:.4f})", flush=True)
    for p in pages_:
        assert int(round(p["t1"] * FPS)) <= A_N - 1, "caption must end before the screen fills the frame"


def props():
    c0, b = CUTS["card"] / FPS, BEAT
    items = [{"kind": "teaser", "t0": c0, "t1": CUTS["logo"] / FPS,
              "lines": [{"text": "SEAMFORGED", "at": c0}, {"text": "COMING SOON", "at": c0 + 2 * b}],
              "sub": {"lines": [], "at": c0}, "win": dict(WIN, at=c0)},
             {"kind": "logo", "t0": CUTS["logo"] / FPS, "t1": CUTS["end"] / FPS + 1, "cta": ""}]
    return {"fps": FPS, "durationInFrames": CUTS["end"], "items": items, "pages": pages(), "palette": BRAND, "size": SIZE}


def gfx():
    js = json.dumps(props(), indent=1)
    (PROJ / "gfx_props.json").write_text(js)
    h = hashlib.sha1((js + (REPO / "remotion/src/gfx/reel/ExplainerGfx.tsx").read_text() + (REPO / "remotion/src/gfx/reel/ReelGfx.tsx").read_text()).encode()).hexdigest()[:10]
    mov = BUILD / f"gfx_{h}.mov"
    if not mov.exists():
        pj = BUILD / "gfx_props.json"; pj.write_text(js)
        tmp = BUILD / f"tmp_gfx_{h}.mov"
        run(["nice", "-n", "5", "npx", "remotion", "render", "ExplainerGfx", str(tmp), f"--props={pj}", "--codec=prores", "--prores-profile=4444",
             "--pixel-format=yuva444p10le", "--image-format=png", "--concurrency=2", "--log=error"], cwd=REPO / "remotion")
        tmp.rename(mov)
    return mov


# ------------------------------------------------------------------ picture
def picture(cl, cart, gmov):
    vid = BUILD / "video.mp4"
    if vid.exists() and nframes(vid) == CUTS["end"]:
        return vid
    tmpv = BUILD / "video_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", str(tmpv)],
                           stdin=subprocess.PIPE)
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gmov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE, bufsize=10 ** 8)
    bg = np.array([int(BRAND["bg"][i:i + 2], 16) for i in (1, 3, 5)], np.uint8)
    b1 = frames_of(cl["B1"], W, H)
    for _ in range(cl["phone_frames"]):          # the phone already played these
        next(b1)

    def card():
        for fr in frames_of(cl["card"], WIN["w"], WIN["h"]):
            base = np.empty((H, W, 3), np.uint8); base[:] = bg
            base[WIN["y"]:WIN["y"] + WIN["h"], WIN["x"]:WIN["x"] + WIN["w"]] = fr
            yield base

    win_mask = np.zeros((H, W), bool)
    bd = WIN["border"] + 2
    yy, xx = np.mgrid[0:H, 0:W]
    x0, y0, x1, y1, rr = WIN["x"] + bd, WIN["y"] + bd, WIN["x"] + WIN["w"] - bd, WIN["y"] + WIN["h"] - bd, max(0, WIN["r"] - bd)
    cx, cy = np.clip(xx, x0 + rr, x1 - rr), np.clip(yy, y0 + rr, y1 - rr)
    win_mask[:] = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1) & ((xx - cx) ** 2 + (yy - cy) ** 2 <= rr ** 2)
    c = CUTS
    segs = [("cartoon", frames_of(cart, W, H), A_N, None),
            ("B1", b1, c["B2"] - c["B1"], "all"),
            ("B2", frames_of(cl["B2"], W, H), c["B3"] - c["B2"], "all"),
            ("B3", frames_of(cl["B3"], W, H), c["B4"] - c["B3"], "all"),
            ("B4", frames_of(cl["B4"], W, H), c["card"] - c["B4"], "all"),
            ("card", card(), c["logo"] - c["card"], "win"),
            ("logo", (np.zeros((H, W, 3), np.uint8) for _ in range(c["end"] - c["logo"])), c["end"] - c["logo"], None)]
    rep, f = [], 0
    for name, gen, n, irlm in segs:
        k, amax = 0, 0.0
        for fr in gen:
            if k >= n:
                break
            ga = np.frombuffer(gp.stdout.read(W * H * 4), np.uint8).reshape(H, W, 4)
            if irlm == "all":
                amax = max(amax, float(ga[:, :, 3].max()))
            elif irlm == "win":
                amax = max(amax, float(ga[:, :, 3][win_mask].max()))
            al = ga[:, :, 3:4].astype(np.float32) / 255.0
            out = fr.astype(np.float32) * (1 - al) + ga[:, :, :3].astype(np.float32) * al
            enc.stdin.write((out + 0.5).astype(np.uint8).tobytes())
            k += 1; f += 1
        assert k == n, (name, k, n)
        rep.append(dict(seg=name, frame0=f - n, frames=n, overlay_alpha_max_on_footage=amax if irlm else None))
        print(name, rep[-1], flush=True)
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    assert f == CUTS["end"]
    (BUILD / "picture.json").write_text(json.dumps(rep, indent=1))
    bad = [r for r in rep if r["overlay_alpha_max_on_footage"]]
    assert not bad, f"overlay pixels on footage: {bad}"
    tmpv.rename(vid)
    return vid


# ------------------------------------------------------------------ audio
def load(p, ch=2):
    pcm = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"])
    return np.frombuffer(pcm, np.float32).reshape(-1, ch).copy()


def write_wav(p, x):
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(x.shape[1]), "-i", "-", "-c:a", "pcm_s24le", str(p)],
        input=x.astype(np.float32).tobytes())


def music(n):
    """Track spliced to the reel: lift (bar 8 downbeat) on frame A_N, the pilot's back-jumps before it, none after."""
    x = load(TRACK)
    t_lift = A_N / FPS
    pre = sum(bt(a) - bt(b) for a, b in JUMPS)
    s0 = bt(LIFT_BEAT) + pre - t_lift
    plan, cur = [], s0
    for a, b in JUMPS:
        plan.append((cur, bt(a) - XF)); cur = bt(b) - XF
    plan.append((cur, len(x) / SR))
    xf = int(XF * 2 * SR)
    out = np.zeros((0, 2), np.float32)
    for a, b in plan:
        seg = x[int(max(0.0, a) * SR):int(b * SR)].copy()
        if a < 0:
            seg = np.concatenate([np.zeros((int(-a * SR), 2), np.float32), seg])
        if len(out) and xf:
            g = np.linspace(0, 1, xf)[:, None]
            seg[:xf] *= np.sqrt(g)
            out[-xf:] *= np.sqrt(1 - g)
            out = np.concatenate([out[:-xf], out[-xf:] + seg[:xf], seg[xf:]])
        else:
            out = np.concatenate([out, seg])
    fin = 0.25 * SR
    out[:int(fin)] *= np.linspace(0, 1, int(fin))[:, None]
    N = int(n / FPS * SR)
    out = np.concatenate([out, np.zeros((max(0, N - len(out)), 2), np.float32)])[:N]
    tail = int(0.4 * SR)
    out[-tail:] *= np.linspace(1, 0, tail)[:, None]
    final_reel = t_lift + (bt(FINAL_BEAT) - bt(LIFT_BEAT))
    return out, dict(track_start_s=round(s0, 3), plan=[[round(a, 3), round(b, 3)] for a, b in plan], lift_reel_s=round(t_lift, 3),
                     final_chord_reel_s=round(final_reel, 3), logo_reel_s=round(CUTS["logo"] / FPS, 3))


def env_db(n, spans, inside, outside, ramp=0.15):
    t = np.arange(n) / SR
    g = np.full(n, outside, np.float32)
    for a, b in spans:
        k = np.clip(np.minimum((t - (a - ramp)) / ramp, ((b + ramp) - t) / ramp), 0, 1)
        g = np.minimum(g, outside + (inside - outside) * k)
    return g


def lufs(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    I = float([l for l in r.stderr.splitlines() if "I:" in l and "LUFS" in l][-1].split("I:")[1].split("LUFS")[0])
    tp = [l for l in r.stderr.splitlines() if "Peak:" in l]
    return I, (float(tp[-1].split("Peak:")[1].split("dBFS")[0]) if tp else None)


def audio():
    mixp = BUILD / "mix.wav"
    n = int(CUTS["end"] / FPS * SR)
    dlg = np.zeros((n, 2), np.float32)
    d = load(OUTD / "ep6_dialogue.wav")
    dlg[:min(n, len(d))] += d[:n]
    spans = [(L["t0"], L["t1"]) for L in TL["lines"]]
    vo_spans = []
    for k, B in sorted(TL["vo_b"].items(), key=lambda kv: int(kv[0])):
        y = load(PROC / B["file"])
        i0 = int((CUTS[B["shot"]] + VO_LEAD) / FPS * SR)
        dlg[i0:i0 + len(y)] += y[:n - i0]
        vo_spans.append((i0 / SR, i0 / SR + len(y) / SR))
    v10 = load(OUTD / "ep6_L10_logo.wav")
    i0 = int(VO10_AT / FPS * SR)
    dlg[i0:i0 + len(v10)] += v10[:n - i0]
    mus, info = music(CUTS["end"])
    t = np.arange(n) / SR
    duck = env_db(n, spans, -13.0, -8.0)                                     # cartoon: under lines / between lines
    duck = np.where(t >= A_N / FPS - 0.05, env_db(n, vo_spans, -9.0, -2.0), duck)   # Part B: under the voice-over
    duck = np.where(t >= CUTS["card"] / FPS, 0.0, duck)                      # app card: music full
    duck = np.where(t >= CUTS["logo"] / FPS, env_db(n, [(VO10_AT / FPS, VO10_AT / FPS + len(v10) / SR)], -8.0, 0.0), duck)
    mix = dlg + mus * (10 ** (duck / 20))[:, None]
    tmp = BUILD / "_mix_raw.wav"
    write_wav(tmp, mix * 0.5)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(tmp), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af", ln, "-ar", str(SR), "-c:a", "pcm_s24le", str(mixp)])
    tmp.unlink()
    I, tp = lufs(mixp)
    info.update(master_lufs=I, true_peak=tp)
    (BUILD / "audio.json").write_text(json.dumps(info, indent=1))
    print("audio", info, flush=True)
    return mixp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="pip_gus_ep6_v1")
    ap.add_argument("--clips-only", action="store_true")
    a = ap.parse_args()
    cl = clips()
    print("clips", {k: str(v) for k, v in cl.items()}, CUTS, flush=True)
    if a.clips_only:
        return
    cart = cartoon(cl)
    gm = gfx()
    vid = picture(cl, cart, gm)
    mixp = audio()
    OUTD.mkdir(parents=True, exist_ok=True)
    out = OUTD / f"{a.name}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-i", str(mixp), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
         "-shortest", "-movflags", "+faststart", str(out)])
    print("done", out, CUTS, flush=True)


if __name__ == "__main__":
    main()
