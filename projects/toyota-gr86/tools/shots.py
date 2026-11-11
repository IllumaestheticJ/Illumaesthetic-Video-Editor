"""Shot specs for the GR86/BRZ scan reel -> projects/toyota-gr86/shots/<name>.json (for ferrari-296/tools/shot.py).
Blender frame (car4.json prep): nose -Y (y -2.11), tail +Y (2.11), ground z 0.19, roof z 1.43, car's left = -X.
  python projects/toyota-gr86/tools/shots.py [explode_secs sep_t lock_t]"""
import json, math, os, sys
B = "/home/user/media/work/gr86/blend/"
OUT = "/home/user/media/work/gr86/shots/"
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots")


def smooth(u):
    u = min(1, max(0, u)); return u * u * (3 - 2 * u)


def orbit(center, radius, z, a0, a1, secs, focal, r1=None, z1=None, f1=None, tz=None, tz1=None, step=0.2):
    keys = []
    n = int(round(secs / step))
    for i in range(n + 1):
        t = i * step; u = smooth(t / secs)
        a = math.radians(a0 + (a1 - a0) * u)
        r = radius + ((r1 or radius) - radius) * u
        zz = z + ((z1 if z1 is not None else z) - z) * u
        tgt = list(center)
        if tz is not None: tgt[2] = tz + ((tz1 if tz1 is not None else tz) - tz) * u
        keys.append({"t": round(t, 3), "loc": [center[0] + r * math.cos(a), center[1] + r * math.sin(a), zz],
                     "target": tgt, "focal": focal + ((f1 or focal) - focal) * u, "ease": "lin"})
    return keys


def spec(name, base, keys, secs, parts=(), **kw):
    s = {"base": [B + b for b in base], "parts": list(parts), "camera": {"keys": keys}, "seconds": secs, "fps": 15,
         "res": "1080x1920", "res_pct": 75, "samples": 12, "out": OUT + name}
    s.update(kw)
    json.dump(s, open(os.path.join(HERE, name + ".json"), "w"), indent=1)


# s1: low front-right 3/4 (the left mirror is a broken capture), slow turntable toward the nose
spec("s1_front34", ["car4.blend"], orbit([-0.3, -0.6, 0.7], 4.9, 0.80, 312, 290, 6.0, 32, r1=4.6), 6.0)
# s2: rear-right 3/4, higher, orbit toward the tail
spec("s2_rear34", ["car4.blend"], orbit([0, 0.35, 0.72], 4.7, 1.45, 35, 68, 6.0, 31, z1=1.25), 6.0)
# s3: extreme close-up, front-right headlight + intake (2 mm detail crop); wheels are rough captures
spec("s3_wheel", ["det_front.blend"], [
    {"t": 0, "loc": [1.75, -3.25, 0.98], "target": [0.62, -1.88, 0.82], "focal": 42},
    {"t": 5.0, "loc": [1.05, -3.55, 0.92], "target": [0.52, -1.95, 0.78], "focal": 46}], 5.0)
# s4: extreme close-up, rear-left lamp + ducktail, slide across the tail
spec("s4_tail", ["det_rear.blend"], [
    {"t": 0, "loc": [-1.75, 3.25, 1.20], "target": [-0.55, 1.95, 0.98], "focal": 40},
    {"t": 5.0, "loc": [-0.95, 3.55, 1.28], "target": [-0.30, 1.98, 1.00], "focal": 44}], 5.0)
# s5: hood opens (beat 1 -> next bar downbeat, 0.612 -> 2.449 s into the shot) on its cowl hinge (rear edge, fitted from the hood panel) over the engine-bay composite
HINGE = [0.0095, -0.6236, 1.0916]
spec("s5_hood", ["comp_hoodopen.blend"], [
    {"t": 0, "loc": [-2.7, -4.6, 1.75], "target": [-0.3, -1.1, 0.85], "focal": 31},
    {"t": 5.0, "loc": [-1.9, -4.1, 2.25], "target": [-0.25, -1.05, 0.80], "focal": 32}], 5.0,
    parts=[{"blend": B + "hood_m.blend", "pivot": HINGE,
            "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": 0.612, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                     {"t": 2.449, "loc": [0, 0, 0], "rot": [-52, 0, 0], "ease": "inout"}]}])
# s6: near top-down; camera offset orbits so the car turns in frame (image-up follows the offset)
spec("s6_top", ["car4.blend"], orbit([0, 0, 0.7], 1.1, 5.9, 250, 300, 5.0, 31, z1=5.6), 5.0)


def explode(secs=10.0, sep=1.0, lock=8.0):
    """Parts lift into layers above the car (portrait stacking), drift, and slam home at `lock` (seconds)."""
    out_t = sep + 1.6
    def k(d):  # d = displaced loc
        z = [0, 0, 0]
        return [{"t": 0, "loc": z, "rot": z}, {"t": sep, "loc": z, "rot": z},
                {"t": out_t, "loc": d, "rot": z, "ease": "out"},
                {"t": lock - 1.6, "loc": [d[0], d[1], d[2] + 0.06], "rot": z, "ease": "inout"},
                {"t": lock, "loc": z, "rot": z, "ease": "in"}]
    parts = [{"blend": B + "hood_m.blend", "keys": k([0, -0.1, 1.2])},
             {"blend": B + "front_bumper.blend", "keys": k([0, -0.5, 0.75])},
             {"blend": B + "rear_bumper.blend", "keys": k([0, 0.5, 0.75])}]
    keys = orbit([0, -0.4, 1.0], 6.6, 3.1, 292, 322, secs, 30, r1=6.9, z1=2.5, tz=0.95, tz1=1.15)
    spec("s7_explode", ["comp_explode.blend"], keys, secs, parts=parts)


if __name__ == "__main__":
    a = [float(v) for v in sys.argv[1:]]
    explode(*a) if a else explode()
    print(sorted(os.listdir(HERE)))
