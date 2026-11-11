"""Shot specs for the Porsche 911 GT3 (992) Temerario-style scan reel -> JSON for tools/shot.py.

    python projects/porsche-gt3-992/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Scan frame (ive prep of the levelled full car, metres): front = -Y, car's right = -X, ground Z=0;
length 4.567 m, height 1.277 m. Shot lengths come from cues.json (the music's accent grid) when present.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = "/home/user/media/work/gt3"
P = f"{W}/prep"
OUT = f"{W}/renders"
SPECS = f"{W}/specs"

CAR = f"{P}/car4.blend"      # 4 mm: full-car moves
BRAKE = f"{P}/frww15.blend"  # 1.5 mm 'FR wheel well' state scan (wheel off): disc, caliper, spring
REAR = f"{P}/rear_2mm.blend"  # 2 mm rear crop: wing close-up

# seconds per shot (render length; the edit trims). Overridden by cues.json "secs" once the music is in.
SECS = {"s1_front34": 5.0, "s2_rear34": 5.0, "s3_wheel": 3.5, "s4_wing": 3.5, "s5_hood": 4.5, "s6_top": 4.0,
        "s7_explode": 11.0}
EXPLODE = {"sep": 1.0, "out": 2.6, "back": 8.0, "lock": 9.6}  # seconds within s7 (overridden by cues.json)
cues = os.path.join(HERE, "..", "cues.json")
if os.path.exists(cues):
    C = json.load(open(cues))
    SECS.update(C.get("secs", {}))
    EXPLODE.update(C.get("explode", {}))


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); +90 = car's left (+X); -90 = car's right (-X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(T, n, r0, r1, a0, a1, h0, h1, c=(0, 0, 0.55), focal=30, tz=None, ease="inout"):
    """Orbit keyed every 1/n of the move (linear loc between far-apart keys would cut a chord toward the car).
    The eased fraction is baked into the keys; segments are linear."""
    keys = []
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u) if ease == "inout" else (1 - (1 - u) ** 2 if ease == "out2" else u)
        keys.append(orbit(T * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c=c, focal=focal,
                          ease="lin", tz=tz))
    return keys


def shots():
    S = SECS
    sh = {
        # 1. slow front 3/4 turntable from the car's right, low
        "s1_front34": {"base": [CAR], "cam": arc(S["s1_front34"], 10, 5.0, 4.9, -26, -54, 0.95, 1.1, focal=30, ease="lin")},
        # 2. rear 3/4 orbit from the car's left, rising a little: wing silhouette
        "s2_rear34": {"base": [CAR], "cam": arc(S["s2_rear34"], 10, 5.1, 4.9, 158, 132, 1.15, 1.6, focal=30, ease="out2")},
        # 3. extreme close-up: front-right brake + suspension (wheel-off state scan); the full car's own wheel
        #    has scan fragments inside the spokes. Slow slide toward the nose, ragged scan edges kept out of frame
        "s3_wheel": {"base": [BRAKE], "cam": [
            {"t": 0, "loc": [-1.78, -0.78, 0.44], "target": [-0.8, -1.34, 0.34], "focal": 41},
            {"t": S["s3_wheel"], "loc": [-1.8, -1.08, 0.42], "target": [-0.8, -1.36, 0.34], "focal": 41, "ease": "inout"}]},
        # 4. extreme close-up: swan-neck wing mounts + duckbill from high rear-left, slide across
        "s4_wing": {"base": [REAR], "cam": [
            {"t": 0, "loc": [1.7, 3.5, 1.75], "target": [0.25, 1.95, 1.1], "focal": 35},
            {"t": S["s4_wing"], "loc": [0.55, 3.7, 1.6], "target": [0.05, 1.95, 1.1], "focal": 35, "ease": "inout"}]},
        # 5. hood (front lid) opens on its rear hinge over the 'Front Hood Open' frunk, camera eases in
        "s5_hood": {"base": [f"{P}/comp_hood.blend"],
                    "parts": [{"blend": f"{P}/hood_lid1.blend", "pivot": [0, -0.87, 0.86],
                               "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                        {"t": EXPLODE.get("hood_start", 0.6), "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                        {"t": EXPLODE.get("hood_end", 2.6), "loc": [0, 0, 0], "rot": [-62, 0, 0], "ease": "inout"}]}],
                    "cam": arc(S["s5_hood"], 8, 4.4, 3.9, 32, 18, 1.75, 2.1, c=(0, -1.0, 0.5), focal=30, ease="out2")},
        # 6. top-down: from a high rear 3/4 up and over to straight down, nose at the top of the frame
        "s6_top": {"base": [CAR], "cam": [
            {"t": 0, "loc": [2.3, 4.4, 3.6], "target": [0, 0.3, 0.5], "focal": 30},
            {"t": S["s6_top"], "loc": [0.0, 0.2, 7.0], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
    }
    # 7. exploded view: panels separate on an accent, drift while the camera orbits, fly home and LOCK on an accent
    sep, out, back, lock = EXPLODE["sep"], EXPLODE["out"], EXPLODE["back"], EXPLODE["lock"]

    def ex(off, rot=(0, 0, 0), delay=0.0):
        return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": sep + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": out + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
                {"t": back, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},
                {"t": lock, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]

    X = f"{P}/x_"
    sh["s7_explode"] = {
        "base": [f"{P}/comp_x.blend"],
        "parts": [  # stacked above the car / pushed fore-aft and down so nothing flies at the lens (lessons)
            {"blend": f"{X}hood.blend", "keys": ex((0, -0.35, 1.05), (-10, 0, 0))},
            {"blend": f"{X}fbumper.blend", "keys": ex((0, -1.05, -0.05))},
            {"blend": f"{X}skirt.blend", "keys": ex((-0.7, 0, -0.1), delay=0.05)},
            {"blend": f"{X}duckbill.blend", "keys": ex((0, 0.3, 1.0), (14, 0, 0), 0.08)},
            {"blend": f"{X}wing.blend", "keys": ex((0, 0.45, 1.75), delay=0.12)},
            {"blend": f"{X}rbumper.blend", "keys": ex((0, 0.7, 0.55), delay=0.04)},
            {"blend": f"{X}diffuser.blend", "keys": ex((0, 0.7, -0.3), delay=0.1)},
            {"blend": f"{X}rlip.blend", "keys": ex((0, 0.95, -0.5), delay=0.14)},
        ],
        "cam": arc(S["s7_explode"], 14, 5.6, 5.4, -174, -128, 5.4, 4.0, c=(0, 0.3, 0.5), focal=26, tz=0.4, ease="inout")}
    return sh


def spec(name, mode, frames=None):
    s = shots()[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if frames:
        sp["frames"] = frames
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    names = sys.argv[2:] or list(shots())
    for n in names:
        print(spec(n, mode, ["first", "mid", "last"] if mode == "preview" else None))
