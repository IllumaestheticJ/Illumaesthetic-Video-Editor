# guess.sh name blend "lx,ly,lz" "tx,ty,tz" focal [WxH] [sensor]
W=/home/user/media/work/smart-450/scan3d
cat > $W/specs/$1.json <<J
{"base": ["$2"], "camera": {"sensor": ${7:-36}, "keys": [{"t": 0, "loc": [$3], "target": [$4], "focal": $5}]},
 "seconds": 0, "res": "${6:-1920x1080}", "res_pct": ${8:-50}, "samples": 6, "out": "$W/look/$1.png"}
J
cd /tmp && /usr/local/bin/blender -b -P /home/user/Illumaesthetic-Video-Editor/projects/smart-450-hellkitten/tools/shot.py -- $W/specs/$1.json 2>&1 | grep -E "Error|IVE_" | tail -1
