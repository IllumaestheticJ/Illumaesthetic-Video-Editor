"""Registration check stills: part (colour) over the car (silver), from 2 views, 30 % res.
  python projects/lexus-is300/tools/regcheck.py <part> "<cam x,y,z>;<target x,y,z>" ["..."] 
Writes /home/user/media/work/is300/chk/<part>_<i>.png via projects/ferrari-296/tools/shot.py."""
import json, subprocess, sys
W = "/home/user/media/work/is300"
part = sys.argv[1]
for i, v in enumerate(sys.argv[2:]):
    cam, tgt = ([float(x) for x in s.split(",")] for s in v.split(";"))
    for solo in (0, 1):
        spec = {"base": [] if solo else [f"{W}/blend/car.blend"],
                "parts": [{"blend": f"{W}/blend/{part}.blend", "color": None if solo else "red"}],
                "camera": {"keys": [{"t": 0, "loc": cam, "target": tgt, "focal": 30}]},
                "seconds": 0, "res_pct": 30, "samples": 8, "out": f"{W}/chk/{part}_{i}{'_solo' if solo else ''}.png"}
        if solo:
            spec["base"] = [f"{W}/blend/{part}.blend"]; spec["parts"] = []
        js = f"{W}/chk/{part}_{i}_{solo}.json"
        json.dump(spec, open(js, "w"))
        subprocess.run(["blender", "-b", "-P", "projects/ferrari-296/tools/shot.py", "--", js],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(spec["out"])
