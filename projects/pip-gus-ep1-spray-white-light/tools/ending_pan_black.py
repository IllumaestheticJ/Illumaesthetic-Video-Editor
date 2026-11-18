"""Alt ending (owner request after v2): no logo card - at the logo cut the question card pans off frame to black.

  python ending_pan_black.py IN.mp4 OUT.mp4 [--at 1410] [--pan 18]

Frames before --at are copied untouched. From --at the last card frame (at-1) slides out to the left with an ease-in over
--pan frames (a camera pan away from the card); the rest holds black (the card's own background tone, so there is no seam) to the end. Audio is copied as-is (the music's final
chord still lands where the logo used to be).
"""
import subprocess, sys
import numpy as np

W, H, FPS = 1080, 1920, 30


def arg(n, d):
    return type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d


def main():
    src, dst = sys.argv[1], sys.argv[2]
    at, pan = arg("--at", 1410), arg("--pan", 18)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a", "-c:a", "copy", "-c:v", "libx264", "-preset", "slow",
                            "-crf", "16", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-colorspace", "bt709", "-movflags", "+faststart", "-shortest", dst], stdin=subprocess.PIPE)
    n, last, black = W * H * 3, None, np.zeros((H, W, 3), np.uint8)
    f = 0
    while True:
        b = dec.stdout.read(n)
        if len(b) < n:
            break
        fr = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        if f < at:
            out, last = fr, fr
            if f == at - 1:   # the card's own near-black (#0b0c0b-ish), so the pan shows no seam: only the text slides away
                black = np.broadcast_to(np.median(fr[:200, :200].reshape(-1, 3), axis=0).astype(np.uint8), (H, W, 3)).copy()
        elif f < at + pan:
            u = (f - at + 1) / pan
            dx = int(round(W * u ** 3))          # ease-in: starts slow, whips off
            out = black.copy()
            if dx < W:
                out[:, :W - dx] = last[:, dx:]
        else:
            out = black
        enc.stdin.write(np.ascontiguousarray(out).tobytes())
        f += 1
    enc.stdin.close()
    enc.wait()
    dec.wait()
    print("frames", f, "pan", at, at + pan)


if __name__ == "__main__":
    main()
