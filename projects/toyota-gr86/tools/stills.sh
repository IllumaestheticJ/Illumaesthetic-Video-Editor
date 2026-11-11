#!/bin/bash
# Check stills at given frame numbers (25 % res, 6 spp), one strip per shot.
#   stills.sh shot f1,f2,... [shot f1,f2 ...]  -> /home/user/media/work/gr86/frame/<shot>.jpg
cd "$(dirname "$0")/../../.."
F=/home/user/media/work/gr86/frame; mkdir -p $F
while [ $# -ge 2 ]; do
  s=$1; fr=$2; shift 2
  python - "$s" "$fr" <<'PY'
import json, sys
s, fr = sys.argv[1], [int(v) for v in sys.argv[2].split(",")]
p = json.load(open(f"projects/toyota-gr86/shots/{s}.json"))
p.update(res_pct=25, samples=6, frames=fr, out=f"/home/user/media/work/gr86/frame/{s}")
json.dump(p, open(f"/home/user/media/work/gr86/frame/{s}.json", "w"))
PY
  python -c "import glob,os; [os.remove(f) for f in glob.glob('$F/$s/f_*.png')]"
  /usr/local/bin/blender -b -P projects/toyota-gr86/tools/shot.py -- $F/$s.json > $F/$s.log 2>&1
  python -c "
from PIL import Image; import glob
fs=sorted(glob.glob('$F/$s/f_*.png')); ims=[Image.open(f) for f in fs]; w,h=ims[0].size
o=Image.new('RGB',(w*len(ims)+8*(len(ims)-1),h),(60,60,60)); [o.paste(im,(i*(w+8),0)) for i,im in enumerate(ims)]; o.save('$F/$s.jpg')"
  echo "$s done"
done
