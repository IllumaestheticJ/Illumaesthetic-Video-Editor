"""Stacked split-screen assembler: two 1080x960 panels (top / bottom) cut on the same frames, labels, logo, music.

    python projects/porsche-gt3-vs-gt3rs/tools/assemble_split.py projects/porsche-gt3-vs-gt3rs/split.json

split.json: {"fps":30, "out":..., "music":{"path","start","fade_out"}, "tags":{"top":"...","bottom":"..."},
  "hud": hud.mov (optional, full frame), "logo": {"src": card.mp4, "frame": 1105}, "end_frame": 1219,
  "fade": {"start_frame": 1065, "frames": 27},           # both panels fade to black before the logo
  "top": [seg...], "bottom": [seg...]}
seg: {"src": png dir, "frames": N, "src_fps": 15, "trim_start": s, "crop_y": 480}   crop_y only for 9:16 sources
Each segment is interpolated to 30 fps and cut to exactly N frames, so every cut is frame-exact on both panels."""
import json, os, subprocess, sys, tempfile
cfg = json.load(open(sys.argv[1])); fps = cfg["fps"]
tmp = tempfile.mkdtemp(prefix="split_")
run = lambda c: subprocess.run(c, check=True)
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"


def panel(name, segs):
    files = []
    for i, s in enumerate(segs):
        o = f"{tmp}/{name}_{i:02d}.mp4"
        vf = []
        if s.get("trim_start"):
            vf.append(f"trim=start={s['trim_start']},setpts=PTS-STARTPTS")
        vf.append(f"minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
        if s.get("fit_vf"):   # custom fit into the 1080x960 panel (e.g. rotate a tall 9:16 shot)
            vf.append(s["fit_vf"])
        elif "crop_y" in s:   # 9:16 source -> 1080 wide, take a 960-high band
            vf += ["scale=1080:1920:flags=lanczos", f"crop=1080:960:0:{s['crop_y']}"]
        else:
            vf.append("scale=1080:960:flags=lanczos")
        if s.get("vf"):
            vf.append(s["vf"])
        vf += [f"tpad=stop_mode=clone:stop_duration=3", "format=yuv444p"]
        run(["ffmpeg", "-y", "-v", "error", "-framerate", str(s.get("src_fps", 15)), "-pattern_type", "glob", "-i", f"{s['src']}/*.png",
             "-vf", ",".join(vf), "-frames:v", str(s["frames"]), "-r", str(fps), "-c:v", "libx264", "-preset", "veryfast", "-crf", "8", o])
        files.append(o)
    lst = f"{tmp}/{name}.txt"; open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    out = f"{tmp}/{name}.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
    return out


top, bot = panel("top", cfg["top"]), panel("bottom", cfg["bottom"])
n_body = sum(s["frames"] for s in cfg["top"]); assert n_body == sum(s["frames"] for s in cfg["bottom"]) == cfg["logo"]["frame"], n_body
end = cfg["end_frame"]; fd = cfg["fade"]
tags = cfg["tags"]
dt = lambda txt, y: (f"drawtext=fontfile={FONT}:text='{txt}':fontcolor=0xe8ecf2@0.92:fontsize=34:x=64:y={y}"
                     f":enable='lt(n,{fd['start_frame']})'")
# header bar per panel: car name left, current section right (labels never sit on the scan)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
lab = []
for y, key in ((48, "top"), (1008, "bottom")):
    for a, b, txt in cfg.get("labels", {}).get(key, []):
        lab.append(f"drawtext=fontfile={MONO}:text='{txt}':fontcolor=0xe8ecf2@0.85:fontsize=26:x=w-64-text_w:y={y}:enable='between(n,{a},{b})'")
cta = cfg.get("cta")
if cta:  # double call-to-action: one line under each panel's header bar, on a dark band
    en = f"between(n,{cta['from']},{fd['start_frame'] + fd['frames']})"
    for y, key in ((96, "top"), (1056, "bottom")):
        lab.append(f"drawbox=x=0:y={y}:w=1080:h=84:color=black@0.6:t=fill:enable='{en}'")
        lab.append(f"drawtext=fontfile={FONT}:text='{cta[key]}':fontcolor=0xe8ecf2:fontsize=40:x=(w-text_w)/2:y={y + 22}:enable='{en}'")
bars = "drawbox=x=0:y=0:w=1080:h=96:color=black@0.6:t=fill,drawbox=x=0:y=960:w=1080:h=96:color=black@0.6:t=fill"
fc = (f"[0:v][1:v]vstack=inputs=2,{bars},drawbox=x=0:y=958:w=1080:h=4:color=0x30343a:t=fill,{dt(tags['top'], 38)},{dt(tags['bottom'], 998)}"
      + ("," + ",".join(lab) if lab else "") + "[st];")
last = "[st]"; inputs = ["-i", top, "-i", bot]; k = 2
if cfg.get("hud") and os.path.exists(cfg["hud"]):
    inputs += ["-i", cfg["hud"]]; fc += f"{last}[{k}:v]overlay=0:0:eof_action=pass[h];"; last = "[h]"; k += 1
fc += f"{last}fade=t=out:s={fd['start_frame']}:n={fd['frames']},format=yuv420p[body];"
inputs += ["-i", cfg["logo"]["src"]]
fc += f"[{k}:v]fps={fps},scale=1080:1920,format=yuv420p,trim=end_frame={end - n_body},setpts=PTS-STARTPTS[lg];[body][lg]concat=n=2:v=1:a=0[v]"; k += 1
m = cfg["music"]; dur = end / fps
inputs += ["-ss", str(m["start"]), "-i", m["path"]]
fc += f";[{k}:a]atrim=0:{dur:.3f},afade=t=out:st={dur - m['fade_out']:.3f}:d={m['fade_out']}[a]"
os.makedirs(os.path.dirname(cfg["out"]), exist_ok=True)
run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", str(fps), "-c:v", "libx264", "-preset", "slow",
     "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-t", f"{dur:.3f}", cfg["out"]])
print(cfg["out"], n_body, end)
