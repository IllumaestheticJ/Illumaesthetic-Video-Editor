"""Build the IS350 reels (resumable; re-run swaps in finished renders / music).

    python projects/lexus-is350-reels/tools/build.py [R1 R2 R3] [--no-gfx] [--no-video]

Steps per reel: 1 music stem (from the music agent's files)  2 dialogue/room stem from the original audio (proxies carry the
same audio track as the 4K originals)  3 ducking + master (-10 LUFS, limiter -1.2 dBFS)  4 Remotion ReelGfx overlay (cached by
props hash)  5 picture: frame-exact hard cuts written frame by frame from the graded 4K intermediates (crop window per frame,
23.976 -> 30 fps by explicit frame mapping; lead-ins into a 1:1 cut END on the solved frame), scan renders (or a tagged
placeholder), gfx alpha-composited, H.264 High CRF 17  6 mux AAC 256k.
Not `ive assemble`: it drops each shot's first frame (smart-450 finding) - this writes every frame itself.
"""
import hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reels import REELS, SPANS, captions, speech_spans, BUILD, OUT, SRC, REND, MUS, FPS, SRC_FPS, NAMES, PROJ  # noqa: E402

SR = 48000
REPO = PROJ.parent.parent
PROXY = Path("/home/user/media/lexus-is350/dropbox")
MIX_FULL = Path("/home/user/media/work/is350-long/music/mix_full.wav")
NICE = ["nice", "-n", "5"]


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ audio helpers
def load(path, t0=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{max(0, t0):.5f}", "-i", str(path)] + (["-t", f"{dur:.5f}"] if dur else []) + \
          ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
    if t0 < 0:
        x = np.vstack([np.zeros((int(round(-t0 * SR)), 2), np.float32), x])
    return x


def place(buf, x, t):
    i = int(round(t * SR))
    if i < 0:
        x, i = x[-i:], 0
    n = min(len(x), len(buf) - i)
    if n > 0:
        buf[i:i + n] += x[:n]


def fade(x, a=0.005, b=0.005):
    x = x.copy(); na, nb = int(a * SR), int(b * SR)
    if na: x[:na] *= np.linspace(0, 1, na)[:, None]
    if nb: x[-nb:] *= np.linspace(1, 0, nb)[:, None]
    return x


def write_wav(path, x):
    path.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", str(path)],
                         stdin=subprocess.PIPE)
    p.communicate(np.ascontiguousarray(x, np.float32).tobytes())


def lufs(path):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    tail = o[o.rfind("Summary:"):]
    I = float(tail.split("I:")[1].split("LUFS")[0]); P = float(tail.split("Peak:")[1].split("dBFS")[0])
    return I, P


# ------------------------------------------------------------------ music per reel
def music_R1(r):
    a = r["anchors"]; d = MUS / "R1"
    buf = np.zeros((int((r["end"] + 1) * SR), 2), np.float32)
    straight = load(d / "R1_stem_run_straight_32s.wav", 0, 6.4)
    place(buf, fade(straight, 0.02, 0.006), a["music0"])                 # calm bars; bar line k46 lands on "go"
    wind = load(d / "R1_stem_windup_stop_8s.wav")
    T = a["crashed"] - a["go"]
    seg = wind[len(wind) - int(round(T * SR)):]                         # last T s of the agent's wind-up: ends in its dead stop
    place(buf, fade(seg, 0.006, 0.003), a["go"])
    cb = load(d / "R1_stem_comeback_optB.wav")                           # k270 drop at 0, hit (k286) at 6.4, ring to 7.8
    hit_i = int(round(6.4 * SR))
    place(buf, fade(cb[:hit_i], 0.0, 0.006), a["now"])
    # 8 more beats from the source piece (P4 k286 -> k294) between the drop bars and the built ending; gain matched by RMS
    k = lambda kk: 360.1463 + 0.4 * kk
    ref = load(MIX_FULL, k(270), 6.4)
    g = np.sqrt(np.mean(cb[:hit_i] ** 2) / max(1e-12, np.mean(ref ** 2)))
    ext = load(MIX_FULL, k(286), 3.2 + 0.012) * g
    place(buf, fade(ext, 0.006, 0.006), a["now"] + 6.4)
    place(buf, fade(cb[hit_i:], 0.006, 0.01), a["logo"])
    return buf, dict(gain_ext=float(g), windup_s=T)


def music_R2(r):
    a = r["anchors"]; x = load(MUS / "R2" / "R2_music_optB.wav")
    i0, i1 = int(round(a["cut_from"] * SR)), int(round(a["cut_to"] * SR))
    xf = int(0.012 * SR)
    head, tail = x[:i0 + xf].copy(), x[i1:].copy()
    ramp = np.linspace(1, 0, xf)[:, None]
    head[-xf:] = head[-xf:] * ramp + tail[:xf] * (1 - ramp)
    y = np.vstack([head, tail[xf:]])
    buf = np.zeros((int((r["end"] + 1) * SR), 2), np.float32); place(buf, y, 0)
    return buf, dict(removed=[a["cut_from"], a["cut_to"]])


def music_R3(r):
    """v2: one continuous, unspliced stretch of P6 from the owner's mix (no mute, no boom, no removed block); only a fade-out at the end.
    Level: the stretch is brought to -10 LUFS like the other music stems (the master loop sets the final level)."""
    a = r["anchors"]
    n = round(r["end"] * FPS) / FPS
    x = load(MIX_FULL, a["music_src0"], n + 0.05)[: int(round(n * SR))]
    write_wav(BUILD / "R3" / "music_raw.wav", x)
    I, _ = lufs(BUILD / "R3" / "music_raw.wav")
    x = x * 10 ** ((-10.0 - I) / 20)
    x = fade(x, 0.03, a["fade_s"])
    buf = np.zeros((int((r["end"] + 1) * SR), 2), np.float32); place(buf, x, 0)
    return buf, {"src": "mix_full.wav P6", "src_in": round(a["music_src0"], 3), "src_out": round(a["music_src0"] + n, 3),
                 "accent_on_cut": round(a["music_src0"] + a["hit"], 3), "gain_db": round(-10.0 - I, 2)}


# ------------------------------------------------------------------ dialogue / room
def src_audio(span, t0, dur):
    clip = SPANS[span]["clip"]
    return load(PROXY / f"{clip}.MP4", t0, dur)


def dialogue(r):
    dia = np.zeros((int((r["end"] + 1) * SR), 2), np.float32)
    room = np.zeros_like(dia)
    for s in r["shots"]:
        if s["kind"] != "irl":
            continue
        span = s["audio_span"] or s["span"]
        mode = SPANS[span]["audio"]
        if mode == "mute":
            continue
        dur = s["t1"] - s["t0"]
        x = src_audio(span, SPANS[span]["a"], dur)
        x = x.mean(axis=1, keepdims=True).repeat(2, axis=1)                 # camera mic: mono centre
        if mode == "room":
            place(room, fade(x * 10 ** (s["gain_db"] / 20), 0.02, 0.02), s["t0"]); continue
        # speech level: normalise the loudest 20 % of 20 ms frames to -20 dBFS RMS (cap +18 dB)
        e = np.sqrt(np.mean(x[: len(x) // 960 * 960, 0].reshape(-1, 960) ** 2, axis=1) + 1e-12)
        ref = np.sqrt(np.mean(np.sort(e)[-max(1, len(e) // 5):] ** 2))
        g = min(10 ** (18 / 20), 10 ** (-20 / 20) / ref)
        fi = 2 / FPS if s["audio"] == "fadein2" else 0.004
        place(dia, fade(x * g, fi, 0.004), s["t0"])
    return dia, room


def duck_env(r, n, depth_db=-13.0, att=0.12, rel=0.35):
    env = np.ones(n, np.float32)
    lo = 10 ** (depth_db / 20)
    for t0, t1 in speech_spans(r):
        a0, a1 = int((t0 - att) * SR), int((t1 + 0.05) * SR)
        env[max(0, a0):max(0, a1)] = np.minimum(env[max(0, a0):max(0, a1)], lo)
    # smooth: one-pole both ways (attack before the word, release after)
    k = np.exp(-1 / (0.06 * SR))
    from scipy.signal import lfilter
    sm = lfilter([1 - k], [1, -k], env)
    sm = lfilter([1 - k], [1, -k], sm[::-1])[::-1]
    return np.minimum(sm, 1).astype(np.float32)[:, None]


def audio(r):
    rid = r["id"]; d = BUILD / rid; d.mkdir(parents=True, exist_ok=True)
    have = (MUS / rid).exists() and any((MUS / rid).glob("*.wav"))
    mus, minfo = (globals()[f"music_{rid}"](r) if have else (np.zeros((int((r["end"] + 1) * SR), 2), np.float32), {"placeholder": True}))
    dia, room = dialogue(r)
    n = int(round(round(r["end"] * FPS) / FPS * SR))
    mus, dia, room = mus[:n], dia[:n], room[:n]
    mus_d = mus * duck_env(r, n)
    mix = mus_d + dia + room
    write_wav(d / "pre.wav", mix)
    I, _ = lufs(d / "pre.wav")
    g = 10 ** ((-10.0 - I) / 20)
    master = OUT / f"{NAMES[rid]}_mix.wav"
    extra = 0.0
    for _ in range(4):   # limiter loses loudness: add make-up gain until the master sits at -10 +- 0.25 LUFS
        write_wav(d / "gain.wav", mix * g * 10 ** (extra / 20))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d / "gain.wav"), "-af",
                        f"aresample=192000,alimiter=limit={0.6 if rid == 'R1' else 0.7}:attack=1.5:release=80:level=disabled,aresample=48000", "-c:a", "pcm_s24le", str(master)], check=True)
        I2, P2 = lufs(master)
        if abs(I2 + 10.0) <= 0.25:
            break
        extra += -10.0 - I2
    write_wav(OUT / f"{NAMES[rid]}_stem_music.wav", mus_d * g * 10 ** (extra / 20))
    write_wav(OUT / f"{NAMES[rid]}_stem_dialogue.wav", dia * g * 10 ** (extra / 20))
    write_wav(OUT / f"{NAMES[rid]}_stem_room.wav", room * g * 10 ** (extra / 20))
    log(rid, "audio", minfo, "master LUFS", I2, "peak", P2)
    return master, dict(music=minfo, lufs=I2, peak=P2)


# ------------------------------------------------------------------ graphics
def gfx(r):
    rid = r["id"]
    items = r["items"] + captions(r)
    n = int(round(r["end"] * FPS))
    props = {"fps": FPS, "durationInFrames": n, "items": items}
    if r.get("palette"):
        props["palette"] = r["palette"]
    pj = BUILD / rid / "gfx_props.json"; pj.parent.mkdir(parents=True, exist_ok=True)
    js = json.dumps(props, indent=1)
    (PROJ / f"gfx_{rid}_props.json").write_text(js)
    h = hashlib.sha1((js + (REPO / "remotion/src/gfx/reel/ReelGfx.tsx").read_text()).encode()).hexdigest()[:10]
    mov = BUILD / rid / f"gfx_{h}.mov"
    if not mov.exists():
        pj.write_text(js)
        log(rid, "rendering gfx", mov.name)
        subprocess.run(NICE + ["npx", "remotion", "render", "ReelGfx", str(mov), f"--props={pj}", "--codec=prores", "--prores-profile=4444",
                               "--pixel-format=yuva444p10le", "--image-format=png", "--concurrency=2", "--log=error"], cwd=REPO / "remotion", check=True)
    return mov


# ------------------------------------------------------------------ picture
def x0_at(span, t):
    kf = SPANS[span]["x0"]
    if len(kf) == 1:
        return kf[0][1]
    ts = [k[0] for k in kf]; xs = [k[1] for k in kf]
    return float(np.interp(t, ts, xs))


def frames_of(mov, w, h, start=0):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(mov), "-vf", f"select=gte(n\\,{start})", "-fps_mode", "passthrough",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10 ** 8)
    sz = w * h * 3
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.stdout.close(); p.wait()


def nframes(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def irl_frames(s, n):
    span = s["span"]; sp = SPANS[span]
    if not (SRC / f"{span}.json").exists():   # 4K intermediate not cut yet: tagged placeholder so the rest can be reviewed
        ph = np.full((1920, 1080, 3), 40, np.uint8)
        cv2.putText(ph, "MISSING SRC", (120, 900), cv2.FONT_HERSHEY_SIMPLEX, 2.4, (0, 120, 255), 6)
        cv2.putText(ph, span, (120, 1000), cv2.FONT_HERSHEY_SIMPLEX, 2.4, (0, 120, 255), 6)
        for _ in range(n):
            yield ph, None
        return
    m = json.loads((SRC / f"{span}.json").read_text())
    if s["end_on_match"]:
        idx = [sp["match_f"] - int(round((n - 1 - j) * SRC_FPS / FPS)) for j in range(n)]
    else:
        idx = [int(round((sp["a"] + j / FPS) * SRC_FPS)) for j in range(n)]
    loc = [i - m["f0"] for i in idx]
    assert loc[0] >= 0 and loc[-1] < m["n"], (span, loc[0], loc[-1], m["n"])
    gen = frames_of(SRC / f"{span}.mov", m["w"], m["h"], loc[0])
    cur, ci = next(gen), loc[0]
    sc = m["w"] / 1920
    for j, li in enumerate(loc):
        while ci < li:
            cur, ci = next(gen), ci + 1
        t = idx[j] / SRC_FPS
        x = int(round(x0_at(span, t) * sc)); x = max(0, min(m["w"] - 1080, x))
        yield cur[:, x:x + 1080], idx[j]


def scan_frames(s, n, r):
    sid = s["scan"]
    mp4 = REND / sid / f"{sid}_preview.mp4"
    start = int(round(s.get("scan_from", 0) * FPS))
    if mp4.exists() and nframes(mp4) >= start + n:
        for j, fr in enumerate(frames_of(mp4, 1080, 1920, start)):
            if j >= n:
                break
            yield fr, None
        return
    # PLACEHOLDER: the matched IRL window (or black for the hero), darkened, tagged
    prev = [q for q in r["shots"] if q["t1"] == s["t0"] and q["kind"] == "irl"]
    base = np.zeros((1920, 1080, 3), np.uint8)
    if prev and prev[0]["end_on_match"]:
        last = None
        for last, _ in irl_frames(prev[0], int(round(prev[0]["t1"] * FPS)) - int(round(prev[0]["t0"] * FPS))):
            pass
        base = (last.astype(np.float32) * 0.35).astype(np.uint8)
    cv2.putText(base, "PLACEHOLDER", (120, 1700), cv2.FONT_HERSHEY_SIMPLEX, 2.4, (0, 200, 255), 6)
    cv2.putText(base, sid, (120, 1790), cv2.FONT_HERSHEY_SIMPLEX, 2.4, (0, 200, 255), 6)
    for _ in range(n):
        yield base, None


def picture(r, gmov):
    rid = r["id"]
    vid = BUILD / rid / "video.mp4"
    total = int(round(r["end"] * FPS))
    enc = subprocess.Popen(NICE + ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(FPS), "-i", "-",
                                   "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                                   "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", str(vid)],
                           stdin=subprocess.PIPE)
    g = frames_of(gmov, 1080, 1920) if False else None
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gmov), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE, bufsize=10 ** 8)
    report, f = [], 0
    for s in r["shots"]:
        a, b = int(round(s["t0"] * FPS)), int(round(s["t1"] * FPS)); n = b - a
        assert a == f, (rid, s, a, f)
        if s["kind"] == "irl":
            src = irl_frames(s, n)
        elif s["kind"] == "scan":
            src = scan_frames(s, n, r)
        else:
            src = ((np.zeros((1920, 1080, 3), np.uint8), None) for _ in range(n))
        idxs = []
        for fr, si in src:
            if fr.shape[:2] != (1920, 1080):
                fr = cv2.resize(fr, (1080, 1920), interpolation=cv2.INTER_AREA)
            gb = gp.stdout.read(1080 * 1920 * 4)
            ga = np.frombuffer(gb, np.uint8).reshape(1920, 1080, 4)
            al = ga[:, :, 3:4].astype(np.float32) / 255.0
            out = fr.astype(np.float32) * (1 - al) + ga[:, :, :3].astype(np.float32) * al
            enc.stdin.write(out.astype(np.uint8).tobytes())
            idxs.append(si); f += 1
        assert len(idxs) == n, (rid, s, len(idxs), n)
        report.append({"t0": s["t0"], "frame": a, "frames": n, "kind": s["kind"], "src": s["span"] or s["scan"] or "logo",
                       "src_first": idxs[0], "src_last": idxs[-1],
                       "placeholder": bool(s["kind"] == "scan" and not (REND / s["scan"] / f"{s['scan']}_preview.mp4").exists())})
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    assert f == total, (f, total)
    return vid, report


def build(rid, do_gfx=True, do_video=True, remux=False):
    r = REELS[rid]()
    OUT.mkdir(parents=True, exist_ok=True)
    master, ainfo = audio(r)
    if not do_video:
        return
    gmov = gfx(r)
    if remux and (BUILD / rid / "video.mp4").exists():   # audio-only change: keep the picture, re-mux
        vid = BUILD / rid / "video.mp4"; rep = json.loads((BUILD / rid / "build.json").read_text())["shots"]
    else:
        vid, rep = picture(r, gmov)
    out = OUT / f"{NAMES[rid]}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-i", str(master), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-cutoff", "18000", "-ar", "48000", "-t", f"{round(r['end'] * FPS) / FPS:.5f}", "-movflags", "+faststart", str(out)], check=True)
    res = {"output": str(out), "frames": nframes(out), "duration": r["end"], "shots": rep, "audio": ainfo, "gfx": gmov.name,
           "anchors": r["anchors"]}
    (BUILD / rid / "build.json").write_text(json.dumps(res, indent=1, default=float))
    log("DONE", out, res["frames"], "placeholders:", [s["src"] for s in rep if s["placeholder"]])


if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if a in REELS] or list(REELS)
    for rid in ids:
        build(rid, do_video="--no-video" not in sys.argv, remux="--remux" in sys.argv)
