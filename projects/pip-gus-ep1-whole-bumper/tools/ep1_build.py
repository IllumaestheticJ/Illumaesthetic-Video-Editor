"""Ep 1 assembly: cartoon frames + real IS350 section + captions/logo overlay + dialogue/music mix -> final mp4.

  python3 tools/ep1_build.py [--ver v1] [--steps gfx,picture,audio,mux]

Inputs (media, not in git):
  frames  /home/user/media/work/ep1/frames/<shot>/<frame>.png              (tools/ep1_anim.py)
  real    /home/user/media/pip-gus-ep3-whole-bumper/ref/explainer_full_v5.mp4  frames 989-1132 = the pilot's owner-approved
          real section (IS350 handheld scan -> sprayed front -> hard 1:1 cut to the scan on frame 1061), no text on it
  voice   /home/user/media/pip-gus-ep3-whole-bumper/voice/ep1_take2_fe0cc2e8.mp3   (approved take 2)
  music   /home/user/media/pip-gus-ep3-whole-bumper/music/077bbd23-....mp3      (pilot's inquisitive_A bed, Higgsfield job 077bbd23)

Timeline (30 fps): cartoon 0-1424 | real 1425-1568 (1:1 cut at 1497) | logo card 1569-END.
Music: the pilot's three 2-bar back-jumps in the intro (beats 10->2, 14->6, 30->22) stretch the track by 14.4 s; it starts at
MUSIC_AT so a beat lands on the hand-off (1425), the 1:1 cut (1497) and the logo card (1569); bass lift at ~33.7 s; final chord
under the logo card.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
M = Path("/home/user/media/pip-gus-ep3-whole-bumper")
WK = Path("/home/user/media/work/ep1")
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
TL = json.loads((PROJ / "ep1_timeline.json").read_text())
LN = {L["n"]: L for L in TL["lines"]}
SHOTS = [(s["id"], s["f0"], s["f1"]) for s in TL["shots"]]
CART_END = TL["total_frames"]            # 1425 = hand-off to the real section
REAL_SRC = M / "ref/explainer_full_v5.mp4"
REAL_F0, REAL_N = 989, 144               # pilot frames 989-1132
LOGO_AT = CART_END + REAL_N              # 1569
BEAT0, BEAT = 0.0203, 0.60001
JUMPS = [(10, 2), (14, 6), (30, 22)]
XF = 0.008
EXTRA = sum((f - t) * BEAT for f, t in JUMPS)          # 14.4 s
MUSIC_AT = CART_END / FPS - BEAT0 - 79 * BEAT          # ~0.08 s: beat 79 of the stretched track on the hand-off
FINAL_HIT = MUSIC_AT + 38.42 + EXTRA                   # reel ~52.9 s, 0.6 s into the logo card
END = int(round((FINAL_HIT + 1.5) * FPS))
VOICE_FX = ("highpass=f=90:poles=2,equalizer=f=3500:t=q:w=1.1:g=3,treble=g=2:f=9000:t=s:w=0.7,"
            "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:knee=4:makeup=3")   # pilot v2 polish (owner: brighter)
CAP = dict(PIP="#619f73", GUS="#ecefec")
BRAND = {"accent": "#619f73", "onAccent": "#0b0c0b", "ink": "#ecefec", "bg": "#0b0c0b", "sub": "#d4d9d4", "sub2": "#c8cec8",
         "label": "#a8b0a8", "dim55": "rgba(236,239,236,0.55)", "dim50": "rgba(236,239,236,0.5)", "plate": "rgba(11,12,11,0.58)",
         "cap": "rgba(11,12,11,0.55)"}
FIX = {"Yup.": "Yep.", "So,": "...So", "one.": "one!", "No.": "...No.", "If": "If"}   # spoken = script wording
# captions: (line, [[word idx], ...], centre y)
PAGES = [
    (1, [[0, 1, 2, 3], [4, 5, 6, 7]], 1520),
    (2, [[0], [1, 2, 3]], 1520), (2, [[4, 5]], 1520),
    (3, [[0, 1, 2], [3, 4, 5]], 1540), (3, [[6, 7, 8], [9, 10, 11]], 1540),
    (4, [[0, 1, 2, 3], [4]], 1560),
    (5, [[0, 1], [2, 3, 4]], 1560),
    (6, [[0, 1, 2, 3]], 1520),
    (7, [[0]], 1790), (7, [[1, 2, 3], [4, 5, 6]], 1760),   # v1.1: low, clear of the bill tags
    (8, [[0, 1, 2], [3, 4, 5]], 1560),
    (9, [[0, 1, 2], [3, 4, 5]], 1540),
    (10, [[0, 1, 2, 3], [4, 5]], 1540), (10, [[6, 7, 8], [9, 10, 11, 12]], 1540),
    (10, [[13, 14, 15]], 1560), (10, [[16, 17, 18], [19, 20, 21]], 1560),
    (11, [[0, 1, 2], [3, 4, 5]], 1540),
    (12, [[0, 1, 2]], 1560), (12, [[3, 4, 5, 6]], 1560),
    (13, [[0, 1, 2, 3]], 1540),
    (14, [[0, 1, 2, 3]], 1540),
]


def word(w):
    return FIX.get(w, w)


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
                        lines=[[dict(w=word(ws[k]["w"]), t0=ws[k]["t0"]) for k in row] for row in rows]))
    used = sorted(k for n_, rows, _ in PAGES for k in sum(rows, []) if True)
    for n in LN:   # every word captioned exactly once
        ks = sorted(k for n_, rows, _ in PAGES if n_ == n for k in sum(rows, []))
        assert ks == list(range(len(LN[n]["words"]))), (n, ks)
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
             "items": [{"kind": "logo", "t0": LOGO_AT / FPS, "t1": END / FPS + 1, "cta": ""}]}
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
def real_frames():
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(REAL_SRC), "-vf", f"select='between(n\\,{REAL_F0}\\,{REAL_F0 + REAL_N - 1})'",
                            "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    out = []
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        out.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    dec.wait()
    assert len(out) == REAL_N, len(out)
    return out


def picture(gmov):
    vid = BUILD / "video.mp4"
    fr_dir = Path(a.frames)
    newest = max(p.stat().st_mtime for s, _, _ in SHOTS for p in (fr_dir / s).glob("*.png"))
    key = f"{gmov.name}|{newest:.0f}"
    stamp = BUILD / "video.key"
    if vid.exists() and nframes(vid) == END and stamp.exists() and stamp.read_text() == key:
        return vid
    real = real_frames()
    tmpv = BUILD / "video_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                            str(tmpv)], stdin=subprocess.PIPE)
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gmov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE,
                          bufsize=10 ** 8)
    shot_of = {fr: s for s, f0, f1 in SHOTS for fr in range(f0, f1)}
    qa = dict(text_over_footage_alpha_max=0.0)
    for fr in range(END):
        foot = False
        if fr < CART_END:
            p = fr_dir / shot_of[fr] / f"{fr:04d}.png"
            im = cv2.imread(str(p), cv2.IMREAD_COLOR)
            if im is None:
                raise SystemExit(f"missing frame {p}")
            img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        elif fr < LOGO_AT:
            img = real[fr - CART_END]
            foot = True
        else:
            img = np.zeros((H, W, 3), np.uint8)
        ga = np.frombuffer(gp.stdout.read(W * H * 4), np.uint8).reshape(H, W, 4)
        al = ga[:, :, 3:4].astype(np.float32) / 255.0
        if foot:   # rule: no text over real footage
            qa["text_over_footage_alpha_max"] = max(qa["text_over_footage_alpha_max"], float(al.max()))
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
    return float(s.split("I:")[1].split("LUFS")[0]), float(s.split("Peak:")[1].split("dBFS")[0])


def smooth(g, sec):
    k = int(sec * SR)
    return np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, "same")[k:-k]


def bt(k):
    return BEAT0 + k * BEAT


def stretched_music(mu):
    """Play the track with the pilot's 2-bar back-jumps (8 ms equal-power crossfades centred before each grid beat)."""
    segs, cur = [], 0.0
    for f, t in JUMPS:
        segs.append((cur, bt(f) - XF)); cur = bt(t) - XF
    segs.append((cur, len(mu) / SR))
    out = []
    xf = int(2 * XF * SR)
    for i, (s0, s1) in enumerate(segs):
        seg = mu[int(s0 * SR):int(s1 * SR) + (xf if i < len(segs) - 1 else 0)].copy()
        if out:
            ramp = np.sin(np.linspace(0, np.pi / 2, xf))[:, None]
            tail = out[-1][-xf:]
            seg[:xf] = seg[:xf] * ramp + tail * np.cos(np.linspace(0, np.pi / 2, xf))[:, None]
            out[-1] = out[-1][:-xf]
        out.append(seg)
    return np.concatenate(out)


def audio():
    master = BUILD / "mix.wav"
    n = int(round(END / FPS * SR))
    vpol = BUILD / "voice_pol.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(M / "voice/ep1_take2_fe0cc2e8.mp3"), "-af", VOICE_FX + ",loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", str(vpol)])
    v = load_wav(vpol)
    dia = np.zeros((n, 2), np.float32)
    s = int(TL["lead"] * SR)
    dia[s:s + len(v)] = v[: n - s]
    mu = stretched_music(load_wav(M / "music/077bbd23-cc16-4c61-a5b8-8ca12d30e386.mp3"))
    mus = np.zeros((n, 2), np.float32)
    s = int(MUSIC_AT * SR)
    mus[s:s + len(mu)] = mu[: n - s]
    write_wav(BUILD / "music_raw.wav", mus)
    Im, _ = lufs(BUILD / "music_raw.wav")
    mus *= 10 ** ((-14.0 - Im) / 20)
    g = np.full(n, -8.0)
    for L in TL["lines"]:
        g[max(0, int((L["t0"] - 0.15) * SR)):int((L["t1"] + 0.1) * SR)] = -13.0
    g[int(CART_END / FPS * SR):] = -3.0      # real section + logo: music carries it
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
                final_hit_reel=round(FINAL_HIT, 3), end_frame=END, logo_at=LOGO_AT, handoff=CART_END)
    (BUILD / "audio.json").write_text(json.dumps(info, indent=1))
    print("audio", info, flush=True)
    return master


def mux(vid, master):
    out = OUT / f"pip_gus_ep1_{a.ver}.mp4"
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
