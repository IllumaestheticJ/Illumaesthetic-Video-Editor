"""Prepare every shot of the Smart 450 reel as an exact-length 1080x1920 30 fps clip in BUILD (resumable, cached).

    python projects/smart-450-hellkitten/tools/prep_video.py [S1 S5 ...] [--force]

IRL: tonemap HLG (the same chain as ive.assemble), upright (the three wrong rotation tags: -noautorotate + 180), scale, then crop
the 9:16 window (scale first so tracked pans move by sub-source-pixel steps). Stills: Ken Burns window cut from the original with
Lanczos. Scan shots: the finished render PNGs (15 fps -> 30 fps, minterpolate; A2 is conformed in two parts so no interpolated frame
blends the state swap), or, while a render is unfinished, a hold-last placeholder built from the PNGs that exist plus the framing
previews, with a small PLACEHOLDER tag burned in. Rebuilding picks up finished renders automatically (cache stamp = frames present).
"""
import glob, hashlib, json, os, subprocess, sys, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SHOTS, DB, DESIGN, SM, SCAN_NEED, FPS


def nout(s):
    """Frames in the prepped file: exactly the shot length (concat_assemble.py keeps every frame; ive.assemble would not)."""
    return s["n"]

W, H = 1080, 1920
BUILD = Path(SM) / "build"
BUILD.mkdir(parents=True, exist_ok=True)
TONEMAP_HLG = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
               "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
LOGO = "/home/user/Illumaesthetic-Video-Editor/remotion/public/illumaesthetic_logo.png"
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(" ".join(map(str, cmd)) + "\n" + r.stderr[-2000:])


def probe_tf(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return r.stdout.strip()


def stamp_ok(out, stamp):
    sf = Path(str(out) + ".stamp")
    if out.exists() and sf.exists() and sf.read_text() == stamp:
        return True
    return False


def write_stamp(out, stamp):
    Path(str(out) + ".stamp").write_text(stamp)


def lerp_expr(keys, idx, scale, n):
    """ffmpeg expression for the interpolated key value (idx 1 = x0, 2 = y0), times scale, as a function of frame n."""
    if len(keys) == 1:
        return f"{keys[0][idx] * scale:.2f}"
    parts = []
    for (f0, *a), (f1, *b) in zip(keys[:-1], keys[1:]):
        v0, v1 = a[idx - 1] * scale, b[idx - 1] * scale
        n0, n1 = f0 * (n - 1), f1 * (n - 1)
        parts.append((n0, n1, v0, v1))
    expr = f"{parts[-1][3]:.2f}"
    for n0, n1, v0, v1 in reversed(parts):
        expr = f"if(lt(n,{n1:.3f}),{v0:.2f}+({v1:.2f}-{v0:.2f})*(n-{n0:.3f})/{max(n1 - n0, 1e-6):.3f},{expr})"
    return expr


def sharp_slip(s):
    """Slip the in-point forward (max 0.6 s) to the first frame whose sharpness (Laplacian variance, 3-frame mean) is >= 80 % of the
    median of the span: v1's S1/S6/S7 opened on motion blur."""
    import cv2
    src = f"{DB}/{s['src']}.mov"
    dur = s["n"] / FPS + 0.7
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s['ss']:.4f}", "-t", f"{dur:.3f}", "-i", src, "-vf", "fps=30,scale=360:640,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    h = 640
    fr = np.frombuffer(r, np.uint8).reshape(-1, h, 360)
    sh = np.array([cv2.Laplacian(f, cv2.CV_64F).var() for f in fr])
    med = np.median(sh[: int(s["n"] + 6)])
    for d in range(0, min(18, len(sh) - s["n"] - 1)):
        if sh[d:d + 3].mean() >= 0.8 * med:
            return s["ss"] + d / FPS, d, sh[:int(s["n"]) + d + 1]
    return s["ss"], 0, sh


def prep_irl(s):
    out = BUILD / f"{s['id']}.mp4"
    ss = s["ss"] if s.get("ss") is not None else s["end_ss"] - (s["n"] - 1) / FPS
    if s.get("sharp"):
        ss, d, _ = sharp_slip({**s, "ss": ss})
    stamp = json.dumps({k: s.get(k) for k in ("src", "n", "win", "keys", "rot180")}, sort_keys=True) + f"v6_{ss:.4f}"
    if stamp_ok(out, stamp):
        return out
    src = f"{DB}/{s['src']}.mov"
    hlg = probe_tf(src) in ("arib-std-b67", "smpte2084")
    pre = ["-display_rotation", "0"] if s.get("rot180") else []
    vf = []
    if s.get("rot180"):
        vf.append("hflip,vflip")
    vf.append("fps=30")
    if hlg:
        vf.append(TONEMAP_HLG)
    if s["win"]:
        w, h = s["win"]
        sc = H / h
        vf.append(f"scale=round(iw*{sc:.6f}):round(ih*{sc:.6f}):flags=lanczos")
        xe = lerp_expr(s["keys"], 1, sc, s["n"])
        ye = lerp_expr(s["keys"], 2, sc, s["n"])
        vf.append(f"crop={W}:{H}:x='round({xe})':y='round({ye})'")
    else:
        vf.append(f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}")
    vf.append("format=yuv420p")
    sh(["ffmpeg", "-y", "-v", "error", *pre, "-ss", f"{ss:.4f}", "-i", src, "-an", "-vf", ",".join(vf),
        "-frames:v", str(s["n"]), *ENC, str(out)])
    write_stamp(out, stamp)
    (BUILD / f"{s['id']}.ss").write_text(f"{ss:.4f}")
    return out


def ffmpeg_pipe(out, extra_in=()):
    return subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                             "-r", str(FPS), "-i", "-", *ENC, str(out)], stdin=subprocess.PIPE)


def lerp(a, b, t):
    return a + (b - a) * t


def prep_still(s):
    out = BUILD / f"{s['id']}.mp4"
    stamp = json.dumps({k: s.get(k) for k in ("id", "n", "img", "mode", "z", "c", "shift", "w", "x0", "y0", "yc", "plate")}, sort_keys=True) + "v8"
    if stamp_ok(out, stamp):
        return out
    img = Image.open(f"{DESIGN}/{s['img']}").convert("RGB")
    n = s["n"]
    ease = lambda t: t * t * (3 - 2 * t)
    p = ffmpeg_pipe(out)
    mode = s["mode"]
    if mode == "fit":
        bg = img.resize((1920, 1920), Image.BILINEAR).crop((420, 0, 1500, 1920)).filter(ImageFilter.GaussianBlur(40))
        bg = Image.eval(bg, lambda v: int(v * 0.55))
    for i in range(n):
        t = ease(i / max(n - 1, 1))
        if mode == "blueprint":
            zoom = 1 + 0.03 * t
            cw = 1210 / zoom; ch = 1440 / zoom
            x0 = 703 - cw / 2; y0 = 720 - ch / 2
            ph = ch * (W / cw)
            body = img.resize((W, round(ph)), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
            canvas = Image.new("RGB", (W, H), (51, 51, 51))
            canvas.paste(body, (0, round((H - ph) / 2)))
        elif mode == "fit":
            z = lerp(*s["z"], t); sc = 0.75 * z
            cx = s["c"][0] + s["shift"][0] * t; cy = s["c"][1] + s["shift"][1] * t
            yc = s.get("yc", 0.5) * H
            im2 = img.resize((round(1440 * sc), round(1440 * sc)), Image.LANCZOS)
            canvas = bg.copy()
            m = np.ones(im2.size[::-1], np.float32); ramp = np.linspace(0, 1, 200)
            m[:200] *= ramp[:, None]; m[-200:] *= ramp[::-1][:, None]
            canvas.paste(im2, (round(W / 2 - cx * sc), round(yc - cy * sc)), Image.fromarray((m * 255).astype(np.uint8)))
        else:
            w = lerp(*s["w"], t); h = w * 16 / 9
            x0 = lerp(*s["x0"], t); y0 = lerp(*s["y0"], t)
            canvas = img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h))
        arr = np.asarray(canvas)
        pl = s.get("plate")
        if pl:   # (frame_from, frame_to, y0, y1, alpha): feathered dark band behind a label
            f0, f1, y0, y1, al = pl
            k = min(1.0, max(0.0, (i - f0) / 8.0)) * min(1.0, max(0.0, (f1 - i) / 6.0))
            if k > 0:
                yy = np.arange(y0, y1); edge = np.minimum(1, np.minimum(yy - y0, y1 - yy) / 80.0)
                arr = arr.astype(np.float32); arr[y0:y1] *= (1 - al * k * edge)[:, None, None]; arr = arr.clip(0, 255).astype(np.uint8)
        p.stdin.write(arr.tobytes())
    p.stdin.close(); p.wait()
    write_stamp(out, stamp)
    return out


def prep_logo(s):
    out = BUILD / f"{s['id']}.mp4"
    stamp = json.dumps({"n": s["n"], "w": 720}) + f"v4_{nout(s)}"
    if stamp_ok(out, stamp):
        return out
    logo = Image.open(LOGO).convert("RGBA")
    lw = 720
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    n = nout(s)
    p = ffmpeg_pipe(out)
    for i in range(n):
        a = min(1.0, (i + 1) / 5.0)                      # pops in over 5 frames on the downbeat
        a *= min(1.0, (n - i) / 16.0)                    # and goes with the music's fade
        sc = 1 + 0.03 * i / n
        L = logo.resize((round(logo.width * sc), round(logo.height * sc)), Image.LANCZOS)
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        L.putalpha(L.getchannel("A").point(lambda v: int(v * a)))
        fr.alpha_composite(L, (W // 2 - L.width // 2, H // 2 - L.height // 2))
        p.stdin.write(np.asarray(fr.convert("RGB")).tobytes())
    p.stdin.close(); p.wait()
    write_stamp(out, stamp)
    return out


# ---------------------------------------------------------------- scan shots
def png_ok(path):
    try:
        return os.path.getsize(path) > 1000 and (os.path.getmtime(path) < __import__("time").time() - 4)
    except OSError:
        return False


def scan_status(scan):
    d = Path(SM) / "renders" / scan / "png"
    have = {}
    for f in glob.glob(str(d / "f_*.png")):
        i = int(Path(f).stem.split("_")[1])
        if png_ok(f):
            have[i] = f
    need = SCAN_NEED[scan]
    complete = all(i in have for i in range(1, need + 1))
    return have, complete


def minterp(frames_dir_pattern, start_number, nframes_out, out_mp4, nin, rate=15.0):
    """15 fps PNG run -> 30 fps with minterpolate; exactly nframes_out frames (pads with the last frame if short)."""
    vf = (f"trim=end_frame={nin},setpts=PTS-STARTPTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale={W}:{H}:flags=lanczos,format=yuv420p,"
          f"tpad=stop_mode=clone:stop_duration=1")
    sh(["ffmpeg", "-y", "-v", "error", "-framerate", f"{rate:.4f}", "-start_number", str(start_number), "-i", frames_dir_pattern,
        "-vf", vf, "-frames:v", str(nframes_out), *ENC, str(out_mp4)])


def prep_scan(s):
    out = BUILD / f"{s['id']}.mp4"
    have, complete = scan_status(s["scan"])
    prev = Path(SM) / "scan3d" / "look" / f"pv_{s['scan']}"
    pv = {}
    for f in glob.glob(str(prev / "f_*.png")):
        pv[int(Path(f).stem.split("_")[1])] = f
    stamp = json.dumps({"scan": s["scan"], "complete": complete, "n": s["n"],
                        "frames": sorted(have)[-1] if complete else sorted(have), "pv": sorted(pv),
                        "t0": s.get("t0"), "sp": s.get("speed"), "last": s.get("last_png"), "need": SCAN_NEED[s["scan"]]}) + f"v7_{nout(s)}"
    if stamp_ok(out, stamp):
        return out, complete
    n = nout(s); t0 = s["t0"]
    pat = str(Path(SM) / "renders" / s["scan"] / "png" / "f_%04d.png")
    if complete:
        first = int(round(t0 * 15)) + 1             # png index at t0 (idx 1 = t 0)
        last = s.get("last_png") or SCAN_NEED[s["scan"]]
        minterp(pat, first, n, out, last - first + 1, rate=15.0 * s.get("speed", 1.0))   # last_png: S10a stops before the state swap (frame frozen)
    else:
        avail = dict(pv); avail.update(have)         # real renders override the previews at the same index
        if not avail:                                # a4 not rendered yet: hold A2's last frame (the same camera it starts from)
            avail = {1: str(Path(SM) / "renders" / "a2_body_on_off" / "png" / "f_0075.png")}
        idxs = sorted(avail)
        font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 30)
        p = ffmpeg_pipe(out)
        cache = {}
        for k in range(n):
            t = t0 + k / 30.0 * s.get("speed", 1.0)
            pidx = t * 15 + 1 + 1e-6
            cands = [i for i in idxs if i <= pidx]
            i = cands[-1] if cands else idxs[0]
            if i not in cache:
                im = Image.open(avail[i]).convert("RGB").resize((W, H), Image.LANCZOS)
                cache = {i: im}
            im = cache[i].copy()
            d = ImageDraw.Draw(im)
            d.rectangle((24, H - 90, 560, H - 40), fill=(0, 0, 0))
            d.text((34, H - 84), f"PLACEHOLDER {s['scan']}", font=font, fill=(255, 80, 80))
            p.stdin.write(np.asarray(im).tobytes())
        p.stdin.close(); p.wait()
    write_stamp(out, stamp)
    return out, complete


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    status = {}
    for s in SHOTS:
        if args and s["id"] not in args:
            continue
        if force:
            for f in BUILD.glob(f"{s['id']}.mp4*"):
                f.unlink()
        k = s["kind"]
        if k == "irl":
            prep_irl(s); status[s["id"]] = "final"
        elif k == "still":
            prep_still(s); status[s["id"]] = "final"
        elif k == "logo":
            prep_logo(s); status[s["id"]] = "final"
        else:
            _, complete = prep_scan(s); status[s["id"]] = "final" if complete else "PLACEHOLDER"
        print(s["id"], status[s["id"]], flush=True)
    (BUILD / "status.json").write_text(json.dumps(status, indent=1)) if not args else None


if __name__ == "__main__":
    main()
