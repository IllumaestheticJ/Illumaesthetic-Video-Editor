"""Mobile-version CTA end card (Remotion MobileCTA) + the matching end camera for the drop shot.

    python3 projects/ferrari-296/tools/cta.py props   -> projects/ferrari-296/cta.json (ive hud ... --comp MobileCTA)
    python3 projects/ferrari-296/tools/cta.py camera  -> prints the drop's final camera key (sensor 20.25)

The 1:1 frame: the listing's cover photo (3465 x 2292, the gallery's slide 1) shown at START_SCALE photo px per video px
with its centre on the frame centre (540, 960). The cover photo's camera was solved against comp_v5 + all parts home
(photo_search.py, 36 mm sensor across the photo width, no lens shift). Same horizontal FOV on a 1080 px crop of the
scaled photo => focal_video = focal_photo * (3465 * START_SCALE / 1080), on a 36 mm width; the shots use 20.25 mm.
Website: illumaesthetic.com/products/ferrari-296-gtb-type-f171-3d-scan-2022, captured 2026-11-12 (Playwright, iPhone 14
Pro UA, viewport 393 x 699 = 9:16 @3x, Photos tab, gspin switch / zoom button / broken "Marker" widget hidden).
"""
import json
import sys

PHOTO_W, PHOTO_H = 3465, 2292
START_SCALE = 0.44
CUT = 956  # video frame of the 1:1 cut (k75)
KJ = json.load(open("/home/user/media/work/music/buckshot_kicks.json"))
_KK = {int(a): b for a, b in KJ["kicks"].items()}


def kf(i):
    """kick i as a CTA-local frame"""
    return round((_KK.get(i, KJ["t0"] + i * KJ["period"]) - CUT / 30) * 30)


def props():
    """v7 (user: "when scrolling through the different photos/options, change the dropdown so the scan price reflects the
    photo"): every swipe is a Dataset option change - the listing's own variant -> featured-image mapping (products/<h>.js):
    Front Bumper F4 $1,000, Hood F12 $800, Rear Bumper R7 $1,000, Engine Bay R6 $600, Side Skirt F7 $800, Fender F10 $800,
    then All Data $4,000 with the CTA. Page screenshots opt_N = the real page with that option selected (price from the
    site, nothing typed by us). Gallery order is monotonic (indices 4,5,9,10,13,16) so the carousel only travels one way."""
    photos = [{"src": "f296_p00.jpg", "w": 3465, "h": 2292}] + [{"src": f"f296_p{i:02d}.jpg", "w": 1800, "h": 1191} for i in range(1, 17)]
    sw = [(kf(80), 4, 1), (kf(81), 5, 2), (kf(82), 9, 3), (kf(83), 10, 4), (kf(84), 13, 5), (kf(85), 16, 6)]
    swipes = [{"at": t - 7, "to": to, "dur": 7} for t, to, _ in sw]
    pages = ([{"src": "f296_mpage_d1.png", "from": 0}] + [{"src": f"f296_opt_{o}.png", "from": t - 7} for t, _, o in sw]
             + [{"src": "f296_opt_7.png", "from": kf(86)}])  # All Data
    return {"width": 1080, "height": 1920, "fps": 30, "durationInFrames": 184, "pageW": 1179, "pages": pages,
            "slot": {"x": 147.37, "y": 177, "w": 884.25, "h": 585.57, "pitch": 896.25}, "photos": photos, "start": 0,
            "startScale": START_SCALE, "hold": 6, "zoomEnd": kf(79), "swipes": swipes, "ctaAt": kf(86), "urlAt": kf(87),
            "drift": 0.02, "ctaBand": 175,
            # dropdown (select 51.5,586.2 275x40.4 CSS) and price (centred, widest "$4,000.00") in screenshot px (@3x)
            "highlights": [{"x": 154.5, "y": 1758.6, "w": 825, "h": 121.2}, {"x": 420, "y": 1434, "w": 324, "h": 84}],
            "title": "SCAN DATA", "sub": "AVAILABLE NOW", "url": "ILLUMAESTHETIC.COM"}


def camera(best="/home/user/media/work/f296/web/fit/s4_best.json"):
    b = json.load(open(best))
    f36 = b["focal"] * PHOTO_W * START_SCALE / 1080
    return {"loc": b["loc"], "target": b["target"], "focal": round(f36 * 20.25 / 36, 3), "iou": b["iou"]}


if __name__ == "__main__":
    if sys.argv[1] == "props":
        json.dump(props(), open("projects/ferrari-296/cta.json", "w"), indent=1)
        print("projects/ferrari-296/cta.json")
    else:
        print(json.dumps(camera(*sys.argv[2:])))
