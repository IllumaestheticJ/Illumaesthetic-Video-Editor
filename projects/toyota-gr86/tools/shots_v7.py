"""v7 specs (user on v6): (1) "the BRZ and GR86 bumper are clipping into each other. have them come off and then split apart";
(2) "there are still bits of the rear trunk left behind".
(2) every re-rendered shot uses base comp_explode7 + lid_v7 (tools/build_v7.py, tools/lid_v7.py).
(1) bumpers: A = the combined part (BRZ skin + GR86 inner face) is shown while the bumper is home and while it pulls straight
    out together; at T_SPLIT A is hidden and B (BRZ skin, fb_brz/rb_brz) + C (GR86 Bomex scan, fb_gr86/rb_gr86) are shown in
    the same pose, then C carries on the old path (tips, drops, parks; the rear lights ride it) and B rises away out of frame.
    Later shots park only C (B gone). Explode: B and C get separate offsets. Reassembly: C lands, then B, then A swaps back in.
Single shots are transformed from their existing specs; x1-x3/h1 are regenerated here (copy of shots_v5 explode code).
  python projects/toyota-gr86/tools/shots_v7.py [--preview]"""
import copy, json, os, sys

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots")
B = "/home/user/media/work/gr86/blend/"
PREVIEW = "--preview" in sys.argv
T_SPLIT = 0.40
FAR = [0, 0, 9.0]
Z = [0, 0, 0]
FB_PIV, RB = [-0.07, -1.818, 0.605], [0.064, 1.817, 0.638]
# BRZ skin leaves upward after the split (rel. to home, via the pulled-out pose), fully out of frame by 1.60 s
BRZ_F_TAIL = [{"t": 0.95, "loc": [0, -0.35, 0.75], "rot": Z, "ease": "out"}, {"t": 1.60, "loc": [0, -0.40, 2.80], "rot": Z, "ease": "in"}]   # straight UP (preview: forward+up flew at the lens)
BRZ_R_TAIL = [{"t": 0.95, "loc": [0, 0.35, 0.75], "rot": Z, "ease": "out"}, {"t": 1.60, "loc": [0, 0.40, 2.80], "rot": Z, "ease": "in"}]


def blend(name):
    return B + name + ".blend"


def load(name):
    return json.load(open(os.path.join(D, name + ".json")))


def v7_geometry(s):
    s["base"] = [b.replace("comp_explode4.blend", "comp_explode7.blend").replace("comp_explode6.blend", "comp_explode7.blend") for b in s["base"]]
    for p in s["parts"]:
        p["blend"] = p["blend"].replace("/lid_v4.blend", "/lid_v7.blend").replace("/lid_v6.blend", "/lid_v7.blend")


def find(s, name):
    return [p for p in s["parts"] if p["blend"].endswith("/" + name + ".blend")]


def split_bumper(s, combined, brz, gr86, tail):
    """A shown to T_SPLIT; C = same keys (GR86 scan) and B = keys to T_SPLIT + tail (BRZ skin) shown from T_SPLIT."""
    a = find(s, combined)[0]; a["show"] = [[0, T_SPLIT]]
    c = copy.deepcopy(a); c["blend"] = blend(gr86); c["show"] = [[T_SPLIT, 99]]
    b = copy.deepcopy(a); b["blend"] = blend(brz); b["show"] = [[T_SPLIT, 99]]
    b["keys"] = [k for k in a["keys"] if k["t"] <= T_SPLIT] + copy.deepcopy(tail)
    s["parts"] += [b, c]


def park_split(s, combined, brz, gr86):
    """combined part (parked) -> GR86 scan with the same keys; BRZ skin gone (left the frame in the removal shot)."""
    a = find(s, combined)[0]; a["blend"] = blend(gr86)
    s["parts"].append({"blend": blend(brz), "keys": [{"t": 0, "loc": FAR, "rot": Z, "ease": "inout"}], "pivot": a.get("pivot")})


def write(name, s, extra=()):
    s = copy.deepcopy(s); s["out"] = "/home/user/media/work/gr86/shots/" + name
    if s["fps"] == 30:
        s["seconds"] = round(59 / 30 + 0.1, 4)
    if PREVIEW:
        s.update(res_pct=30, samples=8, out="/home/user/media/work/gr86/preview/" + name,
                 frames=["first", "mid", "last", *[max(1, round(t * s["fps"])) for t in extra]])
    json.dump(s, open(os.path.join(D, name + ("_pv" if PREVIEW else "") + ".json"), "w"), indent=1)
    print(name, s["seconds"], "s", s["fps"], "fps", len(s["parts"]), "parts")


# front
s = load("c3b_front_bumper_off"); v7_geometry(s); split_bumper(s, "front_bumper_v5", "fb_brz", "fb_gr86", BRZ_F_TAIL)
write("c3b_front_bumper_off7", s, (0.40, 0.70, 1.10))
s = load("c4_front_structure"); v7_geometry(s); park_split(s, "front_bumper_v4", "fb_brz", "fb_gr86"); write("c4_front_structure7", s)
# rear: lid shots only need the v7 base/lid (bumper home = combined part)
for n in ("e1_lid_hinge6", "e2_lid_off_cargo6"):
    s = load(n); v7_geometry(s); write(n[:-1] + "7", s, (0.45,))
s = load("e3_rear_bumper_off6"); v7_geometry(s); split_bumper(s, "rear_bumper_v4", "rb_brz", "rb_gr86", BRZ_R_TAIL)
write("e3_rear_bumper_off7", s, (0.40, 0.70, 1.10))
for n, src in (("e4_rear_beam7", "e4_rear_beam6"), ("f1_reverse_light7", "f1_reverse_light6"), ("f2_plate_light7", "f2_plate_light")):
    s = load(src); v7_geometry(s); park_split(s, "rear_bumper_v4", "rb_brz", "rb_gr86"); write(n, s)

# explode / reassembly (shots_v5 code + split bumpers)
_v5 = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots_v5.py")).read()
exec(_v5.split("# 4  m1:")[0].split('"""', 2)[2])                                   # helpers + constants
exec(_v5[_v5.index("# 14-17  explode"):_v5.index('spec("x1_explode_fr"')])              # EX, HOME, explode_keys, explode_parts
# BRZ skins: front above the GR86 bumper (preview: hidden behind it at +0.60), rear behind + above the GR86 bumper; the plate lamp
# drops below the rear BRZ skin (its v5 pose (0.50,1.05,0.20) lies inside the skin at this offset)
EX.update({"fbB": [0, -1.40, 0.75], "rbB": [0, 1.55, 0.45], "pl": [0.50, 0.95, -0.35]})
HOME.update({"fbB": (7.05, 7.55), "rbB": (6.20, 6.75)})


def explode7(shift):
    def sh(keys):
        return [dict(x, t=round(x["t"] - shift, 4)) for x in keys]
    ps = explode_parts(0)   # unshifted (shift applied below so A/B/C share it)
    for p in ps:
        if p["blend"].endswith("/front_bumper_v5.blend"):
            p["blend"] = blend("fb_gr86")
        if p["blend"].endswith("/rear_bumper_v4.blend"):
            p["blend"] = blend("rb_gr86")
        if p["blend"].endswith("/lid_v4.blend"):
            p["blend"] = blend("lid_v7")
    t_land_f, t_land_r = HOME["fbB"][1], HOME["rbB"][1]
    ps.append(part("fb_brz", explode_keys("fbB", FAR, Z, T_OUT_BIG), FB_PIV))
    ps.append(part("rb_brz", explode_keys("rbB", FAR, Z, T_OUT_BIG), RB))
    for p in ps:   # split pairs shown until the BRZ skin has landed; then the combined part (A) takes over at home
        if p["blend"].endswith(("/fb_gr86.blend", "/fb_brz.blend")):
            p["show"] = [[-99, t_land_f]]
        if p["blend"].endswith(("/rb_gr86.blend", "/rb_brz.blend")):
            p["show"] = [[-99, t_land_r]]
    ps.append(dict(part("front_bumper_v5", [k(0, Z)], FB_PIV), show=[[t_land_f, 99]]))
    ps.append(dict(part("rear_bumper_v4", [k(0, Z)], RB), show=[[t_land_r, 99]]))
    for p in ps:
        p["keys"] = sh(p["keys"])
        if "show" in p:
            p["show"] = [[a - shift, b - shift] for a, b in p["show"]]
    return ps


CAMS = {"x1_explode_fr7": ([2.30, -6.40, 4.60], [-0.38, -0.45, 0.59], 30, 31.7), "x2_explode_rr7": ([2.50, 6.60, 4.40], [0.02, 0.45, 0.34], 34, 35.8),
        "x3_explode_high7": ([1.70, 5.60, 7.00], [0.11, 0.33, 0.17], 40, 42.8)}
for i, (n, (cl, tg, f0, f1)) in enumerate(CAMS.items()):
    s = {"base": [blend("comp_explode7")], "parts": explode7(i * BAR), "camera": {"keys": [cam(0, cl, tg, f0), cam(BAR, cl, tg, f1)]},
         "seconds": 2.0667, "fps": 30, "res": "1080x1920", "res_pct": 75, "samples": 12}
    write(n, s, (0.30, 0.60) if i == 0 else ())
s = {"base": [blend("comp_explode7")], "parts": explode7(3 * BAR),
     "camera": {"keys": [cam(0, [4.40, 1.15, 9.10], [0.12, -0.05, 0.80], 26), cam(BAR, [2.80, 0.70, 6.20], [0, -0.05, 0.80], 26)]},
     "seconds": 2.0667, "fps": 30, "res": "1080x1920", "res_pct": 75, "samples": 12}
write("h1_reassemble7", s, (0.70, 1.30, 1.70))
