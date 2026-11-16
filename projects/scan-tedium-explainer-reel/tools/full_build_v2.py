"""Full explainer reel v2: Part A unchanged + Part B re-timed to the new 100 BPM track + TEASER end card (host scanning on the floor).

    python projects/scan-tedium-explainer-reel/tools/full_build_v2.py --all [--name explainer_full_v2]

Resumable: each step caches its output in BUILD (teaser.mp4, gfx_<hash>.mov, mix wav, video.mp4) and is skipped when present
(--force-<step> is not needed: delete the file). Run detached: setsid nohup python ... > build_v2/run.log 2>&1 &

Music (owner notes v2): ElevenLabs "inquisitive_A.mp3", measured (spectral-flux grid, residual 1.6 ms): 100.00 BPM, beat 0 at
0.0203 s, beat = 0.6 s = 18 frames exactly, bar = 72 frames. Harmony alternates Gm (even bars) / F (odd bars) in 4-bar phrases.
Bars 0-7 intro (no bass; shaker from bar 4; bass pick-up in bar 7), REAL LIFT = bass entry on bar 8 (19.220 s; not ~33 s as
prompted), bass section bars 8-15, final hit bar 16 (38.420 s), rung out by ~39.4 s.
  - Intro extended 6 bars with three 2-bar back-jumps at half-bar points (beat 10->2, 14->6, 30->22; spectral splice score
    5.9-6.5 vs a 5.3 no-edit floor) so the lift lands on frame 989 (hand-off); track enters at 0.654 s.
  - After the lift the track plays on unedited (bars 8-11) and fades on the card: any path lift -> final hit is 2 or 4 bars
    (Gm/F alternation; 3-bar paths score 12+ = audible), i.e. 4.8 s (card would start on the last hit) or 9.6 s (card 5.8 s
    or Part B 7.2 s) - both break the 3-3.5 s card / 4-5 s Part B brief.
Timeline (frames, 30 fps): Part A 0-988 | P2 989-1024 (lift) | P7 1025-1060 | P8 1061-1132 (1:1 cut 1061 = bar 9) |
  teaser card 1133-1231 (bar 10; HOW LONG + window on the downbeat, DID IT TAKE? +1 beat, FULL VIDEO... +2 beats) | end 1232.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import full_build as v1  # noqa: E402
from full_build import PROJ, REPO, OUT, FPS, SR, W, H, A_N, BRAND, irl, scan, smooth, cuts, frames_of, load, write_wav, lufs, nframes  # noqa: E402

W_ = Path("/home/user/media/work/scan-tedium")
BUILD = W_ / "build_v2"
TRACK = W_ / "music/inquisitive_A.mp3"
CUTS = dict(p2=989, p7=1025, p8=1061, card=1133, end=1232)
BEAT0, BEAT = 0.0203, 0.60001          # measured grid (build_v2/grid_v2.npy)
LIFT_BEAT = 32                          # bar 8 downbeat = bass entry
JUMPS = [(10, 2), (14, 6), (30, 22)]    # (from beat, to beat): 2-bar back-jumps in the intro
XF = 0.008                              # splice crossfade (s), centred 8 ms before the grid beat
FADE_S = 1.5
# teaser: E50 of the long-form (FX30547 120.40-125.80, host lying on the floor scanning under the IS350's front).
# 120.40-123.70 only: a background car's plate enters the top 60 px from ~123.6 s and is legible at 123.8 s; the crop starts at y 80.
TEASE = dict(src="/home/user/media/lexus-is350/dropbox/FX30547.MP4", t0=120.40, crop=(300, 80, 1333, 1000))
LUT = REPO / "projects/toyota-mr2-spyder-scan-process/grade/fx3a_slog3cine_to_709.cube"  # same S-Log3 -> 709 grade as the IS350 reels
WIN = dict(x=90, y=560, w=860, h=645, r=30, border=5)


def bt(k):
    return BEAT0 + k * BEAT


def music_plan():
    """Playback list [(track_in, track_out)], reel-time 0 = track s0."""
    t_ho = CUTS["p2"] / FPS
    played_before = sum(bt(a) - bt(b) for a, b in JUMPS)  # extra time from the back-jumps
    s0 = bt(LIFT_BEAT) + played_before - t_ho
    segs, cur = [], s0
    for a, b in JUMPS:
        segs.append((cur, bt(a) - XF)); cur = bt(b) - XF
    segs.append((cur, None))
    return s0, segs


def music(n):
    s0, segs = music_plan()
    x = load(TRACK)
    out, xf = [], int(XF * SR)
    for i, (a, b) in enumerate(segs):
        ia = int(round(a * SR)); ib = len(x) if b is None else int(round(b * SR))
        seg = x[ia - (xf if i else 0): ib + (xf if b is not None else 0)].copy()
        out.append(seg)
    # equal-power crossfades of xf*2 samples centred on each splice
    y = out[0]
    for seg in out[1:]:
        k = 2 * xf
        ramp = np.linspace(0, np.pi / 2, k)[:, None]
        y = np.vstack([y[:-k], y[-k:] * np.cos(ramp) + seg[:k] * np.sin(ramp), seg[k:]])
    y = y[:n]
    if len(y) < n:
        y = np.vstack([y, np.zeros((n - len(y), 2), np.float32)])
    return y.astype(np.float32), s0


# ------------------------------------------------------------------ teaser footage (graded, cropped, 30 fps)
def teaser():
    mp4 = BUILD / "teaser.mp4"
    n = CUTS["end"] - CUTS["card"]
    if mp4.exists() and nframes(mp4) == n:
        return mp4
    x, y, w, h = TEASE["crop"]
    vf = (f"format=rgb48le,lut3d=file={LUT}:interp=tetrahedral,crop={w}:{h}:{x}:{y},scale={WIN['w']}:{WIN['h']}:flags=lanczos,"
          f"fps={FPS},format=yuv444p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{TEASE['t0']:.3f}", "-i", TEASE["src"], "-vf", vf, "-frames:v", str(n), "-an",
                    "-c:v", "libx264", "-crf", "10", "-preset", "medium", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    str(mp4)], check=True)
    assert nframes(mp4) == n
    return mp4


# ------------------------------------------------------------------ gfx
def props():
    c0, c1 = CUTS["card"] / FPS, CUTS["end"] / FPS
    b = BEAT
    item = {"kind": "teaser", "t0": c0, "t1": c1 + 1,
            "lines": [{"text": "HOW LONG", "at": c0}, {"text": "DID IT TAKE?", "at": c0 + b}],
            "sub": {"lines": ["FULL VIDEO", "ON OUR CHANNEL"], "at": c0 + 2 * b},
            "win": dict(WIN, at=c0)}
    return {"fps": FPS, "durationInFrames": CUTS["end"], "items": [item], "pages": v1.pages(), "palette": BRAND, "size": 88}


def gfx():
    js = json.dumps(props(), indent=1)
    (PROJ / "gfx_full_v2_props.json").write_text(js)
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
def picture(gmov, tmp4):
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

    def card():
        for fr in frames_of(tmp4, WIN["w"], WIN["h"], 0):
            base = np.empty((H, W, 3), np.uint8); base[:] = bg
            base[WIN["y"]:WIN["y"] + WIN["h"], WIN["x"]:WIN["x"] + WIN["w"]] = fr
            yield base, None
    # IRL mask for the text-over-IRL check: Part B real shots = whole frame; card = window minus its border
    win_mask = np.zeros((H, W), bool)
    b = WIN["border"] + 2
    yy, xx = np.mgrid[0:H, 0:W]
    x0, y0, x1, y1, rr = WIN["x"] + b, WIN["y"] + b, WIN["x"] + WIN["w"] - b, WIN["y"] + WIN["h"] - b, max(0, WIN["r"] - b)
    cx, cy = np.clip(xx, x0 + rr, x1 - rr), np.clip(yy, y0 + rr, y1 - rr)  # rounded-rect interior (the visible footage)
    win_mask[:] = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1) & ((xx - cx) ** 2 + (yy - cy) ** 2 <= rr ** 2)
    c = CUTS
    segs = [("partA", frames_of(OUT / "partA_v5.mp4", W, H, 0), A_N, None),
            ("P2", irl("R1_SCAN", c["p7"] - c["p2"], t_start=322.0), c["p7"] - c["p2"], "all"),
            ("P7", irl("R2_FRONT", c["p8"] - c["p7"], end_on_match=True), c["p8"] - c["p7"], "all"),
            ("P8", scan("V_MATCH_FRONT", c["card"] - c["p8"]), c["card"] - c["p8"], None),
            ("card", card(), c["end"] - c["card"], "win")]
    rep, f, qa = [], 0, []
    for name, gen, n, irlm in segs:
        k, srcs, amax = 0, [], 0.0
        for item in gen:
            fr, si = item if isinstance(item, tuple) else (item, None)
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
            srcs.append(si); k += 1; f += 1
        assert k == n, (name, k, n)
        rep.append(dict(seg=name, frame0=f - n, frames=n, src_first=srcs[0], src_last=srcs[-1], irl_overlay_alpha_max=amax if irlm else None))
        print(name, rep[-1], flush=True)
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    assert f == CUTS["end"]
    (BUILD / "picture.json").write_text(json.dumps(rep, indent=1, default=str))
    bad = [r for r in rep if r["irl_overlay_alpha_max"]]
    assert not bad, f"overlay pixels on IRL footage: {bad}"
    tmpv.rename(vid)
    return vid


# ------------------------------------------------------------------ audio (v1 ducking scheme, new music)
def audio(name):
    master = OUT / f"{name}_mix.wav"
    if master.exists() and (BUILD / "audio.json").exists():
        return master
    n = int(round(CUTS["end"] / FPS * SR))
    t_ho = CUTS["p2"] / FPS
    mus, s0 = music(n)
    write_wav(BUILD / "music_raw.wav", mus)
    seg = mus[int(t_ho * SR):]
    write_wav(BUILD / "music_B.wav", seg)
    I_B, _ = lufs(BUILD / "music_B.wav")
    mus = mus * 10 ** ((-14.0 - I_B) / 20)
    g = np.full(n, -8.0)
    for l in sorted(cuts()["lines"], key=lambda l: l["t0"]):
        a, b = int((l["t0"] - 0.15) * SR), int((l["t1"] + 0.1) * SR)
        g[max(0, a):b] = -13.0
    g = smooth(g, 0.08)
    pa = int(t_ho * SR); ramp0 = int((t_ho - 0.25) * SR)
    g[ramp0:pa] = np.linspace(g[ramp0], 0.0, pa - ramp0)
    g[pa:] = 0.0
    lin = 10 ** (g / 20)
    f0 = int((CUTS["end"] / FPS - FADE_S) * SR)
    lin[f0:] *= np.cos(np.linspace(0, np.pi / 2, n - f0)) ** 1.5
    lin[:int(0.08 * SR)] *= np.linspace(0, 1, int(0.08 * SR))   # track enters 33 ms after a beat: short fade-in
    mus_d = mus * lin[:, None]
    dia = load(OUT / "partA_dialogue.wav")
    dbuf = np.zeros((n, 2), np.float32); v1.place(dbuf, dia[: int(A_N / FPS * SR)], 0.0)
    mix = mus_d + dbuf
    write_wav(BUILD / "pre.wav", mix)
    I, _ = lufs(BUILD / "pre.wav")
    gain = -14.0 - I
    for _ in range(6):
        write_wav(BUILD / "gain.wav", mix * 10 ** (gain / 20))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / "gain.wav"), "-af",
                        "aresample=192000,alimiter=limit=0.79:attack=1:release=60:level=disabled,aresample=48000", "-c:a", "pcm_s24le", str(master)], check=True)
        I2, P2 = lufs(master)
        if abs(I2 + 14.0) <= 0.2:
            break
        gain += -14.0 - I2
    write_wav(BUILD / "stem_music.wav", mus_d * 10 ** (gain / 20))
    write_wav(BUILD / "stem_dialogue.wav", dbuf * 10 ** (gain / 20))
    info = dict(track_s0=round(s0, 4), jumps_beats=JUMPS, lift_track_s=round(bt(LIFT_BEAT), 4), lift_reel_frame=CUTS["p2"],
                partB_ref_lufs=I_B, master_lufs=I2, master_true_peak=P2, gain_db=gain)
    (BUILD / "audio.json").write_text(json.dumps(info, indent=1))
    print("audio", info, flush=True)
    return master


def mux(name, master):
    out = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BUILD / "video.mp4"), "-i", str(master), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{CUTS['end'] / FPS:.5f}", "-movflags", "+faststart", str(out)], check=True)
    print("DONE", out, nframes(out), flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ("gfx", "audio", "video", "mux", "all"):
        ap.add_argument(f"--{k}", action="store_true")
    ap.add_argument("--name", default="explainer_full_v2")
    a = ap.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True)
    if a.audio or a.all:
        m = audio(a.name)
    if a.gfx or a.video or a.all:
        gm = gfx()
    if a.video or a.all:
        picture(gm, teaser())
    if a.mux or a.all:
        mux(a.name, OUT / f"{a.name}_mix.wav")
