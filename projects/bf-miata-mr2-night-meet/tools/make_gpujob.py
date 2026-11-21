"""Pack the full-quality render (1080x1920, 30 fps, 64 samples) as a GPU job for the owner's PC (knowledge/gpu-worker.md).
One packed .blend per shot + job.json in /home/user/media/bf-miata-mr2-night-meet/gpujob; then
`python scripts/vdrive.py save bf-miata-mr2-night-meet gpujob <that folder>`.  Usage: python3 tools/make_gpujob.py [shots...]"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
J = "/home/user/media/bf-miata-mr2-night-meet/gpujob"
RES, SAMPLES = [1080, 1920], 64
CLOUD_S = 190             # measured: s10 frame 125 at 1080x1920 / 64 spp took 205 s on the cloud CPU incl. about 15 s scene load
T = json.load(open(f"{P}/specs/timeline.json")); O = T["order"]; F = T["f30"]
shots = sys.argv[1:] or [s for s in O if os.path.exists(f"{P}/specs/{s}.json")]
os.makedirs(J + "/specs", exist_ok=True); job = []
for s in shots:
    sp = json.load(open(f"{P}/specs/{s}.json")); i = O.index(s); n30 = min(F[i + 1] - F[i], 2 * sp["frames"] - 1)
    sp.update(res=RES, samples=SAMPLES, blend=f"{J}/{s}.blend", shot=s, frames30=n30); sp.pop("only", None)
    json.dump(sp, open(f"{J}/specs/{s}.json", "w"))
    log = open(f"{J}/specs/{s}.log", "w")
    subprocess.run(["blender", "-b", "--factory-startup", "-P", f"{HERE}/shot.py", "--", f"{J}/specs/{s}.json"], stdout=log, stderr=log)
    assert os.path.exists(f"{J}/{s}.blend"), s
    job.append({"blend": f"{s}.blend", "scene": "Scene", "engine": "CYCLES", "frame_start": 2, "frame_end": 1 + n30,
                "output": f"frames/{s}/f_####.png", "res": RES, "samples": SAMPLES, "fps": 30, "cloud_s_per_frame": CLOUD_S})
    print(s, n30, round(os.path.getsize(f"{J}/{s}.blend") / 1e6), "MB", flush=True)
json.dump({"project": "bf-miata-mr2-night-meet", "archive": "relative", "shots": job}, open(f"{J}/job.json", "w"), indent=1)
print("frames", sum(j["frame_end"] - j["frame_start"] + 1 for j in job))
