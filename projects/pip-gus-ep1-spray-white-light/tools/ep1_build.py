"""Pip & Gus Ep 1 - full build: cartoon (rendered on twos) + real footage (owner's SL600 spray beats, Civic windshield
pull-back, hard 1:1 cut to the Civic scan) + audience-question card (Pip's voice) + logo card; word-by-word captions on the
cartoon only; dialogue + music mix.

    python tools/ep1_build.py [--name ep2_v1] [--no-music] [--only cartoon|real|gfx|audio]

Resumable: each step caches its output in BUILD. No text ever sits on real footage: captions end before the cartoon ends and
the cards are opaque (checked per frame against the overlay alpha).
"""
import argparse, hashlib, json, os, subprocess, sys, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parent.parent
M = Path("/home/user/media/ep1")
BUILD = M / "build"
OUT = M / "out"
FPS, SR, W, H = 30, 48000, 1080, 1920
TL = json.loads((PROJ / "ep1_timeline.json").read_text())
OPEN = TL.get("opening_frames", 0)          # shot O (series callback) runs at negative cartoon frames
A_N = TL["total_frames"] + OPEN              # cartoon frames in the reel (reel frame = cartoon frame + OPEN)
T_OFF = OPEN / FPS
CAP = dict(PIP="#619f73", GUS="#ecefec")
BRAND = {"accent": "#619f73", "onAccent": "#0b0c0b", "ink": "#ecefec", "bg": "#0b0c0b", "sub": "#d4d9d4", "sub2": "#c8cec8",
         "label": "#a8b0a8", "dim55": "rgba(236,239,236,0.55)", "dim50": "rgba(236,239,236,0.5)", "plate": "rgba(11,12,11,0.58)",
         "cap": "rgba(11,12,11,0.55)"}
HLG = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,"
       "format=yuv420p")
OWNER1 = M / "owner_clips/owner_1.mp4"   # owner's SL600 AESUB clip; 23.8-32 s carries no burned-in captions
CIVIC = Path("/home/user/media/civic11/dropbox/v_1957_24.mov")
# real section, frames at 30 fps: (name, source, in-seconds, frames, filter)
REAL = [
    ("glass", OWNER1, 24.60, 18, "scale=1080:1920:flags=lanczos"),         # spraying the headlight glass (1 beat)
    ("black", OWNER1, 27.00, 18, "scale=1080:1920:flags=lanczos"),         # tracking stripes on the black door + mirror
    ("chrome", OWNER1, 29.00, 18, "scale=1080:1920:flags=lanczos"),        # the chrome star badge
    ("civic", CIVIC, 5.002 - 35 / FPS, 36, HLG + ",scale=1080:1920"),      # windshield sprayed; LAST frame = solved f150 (2 beats)
]
SCAN_DIR = M / "scan_civic"   # cam_A render, 15 fps, 2.0 s orbit 10 deg ease-in-out
SCAN_N = 54                   # 3 beats -> the card lands on bar 14's downbeat (pilot v3 music route)
CARD_N, LOGO_N = 90, 90       # card 5 beats; logo from bar 15 beat 2, final chord +54 frames, ring-out
REAL_N = sum(r[3] for r in REAL) + SCAN_N
CUTS = dict(real=A_N, scan=A_N + REAL_N - SCAN_N, card=A_N + REAL_N, logo=A_N + REAL_N + CARD_N)
CUTS["end"] = CUTS["logo"] + LOGO_N
CAP_Y = {}            # per-shot caption centre y (default 1330), set by eye from the contact sheet


def run(cmd, **kw):
    subprocess.run([str(c) for c in cmd], check=True, **kw)


def nframes(p):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                   "stream=nb_read_frames", "-of", "csv=p=0", str(p)]).decode().strip()
    return int(out)


# ------------------------------------------------------------------ cartoon (on twos)
def cartoon():
    mp4 = BUILD / "cartoon.mp4"
    if mp4.exists() and nframes(mp4) == A_N:
        return mp4
    seq = BUILD / "seq"
    seq.mkdir(parents=True, exist_ok=True)
    miss = []
    for s in TL["shots"]:
        for f in range(s["f0"], s["f1"]):
            r = f + OPEN
            src = None
            for g in (f, f - 1):
                p = M / "frames" / s["id"] / f"{g:04d}.png"
                if g >= s["f0"] and p.exists():
                    src = p
                    break
            if src is None:
                miss.append((s["id"], f))
                continue
            dst = seq / f"{r:05d}.png"
            if dst.is_symlink() or dst.exists():
                dst.unlink()
            dst.symlink_to(src)
    assert not miss, f"missing cartoon frames: {miss[:5]} ... ({len(miss)})"
    run(["ffmpeg", "-v", "error", "-y", "-framerate", FPS, "-i", seq / "%05d.png", "-c:v", "libx264", "-crf", "12", "-preset",
         "medium", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", mp4])
    return mp4


# ------------------------------------------------------------------ real footage + scan
def real():
    mp4 = BUILD / "real.mp4"
    if mp4.exists() and nframes(mp4) == REAL_N:
        return mp4
    parts = []
    for name, src, t0, n, vf in REAL:
        p = BUILD / f"real_{name}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.4f}", "-i", src, "-vf", f"{vf},fps={FPS},setsar=1", "-frames:v", n, "-an",
             "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", p])
        assert nframes(p) == n, (name, nframes(p), n)
        parts.append(p)
    # scan: 15 fps PNGs -> 30 fps by motion interpolation (smooth orbit on black interpolates cleanly)
    pngs = sorted(SCAN_DIR.glob("*.png"))
    assert pngs, "scan render missing"
    p = BUILD / "real_scan.mp4"
    pat = str(pngs[0]).rsplit("_", 1)[0] if "_" in pngs[0].stem else None
    lst = BUILD / "scan_list.txt"
    lst.write_text("".join(f"file '{q}'\nduration {1 / 15:.6f}\n" for q in pngs))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf",
         f"fps=15,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,scale={W}:{H},setsar=1", "-frames:v", SCAN_N, "-an",
         "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", p])
    assert nframes(p) == SCAN_N, nframes(p)
    parts.append(p)
    lst2 = BUILD / "real_list.txt"
    lst2.write_text("".join(f"file '{q}'\n" for q in parts))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst2, "-c", "copy", mp4])
    assert nframes(mp4) == REAL_N
    return mp4


# ------------------------------------------------------------------ captions + cards (Remotion ExplainerGfx)
def pages():
    out = []
    lines = [L for L in TL["lines"] if "t0" in L]
    for i, L in enumerate(lines):
        ws = L["words"]
        rows = [ws[k:k + 4] for k in range(0, len(ws), 4)] if len(ws) > 4 else [ws]
        if len(ws) == 5:
            rows = [ws[:3], ws[3:]]
        pg = [rows[k:k + 2] for k in range(0, len(rows), 2)]
        nxt = lines[i + 1]["t0"] if i + 1 < len(lines) else A_N / FPS - T_OFF - 0.1
        shot = L["shot"]
        for j, p in enumerate(pg):
            t0 = p[0][0]["t0"]
            t1 = pg[j + 1][0][0]["t0"] if j + 1 < len(pg) else min(p[-1][-1]["t1"] + 0.35, nxt)
            out.append(dict(t0=round(t0 + T_OFF, 3), t1=round(min(t1 + T_OFF, A_N / FPS - 0.05), 3), color=CAP[L["speaker"]],
                            y=CAP_Y.get(shot, 1330), cx=540, lines=[[dict(w=w["w"], t0=round(w["t0"] + T_OFF, 3)) for w in r] for r in p]))
    return out


def props():
    c, logo = CUTS["card"] / FPS, CUTS["logo"] / FPS
    items = [{"kind": "tease", "t0": c, "t1": logo, "lines": ["WHAT DO YOU", "SPRAY WITH?"], "sub": "TELL US IN THE COMMENTS"},
             {"kind": "logo", "t0": logo, "t1": CUTS["end"] / FPS + 1, "cta": ""}]
    return {"fps": FPS, "durationInFrames": CUTS["end"], "items": items, "pages": pages(), "palette": BRAND, "size": 88}


def gfx():
    js = json.dumps(props(), indent=1)
    (PROJ / "gfx_props.json").write_text(js)
    h = hashlib.sha1((js + (REPO / "remotion/src/gfx/reel/ExplainerGfx.tsx").read_text()).encode()).hexdigest()[:10]
    mov = BUILD / f"gfx_{h}.mov"
    if not mov.exists():
        pj = BUILD / "gfx_props.json"
        pj.write_text(js)
        tmp = BUILD / f"tmp_gfx_{h}.mov"
        run(["nice", "-n", "5", "npx", "remotion", "render", "ExplainerGfx", tmp, f"--props={pj}", "--codec=prores",
             "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png", "--concurrency=2", "--log=error"],
            cwd=REPO / "remotion")
        tmp.rename(mov)
    return mov


def frames(p, w=W, h=H, pix="rgb24", ch=3):
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(p), "-f", "rawvideo", "-pix_fmt", pix, "-"], stdout=subprocess.PIPE,
                          bufsize=10 ** 8)
    n = w * h * ch
    while True:
        b = pr.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, ch)
    pr.wait()


def picture(gmov):
    vid = BUILD / "video.mp4"
    if vid.exists() and nframes(vid) == CUTS["end"]:
        return vid
    tmp = BUILD / "video_tmp.mp4"
    enc = subprocess.Popen(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                            "-movflags", "+faststart", str(tmp)], stdin=subprocess.PIPE)
    g = frames(gmov, pix="rgba", ch=4)
    black = np.zeros((H, W, 3), np.uint8)
    segs = [("cartoon", frames(cartoon()), A_N, False), ("real", frames(real()), REAL_N, True),
            ("cards", (black for _ in range(CARD_N + LOGO_N)), CARD_N + LOGO_N, False)]
    rep, f = [], 0
    for name, gen, n, is_irl in segs:
        k, amax = 0, 0
        for fr in gen:
            if k >= n:
                break
            ga = next(g)
            if is_irl:
                amax = max(amax, int(ga[:, :, 3].max()))
            al = ga[:, :, 3:4].astype(np.float32) / 255.0
            o = fr.astype(np.float32) * (1 - al) + ga[:, :, :3].astype(np.float32) * al
            enc.stdin.write((o + 0.5).astype(np.uint8).tobytes())
            k += 1
            f += 1
        assert k == n, (name, k, n)
        rep.append(dict(seg=name, frame0=f - n, frames=n, overlay_alpha_on_irl=amax if is_irl else None))
        print(rep[-1], flush=True)
    enc.stdin.close()
    enc.wait()
    assert not [r for r in rep if r["overlay_alpha_on_irl"]], f"text over IRL: {rep}"
    (BUILD / "picture.json").write_text(json.dumps(rep, indent=1))
    tmp.rename(vid)
    return vid


# ------------------------------------------------------------------ audio
def load(p, sr=SR):
    pcm = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"])
    return np.frombuffer(pcm, np.float32).reshape(-1, 2).copy()


def write_wav(p, y):
    with wave.open(str(p), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())


def lufs(p):
    o = subprocess.run(["ffmpeg", "-v", "info", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True,
                       text=True).stderr
    tail = o[o.rfind("Summary:"):]
    I = float(tail.split("I:")[1].split("LUFS")[0])
    P = float(tail.split("Peak:")[1].split("dBFS")[0])
    return I, P


def smooth(env, tau):
    from scipy.signal import lfilter
    k = np.exp(-1 / (tau * SR))
    s = lfilter([1 - k], [1, -k], env)
    return lfilter([1 - k], [1, -k], s[::-1])[::-1]


BEAT0, BEAT = 0.0203, 0.60001     # inquisitive_A measured grid (pilot full_build_v2.py), 100 BPM, bar = 4 beats
LIFT_BEAT = 32                   # bar 8 downbeat = bass entry (measured 19.245 s here) -> on the cut to real footage
JUMPS = [(10, 2), (14, 6), (30, 22), (30, 22)]   # 2-bar back-jumps in the intro (pilot-scored splices; the last one played twice)
POST_JUMPS = [(40, 56)]          # end of bar 9 -> bar 14 (pilot v3 route to the real ending, splice score 6.39)
XF = 0.008
TRACK = M / "music/inquisitive_A.mp3"   # Higgsfield ElevenLabs Music v2.5 job 077bbd23 (the pilot's bed, owner 2026-11-17)


def bt(k):
    return BEAT0 + k * BEAT


def music(n):
    t_lift = CUTS["real"] / FPS
    s0 = bt(LIFT_BEAT) + sum(bt(a) - bt(b) for a, b in JUMPS) - t_lift
    x = load(TRACK)
    segs, cur = [], s0
    for a, b in JUMPS + POST_JUMPS:
        segs.append((cur, bt(a) - XF))
        cur = bt(b) - XF
    segs.append((cur, None))
    xf = int(XF * SR)
    pad = max(0, int(round(-s0 * SR)))
    out = []
    for i, (a, b) in enumerate(segs):
        ia = max(0, int(round(a * SR)))
        ib = len(x) if b is None else int(round(b * SR))
        out.append(x[max(0, ia - (xf if i else 0)): ib + (xf if b is not None else 0)].copy())
    y = np.vstack([np.zeros((pad, 2), np.float32), out[0]])
    for seg in out[1:]:
        k = 2 * xf
        ramp = np.linspace(0, np.pi / 2, k)[:, None]
        y = np.vstack([y[:-k], y[-k:] * np.cos(ramp) + seg[:k] * np.sin(ramp), seg[k:]])
    y = y[:n]
    if len(y) < n:
        y = np.vstack([y, np.zeros((n - len(y), 2), np.float32)])
    return y.astype(np.float32), s0


def audio(name, use_music=True):
    master = OUT / f"{name}_mix.wav"
    n = int(round(CUTS["end"] / FPS * SR))
    dia = np.zeros((n, 2), np.float32)
    cb = TL["lines"][0] if TL["lines"][0]["n"] == 0 else None
    if cb:
        c = load(M / "voice/callback.mp3")
        a = int((cb["clip_start"] + T_OFF) * SR)
        dia[a:a + len(c)] += c
    d = load(M / "voice/split/dialogue_cartoon.wav")[:int((A_N / FPS - T_OFF) * SR)]
    a = int(T_OFF * SR)
    dia[a:a + len(d)] += d
    q = load(M / "voice/split/L15_card.wav")
    a = int((CUTS["card"] / FPS + 0.3) * SR)
    dia[a:a + len(q)] += q[:n - a]
    lines = [(L["t0"] + T_OFF, L["t1"] + T_OFF) for L in TL["lines"] if "t0" in L]
    lines.append((CUTS["card"] / FPS + 0.3, CUTS["card"] / FPS + 0.3 + len(q) / SR))
    if use_music:
        mus, s0 = music(n)
        r1 = int(CUTS["real"] / FPS * SR)
        write_wav(BUILD / "music_B.wav", mus[r1:int(CUTS["card"] / FPS * SR)])
        Ib, _ = lufs(BUILD / "music_B.wav")
        mus *= 10 ** ((-14.0 - Ib) / 20)     # real-footage stretch sits at the master level, as in the pilot
        g = np.full(n, -8.0)
        for t0, t1 in lines:
            g[max(0, int((t0 - 0.15) * SR)):int((t1 + 0.1) * SR)] = -13.0
        g = smooth(g, 0.08)
        r0 = int((CUTS["real"] / FPS - 0.25) * SR)
        g[r0:r1] = np.linspace(g[r0], 0.0, r1 - r0)
        c0, c1 = int(CUTS["card"] / FPS * SR), int(CUTS["logo"] / FPS * SR)
        g[r1:] = 0.0
        g[c0:c1] = np.minimum(g[c0:c1], smooth(np.where(np.arange(c0, c1) < lines[-1][1] * SR + 0.1 * SR, -6.0, 0.0), 0.05))
        lin = 10 ** (g / 20)
        f0 = int((CUTS["end"] / FPS - 0.3) * SR)
        lin[f0:] *= np.cos(np.linspace(0, np.pi / 2, n - f0)) ** 1.5
        mix = dia + mus * lin[:, None]
    else:
        s0 = None
        mix = dia
    write_wav(BUILD / "pre.wav", mix)
    I, _ = lufs(BUILD / "pre.wav")
    gain = -14.0 - I
    for _ in range(6):
        write_wav(BUILD / "gain.wav", mix * 10 ** (gain / 20))
        run(["ffmpeg", "-v", "error", "-y", "-i", BUILD / "gain.wav", "-af",
             "aresample=192000,alimiter=limit=0.79:attack=1:release=60:level=disabled,aresample=48000", "-c:a", "pcm_s24le", master])
        I2, P2 = lufs(master)
        if abs(I2 + 14.0) <= 0.2:
            break
        gain += -14.0 - I2
    (BUILD / "audio.json").write_text(json.dumps(dict(master_lufs=I2, true_peak=P2, gain_db=gain, track=str(TRACK), track_s0=s0,
                                                      jumps=JUMPS, post_jumps=POST_JUMPS, cuts=CUTS), indent=1))
    print("audio", I2, P2, flush=True)
    return master


def mux(name, master):
    out = OUT / f"{name}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", BUILD / "video.mp4", "-i", master, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{CUTS['end'] / FPS:.5f}", "-movflags", "+faststart", out])
    print("DONE", out, nframes(out), flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="ep1_v1")
    ap.add_argument("--no-music", action="store_true")
    ap.add_argument("--only", default="", help="cartoon|real|gfx|audio (debug)")
    a = ap.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    print("cuts", CUTS, flush=True)
    if a.only == "cartoon":
        cartoon(); sys.exit()
    if a.only == "real":
        real(); sys.exit()
    if a.only == "gfx":
        gfx(); sys.exit()
    m = audio(a.name, not a.no_music)
    if a.only == "audio":
        sys.exit()
    picture(gfx())
    mux(a.name, m)
