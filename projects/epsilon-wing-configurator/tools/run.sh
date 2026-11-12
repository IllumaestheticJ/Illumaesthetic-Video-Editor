#!/bin/bash
# Sequential capture queue: run.sh [--dry] shot1 shot2 ...  (log: /home/user/media/epsilon-wing-configurator/cap/run.log)
PW=/tmp/claude-0/-home-user-illumaesthetic-video-editor/6fb8d0f8-4dda-5b04-9fc7-53f6c2056edd/scratchpad/pw
T=/home/user/illumaesthetic-video-editor/projects/epsilon-wing-configurator/tools
LOG=/home/user/media/epsilon-wing-configurator/cap/run.log
DRY=""; [ "$1" = "--dry" ] && { DRY="--dry"; shift; }
cp $T/capture.js $PW/; cd $PW
for s in "$@"; do
  t0=$(date +%s)
  if timeout 3000 node capture.js $s $DRY > $PW/$s.log 2>&1; then
    if [ -n "$DRY" ]; then python3 $T/compose.py $s --sheet >/dev/null 2>&1; else python3 $T/compose.py $s >/dev/null 2>&1; python3 $T/compose.py $s --sheet >/dev/null 2>&1; fi
    echo "OK $s $DRY $(( $(date +%s)-t0 ))s" >> $LOG
  else echo "FAIL $s $DRY: $(grep -v CONSOLE $PW/$s.log | grep -m2 -E 'Error|error' | tr '\n' ' ' | cut -c1-300)" >> $LOG; fi
done
echo "DONE $*" >> $LOG
