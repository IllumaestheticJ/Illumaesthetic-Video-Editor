"""Ep 8 real footage: MR2 print timelapse -> 1080x1920 with the printer maker's logo blurred.

The logo sits on the dark plate just below the toolhead's white housing, which moves every frame. Per frame: threshold the
bright housing in the top half, take the largest blob, and blur a box from the blob's lower part down past the plate
(feathered). The landscape frame is shown full width (1080x608, a downscale, so it stays sharp) over a blurred, darkened
fill of itself (lesson: landscape media in 9:16). Usage: python irl_print.py IN.avi OUT.mp4 [--debug DIR]
"""
import sys, subprocess
import numpy as np, cv2

src, dst = sys.argv[1], sys.argv[2]
dbg = sys.argv[sys.argv.index("--debug") + 1] if "--debug" in sys.argv else None
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = 1080, 1920
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps),
                       "-i", "-", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
n = 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    h, w = f.shape[:2]
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    top = (g[: int(h * 0.55)] > 215).astype(np.uint8)
    top = cv2.morphologyEx(top, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    k, lab, st, _ = cv2.connectedComponentsWithStats(top)
    mask = np.zeros((h, w), np.float32)
    for i in range(1, k):  # every bright housing blob (the housing can split in two around the fan)
        x, y, bw, bh = st[i, :4]
        if st[i, cv2.CC_STAT_AREA] > 2500:
            x0, x1 = max(0, x - 110), min(w, x + bw + 130)
            y0, y1 = max(0, y + bh - 70), min(h, y + bh + 120)
            mask[y0:y1, x0:x1] = 1
    mask = cv2.GaussianBlur(mask, (0, 0), 12)[..., None]
    bl = cv2.GaussianBlur(f, (0, 0), 18)
    f = (f * (1 - mask) + bl * mask).astype(np.uint8)
    fg = cv2.resize(f, (W, int(round(h * W / w))), interpolation=cv2.INTER_AREA)
    bgs = cv2.resize(f, (int(w * H / h), H), interpolation=cv2.INTER_AREA)
    cx = (bgs.shape[1] - W) // 2
    bg = cv2.GaussianBlur(bgs[:, cx:cx + W], (0, 0), 40) * 0.35
    out = bg.astype(np.uint8)
    y = (H - fg.shape[0]) // 2
    out[y:y + fg.shape[0]] = fg
    if dbg and n % 4 == 0:
        cv2.imwrite(f"{dbg}/f{n:04d}.jpg", out[y:y + fg.shape[0]])
    ff.stdin.write(out.tobytes()); n += 1
ff.stdin.close(); ff.wait()
print(n, "frames at", fps)
