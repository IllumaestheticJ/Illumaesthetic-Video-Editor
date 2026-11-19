"""Shot list + per-shot renderer for the AESUB spray-gun comment reply.

    python projects/aesub-spray-gun-reply/tools/shots.py preview   # first/mid/last crop check sheet
    python projects/aesub-spray-gun-reply/tools/shots.py render    # 1080x1920 30 fps intermediates (+ audio)

Sony FX3A S-Log3 clips go through the generated LUT (toyota-sera-scan-process/tools/slog3_lut.py) and a
full-height 9:16 window (1215 px of the 3840 frame, x0 in 4K px). Phone clips (HLG/709, rotated) are
auto-rotated by ffmpeg and tonemapped when HLG.
"""
import json
import subprocess
import sys
from pathlib import Path

M = Path("/home/user/media/aesub-spray-gun-reply")
SRC = M / "src"
LUT = M / "slog3_709.cube"
OUT = M / "shots"

# id, file, in (s), out (s), speed, x0 (4K px for FX clips; fraction 0-1 of the post-rotation width for phone clips), audio
SHOTS = [
    dict(id="s01_go", f="FX30541.MP4", i=71.10, o=74.60, sp=1.0, x0=1300, audio=True),
    dict(id="s01b_pour", f="FX30541.MP4", i=77.20, o=80.40, sp=1.0, x0=1450, audio=False,
         pan=[(77.2, 1450), (78.2, 1850), (78.7, 1750), (79.2, 1400), (80.0, 1000), (80.4, 1000)]),
    dict(id="s01c_screw", f="FX30541.MP4", i=82.50, o=84.90, sp=2.0, x0=1050, audio=False,
         pan=[(82.5, 1050), (84.9, 800)]),
    dict(id="s02_front", f="FX30541.MP4", i=98.0, o=100.4, sp=3.0, x0=1900, audio=False),
    dict(id="s03_mirror", f="FX30541.MP4", i=112.6, o=115.0, sp=3.0, x0=1350, audio=False),
    dict(id="s04_door", f="FX30541.MP4", i=145.6, o=148.0, sp=3.0, x0=400, audio=False),
    dict(id="s05_side", f="FX30541.MP4", i=151.6, o=154.0, sp=3.0, x0=1100, audio=False),
    dict(id="s07_done", f="FX30541.MP4", i=166.0, o=168.4, sp=3.0, x0=1250, audio=False),
    dict(id="s08_watch", f="FX30541.MP4", i=189.45, o=190.05, sp=1.0, x0=1350, audio=False),
    dict(id="s10_can", f="FX30547.MP4", i=0.00, o=3.30, sp=1.0, x0=1000, audio=True),
    dict(id="s11_civic_gun", f="civic_1955_14.mov", i=0.0, o=1.3, sp=1.0, x0=0.5, audio=False),
    dict(id="s12_296_can", f="f296_181539.mp4", i=12.0, o=13.6, sp=1.0, x0=0.5, audio=False),
    dict(id="s13_296_scan", f="f296_181812.mp4", i=5.8, o=7.4, sp=1.0, x0=0.5, audio=False),
    dict(id="s14_cleanup", f="FX30553.MP4", i=19.20, o=22.50, sp=1.0, x0=1400, audio=True),
    dict(id="s15_hood", f="FX30553.MP4", i=26.00, o=31.42, sp=1.0, x0=1500, audio=True),
    dict(id="s16_payoff", f="FX30555.MP4", i=13.70, o=21.35, sp=1.0, x0=1250, audio=True),
]


def is_fx(s):
    return s["f"].startswith("FX3")


def vf(s, scale_w=1080):
    if is_fx(s):
        x = s["x0"]
        if s.get("pan"):  # [(t_src, x0), ...] piecewise-linear pan over source time
            pts = s["pan"]
            x = f"{pts[-1][1]}"
            for (t0, x0), (t1, x1) in reversed(list(zip(pts[:-1], pts[1:]))):
                a0, a1 = t0 - s["i"], t1 - s["i"]
                x = f"if(lt(t,{a1:.3f}),{x0}+({x1}-{x0})*(t-{a0:.3f})/{a1 - a0:.3f},{x})"
            x = f"if(lt(t,{pts[0][0] - s['i']:.3f}),{pts[0][1]},{x})"
            x = f"'{x}'"
        crop = f"crop=1215:2160:{x}:0,lut3d='{LUT}'"
    else:
        # rotated phone clips: after autorotate they are 1080x1920 portrait already
        crop = "null"
    sh = f"scale={scale_w}:{scale_w * 16 // 9}:flags=lanczos"
    sp = f"setpts=(PTS-STARTPTS)/{s['sp']}"
    return f"{crop},{sh},{sp},fps=30"


def hdr(s):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
                        "-of", "csv=p=0", str(SRC / s["f"])], capture_output=True, text=True).stdout.strip()
    return p == "arib-std-b67"


def tonemap():
    return ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
            "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")


def render(s, out, scale_w=1080, frames_only=None):
    v = vf(s, scale_w)
    if not is_fx(s) and hdr(s):
        v = tonemap() + "," + v
    dur = (s["o"] - s["i"]) / s["sp"]
    n = int(round(dur * 30))
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s['i']:.3f}", "-t", f"{s['o'] - s['i']:.3f}", "-i", str(SRC / s["f"]),
           "-vf", v, "-frames:v", str(n)]
    if frames_only is not None:
        return cmd
    if s["audio"]:
        cmd += ["-af", "aresample=48000", "-ac", "2", "-c:a", "pcm_s16le"]
    else:
        cmd += ["-an"]
    cmd += ["-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", str(out)]
    subprocess.run(cmd, check=True)
    return n


def preview():
    from PIL import Image, ImageDraw
    tiles = []
    for s in SHOTS:
        row = []
        for u in (0.02, 0.5, 0.98):
            t = s["i"] + u * (s["o"] - s["i"])
            tmp = M / "preview" / f"{s['id']}_{u}.jpg"
            tmp.parent.mkdir(exist_ok=True)
            v = vf(dict(s, sp=1.0), 270).replace(",fps=30", "")
            if not is_fx(s) and hdr(s):
                v = tonemap() + "," + v
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(SRC / s["f"]), "-vf", v,
                            "-frames:v", "1", str(tmp)], check=True)
            im = Image.open(tmp)
            ImageDraw.Draw(im).text((4, 4), f"{s['id']} {t:.1f}", fill="yellow")
            row.append(im)
        tiles.append(row)
    W, H = 270, 480
    cols = 5  # shots per row, 3 frames each
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (W * 3 * cols + 10 * cols, H * rows), (40, 0, 0))
    for k, row in enumerate(tiles):
        for j, im in enumerate(row):
            sheet.paste(im.resize((W, H)), ((k % cols) * (W * 3 + 10) + j * W, (k // cols) * H))
    sheet.save(M / "sheets" / "crop_check.jpg")
    print(M / "sheets" / "crop_check.jpg")


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        preview()
    else:
        OUT.mkdir(exist_ok=True)
        info = {}
        for s in SHOTS:
            if len(sys.argv) > 2 and s["id"] not in sys.argv[2:]:
                continue
            n = render(s, OUT / f"{s['id']}.mp4")
            info[s["id"]] = n
            print(s["id"], n, "frames")
        json.dump(info, open(OUT / "frames.json", "w"), indent=1)
