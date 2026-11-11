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
# Cut grid on the generated track (c5-corvette_track.mp3, 107.96 BPM kick grid b = 0.5013 + 0.5557 k):
# 0 | 4.040 (intro guitar onset) | 9.393 drop (b16) | 13.839 (b24) | 15.506 (b27) | 17.174 (b30, flux peak)
# | 22.175 (b39, kick accent) | 26.621 (b47) | 30.512 (b54, build) | 35.513 (b63, biggest hit) logo | 39.40 end
CUTS = [0, 4.040, 9.393, 13.839, 15.506, 17.174, 22.175, 26.621, 30.512, 35.513]
SLACK = 0.4
def secs(i):
    return round(CUTS[i + 1] - CUTS[i] + SLACK, 3)
def fr(t, i):
    """absolute seconds inside shot i -> shot fraction of the rendered (slack-padded) length"""
    return round(t / secs(i), 4)
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
shot("s2_rear34", CAR, secs(1), [{"t": 0, "az": 128, "el": 9, "dist": 6.2, "target": [0, 0.3, 0.5], "lens": 38},
                            {"t": 1, "az": 158, "el": 13, "dist": 5.8, "target": [0, 0.35, 0.5], "lens": 38}])
# s3 high 3/4 orbit over the front-left, crane down slightly
shot("s3_orbit", CAR, secs(2), [{"t": 0, "az": 60, "el": 28, "dist": 7.4, "target": [0, 0, 0.45], "lens": 38},
                           {"t": 1, "az": 25, "el": 18, "dist": 6.3, "target": [0, -0.1, 0.45], "lens": 38}])
# s4 extreme close-up: front wheel + headlight pod / fender (2 mm), slow slide
shot("s4_wheel", CAR2, secs(3), [{"t": 0, "az": -62, "el": 6, "dist": 1.9, "target": [-0.80, -1.45, 0.38], "lens": 35},
                            {"t": 1, "az": -40, "el": 9, "dist": 1.75, "target": [-0.75, -1.55, 0.40], "lens": 35}])
# s5 extreme close-up: quad round tail lamps (2 mm), slide across the tail
shot("s5_tail", CAR2, secs(4), [{"t": 0, "az": 160, "el": 6, "dist": 1.9, "target": [0.35, 2.15, 0.70], "lens": 35},
                           {"t": 1, "az": 195, "el": 8, "dist": 1.9, "target": [-0.35, 2.15, 0.70], "lens": 35}])
# s6 hood opens on the hinge fitted to the captured hood-open scan; engine bay = that scan as captured
shot("s6_hood", {"base": B + "base_hood.blend", "hood": B + "hood_combo.blend"}, secs(5),
     [{"t": 0, "az": -35, "el": 16, "dist": 4.6, "target": [0, -1.2, 0.65], "lens": 34},
      {"t": 1, "az": -48, "el": 32, "dist": 4.4, "target": [0, -1.3, 0.75], "lens": 34}],
     anims={"hood": [{"t": fr(0.5, 5), "deg": 0}, {"t": fr(3.8, 5), "deg": OPEN}]}, hinges=HINGES, light_ref="base")
# s7 top-down, spinning
shot("s7_top", CAR, secs(6), [{"t": 0, "az": 0, "el": 89.9, "dist": 8.6, "target": [0, 0, 0.4], "lens": 34},
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
an8 = stag(HOME, EX, fr(0.1, 7), fr(2.1, 7), ["tg", "hood", "fb", "fe", "rb"], fr(0.28, 7))  # separate on the 26.621 accent
for k in an8: an8[k].append(dict(t=1.0, **EX2[k]))
shot("s8_explode", EXPL, secs(7), [{"t": 0, "az": -40, "el": 22, "dist": 7.6, "target": [0, -0.15, 0.85], "lens": 32},
                              {"t": 1, "az": -68, "el": 26, "dist": 8.2, "target": [0, 0, 1.0], "lens": 32}],
     anims=an8, hinges=HINGES, light_ref="base")
# s9 side/rear 3/4: panels float, then return home (staggered, reverse order) -> assembled car, fades out
an9 = stag(EX2, HOME, fr(1.3, 8), fr(3.25, 8), ["rb", "fe", "fb", "hood", "tg"], fr(0.16, 8))  # last panel (targa) locks at 3.89 s = 34.402 (b61 kick)
for k in an9: an9[k].insert(0, dict(t=0, **EX2[k]))
# once every panel is home (targa rest 3.89 s) swap the frayed composite for the clean full car - same frame, so the
# swap reads as the car snapping clean on the kick, and the payoff frame before the logo has no part seams (v1 review: ragged -X fender/quarter edges)
SWAP = fr(3.90, 8)  # first car frame = 59 (3.916 s = reel 34.43, on the b61 kick 34.402 where the targa locks)
VIS9 = {"car": [SWAP, 1.01], **{k: [0, SWAP] for k in EXPL}}
shot("s9_reassemble", {**EXPL, **CAR}, secs(8), [{"t": 0, "az": -112, "el": 18, "dist": 8.6, "target": [0, 0.1, 1.0], "lens": 32},
                                 {"t": 1, "az": -148, "el": 11, "dist": 6.3, "target": [0, 0.25, 0.55], "lens": 36}],
     anims=an9, hinges=HINGES, light_ref="base", visible=VIS9)
print("wrote", sorted(os.listdir(OUT)))

# ---------------------------------------------------------------- v2 (reviewer on v1 + the sibling first drafts)
# "Focus more specifically on the removed areas and where the useful data is"; "rotations are wasted"; "front bumper
# removed: frame the front while it comes off, THEN the rear"; bumpers turn about vertical to show the scanned inside.
# No turntables/orbits/top-down spin: every camera move is a straight push on ONE removed area. Only panels that were
# physically removed AND have a removed-state scan move (front bumper, -X fender, hood, rear bumper); the targa has no
# roof-off state, so it stays home. Base = the composite (car trimmed under the parts + the removed states as captured).
V2 = {"tg": B + "targa_reg.blend", **{k: B + PARTS[k] + ".blend" for k in ["fb", "fe", "hood", "rb"]}, "base": B + "base.blend"}
Z = [0, 0, 0]
# parked poses once a panel is off (held in later shots so the state carries through)
P_FB = {"off": [0, -1.1, 1.0], "spin": [180, 0, 0, 1]}      # above the nose, inner face toward a front camera
P_FE = {"off": [-0.35, 0, 0.9]}                              # lifted up/out of the -X front quarter
P_HOOD = {"off": [0, 0.35, 1.0], "deg": OPEN}                # opened on its hinge, then lifted off
P_RB = {"off": [0, 1.3, 0.95], "spin": [180, 0, 0, 1]}       # above/behind the tail, inner face toward a rear camera
HOMEK = {"fb": {"off": Z, "spin": [0, 0, 0, 1]}, "fe": {"off": Z}, "hood": {"off": Z, "deg": 0},
         "rb": {"off": Z, "spin": [0, 0, 0, 1]}}
def held(**poses):
    return {k: [dict(t=0, **v)] for k, v in poses.items()}
def push(az, el, d0, d1, tgt0, tgt1=None, lens=30):
    """straight push along one bearing - no rotation around the car"""
    return [{"t": 0, "az": az, "el": el, "dist": d0, "target": tgt0, "lens": lens},
            {"t": 1, "az": az, "el": el, "dist": d1, "target": tgt1 or tgt0, "lens": lens}]
def v2shot(name, i, cam, anims, **kw):
    shot("v2_" + name, V2, secs(i), cam, anims=anims, hinges=HINGES, light_ref="base", persistent=False, **kw)

# A (0-4.04) HOOK: framed on the nose, the front bumper slides straight out from 0.6 s
v2shot("a_fb_off", 0, push(-28, 9, 4.6, 3.8, [0, -1.95, 0.45]),
       {"fb": [{"t": fr(0.6, 0), "off": Z, "spin": [0, 0, 0, 1]}, {"t": 1, "off": [0, -0.9, 0.05], "spin": [0, 0, 0, 1]}],
        **held(fe=HOMEK["fe"], hood=HOMEK["hood"], rb=HOMEK["rb"])})
# B (4.04-9.39): low head-on push into the exposed crash structure / radiator support; the bumper rises above the nose
# and turns about vertical so its scanned inner face is on camera (bumper upper frame, structure lower frame)
v2shot("b_fb_inside", 1, push(-6, 7, 4.2, 3.3, [0, -2.3, 0.75], [0, -2.25, 0.65]),
       {"fb": [{"t": 0, "off": [0, -0.9, 0.05], "spin": [0, 0, 0, 1]}, {"t": fr(0.3, 1), "off": [0, -0.9, 0.05], "spin": [0, 0, 0, 1]},
               {"t": fr(3.6, 1), **P_FB}],
        **held(fe=HOMEK["fe"], hood=HOMEK["hood"], rb=HOMEK["rb"])})
# C (9.39 DROP-13.84): -X side on the front quarter; the fender lifts off on the drop -> inner wheelhouse + mounts
v2shot("c_fender", 2, push(-80, 8, 3.7, 3.0, [-0.7, -1.35, 0.55], [-0.75, -1.4, 0.5]),
       {"fe": [{"t": fr(0.1, 2), "off": Z}, {"t": fr(1.7, 2), **P_FE}],
        **held(fb=P_FB, hood=HOMEK["hood"], rb=HOMEK["rb"])})
# D (13.84-15.51) close-up: exposed fender mounts / headlight bucket from the -X front corner
v2shot("d_fender_macro", 3, push(-52, 14, 1.75, 1.5, [-0.65, -1.75, 0.6], lens=35),
       held(fb=P_FB, fe=P_FE, hood=HOMEK["hood"], rb=HOMEK["rb"]))
# E (15.51-17.17) close-up: crash bar / radiator support where the bumper was
v2shot("e_nose_macro", 4, push(12, 16, 1.8, 1.55, [0.15, -2.05, 0.45], lens=35),
       held(fb=P_FB, fe=P_FE, hood=HOMEK["hood"], rb=HOMEK["rb"]))
# F (17.17-22.18): hood opens on the fitted hinge, then lifts off; push down into the engine bay (hood-removed state)
v2shot("f_hood", 5, push(-18, 38, 4.4, 3.5, [0, -1.15, 0.7], [0, -1.05, 0.6]),
       {"hood": [{"t": fr(0.3, 5), "off": Z, "deg": 0}, {"t": fr(1.9, 5), "off": Z, "deg": OPEN},
                 {"t": fr(3.4, 5), **P_HOOD}],
        **held(fb=P_FB, fe=P_FE, rb=HOMEK["rb"])})
# G (22.18 kick-26.62): THEN the rear - rear 3/4 framed on the tail, bumper slides straight back -> rear crash bar
v2shot("g_rb_off", 6, push(152, 9, 4.3, 3.5, [0, 2.05, 0.45]),
       {"rb": [{"t": fr(0.1, 6), "off": Z, "spin": [0, 0, 0, 1]}, {"t": fr(1.6, 6), "off": [0, 0.9, 0.05], "spin": [0, 0, 0, 1]}],
        **held(fb=P_FB, fe=P_FE, hood=P_HOOD)})
# H (26.62-30.51): straight behind; the bumper rises and turns about vertical -> its scanned inside on camera
v2shot("h_rb_inside", 7, push(178, 8, 4.2, 3.4, [0, 2.4, 0.8], [0, 2.35, 0.7]),
       {"rb": [{"t": 0, "off": [0, 0.9, 0.05], "spin": [0, 0, 0, 1]}, {"t": fr(2.6, 7), **P_RB}],
        **held(fb=P_FB, fe=P_FE, hood=P_HOOD)})
# I (30.51-35.51): wide high front 3/4, everything flies home (rear first, front bumper last, locking on the 34.402 kick),
# then the clean full car. v1 measured the shot-time->reel mapping ~0.08 s early, so lock/swap are keyed at 3.97/3.98 s.
an_i = stag({k: dict(P_FB if k == "fb" else P_FE if k == "fe" else P_HOOD if k == "hood" else P_RB) for k in HOMEK},
            HOMEK, fr(1.2, 8), fr(3.45, 8), ["rb", "hood", "fe", "fb"], fr(0.173, 8))
SWAP2 = fr(3.98, 8)
v2shot("i_home", 8, push(-38, 24, 8.4, 7.2, [0, -0.1, 0.75], [0, -0.05, 0.6], lens=32), an_i,
       visible={"car": [SWAP2, 1.01], **{k: [0, SWAP2] for k in V2}})
# the clean car is only in the last shot
json.dump({**json.load(open(OUT + "v2_i_home.json")), "objects": {**V2, **CAR}}, open(OUT + "v2_i_home.json", "w"), indent=1)
print("v2 shots", [n for n in sorted(os.listdir(OUT)) if n.startswith("v2_")])
