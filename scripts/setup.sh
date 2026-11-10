#!/bin/bash
# One-time setup of a work box (cloud session or local Linux). Idempotent.
set -e
cd "$(dirname "$0")/.."
pip install -q -r requirements.txt
if ! command -v blender >/dev/null; then
  V=5.3.0
  mkdir -p /opt/blender && cd /opt/blender
  curl -sSL -o b.tar.xz "https://download.blender.org/release/Blender${V%.*}/blender-${V}-linux-x64.tar.xz"
  tar xf b.tar.xz && rm b.tar.xz
  ln -sf "/opt/blender/blender-${V}-linux-x64/blender" /usr/local/bin/blender
  cd - >/dev/null
fi
(cd remotion && npm ci)
mkdir -p /home/user/media/work
echo "ready: $(blender -b --version 2>/dev/null | head -1)"
