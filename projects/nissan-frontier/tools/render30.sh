#!/bin/bash
# v8: true 30 fps finals (short-form lesson: 15 fps + minterpolate ghosts parts that fly in), RESUMABLE after a container restart.
# Output <shot>_30/f_%04d.png. Frames already rendered at 15 fps in <shot>/ are reused as the odd 30-fps frames when REUSE lists the shot
# (same spec, keys are in seconds). Only missing frames are rendered.   REUSE="m1_grille m3_fenders" render30.sh m1_grille m2_flares ...
cd "$(dirname "$0")/../../.."
R=/home/user/media/work/frontier/renders/final
for s in "$@"; do
  spec=$(python projects/nissan-frontier/tools/shots_v8.py final $s)
  python - "$spec" "$R/$s" "$R/${s}_30" "$( [[ " $REUSE " == *" $s "* ]] && echo 1 || echo 0 )" <<'PY'
import json, os, sys
spec, d15, d30, reuse = sys.argv[1:5]
sp = json.load(open(spec)); n = int(round(sp["seconds"] * sp["fps"])); os.makedirs(d30, exist_ok=True)
if reuse == "1" and os.path.isdir(d15):
    for f in sorted(os.listdir(d15)):
        i = int(f[2:6]); dst = f"{d30}/f_{2 * i - 1:04d}.png"
        if 2 * i - 1 <= n and not os.path.exists(dst): os.link(f"{d15}/{f}", dst)
miss = [f for f in range(1, n + 1) if not os.path.exists(f"{d30}/f_{f:04d}.png") or os.path.getsize(f"{d30}/f_{f:04d}.png") < 1000]
sp["out"] = d30; sp["frames"] = miss; json.dump(sp, open(spec, "w"))
print("missing", len(miss), "of", n)
PY
  t0=$(date +%s)
  if [ "$(python -c "import json;print(len(json.load(open('$spec'))['frames']))")" != "0" ]; then
    blender -b -P projects/nissan-frontier/tools/shot.py -- $spec > /home/user/media/nissan-frontier/chk/final30_$s.log 2>&1
  fi
  echo "$s done rc=$? $(( $(date +%s)-t0 ))s frames=$(ls $R/${s}_30 | wc -l)"
done
echo QUEUEDONE
