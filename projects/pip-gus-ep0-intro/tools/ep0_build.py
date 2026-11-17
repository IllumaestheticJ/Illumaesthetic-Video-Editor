"""Ep 0 assembly: cartoon frames + phone footage composite + captions/logo overlay + dialogue/music mix -> final mp4.

  python3 tools/ep0_build.py [--ver v1] [--frames DIR] [--steps gfx,picture,audio,mux]

Inputs (media, not in git):
  frames   /home/user/media/work/pip-gus-ep0/frames/<shot>/<frame>.png  (tools/ep0_anim.py) + screen_corners.json
  phone    /home/user/media/pip-gus-ep0-intro/reels/phone_insert.mp4    (Lola / C5 / MR2 1:1 cuts, 3 x 36 frames)
  voice    /home/user/media/pip-gus-ep0-intro/voice/ep0_take2.mp3        (approved take 2, Higgsfield job 97c78172)
  music    /home/user/media/pip-gus-ep0-intro/music/077bbd23-...mp3      (pilot's inquisitive_A bed)
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
M = Path("/home/user/media/pip-gus-ep0-intro")
WK = Path("/home/user/media/work/pip-gus-ep0")
ap = argparse.ArgumentParser()
ap.add_argument("--ver", default="v1")
ap.add_argument("--frames", default=str(WK / "frames"))
ap.add_argument("--steps", default="gfx,picture,audio,mux")
a = ap.parse_args()
BUILD = WK / f"build_{a.ver}"
OUT = WK / "out"
BUILD.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
FPS, SR, W, H = 30, 48000, 1080, 1920
TL = json.loads((PROJ / "ep0_timeline.json").read_text())
LN = {L["n"]: L for L in TL["lines"]}

SHOTS = [("A", 0, 109), ("B", 109, 199), ("C", 199, 289), ("D", 289, 397), ("E", 397, 505), ("F", 505, 649),
         ("G", 649, 752), ("H1", 752, 778), ("H2", 778, 814), ("H3", 814, 842), ("H4", 842, 865), ("I", 865, 973),
         ("J", 973, 1027), ("K", 1027, 1135)]
CART_END = 1135                       # logo card from here (37.83 s, a beat)
MUSIC_AT = TL["music_at"]             # music t=0 at reel 2.40 s
FINAL_HIT = MUSIC_AT + 38.42          # the track's final chord (pilot analysis) -> reel 40.82 s
END = int(round((FINAL_HIT + 0.9) * FPS))   # chord rings ~0.9 s, then the reel ends
PHONE0 = 397                          # shot E: phone_insert frame = reel frame - PHONE0
VOICE_FX = ("highpass=f=90:poles=2,equalizer=f=3500:t=q:w=1.1:g=3,treble=g=2:f=9000:t=s:w=0.7,"
            "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:knee=4:makeup=3")   # pilot v2 polish (owner: brighter)
CAP = dict(PIP="#619f73", GUS="#ecefec")
BRAND = {"accent": "#619f73", "onAccent": "#0b0c0b", "ink": "#ecefec", "bg": "#0b0c0b", "sub": "#d4d9d4", "sub2": "#c8cec8",
         "label": "#a8b0a8", "dim55": "rgba(236,239,236,0.55)", "dim50": "rgba(236,239,236,0.5)", "plate": "rgba(11,12,11,0.58)",
         "cap": "rgba(11,12,11,0.55)"}
CTA = "WHAT QUESTIONS\nDO YOU HAVE?"   # owner 2026-11-16: the logo card ends with this text

# captions: (line, [[word idx], ...], centre y) - y placed by eye on each page's frames (faces / phone screen clear)
PAGES = [
    (1, [[0, 1, 2]], 1500), (2, [[0, 1, 2]], 1500), (3, [[0, 1, 2], [3, 4]], 1530),
    (4, [[0, 1, 2, 3, 4], [5, 6, 7, 8]], 1500), (4, [[9, 10, 11, 12], [13, 14, 15, 16, 17]], 1500),
    (4, [[18, 19, 20], [21, 22, 23]], 1500),
    (5, [[0, 1], [2, 3, 4, 5]], 1640),
    (6, [[0, 1, 2], [3, 4, 5]], 1500), (6, [[6, 7], [8, 9, 10, 11]], 1500),
    (7, [[0, 1, 2, 3], [4, 5]], 1500), (7, [[6, 7, 8, 9]], 1500),
    (8, [[0, 1], [2, 3]], 1500),
    (9, [[0, 1, 2], [3, 4, 5]], 1500),
    (10, [[0, 1, 2], [3, 4]], 1500),
    (11, [[0, 1], [2, 3, 4]], 1560),
]


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
        out.append(dict(t0=ws[rows[0][0]]["t0"], t1=round(t1, 3), color=CAP[L["speaker"]], y=y, cx=540,
                        lines=[[dict(w=ws[k]["w"], t0=ws[k]["t0"]) for k in row] for row in rows]))
    return out


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def nframes(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


# ------------------------------------------------------------------ gfx (captions + logo card, transparent ProRes)
def gfx():
    props = {"fps": FPS, "durationInFrames": END, "palette": BRAND, "size": 84, "pages": pages(),
             "items": [{"kind": "logo", "t0": CART_END / FPS, "t1": END / FPS + 1, "cta": CTA, "ctaSize": 76, "ctaInk": True}]}
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


# ------------------------------------------------------------------ picture
def phone_frames():
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(M / "reels/phone_insert.mp4"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    out = []
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        out.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    dec.wait()
    return out


def composite(img, foot, corners):
    Mx = cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), np.float32(corners))
    warp = cv2.warpPerspective(foot, Mx, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    f = img.astype(np.float32)
    mag = np.minimum(f[..., 0], f[..., 2]) - f[..., 1]
    m = np.clip((mag - 40) / 80, 0, 1)[..., None]
    spill = mag > 15
    f[spill, 0] = np.minimum(f[spill, 0], f[spill, 1] + 8)
    f[spill, 2] = np.minimum(f[spill, 2], f[spill, 1] + 8)
    return (f * (1 - m) + warp * m).clip(0, 255).astype(np.uint8), m[..., 0]


def picture(gmov):
    vid = BUILD / "video.mp4"
    fr_dir = Path(a.frames)
    # cache key: overlay file + newest rendered frame + phone insert (a frame-count check alone reused a stale picture)
    newest = max(p.stat().st_mtime for s, _, _ in SHOTS for p in (fr_dir / s).glob("*.png"))
    key = f"{gmov.name}|{newest:.0f}|{(M / 'reels/phone_insert.mp4').stat().st_mtime:.0f}"
    stamp = BUILD / "video.key"
    if vid.exists() and nframes(vid) == END and stamp.exists() and stamp.read_text() == key:
        return vid
    corn = json.loads((fr_dir / "screen_corners.json").read_text())["shots"]["E"]["per_frame"]
    phone = phone_frames()
    assert len(phone) == 108, len(phone)
    tmpv = BUILD / "video_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                            str(tmpv)], stdin=subprocess.PIPE)
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gmov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE,
                          bufsize=10 ** 8)
    shot_of = {fr: s for s, f0, f1 in SHOTS for fr in range(f0, f1)}
    qa = dict(text_over_footage_alpha_max=0.0, missing=[])
    for fr in range(END):
        if fr < CART_END:
            p = fr_dir / shot_of[fr] / f"{fr:04d}.png"
            im = cv2.imread(str(p), cv2.IMREAD_COLOR)
            if im is None:
                qa["missing"].append(fr)
                raise SystemExit(f"missing frame {p}")
            img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            foot_m = None
            if shot_of[fr] == "E":
                img, foot_m = composite(img, phone[fr - PHONE0], corn[str(fr)])
        else:
            img = np.zeros((H, W, 3), np.uint8)
            foot_m = None
        ga = np.frombuffer(gp.stdout.read(W * H * 4), np.uint8).reshape(H, W, 4)
        al = ga[:, :, 3:4].astype(np.float32) / 255.0
        if foot_m is not None:   # rule: no text over real footage
            qa["text_over_footage_alpha_max"] = max(qa["text_over_footage_alpha_max"], float((al[..., 0] * (foot_m > 0.5)).max()))
        out = img.astype(np.float32) * (1 - al) + ga[:, :, :3].astype(np.float32) * al
        enc.stdin.write((out + 0.5).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    (BUILD / "picture.json").write_text(json.dumps(qa, indent=1))
    assert qa["text_over_footage_alpha_max"] == 0.0, qa
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
    I = float(s.split("I:")[1].split("LUFS")[0])
    P = float(s.split("Peak:")[1].split("dBFS")[0])
    return I, P


def smooth(g, sec):
    k = int(sec * SR)
    return np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, "same")[k:-k]


def audio():
    master = BUILD / "mix.wav"
    n = int(round(END / FPS * SR))
    # dialogue: pilot polish chain, placed at voice_at
    vpol = BUILD / "voice_pol.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(M / "voice/ep0_take2.mp3"), "-af", VOICE_FX + ",loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", str(vpol)])
    v = load_wav(vpol)
    dia = np.zeros((n, 2), np.float32)
    s = int(TL["voice_at"] * SR)
    dia[s:s + len(v)] = v[: n - s]
    # music: track t=0 at MUSIC_AT, ducked under the lines (-13 dB) / in gaps (-8 dB), full on the logo card
    mu = load_wav(M / "music/077bbd23-cc16-4c61-a5b8-8ca12d30e386.mp3")
    mus = np.zeros((n, 2), np.float32)
    s = int(MUSIC_AT * SR)
    mus[s:s + len(mu)] = mu[: n - s]
    write_wav(BUILD / "music_raw.wav", mus)
    Im, _ = lufs(BUILD / "music_raw.wav")
    mus *= 10 ** ((-14.0 - Im) / 20)
    g = np.full(n, -8.0)
    for L in TL["lines"]:
        g[max(0, int((L["t0"] - 0.15) * SR)):int((L["t1"] + 0.1) * SR)] = -13.0
    g[int(CART_END / FPS * SR):] = -3.0
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
    info = dict(master_lufs=I2, master_true_peak=P2, dialogue_lufs=Id, music_lufs=Imu, music_at=MUSIC_AT, final_hit_reel=FINAL_HIT,
                end_frame=END)
    (BUILD / "audio.json").write_text(json.dumps(info, indent=1))
    print("audio", info, flush=True)
    return master


def mux(vid, master):
    out = OUT / f"pip_gus_ep0_{a.ver}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-i", str(master), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
         "-b:a", "256k", "-ar", "48000", "-t", f"{END / FPS:.5f}", "-movflags", "+faststart", str(out)])
    print("DONE", out, nframes(out), flush=True)
    return out


steps = a.steps.split(",")
gm = gfx() if "gfx" in steps or "picture" in steps else None
vid = picture(gm) if "picture" in steps else BUILD / "video.mp4"
mas = audio() if "audio" in steps else BUILD / "mix.wav"
if "mux" in steps:
    mux(vid, mas)
