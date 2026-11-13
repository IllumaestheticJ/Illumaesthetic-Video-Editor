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

if __name__ == "__main__":
    s = json.load(open(sys.argv[1]))
    s["paint"] = {k: list(v) for k, v in PAINT.items()}
    s["out"] = sys.argv[2]
    p = sys.argv[1].replace(".json", "_color.json")
    json.dump(s, open(p, "w"), indent=1)
    print(p)
