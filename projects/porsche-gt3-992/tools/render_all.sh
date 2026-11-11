#!/bin/bash
# Final renders, strictly one Blender at a time (lessons: serialise heavy jobs). Specs from tools/shots.py final.
cd "$(dirname "$0")/../../.."
for s in "$@"; do
  echo "START $s $(date +%T)"
  blender -b -P projects/porsche-gt3-992/tools/shot.py -- "$s" 2>&1 | grep -E "IVE_RENDER_DONE|Error|rror:" 
  echo "END $s $(date +%T)"
done
echo ALLRENDERED
