"""Scan shot specs for the IS350 speed-run long-form -> JSON for projects/smart-450-hellkitten/tools/shot.py
(house silver look, camera keys, solved-camera start, state-swap visibility windows, transparent stills).

    python projects/lexus-is350-speedrun-long/tools/shots.py preview|final [shot ...]

Prepped frame (metres; scan-process level.py transform, prep --like car.json): nose = -Y, car's LEFT = +X,
right = -X, ground Z = 0, footprint 4.72 x 1.95 m, roof 1.43 m. Plates flattened (tools/deplate.py) before prep.
car = 4 mm (3.3M tris); car25 = 2.5 mm (7.7M) for close-ups; car25rr = car25 with the 'reflector removed' state
spliced in by surface distance (scan-process tools/splice.py, 8 mm); refl = reflector part scan.
Sequences render at 8 fps (+4 tail frames) for 3x minterpolate to 23.976; stills 3840x2160.
Shot ids/durations from edl.json / conclusion_edl.json (lead, 2026-11-13).
"""
import json
import math
import os
import sys

P = "/home/user/media/lexus-is350/prep"
W = "/home/user/media/work/is350-long"
SPECS = f"{W}/scan3d/specs"
MATCH = f"{W}/scan3d/match"
CAR, CAR25, CAR25RR = f"{P}/car.blend", f"{P}/car25.blend", f"{P}/car25rr.blend"
LIGHT = [[-0.975, -2.362, 0.0], [0.975, 2.362, 1.426]]
FPS = 8
TAIL = 4 / FPS
SENSOR = 35.6   # FX3A full frame (matched shots); free shots use the same sensor


def orbit(t, r, az, h, c=(0, 0, 0.6), focal=35, tz=None, ease="inout"):
    """az 0 = camera in front of the nose (-Y); 90 = car's LEFT (+X); -90 = right (-X); 180 = behind."""
    a = math.radians(az)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def solved(path, dist):
    c = json.load(open(path))
    R = c["blender"]["rotation_matrix"]; loc = c["blender"]["location"]
    fwd = [-R[i][2] for i in range(3)]
    tgt = [loc[i] + fwd[i] * dist for i in range(3)]
    return c, loc, fwd, tgt


def push_from(path, dist, amount, secs, drift=(0, 0, 0)):
    """Start exactly on the solved camera, then move `amount` of `dist` along its view axis (no lens shift here)."""
    c, loc, fwd, tgt = solved(path, dist)
    loc1 = [loc[i] + fwd[i] * dist * amount + drift[i] for i in range(3)]
    tgt1 = [tgt[i] + drift[i] for i in range(3)]
    return [{"t": 0, "cam": path, "dist": dist},
            {"t": secs, "loc": loc1, "target": tgt1, "focal": c["focal_mm"], "ease": "inout"}]


def shots():
    S = {}
    # --- 1:1 cuts (16:9, same 1920x1080 frame the solve used) ---
    S["SC_MATCH_REAR"] = {"base": [CAR], "dur": 4.5,
                          "keys": lambda s: push_from(f"{MATCH}/cam_rear_final.json", 2.3, 0.14, s)}
    S["SC_MATCH_FRONT"] = {"base": [CAR], "dur": 5.0,
                           "keys": lambda s: push_from(f"{MATCH}/cam_front.json", 4.2, 0.12, s)}
    # --- title: whole car, front-left 3/4, car in the upper two thirds (lower third clean for G01), slow push ---
    S["SC_TITLE"] = {"base": [CAR], "dur": 6.0, "keys": lambda s: [
        {"t": 0, "loc": [5.0, -6.3, 1.25], "target": [0.15, -0.2, 0.25], "focal": 42},
        {"t": s, "loc": [4.55, -5.75, 1.18], "target": [0.15, -0.2, 0.25], "focal": 42, "ease": "inout"}]}
    # --- result: full car from above-left, slow continuous dolly side -> front-left 3/4 (not a turntable); both right well and rear-left well are ragged, so the rear wheel stays far/small ---
    S["SC_RES_FULL"] = {"base": [CAR], "dur": 7.0, "keys": lambda s: [
        {"t": 0, "loc": [6.2, -1.2, 2.6], "target": [0.0, -0.2, 0.55], "focal": 40},
        {"t": s, "loc": [4.6, -4.6, 2.35], "target": [0.0, -0.45, 0.55], "focal": 40, "ease": "inout"}]}
    
    # --- result: mesh density: 4 mm mesh, dark 1.6 px wire edges, front-left bumper/fender edge diagonal, black lower-left (G11) ---
    S["SC_RES_MESH"] = {"base": [{"blend": CAR, "look": "wire"}], "dur": 5.0, "extra": {"wire_px": 1.6}, "keys": lambda s: [
        {"t": 0, "loc": [1.55, -2.35, 0.28], "target": [0.75, -2.25, 0.55], "focal": 70},
        {"t": s, "loc": [1.52, -2.15, 0.30], "target": [0.75, -2.15, 0.56], "focal": 70, "ease": "inout"}]}
    # --- result: rear-left lower corner, reflector in place -> removed (hard state swap), small drift, no push-in ---
    S["SC_RES_REFLECTOR"] = {"base": [{"blend": CAR25, "vis": [0, 3.0]}, {"blend": CAR25RR, "vis": [3.0, 99]}],
                             "dur": 7.0, "keys": lambda s: [
        {"t": 0, "loc": [1.75, 3.35, 0.85], "target": [0.62, 2.12, 0.45], "focal": 45},
        {"t": s, "loc": [1.55, 3.5, 0.82], "target": [0.6, 2.13, 0.45], "focal": 45, "ease": "inout"}]}
    # --- inserts ---
    S["SC_INS_ROOF"] = {"base": [CAR], "dur": 3.0, "keys": lambda s: [
        {"t": 0, "loc": [-2.6, 3.2, 2.55], "target": [0.0, 0.9, 1.15], "focal": 38},
        {"t": s, "loc": [-2.0, 3.6, 2.5], "target": [0.15, 1.0, 1.15], "focal": 38, "ease": "inout"}]}
    S["SC_INS_WHEEL"] = {"base": [CAR25], "dur": 3.0, "keys": lambda s: [
        {"t": 0, "loc": [2.55, -2.35, 0.62], "target": [0.85, -1.38, 0.36], "focal": 40},
        {"t": s, "loc": [2.5, -1.9, 0.6], "target": [0.85, -1.33, 0.36], "focal": 40, "ease": "inout"}]}
    S["SC_INS_SILL"] = {"base": [CAR], "dur": 3.0, "keys": lambda s: [
        {"t": 0, "loc": [-2.2, -1.3, 0.22], "target": [-0.9, 0.2, 0.25], "focal": 32},
        {"t": s, "loc": [-2.15, -0.8, 0.2], "target": [-0.9, 0.6, 0.25], "focal": 32, "ease": "inout"}]}
    # --- v2 end-montage pairs: frame 1 = the solved IRL frame (full 1920x1080, Rec709), then a slow push along the view axis ---
    S["SC_PAIR_2"] = {"base": [CAR], "dur": 2.75,
                      "keys": lambda s: push_from(f"{MATCH}/cam_541_fiti.json", 2.4, 0.10, s)}
    S["SC_PAIR_3"] = {"base": [CAR], "dur": 2.5,
                      "keys": lambda s: push_from(f"{MATCH}/cam_542_fit.json", 2.4, 0.10, s)}
    # --- conclusion hero: one slow continuous pull-back from the front-LEFT 3/4 (front-right well is ragged), lower-left band clear ---
    S["SC_CON_HERO"] = {"base": [CAR], "dur": 8.0, "keys": lambda s: [  # v2: 8.0 s of the planned 11.76 s
        {"t": 0, "loc": [3.7, -4.6, 1.0], "target": [0.2, -0.6, 0.45], "focal": 40},
        {"t": s, "loc": [5.0, -6.4, 1.3], "target": [0.05, -0.3, 0.4], "focal": 40, "ease": "out2"}]}
    return S


STILLS = {
    "B5_front34_hero": [{"t": 0, "loc": [4.4, -5.0, 1.05], "target": [0.1, -0.35, 0.5], "focal": 45}],
    "B5_side_profile": [{"t": 0, "loc": [8.6, 0.0, 0.85], "target": [0.0, 0.0, 0.62], "focal": 55}],
    "B5_halfhalf_FX30554": [{"t": 0, "cam": f"{MATCH}/cam_front.json", "dist": 4.2}],
}


def main():
    mode = sys.argv[1]
    want = sys.argv[2:]
    os.makedirs(SPECS, exist_ok=True)
    out = []
    for n, d in shots().items():
        if want and n not in want:
            continue
        secs = d["dur"] + TAIL
        s = {"base": d["base"], "light_bbox": LIGHT, "camera": {"sensor": SENSOR, "keys": d["keys"](secs)},
             "seconds": secs, "fps": FPS, "res": "1920x1080", "edl_dur": d["dur"], **d.get("extra", {})}
        if mode == "preview":
            s.update({"res_pct": 30, "samples": 4, "frames": ["first", "mid", "last"], "out": f"{W}/scan3d/look/pv_{n}/"})
            if n == "SC_RES_REFLECTOR":
                s["frames"] = ["first", 24, 25, "last"]
        else:
            s.update({"res_pct": 75, "samples": 8, "out": f"{W}/renders/{n}/png/"})
        p = f"{SPECS}/{n}_{mode}.json"; json.dump(s, open(p, "w"), indent=1); out.append(p)
    for n, keys in STILLS.items():
        if want and n not in want:
            continue
        s = {"base": [CAR25], "light_bbox": LIGHT, "camera": {"sensor": SENSOR, "keys": keys}, "seconds": 0,
             "res": "3840x2160", "transparent": True}
        if mode == "preview":
            s.update({"res_pct": 15, "samples": 4, "out": f"{W}/scan3d/look/pv_{n}.png"})
        else:
            s.update({"res_pct": 100, "samples": 24, "out": f"{W}/renders/B5_stills/{n}_alpha.png"})
        p = f"{SPECS}/{n}_{mode}.json"; json.dump(s, open(p, "w"), indent=1); out.append(p)
    print("\n".join(out))


if __name__ == "__main__":
    main()
