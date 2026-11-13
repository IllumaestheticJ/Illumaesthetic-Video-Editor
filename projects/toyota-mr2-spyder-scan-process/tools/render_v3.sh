#!/bin/bash
# v3 scan renders, one Blender at a time (75 %, 12 spp, 15 fps source). sH holds from source frame 57 on -> render 0..57, copy the hold.
P=$(cd "$(dirname "$0")/.." && pwd); R=/home/user/media/work/mr2/renders3; B="/usr/local/bin/blender -b -P $P/tools/shot.py --"
$B $P/shots/sP.json 2>&1 | grep -E "IVE_SHOT|Error|Traceback"
$B $P/shots/sL.json 2>&1 | grep -E "IVE_SHOT|Error|Traceback"
$B $P/shots/sH.json --range 0,58 2>&1 | grep -E "IVE_SHOT|Error|Traceback"
$B $P/shots/sH_clay.json --range 48,58 2>&1 | grep -E "IVE_SHOT|Error|Traceback"
for d in sH sHc; do for i in $(seq 59 75); do cp $R/$d/f_0058.png $R/$d/f_$(printf %04d $i).png; done; done
echo RENDER_V3_DONE
