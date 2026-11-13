# onion.sh cam.json frame.png name [blend]
W=/home/user/media/work/smart-450/scan3d
B=${4:-/home/user/media/smart-hellkitten/prep/str.blend}
SZ=$(python3 -c "import json;c=json.load(open('$1'));print('%dx%d'%tuple(c['image_size']))")
SEN=$(python3 -c "import json;c=json.load(open('$1'));print(c['sensor_width_mm'])")
cat > $W/specs/$3.json <<J
{"base": ["$B"], "camera": {"sensor": $SEN, "keys": [{"t": 0, "cam": "$1"}]},
 "seconds": 0, "res": "$SZ", "res_pct": 50, "samples": 6, "out": "$W/look/$3.png"}
J
cd /tmp && /usr/local/bin/blender -b -P /home/user/Illumaesthetic-Video-Editor/projects/smart-450-hellkitten/tools/shot.py -- $W/specs/$3.json 2>&1 | grep -E "Error|IVE_" | tail -1
python3 $W/tools/sbs.py $2 $W/look/$3.png $W/look/$3s.jpg
