"""Shot specs for the Sentra promo (v1). All key times are ABSOLUTE video seconds (timing.json); each spec subtracts
its segment start. Writes <work>/shots/<seg>.json for tools/shot.py.

Segments:  main 4.333-37.1 (one continuous camera, cut 1:1 from IMG_3229 @ 4.3 s)
           brake 37.1-41.23 (hub close-up)   final 41.23-43.43 (finished build orbit)
    python projects/nissan-sentra-promo/tools/shots.py [--pct 75] [--samples 12]
"""
import argparse, copy, json, os

W = "/home/user/media/work/sentra"
C = W + "/cad/"
ap = argparse.ArgumentParser(); ap.add_argument("--pct", type=int, default=75); ap.add_argument("--samples", type=int, default=12)
ap.add_argument("--fps", type=int, default=15)
A = ap.parse_args()

CUT = 4.3333  # first scan frame (frame 130 at 30 fps)
END_MAIN = 37.1
CUTCAM = {"loc": [1.25, -3.05, 0.9], "target": [0.69, -1.865, 0.70], "focal": 26}  # hand-matched onion on IMG_3229 @ 4.3 s


def K(t, loc, target, focal, ease="inout"):
    return {"t": t, "loc": loc, "target": target, "focal": focal, "ease": ease}


def drop(t0, t1, start, rot0=(0, 0, 0), bounce=0.012):
    """part keys: parked at `start` offset until t0, eases home by t1 with a small settle bounce along the move."""
    s = [v for v in start]
    n = sum(v * v for v in s) ** 0.5 or 1
    ov = [-v / n * bounce for v in s]
    return [{"t": 0, "loc": s, "rot": list(rot0)}, {"t": t0, "loc": s, "rot": list(rot0)},
            {"t": t1, "loc": ov, "rot": [0, 0, 0], "ease": "in2"},
            {"t": t1 + 0.14, "loc": [-v * 0.4 for v in ov], "rot": [0, 0, 0], "ease": "out"},
            {"t": t1 + 0.3, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "inout"}]


def mirror(keys):
    k = copy.deepcopy(keys)
    for x in k:
        x["loc"][0] = -x["loc"][0]
        x["rot"] = [x["rot"][0], -x["rot"][1], -x["rot"][2]]
    return k


# ---------------- main continuous camera (absolute times) ----------------
cam = [
    K(CUT, CUTCAM["loc"], CUTCAM["target"], 26),
    K(6.9, [1.85, -4.05, 1.15], [0.30, -1.85, 0.55], 26),            # bumper alone in the void
    K(11.6, [2.45, -4.85, 1.35], [0.15, -1.55, 0.55], 26),           # slow drift while the scan line passes
    K(12.9, [4.3, -5.9, 1.75], [0.0, 0.15, 0.55], 28),               # whole car front 3/4 as it builds
    K(15.0, [5.0, 4.9, 1.6], [0.0, 0.75, 0.55], 28),                 # orbit to rear 3/4 (driver side) while it builds
    K(15.5, [3.4, 3.0, 1.05], [0.75, 1.0, 0.70], 30),               # glide along the driver side: body lines
    K(16.95, [3.4, -0.9, 1.05], [0.75, -1.3, 0.70], 30, "lin"),
    K(17.55, [1.55, -2.55, 1.20], [0.60, -1.55, 0.78], 42),          # close on the hood / fender / headlight shut lines
    K(18.55, [1.42, -2.40, 1.14], [0.60, -1.55, 0.78], 46, "lin"),
    K(19.2, [1.05, -3.05, 2.45], [0.0, -1.35, 0.55], 28),            # look down into the bay as the scan line passes
    K(21.4, [0.85, -2.95, 2.50], [0.0, -1.35, 0.55], 28, "lin"),
    K(22.0, [0.85, -4.45, 1.20], [0.05, -2.35, 0.85], 35),           # fog lamps arrive in front of the nose
    K(23.2, [0.75, -4.35, 1.18], [0.05, -2.35, 0.85], 35, "lin"),
    K(25.0, [4.3, -5.6, 1.75], [0.0, 0.10, 0.55], 28),               # pull back: "now we design on top of it"
    K(25.6, [3.1, -4.9, 1.30], [0.15, -1.25, 0.55], 28),             # front 3/4 for the bumper
    K(26.95, [2.7, -4.6, 1.20], [0.25, -1.45, 0.50], 28, "lin"),
    K(27.4, [1.75, -3.55, 0.78], [0.70, -1.80, 0.40], 30),           # driver corner close: fog ducts
    K(28.85, [1.60, -3.40, 0.74], [0.70, -1.80, 0.40], 30, "lin"),
    K(29.4, [3.3, -3.9, 2.3], [0.15, -0.85, 0.60], 28),              # up and back: fenders + hood
    K(31.1, [3.6, -3.4, 2.2], [0.15, -0.75, 0.60], 28, "lin"),
    K(31.7, [4.4, -0.4, 0.55], [0.5, 0.25, 0.32], 26),               # low side: skirts
    K(32.75, [4.4, 0.6, 0.55], [0.5, 0.45, 0.32], 26, "lin"),
    K(33.25, [3.5, 5.4, 1.35], [0.3, 1.6, 0.60], 28),                # rear 3/4: quarter panels
    K(34.35, [3.2, 5.6, 1.30], [0.3, 1.7, 0.60], 28, "lin"),
    K(34.85, [1.7, 5.9, 0.55], [0.0, 2.4, 0.38], 28),                # low rear: diffuser
    K(35.65, [1.6, 5.9, 0.60], [0.0, 2.4, 0.40], 28, "lin"),
    K(36.15, [1.9, 5.5, 2.05], [0.0, 2.25, 0.90], 28),               # high rear: wing adapter
    K(END_MAIN + 0.4, [1.7, 5.4, 2.10], [0.0, 2.25, 0.92], 28, "lin"),
]

# ---------------- parts ----------------
parts = []
# A: the SEMA bumper drops into the void where the real one sat, turns, lifts away as the scan line passes
parts.append({"name": "bumperA", "blend": C + "Uncut_Front_Bumper.blend", "show": [CUT + 0.1, 12.6],
              "keys": [{"t": 0, "loc": [0, 0, 1.1], "rot": [0, 0, 0]}, {"t": 4.45, "loc": [0, 0, 1.1], "rot": [0, 0, 0]},
                       {"t": 5.0, "loc": [0, 0, -0.014], "rot": [0, 0, 0], "ease": "in2"},
                       {"t": 5.14, "loc": [0, 0, 0.006], "rot": [0, 0, 0], "ease": "out"},
                       {"t": 5.3, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                       {"t": 7.0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                       {"t": 9.3, "loc": [0, 0, 0.18], "rot": [0, 0, 28]},          # turns with nothing around it
                       {"t": 10.6, "loc": [0, 0, 0.18], "rot": [0, 0, 28]},
                       {"t": 12.2, "loc": [0, 0, 2.2], "rot": [0, 0, 28], "ease": "in"}]})
# H: stock bumper (loose scan) slides forward and drops away, the SEMA bumper comes in
parts.append({"name": "bumper_stock", "blend": W + "/bumper_stock.blend", "show": [25.5, 26.9],
              "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": 25.55, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                       {"t": 25.95, "loc": [0, -0.55, 0], "rot": [0, 0, 0], "ease": "in2"},
                       {"t": 26.6, "loc": [0, -0.95, -1.4], "rot": [-12, 0, 0], "ease": "in"}]})
parts.append({"name": "bumper", "blend": C + "Uncut_Front_Bumper.blend", "show": [25.95, 99],
              "keys": drop(26.0, 26.55, [0, -1.25, -0.08])})
# F/I: fog lamps fly in, park in front of the nose (above the bumper path), then seat behind the insert frames
fog_park1 = [-0.40, -0.85, 0.62]   # offset from home (home ~ x 0.84, y -1.73, z 0.35)
parts.append({"name": "fog1", "blend": W + "/fog1_home.blend", "show": [21.6, 99],
              "keys": [{"t": 0, "loc": [1.6, -1.6, 1.6], "rot": [0, 0, 0]}, {"t": 21.75, "loc": [1.6, -1.6, 1.6], "rot": [0, 0, 0]},
                       {"t": 22.35, "loc": fog_park1, "rot": [0, 0, 0], "ease": "out2"},
                       {"t": 27.05, "loc": fog_park1, "rot": [0, 0, 0]},
                       {"t": 27.35, "loc": [0, -0.35, 0], "rot": [0, 0, 0], "ease": "inout"},
                       {"t": 27.6, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "out"}]})
fog_park2 = [0.40, -0.85, 0.62]
parts.append({"name": "fog2", "blend": W + "/fog2_home.blend", "show": [21.6, 99],
              "keys": [{"t": 0, "loc": [1.0, -1.9, 1.9], "rot": [0, 0, 0]}, {"t": 21.95, "loc": [1.0, -1.9, 1.9], "rot": [0, 0, 0]},
                       {"t": 22.6, "loc": fog_park2, "rot": [0, 0, 0], "ease": "out2"},
                       {"t": 27.1, "loc": fog_park2, "rot": [0, 0, 0]},
                       {"t": 27.4, "loc": [0, -0.35, 0], "rot": [0, 0, 0], "ease": "inout"},
                       {"t": 27.65, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "out"}]})
# I: fog/duct inserts click into the bumper corners from the front
ins = drop(27.75, 28.2, [0.12, -0.45, 0.0], bounce=0.006)
parts.append({"name": "insD", "blend": C + "Uncut_Front_Bumper_Side_Driver.blend", "show": [27.6, 99], "keys": ins})
parts.append({"name": "insP", "blend": C + "Uncut_Front_Bumper_Side_Passenger.blend", "show": [27.6, 99], "keys": mirror(ins)})
# J: fenders from outboard, hood ducts drop onto the hood
fen = drop(29.0, 29.65, [0.75, 0, 0.35])
parts.append({"name": "fenD", "blend": C + "Uncut_Front_Fender.Driver.blend", "show": [28.9, 99], "keys": fen})
parts.append({"name": "fenP", "blend": C + "Uncut_Front_Fender.Passenger.blend", "show": [28.9, 99], "keys": mirror(fen)})
for i, (nm, dt) in enumerate([("Uncut_Hood_Duct.Driver", 0.0), ("Uncut_Hood_Duct.Centre", 0.12), ("Uncut_Hood_Duct.Passenger", 0.24)]):
    parts.append({"name": nm, "blend": C + nm + ".blend", "show": [29.3, 99], "keys": drop(29.45 + dt, 30.0 + dt, [0, 0, 0.75])})
# K: side skirts from below/outboard.  Uncut_Side_Skirts.Driver sits at -x (file naming), .Passenger at +x
sk = drop(31.45, 32.0, [0.45, 0, -0.35])
parts.append({"name": "skirtP_file", "blend": C + "Uncut_Side_Skirts.Passenger.blend", "show": [31.3, 99], "keys": sk})
parts.append({"name": "skirtD_file", "blend": C + "Uncut_Side_Skirts.Driver.blend", "show": [31.3, 99], "keys": mirror(sk)})
# L: rear quarter panels: rear door skin, rear fender, rear bumper side, from outboard in quick succession
for j, nm in enumerate(["Rear_Door", "Rear_Fender", "Rear_Bumper"]):
    k = drop(33.0 + 0.18 * j, 33.55 + 0.18 * j, [0.7, 0.15 * (j - 1), 0.12])
    parts.append({"name": nm + "D", "blend": C + f"Uncut_{nm}.Driver.blend", "show": [32.8, 99], "keys": k})
    parts.append({"name": nm + "P", "blend": C + f"Uncut_{nm}.Passenger.blend", "show": [32.8, 99], "keys": mirror(k)})
# M: diffuser comes up under the rear
parts.append({"name": "diffuser", "blend": C + "Uncut_Rear_Diffuser.blend", "show": [34.4, 99], "keys": drop(34.6, 35.2, [0, 0.35, -0.55])})
# N: wing adapter drops onto the trunk with a small bounce
parts.append({"name": "wing", "blend": C + "Uncut_Wing_Adapter.blend", "show": [35.7, 99], "keys": drop(35.85, 36.4, [0, 0, 0.8], bounce=0.02)})

reveals = {
    "build": {"axis": "z", "keep": "below", "band": 0.025, "strength": 9,
              "keys": [{"t": 0, "v": -0.06}, {"t": 12.25, "v": -0.06}, {"t": 14.75, "v": 1.45, "ease": "inout"}]},
    "sweep_car": {"axis": "y", "keep": "above", "band": 0.02, "strength": 9,
                  "keys": [{"t": 0, "v": -2.2}, {"t": 18.75, "v": -2.2}, {"t": 20.55, "v": -0.78, "ease": "inout"},
                           {"t": 23.45, "v": -0.78}, {"t": 24.45, "v": -2.2, "ease": "inout"}]},
}
reveals["sweep_bay"] = dict(copy.deepcopy(reveals["sweep_car"]), keep="below")
# scan "gantry": a thin laser line on the floor and one at roof height, sweeping front to back through the void
lines = [{"size": [2.6, 0.008, 0.008], "color": [0.35, 0.8, 1.0], "strength": 40, "show": [9.3, 11.7],
          "keys": [{"t": 0, "loc": [0, -2.75, z]}, {"t": 9.35, "loc": [0, -2.75, z]}, {"t": 11.6, "loc": [0, 0.6, z], "ease": "inout"}]}
         for z in (-0.03, 1.45)]
base = [{"blend": W + "/car.blend", "show": [12.0, 25.55], "rv": ["build", "sweep_car"]},
        {"blend": W + "/bay_s.blend", "show": [18.6, 24.6], "rv": ["sweep_bay"]},
        {"blend": W + "/car_nobump.blend", "show": [25.55, 99]},
        {"blend": W + "/front_fill.blend", "show": [25.55, 99]}]


def shift(obj, t0):
    """deep-copy with every absolute time t -> t - t0 (keys and show windows)."""
    o = copy.deepcopy(obj)
    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == "t" and isinstance(v, (int, float)):
                    x[k] = v - t0
                elif k == "show":
                    x[k] = [v[0] - t0, v[1] - t0]
                else:
                    walk(v)
        elif isinstance(x, list):
            for y in x:
                walk(y)
    walk(o)
    return o


def spec(name, t0, t1, base_, parts_, cam_, reveals_=None, lines_=None, extra=None):
    s = {"base": shift(base_, t0), "parts": shift(parts_, t0), "camera": {"keys": shift(cam_, t0)},
         "seconds": t1 - t0, "fps": A.fps, "res_pct": A.pct, "samples": A.samples, "persistent": False,
         "exposure": -0.8, "out": f"{W}/render/{name}"}
    if reveals_: s["reveals"] = shift(reveals_, t0)
    if lines_: s["lines"] = shift(lines_, t0)
    if extra: s.update(extra)
    os.makedirs(W + "/shots", exist_ok=True)
    json.dump(s, open(f"{W}/shots/{name}.json", "w"), indent=1)
    print(name, round(t1 - t0, 3), "s", int(round((t1 - t0) * A.fps)), "frames")


# render 0.25 s past each segment end (minterpolate eats the tail - lessons)
spec("main", CUT, END_MAIN + 0.25, base, parts, cam, reveals, lines)

# ---------------- brake close-up (hub as captured on the lift, its own scene) ----------------
B = W + "/brake/"
bt0, bt1 = 37.1, 41.23
brake_parts = [
    {"name": "testfit", "blend": C + "Sentra_Front_Right.blend", "show": [0, 39.25],
     "keys": [{"t": 0, "loc": [-0.05, -0.45, 0.02], "rot": [0, 0, 0]}, {"t": 37.35, "loc": [-0.05, -0.45, 0.02], "rot": [0, 0, 0]},
              {"t": 38.05, "loc": [-0.012, 0, 0], "rot": [0, 0, 0], "ease": "in2"}, {"t": 38.2, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "out"}]},
    {"name": "v3", "blend": C + "Sentra_Front_Right_Brake_Adapter_V3.blend", "show": [39.25, 39.95]},
    {"name": "v4", "blend": C + "Sentra_Front_Right_Brake_Adapter_V4.blend", "show": [39.95, 99]},
]
# hub + rotor are the scene; the caliper (scan) comes on last, once V4 is in
brake_base = [{"blend": B + "Senta_SR_FR_Hub.blend"}]
# rotor goes on after V4 (it hides the adapter once seated), then the caliper bolts to the adapter
brake_parts.append({"name": "rotor", "blend": B + "Senta_SR_Front_Rotor.blend", "show": [40.15, 99],
                    "keys": drop(40.2, 40.6, [-0.32, 0, 0.0], bounce=0.004)})
brake_parts.append({"name": "caliper", "blend": B + "Senta_SR_Front_Caliper.blend", "show": [40.4, 99],
                    "keys": drop(40.45, 40.9, [-0.05, -0.45, 0.05])})
brake_cam = [K(bt0, [-1.30, -2.15, 0.42], [-0.72, -1.16, 0.19], 38), K(bt1 + 0.3, [-1.15, -2.05, 0.38], [-0.72, -1.16, 0.19], 42, "lin")]
spec("brake", bt0, bt1 + 0.25, brake_base, brake_parts, brake_cam)

# ---------------- finished build orbit ----------------
ft0, ft1 = 41.23, 43.43
fin_parts = [{"name": p["name"], "blend": p["blend"]} for p in parts if p["name"] not in ("bumperA", "bumper_stock")]
fin_base = [{"blend": W + "/car_nobump.blend"}, {"blend": W + "/front_fill.blend"}]
fin_cam = [K(ft0, [3.6, -4.7, 1.35], [0.0, 0.0, 0.62], 28), K(ft1 + 0.3, [4.9, -2.6, 1.25], [0.0, 0.1, 0.62], 28, "lin")]
spec("final", ft0, ft1 + 0.25, fin_base, fin_parts, fin_cam)
