#!/bin/bash
# Registration render check (after projects/a90-supra/tools/regcheck.sh): part (red) over the car (silver) from two
# angles, plus the part alone from outside and inside. usage: regcheck.sh <part> "<lookx,y,z>" <az_out> [dist] [z]
set -e
B=/home/user/media/subaru-wrx-va/blend; R=/home/user/media/subaru-wrx-va/regcheck; mkdir -p $R
P=$1; L=$2; AZ=$3; D=${4:-3.0}; Z=${5:-1.1}
AZI=$(python -c "print($AZ+180)"); AZ2=$(python -c "print($AZ+40)")
cat > $R/${P}_ov.json <<J
{"seconds":1,"lens":35,"ease":"linear","objects":[{"blend":"$B/car.blend"},{"blend":"$B/$P.blend","color":[0.8,0.08,0.05]}],
 "cam":[{"t":0,"az":$AZ,"dist":$D,"z":$Z,"look":[$L]},{"t":1,"az":$AZ2,"dist":$D,"z":$Z,"look":[$L]}]}
J
cat > $R/${P}_solo.json <<J
{"seconds":1,"lens":35,"ease":"linear","objects":[{"blend":"$B/car.blend","hide":true},{"blend":"$B/$P.blend"}],
 "cam":[{"t":0,"az":$AZ,"dist":$D,"z":$Z,"look":[$L]},{"t":1,"az":$AZI,"dist":$D,"z":$Z,"look":[$L]}]}
J
for k in ov solo; do
  blender -b -P "$(dirname "$0")/shots.py" -- --shot $R/${P}_$k.json --out $R/${P}_$k --stills 0,1 --res-pct 30 --samples 8 >/dev/null 2>&1
done
python - <<PY
from PIL import Image
ims=[Image.open(f"$R/${P}_{k}_{x}.png") for k in ("ov","solo") for x in ("0.00","1.00")]
w,h=ims[0].size; s=Image.new("RGB",(w*4,h//2))
for i,im in enumerate(ims): s.paste(im.crop((0,h//4,w,3*h//4)),(i*w,0))
s.save("$R/${P}_sheet.jpg")
PY
echo $R/${P}_sheet.jpg
