"""Pip & Gus Ep 7 full build: cartoon (rendered frames) with the real big-printer footage in the phone screen, real footage
(big printer, then small printer), the "WHICH DO YOU PREFER RUNNING?" teaser card, the logo card with Pip's voice-only line
13, captions (word by word, cartoon only), music and dialogue mix.

    python projects/pip-gus-ep6-printer-size/tools/ep7_build.py [--name pip_gus_ep7_v1]

Resumable: cached steps in BUILD (clips, gfx_<hash>.mov, cartoon.mp4, video.mp4, mix). Delete a file to redo that step.

Timeline (frames, 30 fps): cartoon 0-906 (S10's last frame 906 = phone screen full frame) | BIG 907-978 (music lift on 907,
bar 8) | SMALL 979-1050 (bar 9) | teaser card 1051-1158 (bar 14 after the 2-bar jump; headline lines on beats) | logo
1159-1249 (Pip's line 13 voice-only from 1164; final chord bar 16 at 1195; ring-out).
Music: the series bed (pilot's ElevenLabs Music v2.5 job 077bbd23 = "inquisitive_A", 100 BPM, beat0 0.0203 s, lift = bass
entry bar 8). Intro stretched with the pilot's measured seamless 2-bar back-jumps (beats 10->2, 14->6, 30->22), lift on
frame 907, post-lift jump end of bar 9 -> bar 14 (pilot splice score 6.39 vs 5.3 floor) so the final chord lands on the logo.
"""
import argparse, hashlib, json, subprocess, sys, wave
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
W_ = Path("/home/user/media/work/ep7")
DROP = Path("/home/user/media/pip-gus-ep6-printer-size/dropbox")
BUILD = W_ / "build"
FRAMES = W_ / "frames"
OUTD = W_ / "out"
W, H, FPS, SR = 1080, 1920, 30, 48000
TL = json.loads((PROJ / "ep7_timeline.json").read_text())
A_N = TL["total_frames"]                       # 907
CUTS = dict(big=A_N, small=A_N + 72, card=A_N + 144, logo=A_N + 252, end=A_N + 343)
VO13_AT = CUTS["logo"] + 5
BIG = dict(src=DROP / "15.50.05.mov", t_full=5.0)       # frame 907 shows 5.0 s; phone (S10) plays 3.3-5.0 s before it
SMALL = dict(src=DROP / "mr2_print.avi", t0=0.45, crop=(405, 720, 430, 0))   # built-in timelapse; logo on the head from ~3.9 s
TEASE = dict(src=DROP / "15.50.09.mov", t0=7.6, crop=(720, 540, 0, 420))    # gantry move, logo (~5 s) avoided
WIN = dict(x=110, y=700, w=860, h=645, r=30, border=5)
BRAND = dict(accent="#619f73", onAccent="#0b0c0b", ink="#ecefec", bg="#0b0c0b", sub="#c8ccc8", sub2="#aeb3ae", label="#aeb3ae")
CAP = dict(PIP="#619f73", GUS="#ecefec")
TRACK = W_ / "music/inquisitive_A.mp3"
BEAT0, BEAT = 0.0203, 0.60001
LIFT_BEAT, JUMPS, POST_JUMPS, XF = 32, [(10, 2), (14, 6), (30, 22)], [(40, 56)], 0.008
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


# ------------------------------------------------------------------ clips
def clips():
    BUILD.mkdir(parents=True, exist_ok=True)
    out = {}
    # big printer: phone part (S10) + full-frame part, one continuous clip from the moment S10 starts
    s10 = [s for s in TL["shots"] if s["id"] == "S10"][0]
    n_phone = A_N - s10["f0"]
    t0 = BIG["t_full"] - n_phone / FPS
    p = BUILD / "big.mp4"
    n = n_phone + (CUTS["small"] - CUTS["big"])
    if not (p.exists() and nframes(p) == n):
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", str(BIG["src"]), "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
             "-frames:v", str(n)] + ENC + [str(p)])
    out["big"], out["big_phone_frames"], out["big_t0"] = p, n_phone, t0
    p = BUILD / "small.mp4"
    n = CUTS["card"] - CUTS["small"]
    if not (p.exists() and nframes(p) == n):
        w, h, x, y = SMALL["crop"]
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{SMALL['t0']:.3f}", "-i", str(SMALL["src"]), "-vf",
             f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,fps={FPS}", "-frames:v", str(n)] + ENC + [str(p)])
    out["small"] = p
    p = BUILD / "teaser.mp4"
    n = CUTS["logo"] - CUTS["card"]
    if not (p.exists() and nframes(p) == n):
        w, h, x, y = TEASE["crop"]
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{TEASE['t0']:.3f}", "-i", str(TEASE["src"]), "-vf",
             f"crop={w}:{h}:{x}:{y},scale={WIN['w']}:{WIN['h']}:flags=lanczos,fps={FPS},format=yuv444p", "-frames:v", str(n)]
            + [e if e != "yuv420p" else "yuv444p" for e in ENC] + [str(p)])
    out["teaser"] = p
    return out


# ------------------------------------------------------------------ cartoon (rendered frames + phone composite)
def cartoon(cl):
    p = BUILD / "cartoon.mp4"
    if p.exists() and nframes(p) == A_N:
        return p
    corn = json.loads((FRAMES / "screen_corners.json").read_text())["shots"]["S10"]["per_frame"]
    big = frames_of(cl["big"], W, H)
    s10f0 = [s for s in TL["shots"] if s["id"] == "S10"][0]["f0"]
    tmp = BUILD / "cartoon_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r",
                            str(FPS), "-i", "-"] + ENC + [str(tmp)], stdin=subprocess.PIPE)
    for s in TL["shots"]:
        for fr in range(s["f0"], s["f1"]):
            im = cv2.imread(str(FRAMES / s["id"] / f"{fr:04d}.png"), cv2.IMREAD_COLOR)
            assert im is not None, (s["id"], fr)
            img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            if s["id"] == "S10":
                foot = next(big)
                if fr == A_N - 1:
                    img = foot                                       # screen fills the frame
                else:
                    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), np.float32(corn[str(fr)]))
                    warp = cv2.warpPerspective(foot, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
                    f = img.astype(np.float32)
                    mag = np.minimum(f[..., 0], f[..., 2]) - f[..., 1]
                    m = np.clip((mag - 40) / 80, 0, 1)[..., None]
                    spill = mag > 15
                    f[spill, 0] = np.minimum(f[spill, 0], f[spill, 1] + 8)
                    f[spill, 2] = np.minimum(f[spill, 2], f[spill, 1] + 8)
                    img = (f * (1 - m) + warp * m).clip(0, 255).astype(np.uint8)
            enc.stdin.write(np.ascontiguousarray(img).tobytes())
    enc.stdin.close(); enc.wait()
    assert nframes(tmp) == A_N
    tmp.rename(p)
    return p


# ------------------------------------------------------------------ captions + cards (Remotion ExplainerGfx)
def caption_tokens(L):
    """Script wording on whisper word times (brand spelled right); a token count mismatch merges into the first word."""
    toks = L["text"].split()
    ws = L["words"]
    if len(toks) != len(ws):                 # "...Show-off." heard as "Show" "off."
        toks = [L["text"]]
        ws = ws[:1]
    return [dict(w=t.lstrip("."), t0=round(w["t0"], 3)) for t, w in zip(toks, ws)]


def screen_rect(fr):
    corn = json.loads((FRAMES / "screen_corners.json").read_text())["shots"]["S10"]["per_frame"]
    c = corn.get(str(fr))
    if not c:
        return None
    xs, ys = [p[0] for p in c], [p[1] for p in c]
    return min(xs), min(ys), max(xs), max(ys)


def pages():
    out = []
    lines = TL["lines"]
    for i, L in enumerate(lines):
        toks = caption_tokens(L)
        # one page per sentence (word ending in . ? !), pages of > 3 words split into two caption lines
        sents, cur = [], []
        for t in toks:
            cur.append(t)
            if t["w"].endswith((".", "?", "!")):
                sents.append(cur); cur = []
        if cur:
            sents.append(cur)
        merged = []                                        # one-word sentences join the next ("Big one?" stays its own page)
        for s in sents:
            if merged and len(merged[-1]) + len(s) <= 4 and len(merged[-1]) <= 1:
                merged[-1] = merged[-1] + s
            else:
                merged.append(s)
        nxt = lines[i + 1]["t0"] if i + 1 < len(lines) else A_N / FPS
        for k, s in enumerate(merged):
            t0 = s[0]["t0"]
            t1 = merged[k + 1][0]["t0"] if k + 1 < len(merged) else min(L["t1"] + 0.3, nxt - 0.02)
            if len(s) > 3:
                h = (len(s) + 1) // 2
                ln = [s[:h], s[h:]]
            else:
                ln = [s]
            out.append(dict(t0=round(t0, 3), t1=round(t1, 3), color=CAP[L["speaker"]], y=1330, cx=540, lines=ln))
    # keep every page off the phone screen (real footage) in S10: move it below the screen
    s10 = [s for s in TL["shots"] if s["id"] == "S10"][0]
    for p in out:
        f0, f1 = int(round(p["t0"] * FPS)), int(round(p["t1"] * FPS))
        if f1 > s10["f0"]:
            p["y"] = 1700
            for fr in range(max(f0, s10["f0"]), min(f1, A_N)):
                r = screen_rect(fr)
                hh = 70 + 60 * (len(p["lines"]) - 1)
                assert r is None or r[3] < p["y"] - hh or fr == A_N - 1, ("caption over the phone screen", fr, r)
            assert f1 <= A_N - 1, "caption must end before the screen fills the frame"
    return out


def props():
    c0, b = CUTS["card"] / FPS, BEAT
    items = [{"kind": "teaser", "t0": c0, "t1": CUTS["logo"] / FPS,
              "lines": [{"text": "WHICH DO YOU", "at": c0}, {"text": "PREFER", "at": c0 + b}, {"text": "RUNNING?", "at": c0 + 2 * b}],
              "sub": {"lines": [], "at": c0}, "win": dict(WIN, at=c0)},
             {"kind": "logo", "t0": CUTS["logo"] / FPS, "t1": CUTS["end"] / FPS + 1, "cta": ""}]
    return {"fps": FPS, "durationInFrames": CUTS["end"], "items": items, "pages": pages(), "palette": BRAND, "size": 88}


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
    big = frames_of(cl["big"], W, H)
    for _ in range(cl["big_phone_frames"]):                 # the phone already played these
        next(big)

    def card():
        for fr in frames_of(cl["teaser"], WIN["w"], WIN["h"]):
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
            ("big", big, c["small"] - c["big"], "all"),
            ("small", frames_of(cl["small"], W, H), c["card"] - c["small"], "all"),
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
        rep.append(dict(seg=name, frame0=f - n, frames=n, irl_overlay_alpha_max=amax if irlm else None))
        print(name, rep[-1], flush=True)
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    assert f == CUTS["end"]
    (BUILD / "picture.json").write_text(json.dumps(rep, indent=1))
    bad = [r for r in rep if r["irl_overlay_alpha_max"]]
    assert not bad, f"overlay pixels on IRL footage: {bad}"
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
    """Track spliced to the reel: lift (bar 8 downbeat) on frame A_N, back-jumps before, the post-lift jump after."""
    x = load(TRACK)
    t_lift = A_N / FPS
    pre = sum(bt(a) - bt(b) for a, b in JUMPS)
    s0 = bt(LIFT_BEAT) + pre - t_lift                       # track time at reel 0 (may be > 0: the track enters mid-intro)
    plan, cur = [], s0
    for a, b in JUMPS + POST_JUMPS:
        plan.append((cur, bt(a) - XF)); cur = bt(b) - XF
    plan.append((cur, len(x) / SR))
    xf = int(XF * 2 * SR)
    out = np.zeros((0, 2), np.float32)
    for a, b in plan:
        seg = x[int(max(0.0, a) * SR):int(b * SR)].copy()
        if len(out) and xf:
            g = np.linspace(0, 1, xf)[:, None]
            seg[:xf] *= np.sqrt(g)
            out[-xf:] *= np.sqrt(1 - g)
            out = np.concatenate([out[:-xf], out[-xf:] + seg[:xf], seg[xf:]])
        else:
            out = np.concatenate([out, seg])
    fin = 0.25 * SR                                          # short fade-in: the track enters mid-intro
    out[:int(fin)] *= np.linspace(0, 1, int(fin))[:, None]
    N = int(n / FPS * SR)
    out = np.concatenate([out, np.zeros((max(0, N - len(out)), 2), np.float32)])[:N]
    tail = int(0.4 * SR)
    out[-tail:] *= np.linspace(1, 0, tail)[:, None]
    final_reel = t_lift + (bt(POST_JUMPS[0][0]) - bt(LIFT_BEAT)) + (bt(FINAL_BEAT) - bt(POST_JUMPS[0][1]))
    return out, dict(track_start_s=round(s0, 3), plan=[[round(a, 3), round(b, 3)] for a, b in plan], lift_reel_s=round(t_lift, 3),
                     final_chord_reel_s=round(final_reel, 3))


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
    d = load(OUTD / "ep7_dialogue.wav")
    dlg[:min(n, len(d))] += d[:n]
    v13 = load(OUTD / "ep7_L13_logo.wav")
    i0 = int(VO13_AT / FPS * SR)
    dlg[i0:i0 + len(v13)] += v13[:n - i0]
    mus, info = music(CUTS["end"])
    spans = [(L["t0"], L["t1"]) for L in TL["lines"]] + [(VO13_AT / FPS, VO13_AT / FPS + len(v13) / SR)]
    t = np.arange(n) / SR
    duck = env_db(n, spans[:-1], -13.0, -8.0)                       # cartoon: under lines / between lines
    duck = np.where(t >= A_N / FPS - 0.05, 0.0, duck)               # footage + teaser card: music full
    duck = np.where(t >= CUTS["logo"] / FPS, env_db(n, spans[-1:], -8.0, 0.0), duck)   # logo: under Pip's line 13
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
    ap.add_argument("--name", default="pip_gus_ep7_v1")
    a = ap.parse_args()
    cl = clips()
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
