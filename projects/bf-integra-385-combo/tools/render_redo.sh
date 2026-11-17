#!/bin/bash
# after the main queue: re-render shots 1-2 with centred cameras (characters removed)
R=/home/user/media/bf-integra-385-combo/work/render_v0
cd "$(dirname "$0")"
until grep -q ALL_DONE /tmp/claude-0/-home-user-Illumaesthetic-Video-Editor/fdb112d0-4e04-56ba-a1e1-dd4c3bc75c0b/tasks/b8o0mfjmn.output; do sleep 20; done
for s in 1 2; do
  blender -b --factory-startup -P shots.py -- --shot $s --out $R/s$s --res-pct 50 --samples 16 --step 2 > $R/s${s}_redo.log 2>&1
  echo "redo shot $s done"
done
echo REDO_DONE
