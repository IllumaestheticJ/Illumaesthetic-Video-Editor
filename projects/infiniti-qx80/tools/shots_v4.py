"""v4 kit-on-scan shots (tools/shot_kit.py). Prepped frame: nose +Y, right +X, floor z=0, car x+-1.08 y+-2.68 z 0..1.94.
  python shots_v4.py <shot>[,<shot>] [--check] [--frames 1,40,80]  -> specs in media/specs, renders in renders/{check,final}/<shot>
D_kit:   music 16.362 -> parts land one group per beat (t = k*0.65), front -> side -> rear, kit in design blue.
E_paint: music 21.562 (the lift) -> Midnight Purple sweep rear -> front over the kitted scan; black trim parts go satin black."""
import json, math, os, subprocess, sys
M = "/home/user/media/infiniti-qx80"; B = M + "/blend"
TOOLS = os.path.dirname(os.path.abspath(__file__))
CAR = [B + "/car4.blend"]
BEAT = 0.65
# group: (landing beat, offset it flies in from (m), paint target after the wrap)
KIT = {
    "front_bumper": (1, (0, 0.9, -0.05), "black"), "lower_grille": (1, (0, 0.9, -0.05), "black"),
    "brake_ducts": (1, (0, 0.9, -0.05), "black"),
    "front_lip": (2, (0, 0.6, -0.45), "black"),
    "naca": (3, (0, 0, 0.8), "black"),
    "flare_fr": (4, (0.8, 0, 0), "purple"), "flare_fl": (4, (-0.8, 0, 0), "purple"),
    "vent_r": (4, (0.8, 0, 0.1), "purple"), "vent_l": (4, (-0.8, 0, 0.1), "purple"),
    "skirt_r": (5, (0.8, 0, -0.2), "black"), "skirt_l": (5, (-0.8, 0, -0.2), "black"),
    "flare_rr": (6, (0.8, 0, 0), "purple"), "flare_rl": (6, (-0.8, 0, 0), "purple"),
    "diffuser": (7, (0, -0.9, -0.1), "black"), "exhaust": (7, (0, -0.9, -0.1), "black"),
    "wing": (7, (0, -0.2, 0.8), "purple"),
}
FLY = 0.45  # seconds of flight before each landing


def orbit(r, az0, az1, z0, z1, tgt0, tgt1, f, secs, n=8, t0=0.0):
    keys = []
    for i in range(n + 1):
        u = i / n; k = u * u * (3 - 2 * u)
        az = math.radians(az0 + (az1 - az0) * k); rr = r[0] + (r[1] - r[0]) * k
        keys.append({"t": t0 + secs * u, "loc": [rr * math.sin(az), rr * math.cos(az), z0 + (z1 - z0) * k],
                     "target": [a + (b - a) * k for a, b in zip(tgt0, tgt1)], "focal": f, "ease": "lin"})
    return keys


def kit_parts(mode):
    parts = []
    for g, (beat, off, paint) in KIT.items():
        p = {"blend": f"{B}/k_{g}.blend", "mat": "kit"}
        if mode == "land":
            tl = beat * BEAT
            p["show"] = [tl - FLY, 99]
            p["keys"] = [{"t": 0, "loc": list(off), "rot": [0, 0, 0]}, {"t": tl - FLY, "loc": list(off), "rot": [0, 0, 0]},
                         {"t": tl, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "out"}]
        else:
            p["paint"] = paint
        parts.append(p)
    return parts


SHOTS = {
    "D_kit": dict(base=CAR, base_paint=None, parts=kit_parts("land"), seconds=5.6, fps=30,
                  camera={"keys": orbit((9.6, 9.4), 38, 148, 2.7, 2.5, (0, 0.2, 0.85), (0, -0.2, 0.85), 32, 5.6)}),
    "E_paint": dict(base=CAR, parts=kit_parts("paint"), seconds=5.6, fps=15,
                    paint={"t0": 0.25, "t1": 3.2, "y0": -3.0, "y1": 3.0, "soft": 0.12},
                    camera={"keys": orbit((10.6, 9.8), 212, 318, 2.5, 1.7, (0, -0.2, 0.85), (0, 0.4, 0.8), 32, 5.6)}),
}



# ---------------- v6: FINAL RENDER 360 (Sentra v6 structure) ----------------
# Finished car = scan without stock wheels (tools/nowheels.py) + kit + Ecky's preview.blend wheels (Volk CE28 + R888R),
# revised grille and T-spec lights. Wrap sweeps rear -> front from blue kit / silver scan; ~277 deg lap (rear-left -> rear ->
# right -> front -> front-left), easing into the solved camera of photo 1702 (match/cam1702_lookat.json, silhouette grid IoU
# 0.870, onion checked) at t 6.0 and holding through the riser to the drop.
def _final_parts():
    paint = {g: KIT[g][2] for g in KIT}
    parts = [{"blend": f"{B}/k_{g}.blend", "mat": "kit", "paint": paint[g]} for g in KIT]
    # v7: wheels without the generic Brembo models + scanned GT-R brakes (brake_assemble.py / brake_on_car.py)
    parts += [{"blend": f"{B}/k_wheels_nobrake.blend", "mat": "silver", "paint": "wheel"},
              {"blend": f"{B}/k_brake_iron.blend", "mat": "silver", "paint": "iron"},
              {"blend": f"{B}/k_brake_caliper.blend", "mat": "silver", "paint": "caliper"},
              {"blend": f"{B}/k_grille_v4.blend", "mat": "silver", "paint": "black"},
              {"blend": f"{B}/k_tspec_lights.blend", "mat": "silver", "paint": "black"}]
    return parts


def _final_cam(secs=7.75, t_land=6.0):
    C = json.load(open(M + "/match/cam1702_lookat.json")); L, T, F = C["loc"], C["target"], C["focal"]
    az_end = math.degrees(math.atan2(L[0], L[1])) % 360            # 322.8: front-left
    r_end = math.hypot(L[0], L[1]); az0 = 240.0; az1 = az_end - 360  # decreasing: 240 -> -37
    keys = []; n = 24
    for i in range(n + 1):
        u = i / n; k = u * u * (3 - 2 * u); t = t_land * u
        az = math.radians(az0 + (az1 - az0) * k)
        z = 1.55 + (L[2] - 1.55) * (k ** 3)
        tgt = [a + (b - a) * (k ** 3) for a, b in zip((0, 0, 0.8), T)]
        keys.append({"t": t, "loc": [r_end * math.sin(az), r_end * math.cos(az), z], "target": tgt, "focal": F, "ease": "lin"})
    keys[-1].update({"loc": L, "target": T})
    keys.append({"t": secs, "loc": L, "target": T, "focal": F, "ease": "lin"})
    return {"keys": keys, "sensor": 20.25}


SHOTS["G_final360"] = dict(base=[B + "/car4_nowheels.blend"], parts=_final_parts(), seconds=7.75, fps=15,
                           paint={"t0": 0.25, "t1": 2.4, "y0": -3.0, "y1": 3.0, "soft": 0.12}, camera=_final_cam())


# ---------------- v7: GT-R BRAKES bench shot (brake_assemble.py hub frame, metres; +X inboard, caliper on -Y) ----------------
# Scanned GT-R ring (base, silver) + our CAD hat and caliper adapter (site green) + scanned GT-R caliper (silver), exploded
# along the hub axis at t 0, landing one per beat (hat, adapter, caliper on section beats 1/2/3), then a slow orbit hold.
BEAT_S = 60 / 128.0
def _brake_parts(fly=0.30):
    P = [("hat_cad", "kit", (-0.14, 0, 0.34), 1), ("adapter_cad", "kit", (0.12, -0.02, -0.24), 2), ("caliper_scan", "silver", (0.16, -0.06, -0.44), 3)]   # portrait: stacked hat above / caliper below
    out = []
    for n, mat, off, beat in P:
        tl = beat * BEAT_S
        out.append({"blend": f"{B}/b_{n}.blend", "mat": mat,
                    "keys": [{"t": 0, "loc": list(off), "rot": [0, 0, 0]}, {"t": tl - fly, "loc": list(off), "rot": [0, 0, 0]},
                             {"t": tl, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "out"}]})
    return out


SHOTS["K_brakes"] = dict(base=[B + "/b_ring_scan.blend"], parts=_brake_parts(), seconds=85 / 30, fps=30,
                         camera={"keys": orbit((1.95, 1.55), 208, 238, 0.45, 0.22, (0.05, -0.03, 0.05), (0.03, -0.05, 0.0), 50, 85 / 30)})


def write(name, check=False, frames=None):
    s = dict(SHOTS[name]); s.setdefault("res", "1080x1920")
    s["res_pct"] = 30 if check else 75; s["samples"] = 8 if check else 12
    s["out"] = f"{M}/renders/{'check' if check else 'final'}/{name}"
    if frames: s["frames"] = frames
    elif check: s["frames"] = ["first", "mid", "last"]
    # paint wipe direction: shot_kit paints y > edge; for a rear->front sweep invert the axis by sweeping edge from +3 to -3
    os.makedirs(M + "/specs", exist_ok=True); p = f"{M}/specs/{name}{'_check' if check else ''}.json"
    json.dump(s, open(p, "w"), indent=1); return p


if __name__ == "__main__":
    names = sys.argv[1].split(","); check = "--check" in sys.argv
    fr = [int(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")] if "--frames" in sys.argv else None
    for n in names:
        p = write(n, check, fr)
        if check or fr:
            r = subprocess.run(["blender", "-b", "-P", TOOLS + "/shot_kit.py", "--", p], capture_output=True, text=True)
            print(n, "ok" if "IVE_RENDER_DONE" in r.stdout else (r.stdout[-1500:] + r.stderr[-1500:]))
        else:
            print(p)
