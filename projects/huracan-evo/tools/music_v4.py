"""v4 music edit: the coupe pre-lift section is 24 beats shorter than v3 (user: "the beginning panning takes too long").
reel_track_a kicks: t = 0.0768 + 0.60006 k (lift k32, last kick k60). Layout (n = output kick index, n0 at 3.0768 s):
  3 s silence (engine start) | k0-k28 | k20-k56 (break, lift at n40, groove) | k40-end
Splices sit 60 ms before a kick peak with a 15 ms crossfade (same method as v3's track_a_hp.wav).
  python tools/music_v4.py OUT.wav
"""
import subprocess
import sys

import numpy as np

SRC = "/home/user/media/work/music/reel_track_a.mp3"
SR = 48000
K0, KP = 0.0768, 0.60006
PRE, XF = 0.060, 0.015


def kt(k):
    return K0 + KP * k - PRE


def main(out):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
    segs = [(0.0, kt(28)), (kt(20), kt(56)), (kt(40), len(x) / SR)]
    lead = np.zeros((int(3.0 * SR), 2), np.float32)
    outa = np.concatenate([lead, x[: int(segs[0][1] * SR)]])
    xf = int(XF * SR)
    r = np.linspace(0, 1, xf)[:, None]
    for a, b in segs[1:]:
        seg = x[int(a * SR): int(b * SR)].copy()
        outa[-xf:] = outa[-xf:] * (1 - r) + seg[:xf] * r
        outa = np.concatenate([outa, seg[xf:]])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", out],
                   input=outa.astype(np.float32).tobytes(), check=True)
    n_lift = 28 + (32 - 20)
    print(out, round(len(outa) / SR, 2), "s; lift n", n_lift, "at", round(3.0768 + KP * n_lift, 3), "s")


if __name__ == "__main__":
    main(sys.argv[1])
