"""Ep 8 full build: cartoon frames (+ the print timelapse corner-pinned into Pip's phone) -> real print timelapse -> logo card
with Pip's voice-over; word-by-word captions on the cartoon only; dialogue + VO (+ music bed when given) mixed to -14 LUFS.

    python projects/pip-gus-ep7-materials/tools/ep8_build.py [--gfx] [--video] [--audio] [--mux] [--all]
           [--music FILE --music-in S] [--name ep8_v1] [--sheet]

Timeline (30 fps): cartoon 0-1120 (frame 1120 = phone screen full frame) | IRL 1121-1255 (4.5 s) | logo 1256-END.
Phone + IRL play the timelapse as one continuous stretch: reel frame PH0+j (A11 start) shows timelapse frame round(j*225/224)
(226 frames at 24 fps -> 225 reel frames, 1.25x), so the screen plays straight into the full-frame IRL with no jump.
Captions are pages of whole words (owner-approved script wording; whisper times per word). A page never overlaps the phone
screen: the build checks the caption alpha against the key-colour mask on every frame (and the IRL section has no overlay).
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
sys.path.insert(0, str(REPO / "projects/lexus-is350-reels/tools"))
from build import load, write_wav, lufs, nframes  # noqa: E402
from reels import BRAND  # noqa: E402

M = Path("/home/user/media/pip-gus-ep7-materials")
FR, BUILD, OUT = M / "frames", M / "build", M / "out"
FPS, SR, W, H = 30, 48000, 1080, 1920
TL = json.loads((PROJ / "ep8_timeline.json").read_text())
CART = TL["frames"]                      # 1121
PH0 = next(x["f0"] for x in TL["shots"] if x["id"] == "A11")   # first phone frame
IRL_N = 135                              # 4.5 s
LOGO_N = 150                             # 5.0 s: VO 4.0 s from +0.35 s, then a short hold
IRL0, LOGO0 = CART, CART + IRL_N
END = LOGO0 + LOGO_N
VO_AT = LOGO0 / FPS + 0.35
TIMELAPSE = M / "work/irl_mr2_print_9x16.mp4"
CAP = dict(PIP="#619f73", GUS="#ecefec")

# caption text per line: (display word, whisper word index whose start time it takes)
WORDS = {
    1: [("Printer's", 0), ("ready!", 1), ("What", 2), ("do", 3), ("we", 4), ("load", 5), ("in", 6), ("it?", 7)],
    2: [("This", 0), ("one!", 1), ("PLA!", 2)],
    3: [(w, i) for i, w in enumerate("Sure. Print a vent and leave it in the sun.".split())],
    4: [("...It's", 0), ("melting!", 1)],
    5: [("PLA's", 0), ("easy", 3), ("to", 4), ("print.", 5), ("It", 6), ("just", 7), ("hates", 8), ("heat.", 9)],
    6: [("Inside", 0), ("the", 1), ("car?", 2), ("PETG.", 3), ("Tougher,", 5), ("handles", 6), ("more", 7), ("heat.", 8)],
    7: [(w, i) for i, w in enumerate("So I'll print it in black!".split())],
    8: [("...Black", 0), ("PETG", 1), ("still", 3), ("melts", 4), ("in", 5), ("the", 6), ("sun.", 7)],
    9: [("And", 0), ("my", 2), ("bumper?", 3)],
    10: [("Outside?", 0), ("ASA.", 1), ("It's", 4), ("made", 5), ("for", 6), ("sun", 7), ("and", 8), ("rain.", 9)],
    14: [("And", 0), ("it", 1), ("depends", 2), ("what", 3), ("it's", 4), ("for.", 5), ("Molds", 6), ("and", 7), ("masters?", 8),
         ("PETG.", 9), ("Things", 10), ("don't", 11), ("stick", 12), ("to", 13), ("it.", 14), ("Or", 15), ("ASA-GF.", 16),
         ("Warps", 21), ("less,", 22), ("nicer", 23), ("finish.", 24)],
    15: [("Like", 0), ("these?!", 1)],
    16: [("...Yeah.", 0), ("Like", 1), ("those.", 2)],
}
A12_0 = next(x["f0"] for x in TL["shots"] if x["id"] == "A12")
CAP_END_MAX = {16: (A12_0 + 54) / FPS}  # last page at the bottom edge: the growing phone screen reaches y 1715 on A12 frame +54 (v1: 1114)
Y = 1420  # default page centre y (lower third, under the faces)
PAGES = [  # (line, rows of display-word indices[, centre y])
    (1, [[0, 1]]), (1, [[2, 3, 4], [5, 6, 7]]),
    (2, [[0, 1], [2]], 950),          # off Pip's sage hoodie (sage text on sage did not read)
    (3, [[0]]), (3, [[1, 2, 3], [4, 5, 6, 7, 8, 9]]),
    (4, [[0, 1]]),
    (5, [[0, 1, 2, 3]]), (5, [[4, 5, 6, 7]]),
    (6, [[0, 1, 2], [3]]), (6, [[4, 5, 6, 7]]),
    (7, [[0, 1, 2], [3, 4, 5]]),
    (8, [[0, 1], [2, 3, 4, 5, 6]]),
    (9, [[0, 1, 2]], 950),
    (10, [[0, 1]]), (10, [[2, 3, 4], [5, 6, 7]]),
    (14, [[0, 1, 2], [3, 4, 5]]), (14, [[6, 7, 8]]), (14, [[9]]), (14, [[10, 11, 12], [13, 14]]), (14, [[15, 16]]),
    (14, [[17, 18], [19, 20]]),
    (15, [[0, 1]], 1790),
    (16, [[0, 1, 2]], 1790),
]


def pages():
    L = {l["n"]: l for l in TL["lines"]}
    out = []
    for i, (n, rows, *y) in enumerate(PAGES):
        l, ws = L[n], WORDS[n]
        t = lambda k: l["words"][ws[k][1]]["t0"]  # noqa: E731
        last = rows[-1][-1]
        wi = ws[last + 1][1] - 1 if last + 1 < len(ws) else len(l["words"]) - 1   # a display word can span several whisper tokens (A -S -A G -F.)
        t1 = min(l["words"][wi]["t1"] + 0.35, l["t1"] + 0.2, CAP_END_MAX.get(n, 99))
        if i + 1 < len(PAGES):
            nn, nrows = PAGES[i + 1][:2]
            t1 = min(t1, L[nn]["words"][WORDS[nn][nrows[0][0]][1]]["t0"])
        out.append(dict(t0=t(rows[0][0]), t1=round(t1, 3), color=CAP[l["speaker"]], y=y[0] if y else Y, cx=540,
                        lines=[[dict(w=ws[k][0], t0=t(k)) for k in row] for row in rows]))
    assert out[-1]["t1"] * FPS <= CART - 1
    return out


def props():
    items = [{"kind": "logo", "t0": LOGO0 / FPS, "t1": END / FPS + 1, "cta": ""}]
    return {"fps": FPS, "durationInFrames": END, "items": items, "pages": pages(), "palette": BRAND, "size": 88}


def gfx():
    js = json.dumps(props(), indent=1)
    (PROJ / "gfx_props.json").write_text(js)
    h = hashlib.sha1((js + (REPO / "remotion/src/gfx/reel/ExplainerGfx.tsx").read_text() + (REPO / "remotion/src/gfx/reel/ReelGfx.tsx").read_text()).encode()).hexdigest()[:10]
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
def shot_of(fr):
    for s in TL["shots"]:
        if s["f0"] <= fr < s["f1"]:
            return s["id"]
    raise KeyError(fr)


def timelapse():
    cap = cv2.VideoCapture(str(TIMELAPSE))
    fs = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        fs.append(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
    n = CART + IRL_N - PH0
    return [fs[min(len(fs) - 1, int(round(j * (len(fs) - 1) / (n - 1))))] for j in range(n)], len(fs)


def composite(img, foot, corners):
    Mx = cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), np.float32(corners))
    warp = cv2.warpPerspective(foot, Mx, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    f = img.astype(np.float32)
    mag = np.minimum(f[..., 0], f[..., 2]) - f[..., 1]
    m = np.clip((mag - 40) / 80, 0, 1)[..., None]
    spill = mag > 15
    f[spill, 0] = np.minimum(f[spill, 0], f[spill, 1] + 8)
    f[spill, 2] = np.minimum(f[spill, 2], f[spill, 1] + 8)
    return (f * (1 - m) + warp * m).clip(0, 255).astype(np.uint8), m[..., 0] > 0.02


def frames():
    """Yields (rgb frame, irl mask or None) for every reel frame."""
    corn = json.loads((FR / "screen_corners.json").read_text())["shots"]
    tl, _ = timelapse()
    full = np.ones((H, W), bool)
    for fr in range(CART):
        img = cv2.cvtColor(cv2.imread(str(FR / shot_of(fr) / f"{fr:04d}.png")), cv2.COLOR_BGR2RGB)
        if fr >= PH0:
            if fr == CART - 1:
                yield tl[fr - PH0], full
                continue
            c = corn[shot_of(fr)]["per_frame"][str(fr)]
            img, mk = composite(img, tl[fr - PH0], c)
            yield img, mk
        else:
            yield img, None
    for j in range(IRL_N):
        yield tl[CART - PH0 + j], full
    for _ in range(LOGO_N):
        yield np.zeros((H, W, 3), np.uint8), None


def picture(gmov, name, sheet=False):
    vid = BUILD / f"{name}_video.mp4"
    tmpv = BUILD / "video_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", str(tmpv)],
                           stdin=subprocess.PIPE)
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gmov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE, bufsize=10 ** 8)
    bad, n = [], 0
    for fr, (img, irlm) in enumerate(frames()):
        ga = np.frombuffer(gp.stdout.read(W * H * 4), np.uint8).reshape(H, W, 4)
        if irlm is not None and ga[:, :, 3][irlm].max() > 0:
            bad.append(fr)
        al = ga[:, :, 3:4].astype(np.float32) / 255.0
        out = img.astype(np.float32) * (1 - al) + ga[:, :, :3].astype(np.float32) * al
        enc.stdin.write((out + 0.5).astype(np.uint8).tobytes())
        n += 1
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    assert n == END, (n, END)
    assert not bad, f"caption pixels over IRL footage on frames {bad[:10]}"
    tmpv.rename(vid)
    print("picture", vid, n, flush=True)
    return vid


# ------------------------------------------------------------------ audio
def smooth(env, tau):
    from scipy.signal import lfilter
    k = np.exp(-1 / (tau * SR))
    s = lfilter([1 - k], [1, -k], env)
    return lfilter([1 - k], [1, -k], s[::-1])[::-1]


def place(buf, x, t):
    i = int(round(t * SR)); x = x[: len(buf) - i]
    buf[i:i + len(x)] += x


def audio(name, music=None, music_in=0.0):
    n = int(round(END / FPS * SR))
    dbuf = np.zeros((n, 2), np.float32)
    place(dbuf, load(M / "voice/ep8_dialogue.wav"), 0.0)
    place(dbuf, load(M / "voice/ep8_vo.wav"), VO_AT)
    mix = dbuf.copy()
    info = dict(vo_at=VO_AT, music=str(music) if music else None)
    if music:
        mus = load(Path(music), music_in, n / SR + 0.1)[:n]
        if len(mus) < n:
            mus = np.vstack([mus, np.zeros((n - len(mus), 2), np.float32)])
        write_wav(BUILD / "music_raw.wav", mus)
        I_m, _ = lufs(BUILD / "music_raw.wav")
        mus = mus * 10 ** ((-14.0 - I_m) / 20)
        g = np.full(n, -9.0)                                    # bed under the cartoon, ducked under speech
        for l in TL["lines"]:
            g[max(0, int((l["t0"] - 0.15) * SR)):int((l["t1"] + 0.1) * SR)] = -15.0
        g[int((VO_AT - 0.15) * SR):int((VO_AT + 4.1) * SR)] = -15.0
        t_irl = IRL0 / FPS
        g[int(t_irl * SR):int(LOGO0 / FPS * SR)] = 0.0         # IRL: the bed opens up (no speech)
        g = smooth(g, 0.08)
        lin = 10 ** (g / 20)
        f0 = int((END / FPS - 1.2) * SR)
        lin[f0:] *= np.cos(np.linspace(0, np.pi / 2, n - f0)) ** 1.5
        lin[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
        mus = mus * lin[:, None]
        mix = mix + mus
        info.update(music_in=music_in, music_ref_lufs=I_m)
    write_wav(BUILD / "pre.wav", mix)
    I, _ = lufs(BUILD / "pre.wav")
    gain, master = -14.0 - I, OUT / f"{name}_mix.wav"
    for _ in range(6):
        write_wav(BUILD / "gain.wav", mix * 10 ** (gain / 20))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / "gain.wav"), "-af",
                        "aresample=192000,alimiter=limit=0.79:attack=1:release=60:level=disabled,aresample=48000", "-c:a", "pcm_s24le", str(master)], check=True)
        I2, P2 = lufs(master)
        if abs(I2 + 14.0) <= 0.2:
            break
        gain += -14.0 - I2
    info.update(master_lufs=I2, master_true_peak=P2, gain_db=gain)
    (BUILD / f"{name}_audio.json").write_text(json.dumps(info, indent=1))
    print("audio", info, flush=True)
    return master


def mux(name):
    out = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / f"{name}_video.mp4"), "-i", str(OUT / f"{name}_mix.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{END / FPS:.5f}", "-movflags", "+faststart", str(out)], check=True)
    print("DONE", out, nframes(out), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ("gfx", "audio", "video", "mux", "all"):
        ap.add_argument(f"--{k}", action="store_true")
    ap.add_argument("--name", default="ep8_v1")
    ap.add_argument("--music", default=None)
    ap.add_argument("--music-in", type=float, default=0.0)
    a = ap.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    if a.audio or a.all:
        audio(a.name, a.music, a.music_in)
    if a.gfx or a.video or a.all:
        gm = gfx()
    if a.video or a.all:
        picture(gm, a.name)
    if a.mux or a.all:
        mux(a.name)
