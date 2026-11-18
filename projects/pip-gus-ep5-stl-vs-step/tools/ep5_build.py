"""Pip & Gus Ep 5 full build: cartoon (E1-E12) + real section (NSX bumper scan -> STEP -> colour map) + closing card,
word-by-word captions on the cartoon only, music bed (pilot track inquisitive_A) and mix.

    python projects/pip-gus-ep5-stl-vs-step/tools/ep5_build.py --all [--name pip_gus_ep5_v1] [--frames DIR] [--real DIR]

Timeline from ep5_timeline.json (frames, 30 fps): E1..E12 cartoon | REAL (132 frames, plays full frame; its first frame is
corner-pinned into Pip's phone screen during E12's push) | CARD (logo + "WHAT SOFTWARE DO YOU USE TO DESIGN PARTS?", L16/L17
as voice only, no captions).
Music: inquisitive_A (100.00 BPM, beat0 0.0203 s, beat 0.6 s; bass entry = bar 8 = beat 32; final chord bar 16 = beat 64).
The intro is extended with 2-bar back-jumps (the pilot's spectrally checked splices, (30->22) used three times) so the bass
entry lands on the first REAL frame; after it, the pilot v3 route lift -> bar 9 -> jump (40->56) -> bars 14, 15 -> final
chord, so the chord lands just after Gus's last line and rings out under the logo.
Rules checked: no overlay pixels on the real section; captions end before REAL.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
sys.path.insert(0, str(REPO / "projects/lexus-is350-reels/tools"))
from build import load, place, write_wav, lufs, nframes  # noqa: E402
from reels import BRAND  # noqa: E402

FPS, SR, W, H = 30, 48000, 1080, 1920
WORK = Path("/home/user/media/work/ep5")
BUILD = WORK / "build"
TL = json.loads((PROJ / "ep5_timeline.json").read_text())
SF = {s["id"]: (s["f0"], s["f1"]) for s in TL["shots"]}
END = TL["frames"]
CAP = dict(PIP="#619f73", GUS="#ecefec")
CTA = "WHAT SOFTWARE DO YOU USE\nTO DESIGN PARTS?"         # owner, 2026-11-17
TRACK = Path("/home/user/media/pip-gus-ep5/music/inquisitive_A.mp3")
DIALOGUE = Path("/home/user/media/pip-gus-ep5/voice/ep5_dialogue.wav")
BEAT0, BEAT = 0.0203, 0.60001
LIFT_BEAT = 32
JUMPS = [(10, 2), (14, 6), (30, 22), (30, 22), (30, 22)]   # 2-bar back-jumps in the intro (pilot splices)
POST_JUMPS = [(40, 56)]                                    # lift -> bar 9 -> bars 14, 15 -> final chord (pilot v3 route)
XF = 0.008
TAIL_FADE = 0.3
KEY = np.array([255, 0, 255], np.int16)


def bt(k):
    return BEAT0 + k * BEAT


# ------------------------------------------------------------------ captions
def pages():
    """One page per sentence (max 2 rows of <= 4 words), cartoon lines 1-15 only; words from the measured take (brand and
    NURBS spelled right). A page leaves 0.35 s after its last word, or when the next page starts."""
    out = []
    lines = [l for l in TL["lines"] if l["n"] <= 15]
    for l in lines:
        ws = l["words"]
        sent, cur = [], []
        for k, w in enumerate(ws):
            cur.append(k)
            if w["w"].rstrip().endswith((".", "?", "!")) or len(cur) == 6:
                sent.append(cur); cur = []
        if cur:
            sent.append(cur)
        for s in sent:
            rows = [s[:4], s[4:]] if len(s) > 4 else [s]
            rows = [r for r in rows if r]
            out.append(dict(t0=ws[s[0]]["t0"], t1=ws[s[-1]]["t1"] + 0.35, color=CAP[l["speaker"]], y=Y_OF.get(l["n"], 1330),
                            cx=500, lines=[[dict(w=ws[k]["w"], t0=ws[k]["t0"]) for k in r] for r in rows]))
    for a, b in zip(out, out[1:]):
        a["t1"] = round(min(a["t1"], b["t0"]), 3)
    real0 = SF["REAL"][0] / FPS
    out[-1]["t1"] = round(min(out[-1]["t1"], real0 - 2 / FPS), 3)
    assert all(p["t1"] * FPS < SF["REAL"][0] for p in out), "caption over the real section"
    return out


Y_OF = {}          # per-line caption centre y overrides (set by eye after the first full cut)


def props():
    c0 = SF["CARD"][0] / FPS
    items = [{"kind": "logo", "t0": c0, "t1": END / FPS + 1, "cta": CTA}]
    return {"fps": FPS, "durationInFrames": END, "items": items, "pages": pages(), "palette": BRAND, "size": 88}


def gfx():
    js = json.dumps(props(), indent=1)
    (PROJ / "gfx_props.json").write_text(js)
    h = hashlib.sha1((js + (REPO / "remotion/src/gfx/reel/ExplainerGfx.tsx").read_text()
                      + (REPO / "remotion/src/gfx/reel/ReelGfx.tsx").read_text()).encode()).hexdigest()[:10]
    mov = BUILD / f"gfx_{h}.mov"
    if not mov.exists():
        pj = BUILD / "gfx_props.json"; pj.write_text(js)
        tmp = BUILD / f"tmp_gfx_{h}.mov"
        subprocess.run(["nice", "-n", "5", "npx", "remotion", "render", "ExplainerGfx", str(tmp), f"--props={pj}", "--codec=prores",
                        "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png", "--concurrency=2", "--log=error"],
                       cwd=REPO / "remotion", check=True)
        tmp.rename(mov)
    return mov


# ------------------------------------------------------------------ picture
def read_png(p):
    im = cv2.imread(str(p), cv2.IMREAD_COLOR)
    assert im is not None, p
    if im.shape[:2] != (H, W):
        im = cv2.resize(im, (W, H), interpolation=cv2.INTER_LANCZOS4)
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


def pin_screen(fr, corners, src):
    """Corner-pin src (9:16) into the phone screen; the key colour is the matte (anything over the screen stays)."""
    h, w = src.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(corners))
    warped = cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_LINEAR)
    d = np.abs(fr.astype(np.int16) - KEY).sum(2)
    a = np.clip((120 - d) / 80.0, 0, 1)[..., None]
    return (fr * (1 - a) + warped * a).astype(np.uint8)


def picture(gmov, frames_dir, real_dir):
    vid = BUILD / "video.mp4"
    if vid.exists() and nframes(vid) == END:
        return vid
    corners = json.loads((frames_dir / "screen_corners.json").read_text())["shots"]["E12"]["per_frame"]
    real0 = read_png(real_dir / "f_0000.png")
    tmpv = BUILD / "video_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                            "-movflags", "+faststart", str(tmpv)], stdin=subprocess.PIPE)
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gmov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE,
                          bufsize=10 ** 8)
    bg = np.array([int(BRAND["bg"][i:i + 2], 16) for i in (1, 3, 5)], np.uint8)
    rep, real_alpha = [], 0.0
    for f in range(END):
        sid = next(s["id"] for s in TL["shots"] if s["f0"] <= f < s["f1"])
        if sid == "REAL":
            fr = read_png(real_dir / f"f_{f - SF['REAL'][0]:04d}.png")
        elif sid == "CARD":
            fr = np.empty((H, W, 3), np.uint8); fr[:] = bg
        else:
            fr = read_png(frames_dir / sid / f"{f:04d}.png")
            if sid == "E12":
                fr = pin_screen(fr, corners[str(f)], real0)
        ga = np.frombuffer(gp.stdout.read(W * H * 4), np.uint8).reshape(H, W, 4)
        if sid == "REAL":
            real_alpha = max(real_alpha, float(ga[:, :, 3].max()))
        al = ga[:, :, 3:4].astype(np.float32) / 255.0
        out = fr.astype(np.float32) * (1 - al) + ga[:, :, :3].astype(np.float32) * al
        enc.stdin.write((out + 0.5).astype(np.uint8).tobytes())
        if f % 150 == 0:
            print("frame", f, sid, flush=True)
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    assert real_alpha == 0.0, f"overlay pixels on the real section (alpha max {real_alpha})"
    tmpv.rename(vid)
    return vid


# ------------------------------------------------------------------ audio
def smooth(env, tau):
    from scipy.signal import lfilter
    k = np.exp(-1 / (tau * SR))
    s = lfilter([1 - k], [1, -k], env)
    return lfilter([1 - k], [1, -k], s[::-1])[::-1]


def extra_lead():
    return SF["REAL"][0] / FPS - (bt(LIFT_BEAT) + sum(bt(a) - bt(b) for a, b in JUMPS))


def music(n):
    t_lift = SF["REAL"][0] / FPS
    extra = sum(bt(a) - bt(b) for a, b in JUMPS)
    s0 = bt(LIFT_BEAT) + extra - t_lift
    lead = max(0.0, -s0)                                    # track enters `lead` s into the reel (pilot: 0.654 s)
    s0 = max(0.0, s0)
    segs, cur = [], s0
    for a, b in JUMPS + POST_JUMPS:
        segs.append((cur, bt(a) - XF)); cur = bt(b) - XF
    segs.append((cur, None))
    x = load(TRACK)
    out, xf = [], int(XF * SR)
    for i, (a, b) in enumerate(segs):
        ia = int(round(a * SR)); ib = len(x) if b is None else int(round(b * SR))
        out.append(x[ia - (xf if i else 0): ib + (xf if b is not None else 0)].copy())
    y = out[0]
    for seg in out[1:]:
        k = 2 * xf
        ramp = np.linspace(0, np.pi / 2, k)[:, None]
        y = np.vstack([y[:-k], y[-k:] * np.cos(ramp) + seg[:k] * np.sin(ramp), seg[k:]])
    if lead:
        y = np.vstack([np.zeros((int(round(lead * SR)), 2), np.float32), y])
    y = y[:n]
    if len(y) < n:
        y = np.vstack([y, np.zeros((n - len(y), 2), np.float32)])
    return y.astype(np.float32), s0


def audio(name):
    master = WORK / f"{name}_mix.wav"
    n = int(round(END / FPS * SR))
    t_lift = SF["REAL"][0] / FPS
    mus, s0 = music(n)
    write_wav(BUILD / "music_raw.wav", mus)
    write_wav(BUILD / "music_B.wav", mus[int(t_lift * SR):])
    I_B, _ = lufs(BUILD / "music_B.wav")
    mus = mus * 10 ** ((-14.0 - I_B) / 20)
    g = np.full(n, -8.0)
    for l in TL["lines"]:
        a, b = int((l["t0"] - 0.15) * SR), int((l["t1"] + 0.1) * SR)
        g[max(0, a):b] = -13.0
    g = smooth(g, 0.08)
    pa, ramp0 = int(t_lift * SR), int((t_lift - 0.25) * SR)
    g[ramp0:pa] = np.linspace(g[ramp0], 0.0, pa - ramp0)
    card0 = int(SF["CARD"][0] / FPS * SR)
    g[pa:card0] = 0.0                                       # real section: music up (no voice)
    lin = 10 ** (g / 20)
    f0 = int((END / FPS - TAIL_FADE) * SR)
    lin[f0:] *= np.cos(np.linspace(0, np.pi / 2, n - f0)) ** 1.5
    l0 = int(round(max(0.0, extra_lead()) * SR))
    lin[l0:l0 + int(0.08 * SR)] *= np.linspace(0, 1, int(0.08 * SR))
    mus_d = mus * lin[:, None]
    dia = load(DIALOGUE)
    dbuf = np.zeros((n, 2), np.float32); place(dbuf, dia[:n], 0.0)
    mix = mus_d + dbuf
    write_wav(BUILD / "pre.wav", mix)
    I, _ = lufs(BUILD / "pre.wav")
    gain = -14.0 - I
    for _ in range(6):
        write_wav(BUILD / "gain.wav", mix * 10 ** (gain / 20))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / "gain.wav"), "-af",
                        "aresample=192000,alimiter=limit=0.79:attack=1:release=60:level=disabled,aresample=48000",
                        "-c:a", "pcm_s24le", str(master)], check=True)
        I2, P2 = lufs(master)
        if abs(I2 + 14.0) <= 0.2:
            break
        gain += -14.0 - I2
    info = dict(track_s0=round(s0, 4), jumps=JUMPS, post_jumps=POST_JUMPS, lift_frame=SF["REAL"][0],
                final_chord_reel_s=round(t_lift + (bt(64) - bt(56)) + (bt(40) - bt(32)), 3), master_lufs=I2, true_peak=P2)
    (BUILD / "audio.json").write_text(json.dumps(info, indent=1))
    print("audio", info, flush=True)
    return master


def mux(name, master):
    out = WORK / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / "video.mp4"), "-i", str(master), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{END / FPS:.5f}", "-movflags", "+faststart",
                    str(out)], check=True)
    print("DONE", out, nframes(out), flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ("gfx", "audio", "video", "mux", "all"):
        ap.add_argument(f"--{k}", action="store_true")
    ap.add_argument("--name", default="pip_gus_ep5_v1")
    ap.add_argument("--frames", default=str(WORK / "frames"))
    ap.add_argument("--real", default=str(WORK / "real"))
    a = ap.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True)
    if a.audio or a.all:
        m = audio(a.name)
    if a.gfx or a.video or a.all:
        gm = gfx()
    if a.video or a.all:
        picture(gm, Path(a.frames), Path(a.real))
    if a.mux or a.all:
        mux(a.name, WORK / f"{a.name}_mix.wav")
