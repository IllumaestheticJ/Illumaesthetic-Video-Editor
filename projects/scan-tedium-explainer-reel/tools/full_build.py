"""Full explainer reel: Part A (cartoon, final) + Part B (real IS350 tail, 1:1 cut) + FULL VIDEO tease card, captions, music, mix.

    python projects/scan-tedium-explainer-reel/tools/full_build.py [--gfx] [--audio] [--video] [--mux] [--all] [--name explainer_full_v1]

Timeline (frames at 30 fps; cut k = first frame of the next shot):
  Part A     0-988   partA_v5.mp4 (frame 988 = phone screen full-frame, FX30541 src frame 7719 at x0 600)
  P2       989-1026  FX30541 from 322.0 s (src 7720 on, R1_SCAN graded 4K intermediate; crop = spans.json R1_SCAN keyframes,
                     600 at 322.0 -> continuous with the phone)
  P7      1027-1064  FX30554, ends on the solved frame 264 (R2_FRONT intermediate, x0 531)
  P8      1065-1140  V_MATCH_FRONT vertical render (clean, *_preview.mp4 from frame 0) - hard 1:1 cut at 1065
  card    1141-1209  FULL VIDEO tease (R3 v3 brand palette) - reel ends on it
Music: P8 of the owner's mix_full.wav, one continuous stretch; its kick return (drop, mix 1169.173 s broadband half-rise)
lands on the hand-off (frame 989); P2->P7 on the next bar line (1170.439), the 1:1 cut on the bar after (1171.705), the card
on the bar after two more (1174.239). Measured with the kick-band/broadband envelopes (see editlog).
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
sys.path.insert(0, str(REPO / "projects/lexus-is350-reels/tools"))
from build import frames_of, load, place, fade, write_wav, lufs, nframes  # noqa: E402
from reels import SPANS, BRAND, SRC_FPS  # noqa: E402

W_ = Path("/home/user/media/work/scan-tedium")
OUT = W_ / "out"
BUILD = W_ / "build_full"
IS = Path("/home/user/media/work/is350-reels")
MIX = Path("/home/user/media/work/is350-long/music/mix_full.wav")
FPS, SR = 30, 48000
W, H = 1080, 1920

A_N = 989
CUTS = dict(p2=989, p7=1027, p8=1065, card=1141, end=1210)
MUSIC = dict(drop_src=1169.173, drop_reel=989 / FPS, fade_s=1.5)
CAP = dict(PIP="#619f73", GUS="#ecefec")

# ------------------------------------------------------------------ captions: pages (word indices per line) + centre y
# y placed by eye on the frames of each page (faces and the phone screen clear; inside x 60-940, y 220-1500).
PAGES = [  # (line n, [[word idx...], [..]], centre y[, centre x (default 500)])
    (1, [[0]], 1330), (1, [[1, 2, 3, 4], [5, 6, 7]], 1330),
    (2, [[0, 1, 2]], 1330, 420), (2, [[3], [4, 5, 6]], 1330, 420),
    (3, [[0, 1, 2, 3]], 1330),
    (4, [[0, 1, 2, 3]], 1330),
    (5, [[0, 1]], 1330),
    (6, [[0, 1], [2, 3]], 1330),
    (7, [[0, 1, 2, 3], [4, 5]], 1330),
    (8, [[0, 1, 2, 3]], 1330),
    (9, [[0]], 1330),
    (10, [[0, 1, 2], [3, 4, 5]], 1330),
    (14, [[0, 1, 2, 3], [4, 5, 6]], 1388),
    (11, [[0]], 1388), (11, [[1, 2, 3], [4, 5]], 1388),
    (12, [[0, 1, 2, 3], [4, 5, 6]], 1330),
    (13, [[0, 1]], 300, 600),
]
TEXT = {  # owner-approved script wording (script.md, v5 table); whisper word times, brand spelled right
    1: "So... how do you scan a whole car?", 2: "The usual way? Dots. Lots of dots.", 3: "One every few inches.",
    4: "Then you scan it?", 5: "In pieces.", 6: "Front. Side. Roof. Back.", 7: "Then I line them all up.", 8: "Is it done yet?",
    9: "No.", 10: "Now we peel the dots off.", 14: "There has to be a better way.", 11: "Wait. I saw an Illumaesthetic video...",
    12: "They did a whole car way faster!", 13: "...Show me.",
}
CAP_END_MAX = {1: 3.2,     # leave before the S2 cut (3.233)
               13: 32.40}  # "Show me." leaves while the growing phone screen is still clear of it


def cuts():
    return json.loads((OUT / "partA_cuts.json").read_text())


def pages():
    L = {l["n"]: l for l in cuts()["lines"]}
    out = []
    for i, (n, rows, y, *cx) in enumerate(PAGES):
        l = L[n]; toks = TEXT[n].split()
        assert len(toks) == len(l["words"]), (n, toks, [w["w"] for w in l["words"]])
        ws = [dict(w=toks[k], t0=l["words"][k]["t0"]) for row in rows for k in row]
        last = l["words"][rows[-1][-1]]["t1"]
        t1 = min(last + 0.35, l["t1"] + 0.2, CAP_END_MAX.get(n, 99))
        if i + 1 < len(PAGES):
            nn, nrows = PAGES[i + 1][:2]
            t1 = min(t1, L[nn]["words"][nrows[0][0]]["t0"])
        out.append(dict(t0=ws[0]["t0"], t1=round(t1, 3), color=CAP[l["speaker"]], y=y, cx=cx[0] if cx else 500,
                        lines=[[dict(w=toks[k], t0=l["words"][k]["t0"]) for k in row] for row in rows]))
    assert out[-1]["t1"] * FPS <= A_N - 1, "caption past Part A"
    return out


def props():
    c0, c1 = CUTS["card"] / FPS, CUTS["end"] / FPS
    items = [{"kind": "tease", "t0": c0, "t1": c1 + 1, "lines": ["HOW LONG", "DID IT TAKE?"], "sub": "FULL VIDEO ON OUR CHANNEL"}]
    return {"fps": FPS, "durationInFrames": CUTS["end"], "items": items, "pages": pages(), "palette": BRAND, "size": 88}


def gfx():
    js = json.dumps(props(), indent=1)
    (PROJ / "gfx_full_props.json").write_text(js)
    h = hashlib.sha1((js + (REPO / "remotion/src/gfx/reel/ExplainerGfx.tsx").read_text() + (REPO / "remotion/src/gfx/reel/ReelGfx.tsx").read_text()).encode()).hexdigest()[:10]
    mov = BUILD / f"gfx_{h}.mov"
    if not mov.exists():
        BUILD.mkdir(parents=True, exist_ok=True)
        pj = BUILD / "gfx_props.json"; pj.write_text(js)
        for old in BUILD.glob("gfx_*.mov"):
            old.unlink()
        subprocess.run(["nice", "-n", "5", "npx", "remotion", "render", "ExplainerGfx", str(mov), f"--props={pj}", "--codec=prores",
                        "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png", "--concurrency=2", "--log=error"],
                       cwd=REPO / "remotion", check=True)
    return mov


# ------------------------------------------------------------------ picture
def x0_at(span, t):
    kf = SPANS[span]["x0"]
    return float(np.interp(t, [k[0] for k in kf], [k[1] for k in kf]))


def irl(span, n, end_on_match=False, t_start=None):
    sp = SPANS[span]; m = json.loads((IS / "src" / f"{span}.json").read_text())
    if end_on_match:
        idx = [sp["match_f"] - int(round((n - 1 - j) * SRC_FPS / FPS)) for j in range(n)]
    else:
        idx = [int(round((t_start + j / FPS) * SRC_FPS)) for j in range(n)]
    loc = [i - m["f0"] for i in idx]
    assert loc[0] >= 0 and loc[-1] < m["n"], (span, loc)
    gen = frames_of(IS / "src" / f"{span}.mov", m["w"], m["h"], loc[0])
    cur, ci = next(gen), loc[0]
    sc = m["w"] / 1920
    log = []
    for j, li in enumerate(loc):
        while ci < li:
            cur, ci = next(gen), ci + 1
        x = int(round(x0_at(span, idx[j] / SRC_FPS) * sc)); x = max(0, min(m["w"] - W, x))
        log.append((idx[j], x))
        yield cur[:, x:x + W], (idx[j], x)


def scan(sid, n):
    mp4 = IS / "renders" / sid / f"{sid}_preview.mp4"
    assert nframes(mp4) >= n
    for j, fr in enumerate(frames_of(mp4, W, H, 0)):
        if j >= n:
            break
        yield fr, (j, None)


def picture(gmov):
    vid = BUILD / "video.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", str(vid)],
                           stdin=subprocess.PIPE)
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gmov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE, bufsize=10 ** 8)
    c = CUTS
    segs = [("partA", frames_of(OUT / "partA_v5.mp4", W, H, 0), A_N),
            ("P2", irl("R1_SCAN", c["p7"] - c["p2"], t_start=322.0), c["p7"] - c["p2"]),
            ("P7", irl("R2_FRONT", c["p8"] - c["p7"], end_on_match=True), c["p8"] - c["p7"]),
            ("P8", scan("V_MATCH_FRONT", c["card"] - c["p8"]), c["card"] - c["p8"]),
            ("card", ((np.zeros((H, W, 3), np.uint8), None) for _ in range(c["end"] - c["card"])), c["end"] - c["card"])]
    rep, f = [], 0
    for name, gen, n in segs:
        k, srcs = 0, []
        for item in gen:
            fr, si = item if isinstance(item, tuple) else (item, None)
            if k >= n:
                break
            ga = np.frombuffer(gp.stdout.read(W * H * 4), np.uint8).reshape(H, W, 4)
            al = ga[:, :, 3:4].astype(np.float32) / 255.0
            out = fr.astype(np.float32) * (1 - al) + ga[:, :, :3].astype(np.float32) * al
            enc.stdin.write((out + 0.5).astype(np.uint8).tobytes())
            srcs.append(si); k += 1; f += 1
        assert k == n, (name, k, n)
        rep.append(dict(seg=name, frame0=f - n, frames=n, src_first=srcs[0], src_last=srcs[-1]))
        print(name, rep[-1], flush=True)
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    assert f == CUTS["end"]
    (BUILD / "picture.json").write_text(json.dumps(rep, indent=1, default=str))
    return vid


# ------------------------------------------------------------------ audio
def smooth(env, tau):
    from scipy.signal import lfilter
    k = np.exp(-1 / (tau * SR))
    s = lfilter([1 - k], [1, -k], env)
    return lfilter([1 - k], [1, -k], s[::-1])[::-1]


def audio():
    n = int(round(CUTS["end"] / FPS * SR))
    t_ho = MUSIC["drop_reel"]
    src0 = MUSIC["drop_src"] - t_ho
    mus = load(MIX, src0, n / SR + 0.1)[:n]
    write_wav(BUILD / "music_raw.wav", mus)
    # level reference: the Part B stretch of the piece (kicks on) -> -14 LUFS before gains
    seg = mus[int(t_ho * SR):]
    write_wav(BUILD / "music_B.wav", seg)
    I_B, _ = lufs(BUILD / "music_B.wav")
    mus = mus * 10 ** ((-14.0 - I_B) / 20)
    # gain curve (dB): Part A bed -13 under speech, -8 in gaps >= 0.6 s; Part B 0 dB from the drop; fade on the card
    t = np.arange(n) / SR
    g = np.full(n, -8.0)
    lines = sorted(cuts()["lines"], key=lambda l: l["t0"])
    for l in lines:
        a, b = int((l["t0"] - 0.15) * SR), int((l["t1"] + 0.1) * SR)
        g[max(0, a):b] = -13.0
    g = smooth(g, 0.08)
    pa = int(t_ho * SR)
    ramp0 = int((t_ho - 0.25) * SR)        # the kick-out bars before the drop are quiet anyway; open just before the drop
    g[ramp0:pa] = np.linspace(g[ramp0], 0.0, pa - ramp0)
    g[pa:] = 0.0
    lin = 10 ** (g / 20)
    fs = MUSIC["fade_s"]; f0 = int((CUTS["end"] / FPS - fs) * SR)
    lin[f0:] *= np.cos(np.linspace(0, np.pi / 2, n - f0)) ** 1.5
    lin[:int(0.03 * SR)] *= np.linspace(0, 1, int(0.03 * SR))
    mus_d = mus * lin[:, None]
    dia = load(OUT / "partA_dialogue.wav")
    dbuf = np.zeros((n, 2), np.float32); place(dbuf, dia[: int(A_N / FPS * SR)], 0.0)
    mix = mus_d + dbuf
    write_wav(BUILD / "pre.wav", mix)
    I, _ = lufs(BUILD / "pre.wav")
    gain, master = -14.0 - I, OUT / "explainer_full_v1_mix.wav"
    for _ in range(5):
        write_wav(BUILD / "gain.wav", mix * 10 ** (gain / 20))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / "gain.wav"), "-af",
                        "aresample=192000,alimiter=limit=0.79:attack=1:release=60:level=disabled,aresample=48000", "-c:a", "pcm_s24le", str(master)], check=True)
        I2, P2 = lufs(master)
        if abs(I2 + 14.0) <= 0.2:
            break
        gain += -14.0 - I2
    write_wav(BUILD / "stem_music.wav", mus_d * 10 ** (gain / 20))
    write_wav(BUILD / "stem_dialogue.wav", dbuf * 10 ** (gain / 20))
    info = dict(music_src_in=round(src0, 4), music_src_out=round(src0 + n / SR, 4), partB_ref_lufs=I_B, master_lufs=I2, master_peak=P2, gain_db=gain)
    (BUILD / "audio.json").write_text(json.dumps(info, indent=1))
    print("audio", info, flush=True)
    return master


def mux(name):
    out = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / "video.mp4"), "-i", str(OUT / "explainer_full_v1_mix.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{CUTS['end'] / FPS:.5f}", "-movflags", "+faststart", str(out)], check=True)
    print("DONE", out, nframes(out))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ("gfx", "audio", "video", "mux", "all"):
        ap.add_argument(f"--{k}", action="store_true")
    ap.add_argument("--name", default="explainer_full_v1")
    a = ap.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True)
    if a.gfx or a.all or a.video:
        gm = gfx()
    if a.audio or a.all:
        audio()
    if a.video or a.all:
        picture(gm)
    if a.mux or a.all:
        mux(a.name)
