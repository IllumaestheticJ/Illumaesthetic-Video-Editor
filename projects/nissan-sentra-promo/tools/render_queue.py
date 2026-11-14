"""Resumable render queue: renders each shot spec in fresh Blender processes of `--chunk` frames, skipping frames
that already exist (non-empty). Order: given names. render_queue.py main brake final [--chunk 30]"""
import json, os, subprocess, sys
W = "/home/user/media/work/sentra"
SHOT = "/home/user/Illumaesthetic-Video-Editor/projects/nissan-sentra-promo/tools/shot.py"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
chunk = int(sys.argv[sys.argv.index("--chunk") + 1]) if "--chunk" in sys.argv else 30
args = [a for a in args if not a.isdigit()]
for name in args:
    s = json.load(open(f"{W}/shots/{name}.json"))
    n = int(round(s["seconds"] * s["fps"])); out = s["out"]; os.makedirs(out, exist_ok=True)
    todo = [f for f in range(1, n + 1) if not (os.path.exists(f"{out}/f_{f:04d}.png") and os.path.getsize(f"{out}/f_{f:04d}.png") > 0)]
    print(name, n, "frames,", len(todo), "to do", flush=True)
    for i in range(0, len(todo), chunk):
        part = dict(s, frames=todo[i:i + chunk])
        pj = f"{W}/shots/_{name}_chunk.json"; json.dump(part, open(pj, "w"))
        r = subprocess.run(["blender", "-b", "-P", SHOT, "--", pj], capture_output=True, text=True)
        ok = sum(os.path.exists(f"{out}/f_{f:04d}.png") for f in todo[i:i + chunk])
        print(name, "chunk", i // chunk, "frames", todo[i], "-", todo[min(i + chunk, len(todo)) - 1], "ok", ok, flush=True)
        if ok == 0: print(r.stdout[-2000:], r.stderr[-2000:], flush=True)
print("QUEUE_DONE", flush=True)
