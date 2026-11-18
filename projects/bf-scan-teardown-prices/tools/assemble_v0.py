"""v0 assembly: exact 30 fps frames composited in PIL -> ffmpeg; music from the song start, -14 LUFS / TP < -1.
Cuts: T1|T2 f402, kit lock f517, T2|Ron f582, Ron|card f629; music from the song start, delayed 40 ms so measured kick attacks hit them."""
import glob, subprocess, sys
from PIL import Image
M = "/home/user/media/bf-scan-teardown-prices/"; O = M + "ov/"
import os, json
VER = os.environ.get("VER", "v0")
OUT = f"/home/user/media/work/out/bf-scan-teardown-prices_{VER}.mp4"; TMP = M + "v0_video.mp4"
FPS, W, H = 30, 1080, 1920
# v0.5 (user: "the scene right before Ron's render takes a bit too long; have clips match the beat"):
# every clip starts/ends on a measured hit of the grid 0.024 + 0.5374 k (k = beat):
#   T1 beats 0-24 (cut on the b24 onset 12.864 + the 40 ms audio delay, measured 12.936 on the output -> f388) | T2 b24-b33 (kit locks on the kick entry b32 = 17.235, ONE beat hold) |
#   Ron b33-b37 (one bar) | end card b37-b42.   Measured kick attacks: b33 17.765, b37 19.905, b42 22.605.
C1, C2, C3 = 388, round(17.765 * 30), round(19.905 * 30)
END = round(float(os.environ.get("END_S", "22.605")) * 30)   # v0.11 (user: end text longer): END_S=25.825 = beat 48, phrase end
T2_T0 = 13.435                                 # song time of T2 frame 0 (15 fps)
t1 = sorted(glob.glob(M + os.environ.get("T1DIR", "r/T1") + "/f*.png")); t2 = sorted(glob.glob(M + os.environ.get("T2DIR", "r/T2v02" if VER != "v0" else "r/T2") + "/f*.png"))
RFPS = int(os.environ.get("RFPS", "15"))      # render fps of T1/T2 dirs: 15 = draft (frames doubled), 30 = full-res v1
RON = os.environ.get("RON", "r/ron7_portrait.png"); MASK = os.environ.get("MASK", "r/ron7_mask.png")
ron = Image.open(M + RON).convert("RGB").resize((W, H), Image.LANCZOS)
# v0.7: end text over Ron's render with depth; car matte from ron_mask_v0.py (alpha above the floor line only).
import numpy as np
eb, ef = Image.open(O + "end_back.png"), Image.open(O + "end_front.png")
ma = np.array(Image.open(M + MASK).getchannel("A").resize((W, H), Image.LANCZOS)).astype(np.float32)
FLOOR = 1088; ma[FLOOR:] = 0; ma = np.clip((ma - 200) * 255 / 55, 0, 255).astype(np.uint8)   # floor glow out, edges kept
carm = Image.fromarray(ma)
PUSH = float(os.environ.get("PUSH", "0"))     # v0.11: slow push-in on Ron's shot, 0 at the 1:1 cut frame -> PUSH at END
PC = (620, 940)                               # zoom centre ~ the car
def zoom(im, n):
    z = 1 + PUSH * max(0, n - C2) / max(1, END - 1 - C2)
    if z == 1: return im
    w, h = W / z, H / z; x0, y0 = PC[0] - PC[0] / z, PC[1] - PC[1] / z
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)
def endframe(n):
    """back text under the car (matte), front layer one beat later (handled by caller)."""
    r, m = zoom(ron, n), zoom(carm, n)
    fr = r.copy(); fr.paste(eb, (0, 0), eb); fr.paste(r, (0, 0), m); return fr
ovl = {k: Image.open(O + k + ".png") for k in ["bf_tag", "p_lip", "p_skirts", "p_rear", "p_wing"]}
# (name, t_in, t_out, xy) in video seconds; 0.15 s alpha fades
# v0.2 (owner safe-zone rule, knowledge/safe-zones.md): every text box inside x 48-920 / y 285-1440 -> tags/cards
# start at y 300 (above the car); the "FULL EPSILON KIT" tag is dropped (the top view fills the safe band).
OV = [("bf_tag", 0.10, 2.10, (0, 300 - 168 + 60)),
      ("p_lip", 4.83, 6.30, (0, 300 - 145 + 40)), ("p_skirts", 6.96, 9.20, (0, 300 - 145 + 40)),
      ("p_rear", 9.92, 11.15, (0, 300 - 145 + 40)), ("p_wing", 11.80, 12.80, (0, 300 - 145 + 40))]
cache = {}
# text boxes for scripts/safezone_check.py (alpha bbox of each overlay at its position, plus the end card's own text)
BOX = []
for name, a0, b0, xy in OV:
    bb = ovl[name].getchannel("A").getbbox()
    BOX.append({"label": name, "t0": a0, "t1": b0, "x": xy[0] + bb[0], "y": xy[1] + bb[1], "w": bb[2] - bb[0], "h": bb[3] - bb[1], "key": True})
for b in json.load(open(O + "endcard_boxes.json")):
    BOX.append(dict(b, t0=round(C3 / FPS, 3), t1=round(END / FPS, 3)))
json.dump(BOX, open(M + f"boxes_{VER}.json", "w"), indent=1)
def load(p):
    if p not in cache:
        cache.clear(); cache[p] = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)
    return cache[p]
ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", TMP], stdin=subprocess.PIPE)
for n in range(END):
    t = n / FPS
    if n < C1:   fr = load(t1[min(len(t1) - 1, n * RFPS // FPS)]).copy()
    elif n < C2:  # T2 now starts earlier (b24): stretch its slow opening drift 13.435-14.466 over 12.867-14.466; lock stays at 17.235
        t1c = C1 / FPS; tt = t if t >= 14.466 else T2_T0 + (t - t1c) / (14.466 - t1c) * (14.466 - T2_T0)
        fr = load(t2[max(0, min(len(t2) - 1, round((tt - T2_T0) * RFPS)))]).copy()
    elif n < C3: fr = zoom(ron, n)
    else:        # v0.7: render stays; back text + car matte on the C3 kick, front layer one beat (16 f) later
        fr = endframe(n)
        if n >= C3 + 16: fr.paste(ef, (0, 0), ef)
        k = min(1, (END - 1 - n) / 15); fr = Image.blend(Image.new("RGB", (W, H)), fr, k)
    for name, a, b, xy in OV:
        if a <= t <= b:
            k = min(1, (t - a) / 0.15, (b - t) / 0.15)
            im = ovl[name]
            if k < 1:
                im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * k)))
            fr.paste(im, xy, im)
    ff.stdin.write(fr.tobytes())
    if n in (0, C1 - 1, C1, 517, C2 - 1, C2, C3 - 1, C3, C3 + 16, END - 16, END - 1): fr.save(M + f"chk/{VER}_f{n:04d}.jpg", quality=85)
ff.stdin.close(); ff.wait()
dur = END / FPS
af = f"adelay=40:all=1,afade=t=out:st={dur - 0.6:.3f}:d=0.6"   # +40 ms: kick attacks (~45 ms before the low-band peak) land on the cut frames
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
