#!/bin/bash
# v3 render queue, one job at a time: scan shots (tools/shot3.py) then CGI shots (tools/cgi_drive.py). Resumable (existing frames skipped).
cd "$(dirname "$0")/../../.."
SH=/home/user/media/work/mr2/shots
for s in "$@"; do
  echo "START $s $(date +%T)"
  case $s in c*) py=cgi_drive.py;; *) py=shot3.py;; esac
  blender -b -P projects/toyota-mr2-spyder/tools/$py -- $SH/$s.json 2>&1 | grep -E "IVE_SHOT_DONE|Error|Traceback|Killed"
  echo "END $s $(date +%T) frames=$(ls /home/user/media/work/renders/mr2/$s 2>/dev/null | wc -l)"
done
echo QUEUE_DONE
