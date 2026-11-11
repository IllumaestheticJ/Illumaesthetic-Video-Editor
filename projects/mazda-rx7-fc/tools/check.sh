#!/bin/bash
# Overlay check: base .blend(s) silver + one part in red from 3 angles, 30 % res, 8 spp.
#   check.sh out_prefix "base1.blend base2.blend" part.blend [color]
# front = +Y, car's right = +X in this project's prepped frame.
out=$1; base=$2; part=$3; col=${4:-red}
S=/home/user/media/work/rx7/specs; mkdir -p $S
bl=$(python -c "import json,sys;print(json.dumps(sys.argv[1].split()))" "$base")
i=0
for cam in '[3.6,4.6,2.6]' '[-4.2,1.2,3.4]' '[0.3,-5.6,2.0]'; do
cat > $S/chk_$i.json <<J
{"base": $bl, "parts": $( [ "$part" = none ] && echo "[]" || echo "[{\"blend\": \"$part\", \"color\": \"$col\"}]" ),
 "camera": {"keys": [{"t": 0, "loc": $cam, "target": [0, 0.3, 0.6], "focal": 30}]},
 "seconds": 0, "res": "1080x1920", "res_pct": 30, "samples": 8, "out": "${out}_$i.png"}
J
blender -b -P projects/mazda-rx7-fc/tools/shot.py -- $S/chk_$i.json > /dev/null 2>&1
i=$((i+1))
done
python - "$out" <<'P'
import sys
from PIL import Image
ims=[Image.open(f"{sys.argv[1]}_{i}.png") for i in range(3)]
o=Image.new("RGB",(ims[0].width*3,ims[0].height));[o.paste(im,(i*im.width,0)) for i,im in enumerate(ims)];o.save(f"{sys.argv[1]}.jpg")
P
echo "${out}.jpg"
