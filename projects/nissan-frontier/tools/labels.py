"""Scan-section labels for the exploded shot: alpha .mov overlay (1080x1920, 30 fps).
Each label = cyan dot on the section (screen anchor from tools/shot.py `anchors_out`, rendered per frame from the
same camera), a thin leader to a title + mono subline in the empty band above or below the truck, fading in/out.
House text rules: one label at a time, off-white #e8ecf2, Inter Display / JetBrains Mono, >= 80 px from the edges,
names only (no numbers beyond the section index).
  labels.py anchors.json timing.json out.mov --secs 10.8667"""
import argparse, json, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
ap = argparse.ArgumentParser(); ap.add_argument("anchors"); ap.add_argument("timing"); ap.add_argument("out")
ap.add_argument("--secs", type=float, required=True); ap.add_argument("--fps", type=int, default=30)
a = ap.parse_args()
A = json.load(open(a.anchors)); afps = A["fps"]; anc = A["anchors"]
labels = json.load(open(a.timing))["labels"]
W, H, M = 1080, 1920, 80
OFF = (232, 236, 242); CY = (64, 209, 255)
FT = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", 66)
FS = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf", 28)
def track(d, xy, text, font, fill, sp):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + sp
    return x - xy[0] - sp
def tw(text, font, sp):
    d = ImageDraw.Draw(Image.new("L", (1, 1))); return sum(d.textlength(c, font=font) for c in text) + sp * (len(text) - 1)
def anchor_at(name, t):
    seq = anc[name]; f = t * afps; i = int(f); u = f - i
    i = max(0, min(i, len(seq) - 1)); j = min(i + 1, len(seq) - 1)
    return [(seq[i][k] * (1 - u) + seq[j][k] * u) for k in (0, 1)]
def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
n = int(round(a.secs * a.fps))
with tempfile.TemporaryDirectory() as td:
    for fi in range(n):
        t = fi / a.fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        for L in labels:
            t0, t1 = L["t"]
            if not (t0 <= t <= t1):
                continue
            al = min(ease((t - t0) / 0.22), ease((t1 - t) / 0.22))
            grow = ease((t - t0) / 0.3)
            ax, ay = anchor_at(L["id"], t); ax *= W; ay *= H
            title, sub = L["title"], L.get("sub", "")
            wt, ws = tw(title, FT, 6), tw(sub, FS, 4)
            bw = max(wt, ws)
            top = L.get("side", "top" if ay < H * 0.5 else "bottom") == "top"  # band nearest the section, so the leader never crosses the truck
            by = int(H * 0.17) if top else int(H * 0.77)
            bx = int(min(max(ax - bw * 0.25, M), W - M - bw))
            # leader: from the block edge straight toward the anchor
            lx = min(max(ax, bx), bx + bw); ly = by + (122 if top else -18)
            ex, ey = lx + (ax - lx) * grow, ly + (ay - ly) * grow
            c = lambda rgb, k=1.0: rgb + (int(255 * al * k),)
            d.line([(lx, ly), (ex, ey)], fill=c(CY, 0.9), width=3)
            r = 9
            d.ellipse([ax - r, ay - r, ax + r, ay + r], outline=c(CY), width=3)
            d.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=c(CY))
            track(d, (bx, by), title, FT, c(OFF), 6)
            if sub:
                track(d, (bx, by + 78), sub, FS, c(CY, 0.95), 4)
        im.save(f"{td}/f_{fi:04d}.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(a.fps), "-i", f"{td}/f_%04d.png",
                    "-c:v", "qtrle", "-pix_fmt", "argb", a.out], check=True)
print(a.out, n)
