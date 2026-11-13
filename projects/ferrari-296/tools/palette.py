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


# v9 (user: "make the car colors less saturated, more pastel colors (except the ferrari red)"): same hues, lifted toward
# white; the body red and the exposure/look stay. Also "true 60 FPS": rendered at 60 fps natively (no minterpolate).
PAINT_V9 = dict(PAINT_V8, **{
    "x_hood": (0.95, 0.85, 0.28),      # butter
    "x_fbumper": (0.95, 0.40, 0.70),   # pastel pink
    "x_wheel": (0.32, 0.46, 0.98),     # periwinkle
    "x_fender": (0.98, 0.55, 0.28),    # apricot
    "x_skirt": (0.28, 0.80, 0.82),     # pastel teal
    "x_rbumper": (0.85, 0.85, 0.88),   # pearl
    "x_diffuser": (0.62, 0.44, 0.98),  # lavender
    "x_ecover": (0.45, 0.70, 0.95),    # baby blue
    "x_eglass": (0.45, 0.70, 0.95),
    "x_etrim_c": (0.65, 0.88, 0.40),   # pistachio
    "x_etrim_l": (0.65, 0.88, 0.40),
    "x_etrim_r": (0.65, 0.88, 0.40),
    "x_exhaust": (0.40, 0.80, 0.55),   # mint
})
FPS_V9 = 60
# f5_front plays x1.0527 faster than rendered (hood k9 / bumper k13 / turn k17 on the kicks). Resampling 60 fps renders at
# 63.162 drops 1 frame in 19 (judder, lessons) -> sample scene time at 63.162 steps/s and play the frames at exactly 60.
FPS_V9_SHOT = {"f5_front": 63.162}


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


if __name__ == "__main__" and len(sys.argv) > 3 and sys.argv[3] in ("v8", "v9"):
    s = json.load(open(sys.argv[1]))
    s["paint"] = {k: list(v) for k, v in (PAINT_V9 if sys.argv[3] == "v9" else PAINT_V8).items()}
    if sys.argv[3] == "v9":
        s["fps"] = FPS_V9_SHOT.get(sys.argv[2].rstrip("/").rsplit("/", 1)[-1], FPS_V9)
    s["paint"]["reveal"] = {}
    for p in s.get("parts", []):
        stem = p["blend"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
        r = reveal(p["keys"]) if p.get("keys") else None
        if r is not None:
            s["paint"]["reveal"][stem] = r
    s["paint_mat"], s["look"], s["exposure"] = {"base": BODY_MAT}, LOOK, EXPOSURE
    s["out"] = sys.argv[2]
    p = sys.argv[1].replace(".json", f"_{sys.argv[3]}.json")
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
