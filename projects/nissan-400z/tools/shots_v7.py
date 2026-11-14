"""Nissan 400Z Temerario reel v7 shot specs (v6 + user 2026-11-14: stance dropped like the real car - body -80 mm onto the
new wheels right after the wheel swap; stock bumper/body trimmed where it poked through the Bomex pieces, staged so each
area is trimmed on the frame its kit piece seats - tools/trim_stock.py, 45 mm ray test).
(v6: (v5 + user 2026-11-14: the Bomex front bumper goes OVER the stock bumper -
stock nose/grilles stay; Bomex mirrors (Mirror/V1 shell + glass backing); stand-in deep-dish mesh wheels swapped 1:1 on a kick) -> JSON for tools/shot.py.
Adds the stock parts v2-v4 skipped (grilles, air ducting, crash-foam state, real mirror scans), the Bomex x Kaido House
body kit (Ron's folder, registered to the scan), and the livery (400z-full.psd projected on the kitted car).
Order and timing: projects/nissan-400z/direction_v5.md; cut frames measured on the decoded kicks (see CUTS).
    python projects/nissan-400z/tools/shots_v7.py preview|final [shot ...]
Prepped frame (m): nose -Y, car's right -X, ground z=0. Kit parts carry keys {t, loc, rot, ease} about the bbox centre."""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/home/user/media/work/z400/blend"
OUT = "/home/user/media/work/z400/renders"
SPECS = "/home/user/media/work/z400/specs"
LIVMAP = json.load(open(os.path.join(HERE, "..", "livery_map.json")))
LIV = {"tex": "/home/user/media/nissan-400z/livery/tex", "map": LIVMAP, "hood": [-0.07, -0.85, 0.75, 0.37],
       "paint": [0.10, 0.10, 0.105], "belt": 0.97, "banner": [-0.07, 1.05, 1.135, 0.125, -0.75, 0.05], "glass_nz": 0.95, "xc": -0.07,
       "cabin": [-0.75, 1.05, 0.80, 1.19, 0.66]}
LIV7 = {**LIV, "map": {**LIVMAP, "Z0": LIVMAP["Z0"] + DROP}, "belt": LIV["belt"] + DROP,
        "banner": LIV["banner"][:2] + [LIV["banner"][2] + DROP] + LIV["banner"][3:],
        "cabin": LIV["cabin"][:2] + [LIV["cabin"][2] + DROP, LIV["cabin"][3] + DROP] + LIV["cabin"][4:]}  # world-space wrap follows the body
KIT = ["front_bumper", "canard_driver", "canard_pass", "front_fender_driver", "front_fender_pass",
       "front_fender_slats_driver", "front_fender_slats_pass", "side_skirts_driver", "side_skirts_pass",
       "rear_fender_driver", "rear_fender_pass", "rear_fender_slats_driver", "rear_fender_slats_pass",
       "gas_cap_x", "ducktail", "diffuser"]
FPS30 = {"STRUCT", "BUMPER", "MIRRORS", "KIT_FRONT", "KIT_SIDE", "REAR"}  # part motion -> native 30 fps (no minterpolate)

# measured cut frames @30: see direction_v5 / onset check
SECS = {"STRUCT": (505, 702), "BUMPER": (702, 787), "MIRRORS": (787, 871), "KIT_FRONT": (871, 984),
        "KIT_SIDE": (984, 1096), "REAR": (1096, 1209), "LIVERY": (1209, 1321), "HERO": (1321, 1377)}


def dur(name):
    a, b = SECS[name]
    return (b - a) / 30.0


def k(t, loc, rot=(0, 0, 0), ease="inout"):
    return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}


def held(blend):
    return {"blend": blend, "keys": [k(0, (0, 0, 0))]}


def cam(keys):
    return keys


def orbit(t, az, el, r, c, focal, ease="inout"):
    a = math.radians(az); e = math.radians(el)
    return {"t": t, "loc": [c[0] + r * math.cos(e) * math.sin(a), c[1] - r * math.cos(e) * math.cos(a), c[2] + r * math.sin(e)],
            "target": list(c), "focal": focal, "ease": ease}


def arc(secs, a0, a1, el0, el1, r0, r1, c0, c1, focal, n=8):
    ks = []
    for i in range(n + 1):
        u = i / n
        c = [p + (q - p) * u for p, q in zip(c0, c1)]
        ks.append(orbit(secs * u, a0 + (a1 - a0) * u, el0 + (el1 - el0) * u, r0 + (r1 - r0) * u, c, focal, "lin"))
    return ks


SHOTS = {}
DROP = -0.08  # m: kit arch lips sat 87-102 mm over the tyres; the built car tucks to ~10-20 mm
BBS = [{"blend": f"{B}/bbs_{w}.blend", "keep_mats": True, "ground": True} for w in ("fl", "fr", "rl", "rr")]  # stand-in wheels (tools/make_bbs.py)
STOCKW = {"blend": f"{B}/stock_wheels.blend"}

# 4. STRUCT: ducting off, swap to crash-foam-removed state
d = dur("STRUCT"); t_duct, t_swap = 18.718 - 16.843, 21.531 - 16.843
SHOTS["STRUCT"] = {
    "base": [{"blend": f"{B}/bhr2_noduct.blend"}],
    "swap": {"t": t_swap, "blend": f"{B}/foam_noduct.blend"},  # hard 1:1 state swap
    "parts": [{"blend": f"{B}/Air_Ducting_2mm.blend",
               "keys": [k(0, (0, 0, 0)), k(t_duct - 0.4, (0, 0, 0)), k(t_duct, (0, -0.18, 0.05), ease="out"),
                        k(t_duct + 1.0, (0, -0.22, 0.95), ease="in"), k(d, (0, -0.22, 0.95))]}],
    "cam": cam([{"t": 0, "loc": [-1.9, -4.6, 1.3], "target": [-0.30, -1.75, 0.75], "focal": 52},
                {"t": d, "loc": [-0.7, -4.4, 1.15], "target": [-0.20, -1.8, 0.75], "focal": 45, "ease": "inout"}])}

# 5. BUMPER: bumper shell alone, upper+lower grille out
d = dur("BUMPER"); tu, tl = 24.343 - 23.406, 24.812 - 23.406
SHOTS["BUMPER"] = {
    "base": [{"blend": f"{B}/car.blend", "hide": True}],  # car hidden; only a light reference
    "show": [f"{B}/bumper_shell_v5.blend"],
    "parts": [{"blend": f"{B}/Upper_Grille_2mm.blend",
               "keys": [k(0, (0, 0, 0)), k(tu, (0, 0, 0)), k(tu + 0.5, (0, -0.14, 0.04), ease="out"), k(tu + 1.1, (0, -0.16, 0.34), ease="in"), k(d, (0, -0.16, 0.34))]},
              {"blend": f"{B}/Lower_Grille_2mm.blend",
               "keys": [k(0, (0, 0, 0)), k(tl, (0, 0, 0)), k(tl + 0.5, (0, -0.14, -0.04), ease="out"), k(tl + 1.1, (0, -0.16, -0.28), ease="in"), k(d, (0, -0.16, -0.28))]}],
    "cam": cam([orbit(0, -30, 15, 3.9, [-0.08, -1.80, 0.45], 60), orbit(d, -24, 18, 3.6, [-0.08, -1.82, 0.47], 60)])}

# 6. MIRRORS: both real mirror scans off, hold on the mounts
d = dur("MIRRORS"); tm = 27.156 - 26.218
SHOTS["MIRRORS"] = {
    "base": [{"blend": f"{B}/comp_explode.blend"}, held(f"{B}/p_wing.blend")],
    "parts": [{"blend": f"{B}/mirror_r_scan.blend", "pivot": [-0.84, -0.44, 1.0],
               "keys": [k(0, (0, 0, 0)), k(tm, (0, 0, 0)), k(tm + 0.45, (-0.15, 0, 0.05), ease="out"), k(tm + 0.9, (-0.17, 0, 0.35), ease="in"), k(d, (-0.17, 0, 0.35))]},
              {"blend": f"{B}/mirror_l_scan.blend", "pivot": [0.84, -0.44, 1.0],
               "keys": [k(0, (0, 0, 0)), k(tm, (0, 0, 0)), k(tm + 0.45, (0.15, 0, 0.05), ease="out"), k(tm + 0.9, (0.17, 0, 0.35), ease="in"), k(d, (0.17, 0, 0.35))]}],
    "cam": cam([orbit(0, -8, 30, 3.6, [-0.06, -0.25, 0.98], 46), orbit(d, -14, 30, 3.75, [-0.06, -0.25, 0.98], 46)])}


def kit(blend, stage, t0, via=None):
    """Install move: part sits staged (out of the body) until t0, then seats home by t0+0.6 via an outboard clearance key."""
    keys = [k(0, stage), k(t0, stage, ease="out")]
    if via:
        keys.append(k(t0 + 0.35, via, ease="lin"))
    keys.append(k(t0 + 0.6, (0, 0, 0), ease="in"))
    return {"blend": blend, "keys": keys}


# 7. KIT_FRONT: front kit installs onto the stripped front
d = dur("KIT_FRONT"); base0 = 29.031
def rel(t): return t - base0
SHOTS["KIT_FRONT"] = {
    # v6: stock bumper + grilles stay on (kb6 = full car minus stock mirrors and wheels); the Bomex front is a surround over it
    "base": [{"blend": f"{B}/kb6_wing.blend", "hide_at": rel(29.968) + 0.6},
             {"blend": f"{B}/kb7F_wing.blend", "show_at": rel(29.968) + 0.6, "hide_at": rel(30.906) + 0.6},  # fenders seated
             {"blend": f"{B}/kb7B_wing.blend", "show_at": rel(30.906) + 0.6},                                 # bumper seated
             held(f"{B}/p_wing.blend"), STOCKW],
    "parts": [
        kit(f"{B}/k_front_fender_driver.blend", (0.15, 0, 0.45), rel(29.968), (0.08, 0, 0)),
        kit(f"{B}/k_front_fender_pass.blend", (-0.15, 0, 0.45), rel(29.968), (-0.08, 0, 0)),
        kit(f"{B}/k_front_fender_slats_driver.blend", (0.15, 0, 0.85), rel(30.437), (0.08, 0, 0)),
        kit(f"{B}/k_front_fender_slats_pass.blend", (-0.15, 0, 0.85), rel(30.437), (-0.08, 0, 0)),
        kit(f"{B}/k_front_bumper.blend", (0, -0.7, 0), rel(30.906), (0, -0.15, 0)),
        kit(f"{B}/k_canard_driver.blend", (0.25, -0.5, 0), rel(31.375)),
        kit(f"{B}/k_canard_pass.blend", (-0.25, -0.5, 0), rel(31.375)),
        kit(f"{B}/k_mirror_driver.blend", (0.30, 0, 0.12), rel(31.843), (0.08, 0, 0)),   # Bomex mirrors onto the bare mounts
        kit(f"{B}/k_mirror_pass.blend", (-0.30, 0, 0.12), rel(31.843), (-0.08, 0, 0))],
    "cam": cam([{"t": 0, "loc": [0.0, -5.6, 1.1], "target": [0, -1.5, 0.6], "focal": 39},
                {"t": d, "loc": [-2.9, -4.9, 1.25], "target": [-0.1, -0.9, 0.55], "focal": 40, "ease": "inout"}])}

FRONT_HELD = [held(f"{B}/k_{n}.blend") for n in ("front_fender_driver", "front_fender_pass", "front_fender_slats_driver",
              "front_fender_slats_pass", "front_bumper", "canard_driver", "canard_pass", "mirror_driver", "mirror_pass")]

# 8. KIT_SIDE: passenger side, skirts/rear fenders/slats/gas cap install
d = dur("KIT_SIDE")
SHOTS["KIT_SIDE"] = {
    "base": [{"blend": f"{B}/kb7B_wing.blend", "hide_at": 34.187 + 0.6 - 32.781},
             {"blend": f"{B}/kb7_wing.blend", "show_at": 34.187 + 0.6 - 32.781},  # skirts seated: side/rear trim
             held(f"{B}/p_wing.blend")] + FRONT_HELD +
            [{**STOCKW, "hide_at": 34.656 - 32.781}] + [{**w, "show_at": 34.656 - 32.781} for w in BBS],  # 1:1 wheel swap on the kick
    "parts": [
        kit(f"{B}/k_rear_fender_pass.blend", (-0.45, 0, 0.25), rel(33.718) + base0 - 32.781, (-0.08, 0, 0)),
        kit(f"{B}/k_rear_fender_driver.blend", (0.45, 0, 0.25), rel(33.718) + base0 - 32.781, (0.08, 0, 0)),
        kit(f"{B}/k_side_skirts_pass.blend", (-0.45, 0, -0.05), 34.187 - 32.781, (-0.08, 0, 0)),
        kit(f"{B}/k_side_skirts_driver.blend", (0.45, 0, -0.05), 34.187 - 32.781, (0.08, 0, 0)),
        kit(f"{B}/k_rear_fender_slats_pass.blend", (-0.75, 0, 0.35), 34.42 - 32.781, (-0.08, 0, 0)),
        kit(f"{B}/k_rear_fender_slats_driver.blend", (0.75, 0, 0.35), 34.42 - 32.781, (0.08, 0, 0)),
        kit(f"{B}/k_gas_cap_x.blend", (-0.35, 0, 0.15), 35.125 - 32.781)],
    "body_drop": [[0, 0.0], [34.656 - 32.781 + 0.12, 0.0], [34.656 - 32.781 + 0.55, DROP]],  # drops onto the new wheels
    "cam": cam(arc(d, -62, -120, 8, 9, 6.6, 5.9, [-0.25, 0.25, 0.55], [-0.2, 0.5, 0.6], 36, n=6))}

SIDE_HELD = FRONT_HELD + [held(f"{B}/k_{n}.blend") for n in ("rear_fender_driver", "rear_fender_pass",
            "side_skirts_driver", "side_skirts_pass", "rear_fender_slats_driver", "rear_fender_slats_pass", "gas_cap_x")] + BBS

# 9. REAR: stock wing off, ducktail + diffuser on
d = dur("REAR")
SHOTS["REAR"] = {
    "base": [{"blend": f"{B}/kb7_wing.blend"}] + SIDE_HELD,
    "body_drop": [[0, DROP]],
    "parts": [
        {"blend": f"{B}/p_wing.blend", "keys": [k(0, (0, 0, 0)), k(0.3, (0, 0, 0)), k(0.75, (0, 0, 0.15), ease="out"), k(1.4, (0, 0.2, 0.6), ease="in"), k(d, (0, 0.2, 0.6))]},
        kit(f"{B}/k_ducktail.blend", (0, 0.1, 0.35), 38.406 - 36.531, (0, 0, 0.08)),
        kit(f"{B}/k_diffuser.blend", (0, 0.45, 0), 38.875 - 36.531, (0, 0.1, 0))],
    "cam": cam(arc(d, -150, -180, 20, 20, 5.3, 4.6, [0.1, 1.4, 0.65], [0, 1.45, 0.65], 46, n=6))}

# 10. LIVERY: full kitted car, livery sweep (camera + material only)
d = dur("LIVERY")
SHOTS["LIVERY"] = {
    "base": [{"blend": f"{B}/kb7_nowing.blend"}] + [{"blend": f"{B}/k_{n}.blend"} for n in KIT + ["mirror_driver", "mirror_pass"]] + BBS,
    "body_drop": [[0, DROP]],
    "livery": {**LIV7, "sweep": [[0, 2.6], [42.156 - 40.281, -2.4]]},
    "cam": cam(arc(d, 140, 78, 9, 9, 5.6, 5.8, [0, 0.4, 0.6], [0, 0.1, 0.6], 40, n=6))}

# 11. HERO: whole kitted liveried car
d = dur("HERO")
SHOTS["HERO"] = {
    "base": [{"blend": f"{B}/kb7_nowing.blend"}] + [{"blend": f"{B}/k_{n}.blend"} for n in KIT + ["mirror_driver", "mirror_pass"]] + BBS,
    "body_drop": [[0, DROP]],
    "livery": {**LIV7, "sweep": [[0, -9.0]]},
    "cam": cam([{"t": 0, "loc": [3.9, -4.4, 0.9], "target": [0, -0.25, 0.55], "focal": 40},
                {"t": d, "loc": [3.75, -4.2, 0.95], "target": [0, -0.25, 0.55], "focal": 41, "ease": "inout"}])}


def spec(name, mode):
    s = SHOTS[name]; final = mode == "final"
    fps = 30 if name in FPS30 else 15
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 36, "keys": s["cam"]},
          "seconds": dur(name) + 1.0 / fps, "fps": fps, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 7,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}", "persist": False}
    for key in ("swap", "show", "livery", "body_drop"):
        if key in s:
            sp[key] = s[key]
    if mode == "frames":
        sp["frames"] = ["first", "mid", "last"]; sp["out"] = f"{OUT}/frames/{name}"
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"; json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
