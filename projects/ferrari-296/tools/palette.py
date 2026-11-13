"""v7 per-part palette (linear RGB into AgX on black). Pastels in the spirit of the listing's explode photos (green body,
pink/olive/salmon/lavender parts) - every moving part distinct from the body and from the part that comes off next to it.
    python3 projects/ferrari-296/tools/palette.py <spec.json> <out_dir>   -> writes spec with "paint" + new out, prints path
"""
import json
import sys

PAINT = {  # first test (0.30,0.50,0.32 body) washed out to near-white under the studio key -> deeper, more saturated
    "base": (0.06, 0.26, 0.09),       # body: green
    "x_hood": (0.50, 0.40, 0.02),     # olive yellow
    "x_fbumper": (0.60, 0.04, 0.34),  # pink
    "x_wheel": (0.04, 0.10, 0.65),    # blue
    "x_fender": (0.70, 0.26, 0.02),   # amber
    "x_skirt": (0.01, 0.40, 0.45),    # teal
    "x_rbumper": (0.70, 0.10, 0.06),  # red-salmon
    "x_diffuser": (0.26, 0.10, 0.65), # violet
    "x_ecover": (0.06, 0.30, 0.75),   # sky
    "x_exhaust": (0.85, 0.16, 0.01),  # orange
}

# v8 (user: "start with the car being red (cause ferrari)"): the body is Rosso red and every part starts red too, so
# the opening car is all red; a part changes to its own colour over 0.3 s when it first leaves home (paint["reveal"],
# shot.py). Red rear bumper -> pearl, orange exhaust -> green so nothing else is red/orange next to the red body.
PAINT_V8 = {
    "base": (0.50, 0.010, 0.006),     # body: Ferrari red (with BODY_MAT + LOOK below)
    "x_hood": (0.50, 0.40, 0.02),     # olive yellow
    "x_fbumper": (0.60, 0.04, 0.34),  # pink
    "x_wheel": (0.04, 0.10, 0.65),    # blue
    "x_fender": (0.70, 0.30, 0.02),   # amber
    "x_skirt": (0.01, 0.40, 0.45),    # teal
    "x_rbumper": (0.62, 0.62, 0.66),  # pearl
    "x_diffuser": (0.26, 0.10, 0.65), # violet
    "x_ecover": (0.06, 0.30, 0.75),   # sky
    "x_eglass": (0.06, 0.30, 0.75),   # sky (moves with the cover)
    "x_etrim_c": (0.30, 0.62, 0.02),  # lime
    "x_etrim_l": (0.30, 0.62, 0.02),
    "x_etrim_r": (0.30, 0.62, 0.02),
    "x_exhaust": (0.03, 0.42, 0.14),  # green
}


# a red albedo under the studio key + AgX came out salmon/pink whatever the value (highlights desaturate): matte-ish body
# (rough 0.45, metal 0, specular 0.3) + "AgX - Punchy" at exposure -1.7 reads as Rosso; the other parts get richer too.
BODY_MAT, LOOK, EXPOSURE = [0.45, 0.0, 0.3], "AgX - Punchy", -1.7


def _home(k):
    return not any(abs(v) > 1e-6 for v in list(k["loc"]) + list(k["rot"]))


def reveal(keys):
    """local time a part first leaves home: None = never (stays red), -1e9 = already off at the start"""
    if not _home(keys[0]):
        return -1e9
    for a, b in zip(keys, keys[1:]):
        if not _home(b):
            return a["t"]
    return None


if __name__ == "__main__" and len(sys.argv) > 3 and sys.argv[3] == "v8":
    s = json.load(open(sys.argv[1]))
    s["paint"] = {k: list(v) for k, v in PAINT_V8.items()}
    s["paint"]["reveal"] = {}
    for p in s.get("parts", []):
        stem = p["blend"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
        r = reveal(p["keys"]) if p.get("keys") else None
        if r is not None:
            s["paint"]["reveal"][stem] = r
    s["paint_mat"], s["look"], s["exposure"] = {"base": BODY_MAT}, LOOK, EXPOSURE
    s["out"] = sys.argv[2]
    p = sys.argv[1].replace(".json", "_v8.json")
    json.dump(s, open(p, "w"), indent=1)
    print(p, s["paint"]["reveal"])
    sys.exit()

if __name__ == "__main__":
    s = json.load(open(sys.argv[1]))
    s["paint"] = {k: list(v) for k, v in PAINT.items()}
    s["out"] = sys.argv[2]
    p = sys.argv[1].replace(".json", "_color.json")
    json.dump(s, open(p, "w"), indent=1)
    print(p)
