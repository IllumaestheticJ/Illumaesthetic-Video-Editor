"""Compose a stills-based reel: per-shot slow push-in (Ken Burns) + text cards, piped to ffmpeg, music at -14 LUFS.

Usage: python compose.py spec.json cards_dir out.mp4
Shot modes: crop (9:16 crop around cx,cy of a landscape photo), white_band (product photo on white,
full width, centred on band_cy), black (empty black frame for the end card).
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

W, H = 1080, 1920


def load(spec):
    cache = {}
    for s in spec["shots"]:
        if s.get("src"):
            cache[s["id"]] = Image.open(os.path.join(spec["store"], s["src"])).convert("RGB")
    return cache


def shot_frame(s, img, u):
    z = s.get("z0", 1) + (s.get("z1", 1) - s.get("z0", 1)) * u
    if s["mode"] == "black":
        return Image.new("RGB", (W, H), (0, 0, 0))
    if s["mode"] == "crop":
        ih = img.height / z
        iw = ih * W / H
        cx = min(max(s["cx"], iw / 2), img.width - iw / 2)
        cy = min(max(s["cy"], ih / 2), img.height - ih / 2)
        box = (cx - iw / 2, cy - ih / 2, cx + iw / 2, cy + ih / 2)
        return img.resize((W, H), Image.LANCZOS, box=box)
    if s["mode"] == "white_band":
        fr = Image.new("RGB", (W, H), img.getpixel((3, 3)))
        w = int(W * z); h = int(img.height * w / img.width)
        p = img.resize((w, h), Image.LANCZOS)
        fr.paste(p, (int(s.get("cx", W // 2) - w // 2), s["band_cy"] - h // 2))
        return fr
    raise ValueError(s["mode"])


def main():
    spec = json.load(open(sys.argv[1])); cards_dir = sys.argv[2]; out = sys.argv[3]
    cards = json.load(open(os.path.join(cards_dir, "cards.json")))
    pngs = [(c, Image.open(c["png"]).convert("RGBA")) for c in cards]
    imgs = load(spec)
    fps, dur = spec["fps"], spec["dur"]
    n = int(round(dur * fps))
    silent = out.replace(".mp4", "_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
                           "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    for i in range(n):
        t = (i + 0.5) / fps
        s = next(x for x in spec["shots"] if x["t0"] <= t < x["t1"])
        u = (t - s["t0"]) / (s["t1"] - s["t0"])
        fr = shot_frame(s, imgs.get(s["id"]), u).convert("RGBA")
        for c, im in pngs:
            if c["t0"] <= t < c["t1"]:
                a = 1.0 if c["fade"] <= 0 else min(1.0, (t - c["t0"]) / c["fade"])
                if a < 1:
                    im2 = im.copy(); im2.putalpha(im.split()[3].point(lambda v: int(v * a))); fr.alpha_composite(im2)
                else:
                    fr.alpha_composite(im)
        fo = spec.get("video_fade_out", 0.5)
        if t > dur - fo:
            k = max(0.0, (dur - t) / fo)
            fr = Image.eval(fr.convert("RGB"), lambda v: int(v * k)).convert("RGBA")
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    m = spec["music"]
    af = (f"atrim=start={m['start']}:duration={dur},asetpts=PTS-STARTPTS,"
          f"afade=t=out:st={dur - m['fade_out']}:d={m['fade_out']},"
          f"loudnorm=I=-14:TP=-1.5:LRA=11:linear=true")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", m["path"], "-filter_complex", f"[1:a]{af}[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                    "-shortest", out], check=True)
    print(out)


if __name__ == "__main__":
    main()
