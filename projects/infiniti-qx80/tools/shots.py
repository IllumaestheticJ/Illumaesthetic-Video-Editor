"""Shot specs for the Infiniti QX80 scan reel (rendered by tools/shot.py).
Prepped frame (m): nose +Y, car's right +X, floor z=0. Car x +-1.08, y +-2.68, z 0..1.94.
  python shots.py <shot|all> [--check] [--pct N]   -> writes /home/user/media/infiniti-qx80/specs/<shot>.json
--check renders first/mid/last at 30 % / 8 spp into renders/check/<shot>; otherwise full 75 % / 12 spp / 15 fps.
"""
import json, math, os, subprocess, sys
M = "/home/user/media/infiniti-qx80"
B = M + "/blend"
TOOLS = os.path.dirname(os.path.abspath(__file__))
CAR = [B + "/car4.blend"]

def orbit(r, az0, az1, z0, z1, tgt0, tgt1, f0, f1, secs, n=6, ease_last="inout"):
    """camera on a circle around the car's centre; az in degrees, 0 = +Y (nose), 90 = +X (right side)."""
    keys = []
    for i in range(n + 1):
        u = i / n
        k = u * u * (3 - 2 * u)  # eased along the whole move via dense linear keys
        az = math.radians(az0 + (az1 - az0) * k)
        rr = r[0] + (r[1] - r[0]) * k if isinstance(r, (list, tuple)) else r
        keys.append({"t": secs * u, "loc": [rr * math.sin(az), rr * math.cos(az), z0 + (z1 - z0) * k],
                     "target": [a + (b - a) * k for a, b in zip(tgt0, tgt1)], "focal": f0 + (f1 - f0) * k, "ease": "lin"})
    return keys

SHOTS = {}
# s1: low front-right 3/4 turntable - the hero, nose sweeps toward camera
SHOTS["s1_front34"] = dict(base=CAR, seconds=5.6, camera={"keys": orbit((5.4, 5.2), 52, 30, 0.85, 0.95, (0.0, 0.5, 0.92), (0.0, 0.8, 0.95), 30, 30, 5.6)})
# s2: rear-left 3/4 orbit, slight rise
SHOTS["s2_rear34"] = dict(base=CAR, seconds=3.6, camera={"keys": orbit(5.6, 216, 236, 1.0, 1.35, (0.0, -0.3, 0.95), (0.0, -0.3, 0.9), 30, 30, 3.6)})
# s3: extreme close-up: grille + badge, sliding across the nose
SHOTS["s3_grille"] = dict(base=CAR, seconds=2.2, camera={"keys": [
    {"t": 0, "loc": [0.95, 4.0, 1.05], "target": [0.05, 2.6, 0.88], "focal": 50},
    {"t": 2.2, "loc": [0.15, 4.0, 1.1], "target": [-0.05, 2.6, 0.9], "focal": 50, "ease": "inout"}]})
# s4: extreme close-up: right front wheel, push in
SHOTS["s4_wheel"] = dict(base=CAR, seconds=2.8, camera={"keys": [
    {"t": 0, "loc": [3.0, 3.2, 0.62], "target": [1.0, 1.75, 0.45], "focal": 40},
    {"t": 2.8, "loc": [2.6, 2.75, 0.55], "target": [1.0, 1.7, 0.45], "focal": 40, "ease": "inout"}]})
# s6: rise from high rear 3/4 to straight top-down while yawing
SHOTS["s6_top"] = dict(base=CAR, seconds=2.8, camera={"keys": [
    {"t": 0, "loc": [3.2, -4.4, 5.4], "target": [0, -0.2, 0.8], "focal": 30},
    {"t": 2.8, "loc": [0.0, -0.01, 7.6], "target": [0, 0, 0.8], "focal": 30, "ease": "inout"}]})

# s5: hood opens on the fitted hinge (37.2 deg = the captured open hood), camera eases in from front-right high
HOOD = {"blend": B + "/hood_part.blend", "pivot": [0.0609, 1.2197, 1.2671],
        "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": 0.65, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                 {"t": 2.6, "loc": [0, 0, 0], "rot": [37.19, 0, 0], "ease": "inout"}]}
SHOTS["s5_hood"] = dict(base=[B + "/base_hood.blend"], parts=[HOOD], seconds=5.4, camera={"keys": [
    {"t": 0, "loc": [4.0, 5.4, 2.3], "target": [0.0, 1.5, 1.0], "focal": 30},
    {"t": 5.4, "loc": [3.1, 4.9, 2.9], "target": [0.0, 1.3, 1.05], "focal": 30, "ease": "inout"}]})

# s7: exploded view - panels lift into layers ABOVE the car (portrait stacking, Temerario 25-31 s), hold while the
# camera orbits front-right -> right side, then fly home and lock. Times come from the music (EXPLODE_T).
EXPLODE_T = {"sep": 0.05, "out": 2.6, "back": 7.8, "lock": 10.4, "secs": 13.2}
def xpart(blend, off, rot=(0, 0, 0), stagger=0.0, pivot=None):
    T = EXPLODE_T; z = [0, 0, 0]
    d = {"blend": B + "/" + blend, "keys": [
        {"t": 0, "loc": z, "rot": z}, {"t": T["sep"] + stagger, "loc": z, "rot": z},
        {"t": T["out"] + stagger, "loc": list(off), "rot": list(rot), "ease": "out"},
        {"t": T["back"] - stagger * 0.5, "loc": [v * 1.06 for v in off], "rot": list(rot), "ease": "lin"},
        {"t": T["lock"] - stagger * 0.5, "loc": z, "rot": z, "ease": "in"}]}
    if pivot: d["pivot"] = pivot
    return d
XPARTS = [
    xpart("hood_part.blend", (0, 0.1, 1.45), (-10, 0, 0), 0.0),
    xpart("x_side_vents_3mm.blend", (0, 0.05, 0.95), (0, 0, 0), 0.08),
    xpart("x_fender_inner_3mm.blend", (0.35, 0.05, 0.85), (0, 0, 0), 0.16),
    xpart("x_front_bumper_duct_3mm.blend", (0.0, 0.5, 0.45), (0, 0, 0), 0.24),
    xpart("x_wing_3mm.blend", (0, -0.3, 0.7), (0, 0, 0), 0.32),
    xpart("x_exhaust_cover_3mm.blend", (0, -0.6, 0.3), (0, 0, 0), 0.40),
]
SHOTS["s7_explode"] = dict(base=[B + "/x_base_explode.blend"], parts=XPARTS,
    seconds=EXPLODE_T["secs"], camera={"keys": orbit((8.4, 8.8), 35, 68, 2.5, 2.3, (0.0, 0.2, 1.65), (0.0, 0.0, 1.6), 30, 30, EXPLODE_T["secs"])})

def write(name, check=False, pct=75):
    s = dict(SHOTS[name]); s.setdefault("fps", 15); s.setdefault("res", "1080x1920")
    s["res_pct"] = 30 if check else pct; s["samples"] = 8 if check else 12
    s["out"] = f"{M}/renders/{'check' if check else 'final'}/{name}"
    if check: s["frames"] = ["first", "mid", "last"]
    os.makedirs(M + "/specs", exist_ok=True); p = f"{M}/specs/{name}{'_check' if check else ''}.json"
    json.dump(s, open(p, "w"), indent=1); return p

if __name__ == "__main__":
    names = list(SHOTS) if sys.argv[1] == "all" else sys.argv[1].split(",")
    check = "--check" in sys.argv
    for n in names:
        p = write(n, check)
        if check:
            subprocess.run(["blender", "-b", "-P", TOOLS + "/shot.py", "--", p], capture_output=True)
            print("checked", n)
        else:
            print(p)
