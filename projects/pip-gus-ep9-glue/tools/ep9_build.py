"""Ep 9 assembly: cartoon frames + phone-screen corner pin + Part B + finale tag + logo card, gfx overlay, audio mix.

Output frames (30 fps, 1080x1920), take frames are the Blender render's numbering (tools/ep9_scene.py):
  0    - 1138  Part A        take frames 0 - 1138 (E12: the timelapse plays in the phone screen, corner-pinned, key-matted)
  1139 - 1288  Part B        timelapse frames 76 - 177 (102), then the finished 350Z (48)
  1289 - 1402  finale tag    take frames 1139 - 1252
  1403 - 1492  logo card     (from the gfx overlay, opaque)
Checks: no gfx pixel (alpha > 0) over real footage - all of Part B and the phone screen area in E12.

Usage: python ep9_build.py FRAMES_DIR OUT.mp4 [--corners screen_corners.json]
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

W, H, FPS = 1080, 1920, 30
A_N, B_N, TAG_N, LOGO_N = 1139, 150, 114, 90
TOTAL = A_N + B_N + TAG_N + LOGO_N
PHONE_N = 76                       # timelapse frames shown in the phone before Part B
WORK = Path("/home/user/media/pip-gus-ep9-glue/work")
GFX = Path("/home/user/media/pip-gus-ep9-glue/gfx/ep9_gfx.mov")
MIX = Path("/home/user/media/pip-gus-ep9-glue/audio/ep9_mix.wav")
KEY = np.array([255, 0, 255], np.int16)


def frames(path, n=None):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE,
                         bufsize=10 ** 8)
    k = 0
    while n is None or k < n:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
        k += 1
    p.stdout.close(); p.wait()


def render_frame(fd, f):
    im = cv2.imread(str(fd / f"{f:05d}.png"), cv2.IMREAD_COLOR)
    assert im is not None, f"missing frame {f}"
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    if im.shape[:2] != (H, W):
        im = cv2.resize(im, (W, H), interpolation=cv2.INTER_LANCZOS4)
    return im


def pin(base, src, quad):
    """Corner-pin src (upright 9:16) into quad (tl, tr, br, bl px), only where base shows the magenta key."""
    q = np.array(quad, np.float32)
    M = cv2.getPerspectiveTransform(np.array([[0, 0], [W, 0], [W, H], [0, H]], np.float32), q)
    warped = cv2.warpPerspective(src, M, (W, H), flags=cv2.INTER_LINEAR)
    d = np.abs(base.astype(np.int16) - KEY).sum(2)
    a = np.clip((160 - d) / 100.0, 0, 1)[..., None]          # soft key: pure key -> 1, edges blend
    poly = np.zeros((H, W), np.uint8)
    cv2.fillConvexPoly(poly, q.astype(np.int32), 1)
    a = a * poly[..., None]
    return (base * (1 - a) + warped * a + 0.5).astype(np.uint8), a[..., 0] > 0.05


def main():
    fd, outp = Path(sys.argv[1]), Path(sys.argv[2])
    cj = json.loads(Path(sys.argv[sys.argv.index("--corners") + 1]).read_text()) if "--corners" in sys.argv else {}
    tl = list(frames(WORK / "tl_178.mp4"))
    z350 = list(frames(WORK / "partB_350z.mp4", 48))
    assert len(tl) == 178 and len(z350) == 48, (len(tl), len(z350))
    e12 = sorted(int(k) for k in cj)
    tmpv = outp.with_suffix(".video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-colorspace", "bt709", str(tmpv)], stdin=subprocess.PIPE)
    gp = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(GFX), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE,
                          bufsize=10 ** 8)
    bad, rep = [], {}
    phone_first = e12[-1] - PHONE_N + 1 if e12 else None
    for of in range(TOTAL):
        real = None
        if of < A_N:
            base = render_frame(fd, of)
            if str(of) in cj and of >= phone_first:
                base, real = pin(base, tl[of - phone_first], cj[str(of)])
            seg = "A"
        elif of < A_N + B_N:
            k = of - A_N
            base = tl[PHONE_N + k] if k < 102 else z350[k - 102]
            real = np.ones((H, W), bool)
            seg = "B"
        elif of < A_N + B_N + TAG_N:
            base = render_frame(fd, of - B_N)
            seg = "tag"
        else:
            base = np.zeros((H, W, 3), np.uint8)
            seg = "logo"
        g = np.frombuffer(gp.stdout.read(W * H * 4), np.uint8).reshape(H, W, 4)
        al = g[..., 3:4].astype(np.float32) / 255
        if real is not None and (g[..., 3][real] > 8).any():
            bad.append(of)
        out = base.astype(np.float32) * (1 - al) + g[..., :3].astype(np.float32) * al
        enc.stdin.write((out + 0.5).astype(np.uint8).tobytes())
        rep[seg] = rep.get(seg, 0) + 1
    enc.stdin.close(); enc.wait(); gp.stdout.close(); gp.wait()
    print("segments:", rep, "text-over-real frames:", bad[:20], len(bad))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmpv), "-i", str(MIX), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", str(outp)], check=True)
    tmpv.unlink()
    print(outp)
    if bad:
        sys.exit("FAIL: captions over real footage on frames " + str(bad[:20]))


if __name__ == "__main__":
    main()
