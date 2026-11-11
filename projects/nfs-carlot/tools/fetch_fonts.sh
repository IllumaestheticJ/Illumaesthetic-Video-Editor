#!/bin/bash
# Fonts for the drawn Acura Integra name plate. Google Fonts hosts are not reachable from the cloud environment,
# the npm registry is: pull the fontsource packages and convert the latin .woff files to .ttf.
#   Roboto Condensed 500 = maker name (the game sets "Honda", "Mazda" in a condensed grotesque)
#   Michroma 400        = model name (Microgramma-style, like the real INTEGRA badge; drawn with a stroke for weight)
set -e
OUT=${1:-/home/user/media/nfs-carlot/fonts}; TMP=$(mktemp -d); mkdir -p "$OUT"; cd "$TMP"
pip install -q fonttools brotli
for p in michroma roboto-condensed; do npm pack --silent @fontsource/$p >/dev/null; done
for t in *.tgz; do mkdir -p "x_$t" && tar -xzf "$t" -C "x_$t"; done
python3 -I - "$OUT" <<'PY'
import glob, sys
from fontTools.ttLib import TTFont
for w in ("michroma-latin-400-normal", "roboto-condensed-latin-500-normal"):
    f = TTFont(glob.glob(f"./**/{w}.woff", recursive=True)[0]); f.flavor = None; f.save(f"{sys.argv[1]}/{w}.ttf")
PY
ls "$OUT"
