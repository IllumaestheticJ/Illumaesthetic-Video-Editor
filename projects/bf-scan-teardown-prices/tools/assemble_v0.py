"""v0 assembly: exact 30 fps frames composited in PIL -> ffmpeg; music from the song start, -14 LUFS / TP < -1.
Cuts (song s = video s): T1|T2 13.398 (f402), T2|Ron 19.390 (f582), Ron|card 20.985 (f630); kit locks 17.235 (f517)."""
import glob, subprocess, sys
from PIL import Image
M = "/home/user/media/bf-scan-teardown-prices/"; O = M + "ov/"
OUT = "/home/user/media/work/out/bf-scan-teardown-prices_v0.mp4"; TMP = M + "v0_video.mp4"
FPS, W, H = 30, 1080, 1920
C1, C2, C3, END = 402, 582, 630, 708          # frame numbers
T2_T0 = 13.435                                 # song time of T2 frame 0 (15 fps)
t1 = sorted(glob.glob(M + "r/T1/f*.png")); t2 = sorted(glob.glob(M + "r/T2/f*.png"))
ron = Image.open(M + "r/ron7_portrait.png").convert("RGB").resize((W, H), Image.LANCZOS)
endc = Image.open(O + "endcard.png").convert("RGB")
ovl = {k: Image.open(O + k + ".png") for k in ["bf_tag", "kit_tag", "p_lip", "p_skirts", "p_rear", "p_wing", "eps_1to1", "eps_micro", "del_micro"]}
# (name, t_in, t_out, xy) in video seconds; 0.15 s alpha fades
OV = [("bf_tag", 0.10, 2.10, (0, 60)),
      ("eps_1to1", 0.25, 2.60, (790, 740)),
      ("p_lip", 4.83, 6.30, (0, 40)), ("p_skirts", 6.96, 9.20, (0, 40)),
      ("p_rear", 9.92, 11.15, (0, 40)), ("p_wing", 11.80, 13.33, (0, 40)),
      ("kit_tag", 13.45, 14.40, (0, 40)),
      ("eps_micro", 13.45, 14.40, (sys.argv[1:] and int(sys.argv[1]) or 360, int(sys.argv[2]) if len(sys.argv) > 2 else 1350)),
      ("del_micro", 13.45, 14.40, (int(sys.argv[3]) if len(sys.argv) > 3 else 520, int(sys.argv[4]) if len(sys.argv) > 4 else 1490))]
cache = {}
def load(p):
    if p not in cache:
        cache.clear(); cache[p] = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)
    return cache[p]
ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", TMP], stdin=subprocess.PIPE)
for n in range(END):
    t = n / FPS
    if n < C1:   fr = load(t1[min(len(t1) - 1, n // 2)]).copy()
    elif n < C2: fr = load(t2[max(0, min(len(t2) - 1, round((t - T2_T0) * 15)))]).copy()
    elif n < C3: fr = ron.copy()
    else:        fr = endc.copy()
    if n >= C3:  # end card fades in from black over 4 frames, everything fades out over the last 0.5 s
        k = min(1, (n - C3 + 1) / 4) * min(1, (END - 1 - n) / 15); fr = Image.blend(Image.new("RGB", (W, H)), fr, k)
    for name, a, b, xy in OV:
        if a <= t <= b:
            k = min(1, (t - a) / 0.15, (b - t) / 0.15)
            im = ovl[name]
            if k < 1:
                im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * k)))
            fr.paste(im, xy, im)
    ff.stdin.write(fr.tobytes())
    if n in (0, C1 - 1, C1, 517, C2 - 1, C2, C3, END - 1): fr.save(M + f"chk/f{n:04d}.jpg", quality=85)
ff.stdin.close(); ff.wait()
dur = END / FPS
af = f"afade=t=out:st={dur - 0.6:.3f}:d=0.6"
meas = subprocess.run(["ffmpeg", "-v", "info", "-t", f"{dur}", "-i", "/home/user/media/work/music/xxx.m4a", "-af", af + ",ebur128=peak=true", "-f", "null", "-"],
                      capture_output=True, text=True).stderr
I = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
TP = float([l for l in meas.splitlines() if l.strip().startswith("Peak:")][-1].split()[1])
g = min(-14.0 - I, -1.5 - TP)   # target -14 LUFS, the -1 dBFS true-peak ceiling wins (1.5 dB AAC headroom)
print("music I", I, "TP", TP, "gain dB", round(g, 2))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", TMP, "-t", f"{dur}", "-i", "/home/user/media/work/music/xxx.m4a",
                "-af", f"{af},volume={g:.2f}dB", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                "-ar", "48000", "-shortest", "-movflags", "+faststart", OUT], check=True)
print("wrote", OUT)
