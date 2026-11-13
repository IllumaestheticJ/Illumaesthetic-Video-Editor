"""Composite v2 HUD / cue frames over the real footage frames (from gfx_v2_frames.py) for review sheets."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
P = Path("/home/user/Illumaesthetic-Video-Editor/projects/lexus-is350-speedrun-long")
V = Path("/home/user/media/work/is350-long/gfx/v2")
FR = V / "frames"
(V / "comp").mkdir(exist_ok=True)
hud = json.load(open(P / "gfx_v2_hud_props.json"))
cues = json.load(open(P / "gfx_v2_cues_props.json"))
edl = json.load(open(P / "edl_v2.json"))
segs = hud["segments"]


def grab(mov, t, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(mov), "-frames:v", "1", "-c:v", "png", "-pix_fmt", "rgba", str(out)], check=True)
    return Image.open(out).convert("RGBA")


def bg_for(t):
    for e in edl["events"]:
        pass
    # event containing t in the (possibly retimed) hud segment list
    for s in segs:
        if s["t0"] <= t < s["t1"]:
            eid = s["id"].split("_0")[0] if False else s["id"]
            base = eid.rstrip("abcd") if eid not in ("T_02b",) else eid
            for k in (1, 0, 2):
                for cand in (eid, base, eid[:-1]):
                    f = FR / f"{cand}_{k}.jpg"
                    if f.exists():
                        return Image.open(f).convert("RGBA")
    return Image.new("RGBA", (1920, 1080), (8, 8, 8, 255))


def comp(t, extra=()):
    bg = bg_for(t)
    h = grab(V / "HUD_v2.mov", t, V / "comp" / "_h.png")
    bg.alpha_composite(h, (0, 0))
    for mov, tc in extra:
        bg.alpha_composite(grab(mov, tc, V / "comp" / "_c.png"))
    return bg


mode = sys.argv[1]
if mode == "hud":
    items = [s for s in segs if s["visible"] and (FR / f"{s['id'][:4].rstrip('abcd_') if False else s['id']}_1.jpg").exists() or s["visible"]]
    sel = []
    seen = set()
    for s in segs:
        if not s["visible"] or s["id"] in seen:
            continue
        seen.add(s["id"])
        sel.append(s)
    W, H = 480, 270
    per = 16
    for si in range(0, len(sel), per):
        chunk = sel[si:si + per]
        sh = Image.new("RGB", (W * 4, H * 4), (0, 0, 0))
        for i, s in enumerate(chunk):
            t = s["t0"] + (s["t1"] - s["t0"]) * 0.5
            im = comp(t).convert("RGB")
            d = ImageDraw.Draw(im)
            d.text((10, 250), f"{s['id']} t={t:.1f}", fill=(255, 255, 0))
            sh.paste(im.resize((W, H)), ((i % 4) * W, (i // 4) * H))
        sh.save(V / "comp" / f"hud_sheet_{si // per}.jpg", quality=88)
    print("sheets", (len(sel) + per - 1) // per)
else:
    W, H = 640, 360
    chunks = [c for c in cues]
    per = 9
    for si in range(0, len(chunks), per):
        sh = Image.new("RGB", (W * 3, H * 3), (0, 0, 0))
        for i, c in enumerate(chunks[si:si + per]):
            mov = V / c["file"]
            tc = (c["out"] - c["in"]) * 0.7
            t = c["in"] + tc
            bg = bg_for(t)
            if c["comp"] == "CardV2":
                im = Image.open(grab_f := V / "comp" / "_c.png") if False else None
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{min(tc, (c['out']-c['in'])-0.1):.3f}", "-i", str(mov), "-frames:v", "1", str(V / "comp" / "_c.png")], check=True)
                im = Image.open(V / "comp" / "_c.png").convert("RGBA")
                h = grab(V / "HUD_v2.mov", t, V / "comp" / "_h.png")
                im.alpha_composite(h, (0, 0))
            else:
                im = bg.copy()
                if c["comp"] in ("ScanLabel",) :
                    im = Image.new("RGBA", (1920, 1080), (12, 12, 12, 255)) if c["cue"] != "G01_v2" else Image.new("RGBA", (1920, 1080), (12, 12, 12, 255))
                im.alpha_composite(grab(V / "HUD_v2.mov", t, V / "comp" / "_h.png"), (0, 0))
                im.alpha_composite(grab(mov, min(tc, (c['out']-c['in'])-0.1), V / "comp" / "_c.png"))
            d = ImageDraw.Draw(im.convert("RGB"))
            imr = im.convert("RGB")
            ImageDraw.Draw(imr).text((10, 10), f"{c['cue']} t={t:.1f}", fill=(255, 255, 0))
            sh.paste(imr.resize((W, H)), ((i % 3) * W, (i // 3) * H))
            imr.save(V / "comp" / f"cue_{c['cue']}.jpg", quality=90)
        sh.save(V / "comp" / f"cue_sheet_{si // per}.jpg", quality=88)
