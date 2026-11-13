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
from PIL import Image, ImageDraw, ImageFont

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


def prep_irl(s):
    out = BUILD / f"{s['id']}.mp4"
    stamp = json.dumps({k: s.get(k) for k in ("src", "ss", "n", "win", "keys", "rot180")}, sort_keys=True) + f"v5_{nout(s)}"
    if stamp_ok(out, stamp):
        return out
    src = f"{DB}/{s['src']}.mov"
    hlg = probe_tf(src) in ("arib-std-b67", "smpte2084")
    pre = ["-display_rotation", "0"] if s.get("rot180") else []   # drop the wrong -90 tag on the input (a bare -noautorotate leaves it as side data on the output, and every later decoder rotates it again)
    vf = []
    if s.get("rot180"):
        vf.append("hflip,vflip")
    vf.append("fps=30")
    if hlg:
        vf.append(TONEMAP_HLG)
    if s["win"]:
        w, h = s["win"]
        sc = H / h
        # source dims after rotation fix (landscape 1920x1080 or the 3:4 sizes): scale by sc, crop at scaled offsets
        vf.append(f"scale=round(iw*{sc:.6f}):round(ih*{sc:.6f}):flags=lanczos")
        xe = lerp_expr(s["keys"], 1, sc, s["n"])
        ye = lerp_expr(s["keys"], 2, sc, s["n"])
        vf.append(f"crop={W}:{H}:x='round({xe})':y='round({ye})'")
    else:
        vf.append(f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}")
    vf.append("format=yuv420p")
    sh(["ffmpeg", "-y", "-v", "error", *pre, "-ss", f"{s['ss']:.4f}", "-i", src, "-an", "-vf", ",".join(vf),
        "-frames:v", str(nout(s)), *ENC, str(out)])
    write_stamp(out, stamp)
    return out


def ffmpeg_pipe(out, extra_in=()):
    return subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                             "-r", str(FPS), "-i", "-", *ENC, str(out)], stdin=subprocess.PIPE)


def window_frame(img, win, flat):
    """win = (x0, y0, w, h) in source px, may be fractional; returns the 1080x1920 RGB array (Lanczos from the source)."""
    x0, y0, w, h = win
    # affine crop+scale in one resample (PIL transform with Lanczos is not available -> crop box + resize with box)
    out = img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h))
    return np.asarray(out)


PLATE_X0, PLATE_X1, PLATE_Y0, PLATE_Y1 = 40, 520, 1296, 1500
_m = np.zeros((PLATE_Y1 - PLATE_Y0, PLATE_X1 - PLATE_X0), np.float32)
_m[30:-30, 30:-30] = 1.0
PLATE_MASK = np.asarray(Image.fromarray((_m * 255).astype(np.uint8)).filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(14))).astype(np.float32) / 255.0


def prep_still(s):
    out = BUILD / f"{s['id']}.mp4"
    stamp = json.dumps({"id": s["id"], "n": s["n"], "img": s["img"]}) + f"v5_{nout(s)}"
    if stamp_ok(out, stamp):
        return out
    img = Image.open(f"{DESIGN}/{s['img']}").convert("RGB")
    n = nout(s)
    p = ffmpeg_pipe(out)
    ease = lambda t: t * t * (3 - 2 * t)
    for i in range(n):
        t = ease(i / (n - 1))
        if s["id"] == "S19":
            # Blueprint: crop x 98..1308 (car 1114 px wide), 3 % push-in; the still's flat grey (51,51,51) pads top and bottom
            zoom = 1 + 0.03 * t
            cw = 1210 / zoom
            cx = (98 + 1308) / 2 + 0 * t
            ch = 1440 / zoom
            x0 = cx - cw / 2
            y0 = 720 - ch / 2
            sc = W / cw
            ph = ch * sc                     # scaled height of the full 1440-row band (< 1920)
            body = img.resize((W, round(ph)), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
            canvas = Image.new("RGB", (W, H), (51, 51, 51))
            canvas.paste(body, (0, round((H - ph) / 2)))
            arr = np.asarray(canvas)
        else:
            # RenderDay1: 810x1440 @ x0 310 -> 778x1383 @ x0 326, y0 0 -> 44 (4 % push, car stays in with ~20 px margin)
            w = 810 + (778 - 810) * t; h = 1440 + (1383 - 1440) * t
            x0 = 310 + (326 - 310) * t; y0 = 0 + 44 * t
            arr = window_frame(img, (x0, y0, w, h), None)
            # dark plate behind the HELLKITTEN / DESIGN RENDER label (it straddles the yellow arrow): label frames 23..84 of this shot
            k = min(1.0, max(0.0, (i - 23) / 8.0)) * min(1.0, max(0.0, (84 - i) / 6.0))
            if k > 0:
                arr = arr.astype(np.float32)
                arr[PLATE_Y0:PLATE_Y1, PLATE_X0:PLATE_X1] *= (1 - 0.55 * k * PLATE_MASK[:, :, None])
                arr = arr.clip(0, 255).astype(np.uint8)
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
        a *= min(1.0, (n - i) / 10.0)                    # and goes with the music's fade
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
                        "t0": s.get("t0"), "swap": s.get("swap_t"), "ps": s.get("post_speed"), "need": SCAN_NEED[s["scan"]]}) + f"v6_{nout(s)}"
    if stamp_ok(out, stamp):
        return out, complete
    n = nout(s); t0 = s["t0"]
    pat = str(Path(SM) / "renders" / s["scan"] / "png" / "f_%04d.png")
    if complete:
        first = int(round(t0 * 15)) + 1             # png index at t0 (idx 1 = t 0)
        swap = s.get("swap_t")
        if swap is None:
            minterp(pat, first, n, out, SCAN_NEED[s["scan"]] - first + 1)
        else:
            k_swap = int(round((swap - t0) * 30))       # output frame where the stripped state starts
            sidx = int(round(swap * 15)) + 1             # png index of the first stripped frame (25)
            a, b = BUILD / f"{s['id']}_pre.mp4", BUILD / f"{s['id']}_post.mp4"
            # pre-swap: assembled frames only (png first .. sidx-1), the last one frozen for the odd frame before the swap
            minterp(pat, first, k_swap, a, sidx - first)
            minterp(pat, sidx, n - k_swap, b, SCAN_NEED[s["scan"]] - sidx + 1, rate=15.0 * s.get("post_speed", 1.0))
            lst = BUILD / f"{s['id']}_list.txt"
            lst.write_text(f"file '{a}'\nfile '{b}'\n")
            sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset",
                "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-frames:v", str(n), str(out)])
    else:
        avail = dict(pv); avail.update(have)         # real renders override the previews at the same index
        idxs = sorted(avail)
        font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 30)
        p = ffmpeg_pipe(out)
        cache = {}
        for k in range(n):
            t = t0 + k / 30.0
            if s.get("swap_t") is not None and t >= s["swap_t"]:
                t = s["swap_t"] + (k - int(round((s["swap_t"] - t0) * 30))) / 30.0 * s.get("post_speed", 1.0)
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
