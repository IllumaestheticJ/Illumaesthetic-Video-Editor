#!/bin/bash
# Render spec files one at a time (never in parallel). render_all.sh spec.json [...]
for s in "$@"; do
  echo "== $(date +%T) $s"
  blender -b -P projects/mazda-rx7-fc/tools/shot.py -- "$s" 2>&1 | grep -E "IVE_RENDER_DONE|Error|error" | tail -3
done
echo "== ALL DONE $(date +%T)"
