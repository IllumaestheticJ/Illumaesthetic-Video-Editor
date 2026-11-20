#!/bin/bash
# Fonts to redraw the mod shop's menu text. Google Fonts hosts are not reachable from the cloud environment,
# the npm registry is: pull the fontsource packages and convert the latin .woff files to .ttf.
#   Lexend            = the game's list and status text ("Front Bumper", "Applied")
#   condensed caps    = titles and option names ("BODYWORK / SPOILER", "CUSTOM WING"): candidates compared in ui.py
set -e
OUT=${1:-/home/user/media/gta6-customs/fonts}; TMP=$(mktemp -d); mkdir -p "$OUT"; cd "$TMP"
pip install -q fonttools brotli
for p in lexend oswald barlow-condensed bebas-neue saira-extra-condensed antonio; do npm pack --silent @fontsource/$p >/dev/null; done
for t in *.tgz; do mkdir -p "x_$t" && tar -xzf "$t" -C "x_$t"; done
python3 -I - "$OUT" <<'PY'
import glob, sys, os
from fontTools.ttLib import TTFont
want = ["lexend-latin-300-normal", "lexend-latin-400-normal", "lexend-latin-500-normal", "oswald-latin-500-normal", "oswald-latin-600-normal",
        "barlow-condensed-latin-600-normal", "barlow-condensed-latin-700-normal", "bebas-neue-latin-400-normal",
        "saira-extra-condensed-latin-600-normal", "saira-extra-condensed-latin-700-normal", "antonio-latin-600-normal", "antonio-latin-700-normal"]
for w in want:
    g = glob.glob(f"./**/{w}.woff", recursive=True)
    if not g: print("missing", w); continue
    f = TTFont(g[0]); f.flavor = None; f.save(f"{sys.argv[1]}/{w}.ttf")
PY
ls "$OUT"
