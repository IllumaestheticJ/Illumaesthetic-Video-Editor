"""Paint a burned-in caption out of a clip where it sits on clean sky, keeping the FULL frame (no crop).
    python tools/uncaption.py SRC IN OUT OUTFILE [--box x0,y0,x1,y1] [--slow 1.08]
Each column inside the box is replaced by a linear ramp between the sky just above and just below it
(blurred along x), plus matched grain. Only valid when the box contains nothing but sky."""
import argparse, subprocess, numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("t0", type=float); ap.add_argument("t1", type=float)
ap.add_argument("out"); ap.add_argument("--box", default="80,365,1000,565"); ap.add_argument("--slow", type=float, default=1.0); a = ap.parse_args()
x0, y0, x1, y1 = map(int, a.box.split(","))
cap = cv2.VideoCapture(a.src); fps = cap.get(cv2.CAP_PROP_FPS); cap.release()
w, h = 1080, 1920
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(a.t0), "-i", a.src, "-t", str((a.t1 - a.t0) * a.slow), "-vf", f"setpts={a.slow}*PTS,scale={w}:{h},fps=30",
                        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "30", "-i", "-",
                        "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
rng = np.random.default_rng(0); n = 0
while True:
    b = dec.stdout.read(w * h * 3)
    if len(b) < w * h * 3: break
    f = np.frombuffer(b, np.uint8).reshape(h, w, 3).astype(np.float32)
    top = cv2.blur(f[y0 - 14:y0, x0:x1].mean(0, keepdims=True), (41, 1))[0]
    bot = cv2.blur(f[y1:y1 + 14, x0:x1].mean(0, keepdims=True), (41, 1))[0]
    t = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
    fill = top[None] * (1 - t) + bot[None] * t
    sig = float(np.std(f[y0 - 14:y0, x0:x1] - cv2.blur(f[y0 - 14:y0, x0:x1], (5, 5))))
    fill += rng.normal(0, sig, fill.shape).astype(np.float32)
    m = np.zeros((h, w), np.float32); m[y0:y1, x0:x1] = 1; m = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
    g = f.copy(); g[y0:y1, x0:x1] = fill
    f = f * (1 - m) + g * m
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); n += 1
enc.stdin.close(); enc.wait(); print(n, "frames ->", a.out)
