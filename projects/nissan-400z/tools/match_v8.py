"""1:1 match of the finished kitted, liveried, dropped car to the user's SEMA photo (b096156c, 1206x2144, iPhone 16 Pro
main 24 mm-eq). Writes a one-frame spec of the v7 HERO scene from a camera {loc, target, focal(sensor 36), roll}.
  python match_v8.py render cam.json out.png [pct]      -> spec path (render it with tools/shot.py)
  python match_v8.py raycast cam.json pts.json out.json -> spec path
  python match_v8.py export cam.json verts.npz          -> spec path (world vertices for fit_cam.py)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shots_v8 as S7
W, H = 1206, 2144
mode, camf = sys.argv[1], sys.argv[2]
c = json.load(open(camf))
h = S7.SHOTS["HERO"]
key = {"t": 0, "loc": c["loc"], "target": c["target"], "focal": c["focal"], "roll": c.get("roll", 0.0)}
sp = {"base": h["base"], "parts": [], "camera": {"sensor": 36, "keys": [key], "shift": c.get("shift", [0, 0])},
      "seconds": 1 / 15, "fps": 15, "res": f"{W}x{H}", "res_pct": 100, "samples": 16, "persist": False,
      "livery": h["livery"], "body_drop": h["body_drop"]}
if mode == "render":
    sp["out"] = sys.argv[3]; sp["res_pct"] = int(sys.argv[4]) if len(sys.argv) > 4 else 100
elif mode == "export":
    sp["out"] = "/tmp/unused.png"; sp["export"] = {"frame": 1, "out": sys.argv[3]}
else:
    sp["out"] = "/tmp/unused.png"; sp["raycast"] = {"frame": 1, "points": json.load(open(sys.argv[3])), "out": sys.argv[4]}
p = f"/home/user/media/work/z400/specs/match_{mode}.json"; json.dump(sp, open(p, "w"), indent=1); print(p)
