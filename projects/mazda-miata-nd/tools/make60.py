"""True 60 fps build of the v10 reel (user: "true 60 FPS"). Every scan shot is re-rendered at 60 fps (no interpolation) with
the same specs, camera keys and quality as the 15 fps finals (75 %, 12 spp, persistent data off); the phone CTA and logo are
rendered at 60 fps; the reel is assembled at 60 fps with exact frame counts (2 x the 30 fps slots), then the labels are
burned in from a 60 fps HUD. Sequential, one Blender job at a time. Log: renders_60/make60.log
  python projects/mazda-miata-nd/tools/make60.py"""
import importlib.util, json, os, subprocess, sys, time, glob
import numpy as np
from PIL import Image

REPO = "/home/user/Illumaesthetic-Video-Editor"
W = "/home/user/media/work/miata"
T = f"{REPO}/projects/mazda-miata-nd/tools"
OUT60 = f"{W}/renders_60/final"
LOG = f"{W}/renders_60/make60.log"
os.makedirs(OUT60, exist_ok=True)


def log(*a):
    line = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp)
    argv = sys.argv; sys.argv = [argv[0]]
    sp.loader.exec_module(m); sys.argv = argv
    return m


s1 = load(f"{T}/shots.py", "shots_v1")
s3 = load(f"{T}/shots_v3.py", "shots_v3")
s6 = load(f"{T}/shots_v6.py", "shots_v6")
s9 = load(f"{T}/shots_v9.py", "shots_v9")   # also has v5 (+ v10 camera) loaded as s9.v5
v5 = s9.v5

import yaml
proj = yaml.safe_load(open(f"{REPO}/projects/mazda-miata-nd/project_v10.yaml"))
clips = [c for c in proj["timeline"] if "transition" not in c]


def spec_json(cid, src):
    if cid.startswith("v6_"):
        p = s6.spec(cid, "final")
    elif cid == "s4_lamp":
        p = s1.spec(cid, "final")
    elif cid == "v3_r_bumper":
        p = s3.spec(cid, "final")
    else:
        p = v5.spec(cid, "final")
    return json.load(open(p))


def run_blender(sp):
    path = f"{W}/specs/t60_{os.path.basename(sp['out'])}_{len(sp.get('frames') or [])}_{int(time.time()*1000)%100000}.json"
    json.dump(sp, open(path, "w"), indent=1)
    t0 = time.time()
    r = subprocess.run(["/usr/local/bin/blender", "-b", "-P", f"{T}/shot.py", "--", path], capture_output=True, text=True)
    ok = "IVE_RENDER_DONE" in r.stdout
    log(f"  blender {os.path.basename(sp['out'])} frames={len(sp.get('frames') or [])} {'OK' if ok else 'FAILED'} {time.time()-t0:.0f}s")
    if not ok:
        log(r.stdout[-1500:], r.stderr[-1500:])
        raise SystemExit("render failed")


def to60(sp, seconds, out, frames=None):
    sp = dict(sp)
    sp.update({"fps": 60, "seconds": seconds, "persistent": False, "res_pct": 75, "samples": 12, "out": out})
    sp["frames"] = frames
    if frames is None:
        sp.pop("frames", None)
    return sp


# ---- 1. scan shots at 60 fps
jobs = []
for c in clips:
    cid = c["id"]
    if cid in ("cta", "logo"):
        continue
    slot = int(c["frames"])
    src = c["src"]
    base = spec_json(cid, src)
    if cid == "v3_x_home":
        N = 2 * slot
        parts = to60(base, slot / 30, f"{OUT60}/{cid}", frames=list(range(1, 65)))
        cj = v5.spec("v3_x_home_clean", "final")
        clean = to60(json.load(open(cj)), slot / 30, f"{OUT60}/{cid}", frames=list(range(65, N + 1)))
        jobs += [parts, clean]
    else:
        jobs.append(to60(base, slot / 30, f"{OUT60}/{cid}"))
    log(f"{cid}: slot {slot} -> {2*slot} frames at 60 fps")

total = sum(len(j["frames"]) if j.get("frames") else round(j["seconds"] * 60) for j in jobs)
log(f"total scan frames at 60 fps: {total}")

done_marker = f"{W}/renders_60/renders_done.txt"
if not os.path.exists(done_marker):
    for j in jobs:
        run_blender(j)
    open(done_marker, "w").write("ok\n")
log("renders done")

# ---- 2. lighting check on every 60 fps folder
for d in sorted(glob.glob(f"{OUT60}/*")):
    fs = sorted(glob.glob(d + "/*.png"))
    m = [np.asarray(Image.open(f).convert("L")).mean() for f in fs[::4]]
    log(f"  luma {os.path.basename(d)} n={len(fs)} min {min(m):.0f} max {max(m):.0f}")
    if min(m) < 15:
        log("  !! possible lighting dropout in", d)

# ---- 3. CTA and logo at 60 fps
log("cta + logo at 60 fps")
subprocess.run(["python", f"{T}/cta_card.py", f"{W}/renders_v10/final/v3_x_home/f_0030.png", f"{W}/web/nd_mobile_v5.png",
                f"{W}/out/cta_v5_60.mp4", "--map", f"{W}/web/cta_map.json", "--secs", "2.6", "--fps", "60"], check=True, cwd=REPO)
subprocess.run(["python", f"{REPO}/projects/ferrari-296/tools/logo_card.py", f"{REPO}/remotion/public/illumaesthetic_logo.png",
                f"{W}/out/logo_card_v4_60.mp4", "--secs", "2.2", "--fps", "60", "--width", "760"], check=True, cwd=REPO)

# ---- 4. 60 fps project file: exact frame counts, no interpolation
p60 = json.loads(json.dumps(proj))
p60["output"]["fps"] = 60
p60["output"]["path"] = f"{W}/out/miata_nd_v10_true60_nolabels.mp4"
for c in p60["timeline"]:
    if "transition" in c:
        continue
    if c["id"] == "cta":
        c["src"] = f"{W}/out/cta_v5_60.mp4"
    elif c["id"] == "logo":
        c["src"] = f"{W}/out/logo_card_v4_60.mp4"
    else:
        c["src"] = f"{OUT60}/{c['id']}"
    c["frames"] = 2 * int(c["frames"])
    c["dur"] = c["frames"] / 60
    for k in ("src_fps", "interpolate"):
        c.pop(k, None)
yaml.safe_dump(p60, open(f"{REPO}/projects/mazda-miata-nd/project_v10_true60.yaml", "w"), sort_keys=False)
log("project_v10_true60.yaml written")

# ---- 5. assemble, then 60 fps labels
subprocess.run(["python", f"{REPO}/projects/honda-s2000/tools/concat_assemble.py",
                f"{REPO}/projects/mazda-miata-nd/project_v10_true60.yaml"], check=True, cwd=REPO)
ov = json.load(open(f"{REPO}/projects/mazda-miata-nd/overlay_v10.json"))
ov["fps"] = 60; ov["durationInFrames"] = 2 * ov["durationInFrames"]
for it in ov["items"]:
    it["from"] *= 2; it["duration"] *= 2
json.dump(ov, open(f"{REPO}/projects/mazda-miata-nd/overlay_v10_true60.json", "w"), indent=1)
subprocess.run(["python", "-m", "ive", "hud", f"{REPO}/projects/mazda-miata-nd/overlay_v10_true60.json",
                f"{W}/out/hud_v10_true60.mov"], check=True, cwd=REPO)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{W}/out/miata_nd_v10_true60_nolabels.mp4", "-i", f"{W}/out/hud_v10_true60.mov",
                "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v]", "-map", "[v]", "-map", "0:a",
                "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-r", "60", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart",
                f"{W}/out/miata_nd_v10_true60.mp4"], check=True)
log("DONE", f"{W}/out/miata_nd_v10_true60.mp4")
