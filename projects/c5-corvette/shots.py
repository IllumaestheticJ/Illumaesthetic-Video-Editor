"""Shot list for the C5 Corvette Temerario-style reel -> one tools/shot.py JSON per shot.
  python projects/c5-corvette/shots.py            # writes /home/user/media/work/c5/shots/*.json
Shots are rendered with ~0.5-1 s of slack and trimmed to the music's accent grid in project.yaml (the track arrives
after the renders start). Prepped frame (m): ground z=0, nose at -Y (y=-2.29), Fender outer part = -X side.
Camera az: 0 = in front of the nose, -90 = -X side (fender part side), +-180 = behind.
"""
import json, os
B = "/home/user/media/work/c5/blend/"
OUT = "/home/user/media/work/c5/shots/"
R = "/home/user/media/work/renders/c5/"
HINGE = json.load(open(os.path.join(os.path.dirname(__file__), "hinge.json")))
FPS, EXP = 15, -0.5
CAR = {"car": B + "car.blend"}
CAR2 = {"car": B + "car2.blend"}           # 2 mm for close-ups
PARTS = {"hood": "hood_combo", "fb": "front_bumper", "fe": "Fender_outer", "rb": "rear_bumper_inside", "tg": "targa_reg"}
EXPL = {"base": B + "base.blend", **{k: B + v + ".blend" for k, v in PARTS.items()}}
HINGES = {"hood": {"p": HINGE["p"], "axis": HINGE["axis"]}}
OPEN = HINGE["open_deg"]  # 46 deg = the captured hood-open pose

def shot(name, objs, seconds, cam, **kw):
    d = {"objects": objs, "seconds": seconds, "fps": FPS, "out": R + name, "exposure": EXP, "camera": cam}
    d.update(kw)
    json.dump(d, open(OUT + name + ".json", "w"), indent=1)

def keys(state_list):
    """[(t, {part: {...}})] -> anims dict"""
    an = {}
    for t, st in state_list:
        for k, v in st.items():
            an.setdefault(k, []).append(dict(t=t, **v))
    return an

os.makedirs(OUT, exist_ok=True)
T = [0, 0, 0.55]
# s1 front 3/4 low turntable (fades up from black in assembly)
shot("s1_front34", CAR, 4.6, [{"t": 0, "az": -28, "el": 5, "dist": 6.6, "target": [0, -0.25, 0.5], "lens": 38},
                             {"t": 1, "az": -58, "el": 8, "dist": 6.4, "target": [0, -0.2, 0.5], "lens": 38, "lin": False}])
# s2 rear 3/4 orbit, the other side (quad tail lamps toward camera)
shot("s2_rear34", CAR, 4.0, [{"t": 0, "az": 128, "el": 9, "dist": 6.2, "target": [0, 0.3, 0.5], "lens": 38},
                            {"t": 1, "az": 158, "el": 13, "dist": 5.8, "target": [0, 0.35, 0.5], "lens": 38}])
# s3 high 3/4 orbit over the front-left, crane down slightly
shot("s3_orbit", CAR, 3.6, [{"t": 0, "az": 60, "el": 28, "dist": 7.4, "target": [0, 0, 0.45], "lens": 38},
                           {"t": 1, "az": 25, "el": 18, "dist": 6.3, "target": [0, -0.1, 0.45], "lens": 38}])
# s4 extreme close-up: front wheel + headlight pod / fender (2 mm), slow slide
shot("s4_wheel", CAR2, 3.0, [{"t": 0, "az": -62, "el": 6, "dist": 1.9, "target": [-0.80, -1.45, 0.38], "lens": 35},
                            {"t": 1, "az": -40, "el": 9, "dist": 1.75, "target": [-0.75, -1.55, 0.40], "lens": 35}])
# s5 extreme close-up: quad round tail lamps (2 mm), slide across the tail
shot("s5_tail", CAR2, 3.0, [{"t": 0, "az": 160, "el": 6, "dist": 1.9, "target": [0.35, 2.15, 0.70], "lens": 35},
                           {"t": 1, "az": 195, "el": 8, "dist": 1.9, "target": [-0.35, 2.15, 0.70], "lens": 35}])
# s6 hood opens on the hinge fitted to the captured hood-open scan; engine bay = that scan as captured
shot("s6_hood", {"base": B + "base_hood.blend", "hood": B + "hood_combo.blend"}, 4.4,
     [{"t": 0, "az": -35, "el": 16, "dist": 4.6, "target": [0, -1.2, 0.65], "lens": 34},
      {"t": 1, "az": -48, "el": 32, "dist": 4.4, "target": [0, -1.3, 0.75], "lens": 34}],
     anims={"hood": [{"t": 0.12, "deg": 0}, {"t": 0.75, "deg": OPEN}]}, hinges=HINGES, light_ref="base")
# s7 top-down, spinning
shot("s7_top", CAR, 3.6, [{"t": 0, "az": 0, "el": 89.9, "dist": 8.6, "target": [0, 0, 0.4], "lens": 34},
                         {"t": 1, "az": 75, "el": 89.9, "dist": 6.9, "target": [0, 0, 0.4], "lens": 34, "lin": True}])
# s8 exploded: high front 3/4 on the fender side; panels lift off in a stagger, stacked ABOVE the car (portrait frame)
HOME = {k: {"off": [0, 0, 0]} for k in PARTS}; HOME["hood"]["deg"] = 0
EX = {"tg": {"off": [0, 0.05, 1.05]}, "hood": {"off": [0, -0.15, 0.95], "deg": 0},
      "fb": {"off": [0, -0.42, 0.6]}, "fe": {"off": [-0.42, -0.1, 0.55]}, "rb": {"off": [0, 0.42, 0.6]}}
EX2 = {k: {"off": [v["off"][0] * 1.08, v["off"][1] * 1.08, v["off"][2] * 1.08 + 0.05], **({"deg": 0} if k == "hood" else {})} for k, v in EX.items()}
def stag(a, b, t0, t1, order, step):
    out = {}
    for i, k in enumerate(order):
        s0 = t0 + i * step
        out[k] = [dict(t=s0, **a[k]), dict(t=min(1, s0 + (t1 - t0)), **b[k])]
    return out
an8 = stag(HOME, EX, 0.08, 0.62, ["tg", "hood", "fb", "fe", "rb"], 0.07)
for k in an8: an8[k].append(dict(t=1.0, **EX2[k]))
shot("s8_explode", EXPL, 5.0, [{"t": 0, "az": -40, "el": 22, "dist": 7.6, "target": [0, -0.15, 0.85], "lens": 32},
                              {"t": 1, "az": -68, "el": 26, "dist": 8.2, "target": [0, 0, 1.0], "lens": 32}],
     anims=an8, hinges=HINGES, light_ref="base")
# s9 side/rear 3/4: panels float, then return home (staggered, reverse order) -> assembled car, fades out
an9 = stag(EX2, HOME, 0.30, 0.78, ["rb", "fe", "fb", "hood", "tg"], 0.05)
for k in an9: an9[k].insert(0, dict(t=0, **EX2[k]))
shot("s9_reassemble", EXPL, 5.2, [{"t": 0, "az": -112, "el": 18, "dist": 8.6, "target": [0, 0.1, 1.0], "lens": 32},
                                 {"t": 1, "az": -148, "el": 11, "dist": 6.3, "target": [0, 0.25, 0.55], "lens": 36}],
     anims=an9, hinges=HINGES, light_ref="base")
print("wrote", sorted(os.listdir(OUT)))
