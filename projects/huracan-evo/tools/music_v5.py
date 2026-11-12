"""v5 (30 s cut) music edit: 3 s silence for the reference engine start, then reel_track_a from kick k20 (break) to the end.
Output kicks n = k - 20 at t = 3.0768 + 0.60006 n: lift (k32) n12 = 10.278 s; last kick (k60) n40 = 27.079 s; reverb tail after.
0.25 s fade-in at the entry so the pad does not start on a hard edge.   python tools/music_v5.py OUT.wav"""
import subprocess
import sys

SRC = "/home/user/media/work/music/reel_track_a.mp3"


def main(out):
    # seek to k20 - 0.0768 s, delay 3 s -> k20 lands at 3.0768 (same grid as v3/v4)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{0.60006 * 20:.5f}", "-i", SRC,
                    "-af", "afade=t=in:d=0.25,adelay=3000|3000,aresample=48000", "-ac", "2", "-c:a", "pcm_s24le", out], check=True)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
