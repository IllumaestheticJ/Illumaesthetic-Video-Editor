#!/bin/bash
# Same CLI as `ive render`, using the project's renderer copy (adds --part-look / --part-accent).
exec blender -b -P "$(dirname "$0")/scan_render_parts.py" -- "$@" 2>&1 | grep -E "^IVE_|Error|Traceback" 
