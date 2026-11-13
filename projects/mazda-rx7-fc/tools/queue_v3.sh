#!/bin/bash
# Resumable v3 final queue (lessons: container restarts kill queues silently). For each shot, render only the frames
# not yet on disk, one Blender job at a time.   bash projects/mazda-rx7-fc/tools/queue_v3.sh [shot ...]
cd /home/user/Illumaesthetic-Video-Editor
SHOTS=${@:-k_front k_sides k_rbumper_off k_rear k_reveal}
for s in $SHOTS; do
  python projects/mazda-rx7-fc/tools/shots_v3.py final $s >/dev/null
  python - "$s" <<'PY'
import json, os, sys
s = sys.argv[1]; p = f"/home/user/media/work/rx7/specs/final_{s}.json"; d = json.load(open(p))
n = int(round(d["seconds"] * d["fps"])); have = set(os.listdir(d["out"])) if os.path.isdir(d["out"]) else set()
miss = [f for f in range(1, n + 1) if f"f_{f:04d}.png" not in have]
d["frames"] = miss; json.dump(d, open(p, "w")); print(s, "missing", len(miss))
PY
  bash projects/mazda-rx7-fc/tools/render_all.sh /home/user/media/work/rx7/specs/final_$s.json
done
echo "== QUEUE V3 DONE $(date +%T)"
