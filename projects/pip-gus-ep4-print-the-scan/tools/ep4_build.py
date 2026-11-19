"""Ep 4 assembly: cartoon frames (+ real footage corner-pinned into Pip's phone) + real GT350 section + captions/logo overlay
+ dialogue/music mix -> final mp4. Based on the sibling episodes' build (pip-gus-ep1-whole-bumper/tools/ep1_build.py).

  python3 tools/ep4_build.py [--ver v1] [--steps gfx,picture,audio,mux]

Inputs (media, not in git), M = /home/user/media/pip-gus-ep4-print-the-scan:
  frames  M/frames/<shot>/<frame>.png  + M/frames/screen_corners.json        (tools/ep4_anim.py via render_partA.sh)
  photos  M/photos/IMG_0763.jpeg (crash), IMG_0770.jpeg (scanning, bumper off) - owner's photos
  renders M/partB/scan/NNNN.png (bumper-off scan, reverse-engineered bumper slides on), M/partB/lip/NNNN.png (lip slides in)
          (tools/partB_render.py on the owner's GT350_Lip.blend)
  voice   M/voice/partA_dialogue.wav (lines 1-15 at reel times), M/voice/L16_logo.wav (Pip over the logo card)  (ep4_timeline.py)
  music   M/music/077bbd23-....mp3  = inquisitive_A, the series bed (Higgsfield ElevenLabs Music job 077bbd23)

Timeline (30 fps), beat = 18 frames from the hand-off:
  cartoon 0-1051 (E12 995-1051: the crash photo plays on the phone screen, full frame on 1051)
  real 1052-1195: crash photo 1052-1069 | scanning photo 1070-1105 | HARD CUT (beat) | scan + bumper 1106-1159 | lip 1160-1195
  logo card 1196-END (plain logo, no text; Pip's question as voice only)
Music: the pilot's three 2-bar intro back-jumps (+14.4 s) put the bass lift (bar 8) on the hand-off; then end of bar 8 -> bar 15
(Gm -> F, the track's own alternation), so the final chord (bar 16) lands on the logo card.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
M = Path("/home/user/media/pip-gus-ep4-print-the-scan")
ap = argparse.ArgumentParser()
ap.add_argument("--ver", default="v2")
ap.add_argument("--steps", default="gfx,picture,audio,mux")
a = ap.parse_args()
BUILD = M / f"build_{a.ver}"
OUT = M / "out"
BUILD.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
FPS, SR, W, H = 30, 48000, 1080, 1920
TL = json.loads((PROJ / "ep4_timeline.json").read_text())
LN = {L["n"]: L for L in TL["lines"]}
SHOTS = [(s["id"], s["f0"], s["f1"]) for s in TL["shots"]]
CART_END = TL["total_frames"]                   # 1052 = hand-off (phone full frame on 1051)
PHONE_F0 = SF_E12 = [s for s in SHOTS if s[0] == "E12"][0][1]   # real footage starts on the phone screen here
B = 18                                          # frames per beat (100 BPM)
H9 = B // 2                                     # half a beat
# v2 recap (owner: "show everything from start to finish", faster; end on the real finished bumper): (name, start frame)
SEQ = [("crash", PHONE_F0), ("crash2", CART_END + H9), ("broken", CART_END + 2 * H9), ("scanning", CART_END + 3 * H9),
       ("r_scan", CART_END + 4 * H9), ("r_trace", CART_END + 5 * H9), ("r_car", CART_END + 7 * H9), ("r_lip", CART_END + 8 * H9),
       ("done_close", CART_END + 10 * H9), ("done_car", CART_END + 12 * H9)]
CUTS = dict(logo=CART_END + 8 * B, **{n: f for n, f in SEQ})
PHONE_SHOTS = ("E4", "E8", "E9", "E10", "E11", "E12")
BEAT0, BEAT = 0.0203, 0.60001
JUMPS = [(10, 2), (14, 6), (30, 22)]            # pilot's 2-bar intro back-jumps
POST = [(36, 60)]                               # end of bar 8 -> bar 15 (Gm -> F)
XF = 0.008
EXTRA = sum((f - t) * BEAT for f, t in JUMPS)   # 14.4 s
MUSIC_AT = CART_END / FPS - (BEAT0 + 32 * BEAT + EXTRA)          # bar-8 lift on the hand-off
FINAL_HIT = CART_END / FPS + 8 * BEAT                            # bar 16 downbeat, reel time
VO_AT = CUTS["logo"] / FPS + 0.2
VO_LEN = 2.95
END = int(round((max(FINAL_HIT + 1.6, VO_AT + VO_LEN + 0.6)) * FPS))
CAP = dict(PIP="#619f73", GUS="#ecefec")
BRAND = {"accent": "#619f73", "onAccent": "#0b0c0b", "ink": "#ecefec", "bg": "#0b0c0b", "sub": "#d4d9d4", "sub2": "#c8cec8",
         "label": "#a8b0a8", "dim55": "rgba(236,239,236,0.55)", "dim50": "rgba(236,239,236,0.5)", "plate": "rgba(11,12,11,0.58)",
         "cap": "rgba(11,12,11,0.55)"}
Y0, YP = 1560, 1345        # YP: phone shots - below the phone, over the hats (eyes stay clear)
PAGES = [   # (line, rows of word indices, centre y)
    (1, [[0, 1, 2], [3, 4, 5, 6, 7]], Y0),
    (2, [[0, 1]], Y0), (2, [[2, 3, 4]], Y0),
    (3, [[0, 1, 2], [3, 4, 5]], Y0),
    (4, [[0, 1, 2], [3, 4]], YP), (4, [[5, 6]], YP),
    (5, [[0, 1, 2, 3]], Y0), (6, [[0]], Y0),
    (7, [[0, 1, 2, 3]], Y0),
    (8, [[0, 1, 2, 3]], Y0),
    (9, [[0, 1, 2], [3, 4]], YP),
    (10, [[0, 1, 2], [3, 4, 5, 6]], YP),
    (11, [[0, 1, 2], [3, 4, 5, 6]], YP),
    (12, [[0, 1, 2, 3], [4, 5, 6, 7]], YP),
    (13, [[0, 1]], YP),
    (14, [[0]], YP), (14, [[1, 2, 3]], YP),
    (15, [[0, 1, 2, 3]], YP),
]


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def nframes(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


CORN = json.loads((M / "frames/screen_corners.json").read_text()) if (M / "frames/screen_corners.json").exists() else None


def corners(fr):
    if not CORN:
        return None
    for sh in CORN["shots"].values():
        c = sh["per_frame"].get(str(fr))
        if c:
            return c
    return None


def screen_bottom(fr):
    c = corners(fr)
    return max(p[1] for p in c) if c else 0


def pages():
    out = []
    for i, (n, rows, y) in enumerate(PAGES):
        L = LN[n]
        ws = L["words"]
        last = ws[rows[-1][-1]]["t1"]
        t1 = min(last + 0.35, L["t1"] + 0.25)
        if i + 1 < len(PAGES):
            nn, nrows = PAGES[i + 1][:2]
            t1 = min(t1, LN[nn]["words"][nrows[0][0]]["t0"])
        t1 = min(t1, CART_END / FPS - 1 / FPS)
        if n == 15:   # rule: no text over real footage - leave before the growing screen reaches the caption band
            for fr in range(int(ws[0]["t0"] * FPS), CART_END):
                if screen_bottom(fr) > y - 110:
                    t1 = min(t1, fr / FPS - 1 / FPS)
                    break
        out.append(dict(t0=ws[rows[0][0]]["t0"], t1=round(t1, 3), color=CAP[L["speaker"]], y=y, cx=540,
                        lines=[[dict(w=ws[k]["w"], t0=ws[k]["t0"]) for k in row] for row in rows]))
    for n in LN:   # every word captioned exactly once
        ks = sorted(k for n_, rows, _ in PAGES if n_ == n for k in sum(rows, []))
        assert ks == list(range(len(LN[n]["words"]))), (n, ks)
    return out


# ------------------------------------------------------------------ gfx (captions + logo card, transparent ProRes)
def gfx():
    props = {"fps": FPS, "durationInFrames": END, "palette": BRAND, "size": 84, "pages": pages(),
             "items": [{"kind": "logo", "t0": CUTS["logo"] / FPS, "t1": END / FPS + 1, "cta": ""}]}
    js = json.dumps(props, indent=1)
    (PROJ / f"gfx_{a.ver}_props.json").write_text(js)
    h = hashlib.sha1((js + "".join((REPO / "remotion/src/gfx/reel" / f).read_text() for f in ("ExplainerGfx.tsx", "ReelGfx.tsx"))).encode()).hexdigest()[:10]
    mov = BUILD / f"gfx_{h}.mov"
    if not mov.exists():
        pj = BUILD / "gfx_props.json"
        pj.write_text(js)
        tmp = BUILD / f"tmp_{h}.mov"
        run(["nice", "-n", "5", "npx", "remotion", "render", "ExplainerGfx", str(tmp), f"--props={pj}", "--codec=prores",
             "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png", "--concurrency=2", "--log=error"],
            cwd=REPO / "remotion")
        tmp.rename(mov)
    return mov


# ------------------------------------------------------------------ real section frames
_PH = {}


def photo(name, k, cx, push=0.06):
    """9:16 window of a 4:3 photo (full height), slow push-in; k 0..1 over the shot."""
    if name not in _PH:
        _PH[name] = cv2.cvtColor(cv2.imread(str(M / "photos" / name)), cv2.COLOR_BGR2RGB)
    im = _PH[name]
    h, w = im.shape[:2]
    s = 1.0 + push * k
    ch = h / s
    cw = ch * 9 / 16
    x0 = min(max(cx - cw / 2, 0), w - cw)
    y0 = (h - ch) / 2
    Mx = np.array([[W / cw, 0, -x0 * W / cw], [0, H / ch, -y0 * H / ch]], np.float32)
    out = cv2.warpAffine(im, Mx, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    blur = cv2.GaussianBlur(out, (0, 0), 1.2)
    return cv2.addWeighted(out, 1.35, blur, -0.35, 0)   # light unsharp after the 1.78x upscale


def render_frame(shot, i):
    p = M / "partB" / shot / f"{i:04d}.png"
    im = cv2.imread(str(p), cv2.IMREAD_COLOR)
    if im is None:
        raise SystemExit(f"missing {p}")
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


def fitw(name, k):
    """Whole 4:3 photo fitted to the frame width over a blurred, darkened fill of itself; slow push."""
    if name not in _PH:
        _PH[name] = cv2.cvtColor(cv2.imread(str(M / "photos" / name)), cv2.COLOR_BGR2RGB)
    im = _PH[name]
    bg = cv2.GaussianBlur(photo(name, 0, im.shape[1] / 2, 0), (0, 0), 40)
    bg = (bg * 0.45).astype(np.uint8)
    s_ = (W / im.shape[1]) * (1.0 + 0.05 * k)
    fg = cv2.resize(im, None, fx=s_, fy=s_, interpolation=cv2.INTER_LANCZOS4)
    h, w = fg.shape[:2]
    x0 = (w - W) // 2
    fg = fg[:, x0:x0 + W]
    y0 = (H - h) // 2
    bg[y0:y0 + h] = fg
    return bg


def rframe(name, i):
    p = M / "v2/recap" / name / f"{i:04d}.png"
    im = cv2.imread(str(p), cv2.IMREAD_COLOR)
    if im is None:
        raise SystemExit(f"missing {p}")
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


PHOTO = dict(crash=("IMG_0763.jpeg", 640), crash2=("IMG_0764.jpeg", 820), broken=("IMG_0771.jpeg", 560),
             scanning=("IMG_0770.jpeg", 330), done_close=("IMG_0767.jpeg", 900))


def real(fr):
    """Recap picture for reel frame fr (on the phone screen during E12, full frame from the hand-off)."""
    k = max(i for i, (n, f) in enumerate(SEQ) if f <= fr)
    name, f0 = SEQ[k]
    f1 = SEQ[k + 1][1] if k + 1 < len(SEQ) else CUTS["logo"]
    u = (fr - f0) / max(1, f1 - f0)
    if name in PHOTO:
        return photo(PHOTO[name][0], u, PHOTO[name][1])
    if name == "done_car":
        return photo("IMG_0765.jpeg", u, 480, push=0.04)
    return rframe(name, fr - f0)


def phone_content(fr):
    if fr >= PHONE_F0:
        return real(fr)
    im = cv2.imread(str(M / "v2/phone" / f"{fr:04d}.png"), cv2.IMREAD_COLOR)
    if im is None:
        raise SystemExit(f"missing phone frame {fr}")
    return cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2RGB), (W, H), interpolation=cv2.INTER_LANCZOS4)


def composite_phone(img, fr):
    """Corner-pin the Blender scene / recap into the key-coloured phone screen."""
    c = corners(fr)
    if c is None:
        return img
    src = np.float32([[0, 0], [W - 1, 0], [W - 1, H - 1], [0, H - 1]])
    Hm = cv2.getPerspectiveTransform(src, np.float32(c))
    warped = cv2.warpPerspective(phone_content(fr), Hm, (W, H), flags=cv2.INTER_AREA)
    f = img.astype(np.int16)
    key = (np.abs(f[:, :, 0] - 255) + np.abs(f[:, :, 1] - 0) + np.abs(f[:, :, 2] - 255)).astype(np.float32)
    al = np.clip(1.0 - (key - 60) / 120.0, 0, 1)[:, :, None]   # soft key edge
    return (img * (1 - al) + warped * al).astype(np.uint8)


def picture(gmov):
    vid = BUILD / "video.mp4"
    fr_dir = M / "frames"
    newest = max(p.stat().st_mtime for s, _, _ in SHOTS for p in (fr_dir / s).glob("*.png"))
    key = f"{gmov.name}|{newest:.0f}|{END}"
    stamp = BUILD / "video.key"
    if vid.exists() and nframes(vid) == END and stamp.exists() and stamp.read_text() == key:
        return vid
    tmpv = BUILD / "video_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                            str(tmpv)], stdin=subprocess.PIPE)
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gmov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE,
                          bufsize=10 ** 8)
    shot_of = {fr: s for s, f0, f1 in SHOTS for fr in range(f0, f1)}
    qa = dict(text_over_footage_alpha_max=0.0, text_over_phone_screen_px=0)
    for fr in range(END):
        foot, scr = False, None
        if fr < CART_END:
            p = fr_dir / shot_of[fr] / f"{fr:04d}.png"
            im = cv2.imread(str(p), cv2.IMREAD_COLOR)
            if im is None:
                raise SystemExit(f"missing frame {p}")
            img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            scr = None
            if shot_of[fr] in PHONE_SHOTS:
                scr = np.all(img == (255, 0, 255), axis=2)
                img = composite_phone(img, fr)
        elif fr < CUTS["logo"]:
            img = real(fr)
            foot = True
        else:
            img = np.zeros((H, W, 3), np.uint8)
        ga = np.frombuffer(gp.stdout.read(W * H * 4), np.uint8).reshape(H, W, 4)
        al = ga[:, :, 3:4].astype(np.float32) / 255.0
        if foot:   # rule: no text over real footage
            qa["text_over_footage_alpha_max"] = max(qa["text_over_footage_alpha_max"], float(al.max()))
        elif scr is not None:
            qa["text_over_phone_screen_px"] += int(((al[:, :, 0] > 0.05) & scr).sum())
        out = img.astype(np.float32) * (1 - al) + ga[:, :, :3].astype(np.float32) * al
        enc.stdin.write((out + 0.5).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    (BUILD / "picture.json").write_text(json.dumps(qa, indent=1))
    assert qa["text_over_footage_alpha_max"] == 0.0 and qa["text_over_phone_screen_px"] == 0, qa
    tmpv.rename(vid)
    stamp.write_text(key)
    return vid


# ------------------------------------------------------------------ audio
def load_wav(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def write_wav(p, x):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", "-c:a", "pcm_f32le", str(p)],
                   input=np.ascontiguousarray(x, np.float32).tobytes(), check=True)


def lufs(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    s = r[r.rfind("Summary"):]
    return float(s.split("I:")[1].split("LUFS")[0]), float(s.split("Peak:")[1].split("dBFS")[0])


def smooth(g, sec):
    k = int(sec * SR)
    return np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, "same")[k:-k]


def bt(k):
    return BEAT0 + k * BEAT


def edited_music(mu):
    """The track with the intro back-jumps and the post-lift jump (8 ms equal-power crossfades before each grid beat)."""
    segs, cur = [], 0.0
    for f, t in JUMPS + POST:
        segs.append((cur, bt(f) - XF)); cur = bt(t) - XF
    segs.append((cur, len(mu) / SR))
    out, xf = [], int(2 * XF * SR)
    for i, (s0, s1) in enumerate(segs):
        seg = mu[int(s0 * SR):int(s1 * SR) + (xf if i < len(segs) - 1 else 0)].copy()
        if out:
            ramp = np.sin(np.linspace(0, np.pi / 2, xf))[:, None]
            seg[:xf] = seg[:xf] * ramp + out[-1][-xf:] * np.cos(np.linspace(0, np.pi / 2, xf))[:, None]
            out[-1] = out[-1][:-xf]
        out.append(seg)
    return np.concatenate(out)


def audio():
    master = BUILD / "mix.wav"
    n = int(round(END / FPS * SR))
    dia = np.zeros((n, 2), np.float32)
    v = load_wav(M / "voice/partA_dialogue.wav")
    dia[:min(n, len(v))] = v[:n]
    vo = load_wav(M / "voice/L16_logo.wav")
    s = int(VO_AT * SR)
    dia[s:s + len(vo)] += vo[:max(0, n - s)]
    mu = edited_music(load_wav(M / "music/077bbd23-cc16-4c61-a5b8-8ca12d30e386.mp3"))
    mus = np.zeros((n, 2), np.float32)
    s = int(MUSIC_AT * SR)
    if s >= 0:
        mus[s:s + len(mu)] = mu[:max(0, n - s)]
    else:
        mus[:min(n, len(mu) + s)] = mu[-s:-s + n]
    write_wav(BUILD / "music_raw.wav", mus)
    Im, _ = lufs(BUILD / "music_raw.wav")
    mus *= 10 ** ((-14.0 - Im) / 20)
    g = np.full(n, -8.0)
    for L in TL["lines"]:
        g[max(0, int((L["t0"] - 0.15) * SR)):int((L["t1"] + 0.1) * SR)] = -13.0
    g[int(CART_END / FPS * SR):] = -3.0                    # real section: music carries it
    g[int((VO_AT - 0.1) * SR):] = -9.0                     # under Pip's question on the logo card
    g = smooth(g, 0.08)
    lin = 10 ** (g / 20)
    f0 = int((END / FPS - 0.5) * SR)
    lin[f0:] *= np.cos(np.linspace(0, np.pi / 2, n - f0)) ** 1.5
    mus *= lin[:, None]
    mix = mus + dia
    write_wav(BUILD / "pre.wav", mix)
    I, _ = lufs(BUILD / "pre.wav")
    gain = -14.0 - I
    for _ in range(6):
        write_wav(BUILD / "gain.wav", mix * 10 ** (gain / 20))
        run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / "gain.wav"), "-af",
             "aresample=192000,alimiter=limit=0.79:attack=1:release=60:level=disabled,aresample=48000", "-c:a", "pcm_s24le", str(master)])
        I2, P2 = lufs(master)
        if abs(I2 + 14.0) <= 0.2:
            break
        gain += -14.0 - I2
    write_wav(BUILD / "stem_dialogue.wav", dia * 10 ** (gain / 20))
    write_wav(BUILD / "stem_music.wav", mus * 10 ** (gain / 20))
    Id, _ = lufs(BUILD / "stem_dialogue.wav")
    Imu, _ = lufs(BUILD / "stem_music.wav")
    info = dict(master_lufs=I2, master_true_peak=P2, dialogue_lufs=Id, music_lufs=Imu, music_at=round(MUSIC_AT, 4),
                final_hit_reel=round(FINAL_HIT, 3), vo_at=round(VO_AT, 3), end_frame=END, cuts=CUTS, handoff=CART_END)
    (BUILD / "audio.json").write_text(json.dumps(info, indent=1))
    print("audio", info, flush=True)
    return master


def mux(vid, master):
    out = OUT / f"pip_gus_ep4_{a.ver}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-i", str(master), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
         "-b:a", "256k", "-ar", "48000", "-t", f"{END / FPS:.5f}", "-movflags", "+faststart", str(out)])
    print("DONE", out, nframes(out), flush=True)
    return out


if __name__ == "__main__":
    steps = a.steps.split(",")
    gm = gfx() if "gfx" in steps or "picture" in steps else None
    vid = picture(gm) if "picture" in steps else BUILD / "video.mp4"
    mas = audio() if "audio" in steps else BUILD / "mix.wav"
    if "mux" in steps:
        mux(vid, mas)
