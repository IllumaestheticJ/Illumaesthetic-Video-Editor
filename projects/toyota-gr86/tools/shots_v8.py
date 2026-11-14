"""v8 specs (user on v7): "the two BRZ and GR86 bumpers are still clipping each other on the sidemarker scene" and
"BRZ and GR86 rear bumpers are the same - don't need to do the splitting thing".
- every at-rest bumper becomes the fused v8 part (tools/fuse_v8.py: BRZ skin + only the GR86 surface BEHIND it - no z-fight,
  no GR86 shape poking through): front_bumper_v8m (markers in: c1, c2), front_bumper_v8 (markers out: m1, c3b before the
  split, h1 after landing), rear_bumper_v8 (rear, everywhere it is one part).
- rear: no split any more (e3 = one bumper on the old path, lights riding it; explode/reassembly without the rear BRZ skin).
- front split (c3b, explode, reassembly) unchanged.
Patches the existing specs; writes shots/<name>8.json (+ _pv previews).   python projects/toyota-gr86/tools/shots_v8.py [--preview]"""
import copy, json, os, sys

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots")
B = "/home/user/media/work/gr86/blend/"
PREVIEW = "--preview" in sys.argv
SWAP = {"front_bumper_v4": "front_bumper_v8m", "front_bumper_v5": "front_bumper_v8", "rear_bumper_v4": "rear_bumper_v8",
        "comp_explode4": "comp_explode7", "comp_explode6": "comp_explode7", "lid_v4": "lid_v7", "lid_v6": "lid_v7"}


def name_of(p):
    return p["blend"].split("/")[-1][:-6]


def patch(src, out, rear_unsplit=False, extra=()):
    s = json.load(open(os.path.join(D, src + ".json")))
    s["base"] = [B + SWAP.get(b.split("/")[-1][:-6], b.split("/")[-1][:-6]) + ".blend" for b in s["base"]]
    parts = []
    for p in s["parts"]:
        n = name_of(p)
        if rear_unsplit and n in ("rb_brz", "rb_gr86") and p.get("show") and p["show"][0][0] >= 0.39 and p["show"][0][0] <= 0.41:
            continue                                   # e3: the split pair (shown from the split on) is gone
        if rear_unsplit and n == "rb_brz":
            continue                                   # explode / reassembly: no rear BRZ skin
        if n in SWAP:
            p["blend"] = B + SWAP[n] + ".blend"
        if rear_unsplit and n == "rear_bumper_v4" and p.get("show") == [[0, 0.4]]:
            p.pop("show")                              # e3: the one rear bumper carries on along the old path
        parts.append(p)
    s["parts"] = parts
    if s["fps"] == 30:
        s["seconds"] = round(59 / 30 + 0.1, 4)
    s["out"] = "/home/user/media/work/gr86/shots/" + out
    if PREVIEW:
        s.update(res_pct=30, samples=8, out="/home/user/media/work/gr86/preview/" + out,
                 frames=["first", "mid", "last", *[max(1, round(t * s["fps"])) for t in extra]])
    json.dump(s, open(os.path.join(D, out + ("_pv" if PREVIEW else "") + ".json"), "w"), indent=1)
    print(out, s["seconds"], "s", len(parts), "parts:", sorted({name_of(p) for p in parts if "bumper" in name_of(p) or name_of(p).startswith(("fb_", "rb_"))}))


patch("c1_hood_hinge", "c1_hood_hinge8")
patch("c2_hood_off", "c2_hood_off8")
patch("m1_side_marker", "m1_side_marker8", extra=(0.30, 1.30))
patch("c3b_front_bumper_off7", "c3b_front_bumper_off8")
patch("e1_lid_hinge7", "e1_lid_hinge8")
patch("e2_lid_off_cargo7", "e2_lid_off_cargo8")
patch("e3_rear_bumper_off7", "e3_rear_bumper_off8", rear_unsplit=True, extra=(0.40, 0.80))
for n in ("x1_explode_fr", "x2_explode_rr", "x3_explode_high", "h1_reassemble"):
    patch(n + "7", n + "8", rear_unsplit=True)
