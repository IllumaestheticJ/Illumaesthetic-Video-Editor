"""A90 v2 shot JSONs (projects/a90-supra/shots_v2/*.json) for tools/shots.py - section-by-section explode.

The explode state is defined ONCE on the reel timeline (seconds, 120 BPM, bar = 2 s) in PARTS below; every shot is a
window [start - PRE, end] of that one timeline, so a part parked in shot N starts shot N+1 exactly where it was
(continuous across the soft cuts). PRE = dissolve pre-roll (Temerario ~0.3 s soft transitions).

    python projects/a90-supra/tools/plan_v2.py            # writes shots_v2/*.json
Frame (Blender, m): nose +X, right side -Y, floor z=0, wheel centres x +1.23 / -1.24, y +-0.80, z ~0.19.
"""
import json
import os

B = "/home/user/media/work/a90/blend/"
OUT = os.path.join(os.path.dirname(__file__), "..", "shots_v2")
BPM = 120
BAR = 2.0
PRE = 0.3            # soft-transition pre-roll rendered before every shot after the first
TAIL = 0.1           # 3 frames @30: minterpolate eats the tail (subaru-sti lesson)

# ---------------------------------------------------------------- shots (reel seconds)
SHOTS = [  # id, start, end, focus
    ("v01_whole", 0.0, 4.0, "whole car, wheels + suspension on (side profile, fade up)"),
    ("v03_fbump", 4.0, 12.0, "front end: face -> front bumper off (inside shown) + radar module -> crash beam / radiators behind it"),
    ("v04_fcorner", 12.0, 16.0, "front wheels + suspension + fender section, pulled outboard"),
    ("v05_side", 16.0, 20.0, "right side: door trim, upper + lower skirt off -> structure under them"),
    ("v06_rbump", 20.0, 26.0, "rear bumper off (inside shown) -> structure behind the rear bumper"),
    ("v07_rcorner", 26.0, 30.0, "rear wheels + suspension pulled outboard"),
    ("v08_lineup", 30.0, 34.0, "full exploded line-up (every section at once, only time)"),
    ("v09a_reasm", 34.0, 36.0, "reassembly - every part flies home, LOCK on 36.0"),
    ("v09b_clean", 36.0, 38.0, "clean assembled car (swap to car.blend on the lock), fade to black 37-38"),
]


def W(name, lite=None):
    return {"name": name, "full": B + name + ".blend", "lite": B + (lite or name) + ".blend"}


# ---------------------------------------------------------------- parts: global keys (T s, loc m, rot deg, ease)
# glow: release pulse on the part (rim emission), see shots.py highlight_mat. dim: parked parts out of focus.
def pulse(T, end):
    """Rim-glow envelope: 0 -> 1 in 0.25 s at release, 0.3 while its section is the focus, off 0.5 s after."""
    return [(T - 0.05, 0), (T + 0.25, 1.0), (T + 1.4, 0.3), (end, 0.3), (end + 0.5, 0)]


H = [0, 0, 0]
PARTS = {
    # ---- section A: front bumper (radar module = Radar Cover + Radar Mounting Grille scans, carved out of the bumper)
    "fbump": dict(w=W("n_fbump_norad", "L_fbump_norad"), keys=[
        (7.0, H, H, None), (8.0, [0.40, 0, 0], H, "ease_out"),
        (9.6, [1.40, -0.10, 1.00], [0, 115, 0], "ease_in_out")], glow=pulse(7.0, 12.0)),
    "radar": dict(w=W("n_radar_mod"), keys=[
        (7.0, H, H, None), (8.0, [0.40, 0, 0], H, "ease_out"),
        (9.0, [0.40, 0, 0], H, None), (10.2, [0.70, 0.95, -0.02], H, "ease_in_out")], glow=pulse(9.0, 12.0)),
    # ---- section B: front corner (fender section, FR wheel/caliper/rotor/coilover, FL corner as one unit)
    "fender": dict(w=W("fender"), keys=[
        (12.5, H, H, None), (13.5, [0.0, -0.80, -0.05], [-35, 0, 0], "ease_in_out")], glow=pulse(12.5, 16.0)),
    "fr_wheel": dict(w=W("p_FR_wheel", "L_FR_wheel"), keys=[
        (13.0, H, H, None), (14.0, [0.50, -0.80, -0.05], H, "ease_in_out")], glow=pulse(13.0, 16.0)),
    "fr_caliper": dict(w=W("p_FR_caliper"), keys=[
        (13.5, H, H, None), (14.0, [0, -0.08, 0.28], H, "ease_out"),
        (14.6, [0, -0.55, 0.30], H, "ease_in_out")], glow=pulse(13.5, 16.0)),
    "fr_rotor": dict(w=W("p_FR_rotor"), keys=[
        (14.0, H, H, None), (14.8, [0, -0.62, 0], H, "ease_in_out")], glow=pulse(14.0, 16.0)),
    "fr_coil": dict(w=W("p_FR_coilover"), keys=[
        (14.5, H, H, None), (14.9, [0, 0, -0.14], H, "ease_out"),
        (15.5, [0, -0.36, -0.14], H, "ease_in_out")], glow=pulse(14.5, 16.0)),
    "fl_corner": dict(w=W("L_corner_FL"), keys=[
        (13.0, H, H, None), (14.2, [0, 0.85, 0], H, "ease_in_out")], glow=[]),
    # ---- section C: right side (Door Trim, Upper Skirt, Lower Skirt) -> Under Door Trim / Chassis Under Upper Skirt
    "dtrim": dict(w=W("n_dtrim"), keys=[
        (16.5, H, H, None), (17.4, [0, -0.62, 0.10], [-35, 0, 0], "ease_in_out")], glow=pulse(16.5, 20.0)),
    "uskirt": dict(w=W("n_uskirt"), keys=[
        (17.5, H, H, None), (18.5, [0, -0.50, -0.38], [-35, 0, 0], "ease_in_out")], glow=pulse(17.5, 20.0)),
    "lskirt": dict(w=W("n_lskirt"), keys=[
        (18.5, H, H, None), (19.5, [0, -0.42, -0.70], [-35, 0, 0], "ease_in_out")], glow=pulse(18.5, 20.0)),
    # ---- section D: rear bumper -> Under Rear Bumper
    "rbump": dict(w=W("rbump", "L_rbump"), keys=[
        (21.0, H, H, None), (22.0, [-0.40, 0, 0], H, "ease_out"),
        (23.6, [-1.40, 0.10, 1.00], [0, -115, 0], "ease_in_out")], glow=pulse(21.0, 26.0)),
    # ---- section E: rear corner (RR wheel/caliper/rotor/spring/damper, RL corner as one unit)
    "rr_wheel": dict(w=W("p_RR_wheel", "L_RR_wheel"), keys=[
        (26.5, H, H, None), (27.5, [-0.25, -0.85, 0], H, "ease_in_out")], glow=pulse(26.5, 30.0)),
    "rr_caliper": dict(w=W("p_RR_caliper"), keys=[
        (27.0, H, H, None), (27.5, [0.06, -0.06, 0.26], H, "ease_out"),
        (28.1, [0.06, -0.55, 0.28], H, "ease_in_out")], glow=pulse(27.0, 30.0)),
    "rr_rotor": dict(w=W("p_RR_rotor"), keys=[
        (27.5, H, H, None), (28.3, [0, -0.62, 0], H, "ease_in_out")], glow=pulse(27.5, 30.0)),
    "rr_spring": dict(w=W("p_RR_spring"), keys=[
        (28.0, H, H, None), (28.4, [0, 0, -0.10], H, "ease_out"),
        (29.0, [0.12, -0.42, -0.10], H, "ease_in_out")], glow=pulse(28.0, 30.0)),
    "rr_damper": dict(w=W("p_RR_damper"), keys=[
        (28.5, H, H, None), (28.9, [0, 0, -0.16], H, "ease_out"),
        (29.5, [-0.12, -0.30, -0.16], H, "ease_in_out")], glow=pulse(28.5, 30.0)),
    "rl_corner": dict(w=W("L_corner_RL"), keys=[
        (26.5, H, H, None), (27.7, [0, 0.85, 0], H, "ease_in_out")], glow=[]),
}
# reassembly: everything flies home 34.2-34.65 -> 36.0 (ease_in, locks on the 36.0 impact), staggered by section
HOME_ORDER = [["lskirt", "uskirt", "dtrim"], ["rr_damper", "rr_spring", "rr_rotor", "rr_caliper", "rr_wheel", "rl_corner"],
              ["fr_coil", "fr_rotor", "fr_caliper", "fr_wheel", "fl_corner", "fender"], ["radar", "rbump", "fbump"]]
for i, grp in enumerate(HOME_ORDER):
    for n in grp:
        PARTS[n]["keys"] += [(34.2 + 0.15 * i, PARTS[n]["keys"][-1][1], PARTS[n]["keys"][-1][2], None),
                             (36.0, H, H, "ease_in")]

# parked parts dim while another section is the focus (0.6 -> ~-20 % display), all undimmed for the line-up and reassembly
SECTION_END = {"fbump": 12, "radar": 12, "fender": 16, "fr_wheel": 16, "fr_caliper": 16, "fr_rotor": 16, "fr_coil": 16,
               "fl_corner": 16, "dtrim": 20, "uskirt": 20, "lskirt": 20, "rbump": 26, "rr_wheel": 30, "rr_caliper": 30,
               "rr_rotor": 30, "rr_spring": 30, "rr_damper": 30, "rl_corner": 30}
for n, p in PARTS.items():
    e = SECTION_END[n]
    p["dim"] = [(e, 0), (e + 0.6, 0.6), (29.4, 0.6), (30.0, 0)] if e < 30 else []

# ---- cameras (shot fraction t, or "T" = reel seconds; az from +X, -90 = right side)
CAMS = {
    "v01_whole": dict(lens=35, cam=[{"t": 0, "az": -90, "dist": 6.6, "z": 0.75, "look": [0.25, 0, 0.42]},
                                    {"t": 1, "az": -78, "dist": 6.4, "z": 0.85, "look": [0.05, 0, 0.42]}]),
    "v03_fbump": dict(lens=35, cam=[{"T": 3.7, "az": -33, "dist": 4.6, "z": 0.70, "look": [1.10, -0.05, 0.45]},
                                    {"T": 6.6, "az": -40, "dist": 3.0, "z": 1.00, "look": [1.75, -0.20, 0.42]},
                                    {"T": 8.7, "az": -38, "dist": 4.6, "z": 1.70, "look": [2.40, -0.15, 0.80]},
                                    {"T": 9.9, "az": -34, "dist": 4.4, "z": 1.60, "look": [2.50, -0.15, 0.80]},
                                    {"T": 12.1, "az": -24, "dist": 1.45, "z": 0.62, "look": [2.00, -0.15, 0.30]}]),
    "v04_fcorner": dict(lens=32, cam=[{"t": 0, "az": -55, "dist": 2.5, "z": 2.1, "look": [1.15, -0.95, 0.25]},
                                      {"t": 0.55, "az": -68, "dist": 2.4, "z": 1.9, "look": [1.10, -1.05, 0.22]},
                                      {"t": 1, "az": -78, "dist": 2.0, "z": 1.45, "look": [1.20, -1.15, 0.22]}]),
    "v05_side": dict(lens=38, cam=[{"t": 0, "az": -90, "dist": 2.5, "z": 2.3, "look": [0.10, -1.10, 0.05]},
                                   {"t": 1, "az": -90, "dist": 2.3, "z": 2.1, "look": [-0.45, -1.10, 0.05]}]),
    "v06_rbump": dict(lens=35, cam=[{"t": 0, "az": -140, "dist": 3.0, "z": 1.0, "look": [-1.75, -0.2, 0.42]},
                                    {"t": 0.40, "az": -142, "dist": 5.0, "z": 1.8, "look": [-2.4, -0.05, 0.80]},
                                    {"t": 0.62, "az": -146, "dist": 4.9, "z": 1.7, "look": [-2.5, -0.05, 0.80]},
                                    {"t": 1, "az": -156, "dist": 1.45, "z": 0.62, "look": [-2.0, -0.15, 0.32]}]),
    "v07_rcorner": dict(lens=32, cam=[{"t": 0, "az": -125, "dist": 2.5, "z": 2.1, "look": [-1.15, -0.95, 0.25]},
                                      {"t": 0.55, "az": -112, "dist": 2.4, "z": 1.9, "look": [-1.15, -1.05, 0.22]},
                                      {"t": 1, "az": -102, "dist": 2.0, "z": 1.45, "look": [-1.25, -1.15, 0.22]}]),
    "v08_lineup": dict(lens=28, cam=[{"t": 0, "az": -97, "dist": 2.3, "z": 4.8, "look": [0.0, -0.1, 0.3], "up": [1, 0, 0]},
                                     {"t": 1, "az": -83, "dist": 2.3, "z": 4.7, "look": [0.0, -0.1, 0.3], "up": [1, 0, 0]}]),
    "v09a_reasm": dict(lens=35, cam=[{"t": 0, "az": -142, "dist": 8.2, "z": 3.4, "look": [-0.1, 0, 0.5]},
                                     {"t": 1, "az": -134, "dist": 6.9, "z": 2.7, "look": [-0.1, 0, 0.4]}]),
    "v09b_clean": dict(lens=35, cam=[{"t": 0, "az": -134, "dist": 6.9, "z": 2.7, "look": [-0.1, 0, 0.4]},
                                     {"t": 1, "az": -128, "dist": 6.6, "z": 2.4, "look": [-0.1, 0, 0.4]}]),
}
# full-res part meshes only where the part is the close-up subject; lite (3.5-4 mm) everywhere else
FULL = {"v03_fbump": {"fbump", "radar"}, "v04_fcorner": {"fr_wheel", "fr_caliper", "fr_rotor", "fr_coil", "fender"},
        "v06_rbump": {"rbump"}, "v07_rcorner": {"rr_wheel", "rr_caliper", "rr_rotor", "rr_spring", "rr_damper"}}


def seg_state(keys, T):
    """State (loc, rot) at reel time T with the same per-segment easing shots.py uses."""
    import math

    def ease(u, kind):
        return {"ease_in_out": u * u * (3 - 2 * u), "ease_out": 1 - (1 - u) ** 2, "ease_in": u * u,
                "sine": 0.5 - 0.5 * math.cos(math.pi * u)}.get(kind, u)
    if T <= keys[0][0]:
        return keys[0][1], keys[0][2]
    if T >= keys[-1][0]:
        return keys[-1][1], keys[-1][2]
    for (Ta, la, ra, _), (Tb, lb, rb, kb) in zip(keys, keys[1:]):
        if Ta <= T <= Tb:
            u = ease((T - Ta) / (Tb - Ta) if Tb > Ta else 1, kb or "ease_in_out")
            return [x + (y - x) * u for x, y in zip(la, lb)], [x + (y - x) * u for x, y in zip(ra, rb)]


def env_state(env, T):
    if not env:
        return 0.0
    if T <= env[0][0]:
        return env[0][1]
    if T >= env[-1][0]:
        return env[-1][1]
    for (Ta, a), (Tb, b) in zip(env, env[1:]):
        if Ta <= T <= Tb:
            u = (T - Ta) / (Tb - Ta)
            u = u * u * (3 - 2 * u)
            return a + (b - a) * u


def shot_keys(keys, T0, T1):
    """Window the global part keys to [T0, T1]; a segment cut by a window edge is split at its exact eased state.
    NOTE: a split segment re-eases inside the window (shots.py eases per segment) - parts are planned to move only
    well inside one shot, so splits only ever land on held states (checked below)."""
    out = []
    l0, r0 = seg_state(keys, T0)
    out.append({"t": 0.0, "loc": [round(v, 4) for v in l0], "rot": [round(v, 3) for v in r0]})
    for T, l, r, e in keys:
        if T0 < T < T1:
            k = {"t": round((T - T0) / (T1 - T0), 5), "loc": l, "rot": r}
            if e:
                k["ease"] = e
            out.append(k)
    l1, r1 = seg_state(keys, T1)
    out.append({"t": 1.0, "loc": [round(v, 4) for v in l1], "rot": [round(v, 3) for v in r1]})
    return out


def env_keys(env, T0, T1, step=0.1):
    """Sample an envelope densely enough inside the window (shots.py eases per segment)."""
    pts, T = [], T0
    while T < T1 - 1e-6:
        pts.append(T)
        T += step
    pts.append(T1)
    pts += [x[0] for x in env if T0 < x[0] < T1]
    pts = sorted(set(round(p, 4) for p in pts))
    vals = [(p, env_state(env, p)) for p in pts]
    if all(abs(v) < 1e-4 for _, v in vals):
        return None
    return [{"t": round((p - T0) / (T1 - T0), 5), "v": round(v, 4), "ease": "linear"} for p, v in vals]


def moving_at_edge(keys, T):
    for (Ta, la, ra, _), (Tb, lb, rb, _) in zip(keys, keys[1:]):
        if Ta < T < Tb and (la != lb or ra != rb):
            return True
    return False


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (sid, start, end, focus) in enumerate(SHOTS):
        T0 = start - (PRE if i and sid != "v09b_clean" else 0.0)  # 36.0 lock = hard cut
        T1 = end + TAIL
        clean = sid == "v09b_clean"
        intact = sid == "v01_whole" or clean
        objs = [{"blend": B + ("car.blend" if intact else "base_v2.blend")},
                {"blend": B + "n_interior6.blend"}]
        if intact:  # intact car: clean full scan + the four corners (lite) - no composite seams
            objs += [{"blend": B + f"L_corner_{c}.blend"} for c in ("FR", "FL", "RR", "RL")]
        else:
            for n, p in PARTS.items():
                for edge in (T0, T1):
                    if moving_at_edge(p["keys"], edge):
                        print(f"WARN {sid}: {n} is mid-move at the window edge {edge:.2f}s")
                full = n in FULL.get(sid, set())
                o = {"blend": p["w"]["full"] if full else p["w"]["lite"], "keys": shot_keys(p["keys"], T0, T1)}
                g = env_keys(p.get("glow"), T0, T1)
                d = env_keys(p.get("dim"), T0, T1)
                if g:
                    o["glow"] = g
                if d:
                    o["dim"] = d
                objs.append(o)
        spec = {"_focus": focus, "_reel": [start, end], "_window": [round(T0, 3), round(T1, 3)],
                "seconds": round(T1 - T0, 3), "lens": CAMS[sid]["lens"],
                "ease": "sine" if len(CAMS[sid]["cam"]) == 2 else "linear",
                "objects": objs,
                "cam": [dict({k: v for k, v in c.items() if k != "T"}, t=round((c["T"] - T0) / (T1 - T0), 5))
                        if "T" in c else c for c in CAMS[sid]["cam"]]}
        json.dump(spec, open(os.path.join(OUT, sid + ".json"), "w"), indent=1)
        print(sid, f"{T0:.1f}-{T1:.1f}s", len(objs), "objects")


if __name__ == "__main__":
    main()
