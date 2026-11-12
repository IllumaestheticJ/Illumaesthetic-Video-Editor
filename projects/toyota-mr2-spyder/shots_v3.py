"""v3 shot list (direction.md 2026-11-12): front hero with the REAL bumper part -> underbody front/rear -> engine bay ->
Epsilon kit install on the scan (two 3/4 shots, kit in red) -> CGI drive (tools/cgi_drive.py) from the same pose.
  python projects/toyota-mr2-spyder/shots_v3.py      # writes /home/user/media/work/mr2/shots/{v1_front,...}.json
Scan shots: tools/shot3.py at 15 fps; a shot's fractions map onto its whole slot (src_fps = 30 N / (slot + 4)).
Music: beat n at 0.344 + 0.4915 n s (East City, ~122.1 BPM); times below are beats."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shots as S

B, OUT, R = S.B, S.OUT, S.RENDERS
RED = [0.66, 0.035, 0.05]
HOOD_UP, LID_UP = 53.0, S.H_LID["open_deg"] * 0.9
K = lambda n: B + "k_" + n + ".blend"
BODY = {"base": B + "base.blend", "hood": B + "hood.blend", "lid": B + "rearlid.blend"}
REAR_KIT = ["duckbill", "tc_wing_kit", "rear_spats", "diffuser", "hardtop"]
FRONT_KIT = ["side_skirts", "hood_vents", "eyelids", "front_bumper"]


def cam(n0, n1, keys):
    return [dict(t=(n - n0) / (n1 - n0), az=az, el=el, dist=d, target=tg, lens=l, **({"lin": True} if lin else {}))
            for n, az, el, d, tg, l, lin in keys]


def mv(n0, n1, keys, field="off"):
    return [dict(t=(n - n0) / (n1 - n0), **{field: v}) for n, v in keys]


def shot(name, n0, n1, objects, camera, frames, anims=None, visible=None, **extra):
    d = dict(objects=objects, seconds=frames / 15, fps=15, res=[1080, 1920], res_pct=75, samples=12, camera=camera,
             out=R + name, anims=anims or {}, visible=visible or {}, exposure=S.EXPOSURE, hinges=S.HINGES, persistent=False,
             light_ref=next(iter(objects)))
    d.update(extra)
    return name, d


f = lambda n0, n1: (lambda n: (n - n0) / (n1 - n0))
SHOTS = []

# S1 front hero, n 0-16
t = f(0, 16)
SHOTS.append(shot("v1_front", 0, 16,
    dict(car=B + "car2.blend", **BODY, top=B + "hardtop.blend", bp=B + "bumper_part.blend"),
    cam(0, 16, [(0, -155, 10, 8.6, [0, 0.10, 0.55], 50, 0), (4.5, -160, 13, 5.6, [0, 1.00, 0.75], 50, 0),
                (7.5, -166, 12, 4.3, [0, 1.55, 0.45], 50, 0), (12, -172, 18, 2.1, [0, 1.55, 0.62], 50, 0),
                (16, -173, 20, 1.9, [0, 1.55, 0.62], 50, 1)]), 121,
    anims={"hood": mv(0, 16, [(1, 0), (4.5, HOOD_UP)], "deg"),
           "bp": mv(0, 16, [(8, [0, 0, 0]), (9.5, [0, 0.5, 0]), (11, [0, 0.5, -0.95]), (11.5, [0, 0.5, -0.95]), (13.5, [0, 0.5, -2.6])])},
    visible={"car": [0, t(1)], "base": [t(1), 1.01], "hood": [t(1), 1.01], "lid": [t(1), 1.01], "top": [t(1), 1.01], "bp": [t(1), t(13.5)]}))

# S2 underbody, n 16-20 and 20-24: each scan alone, camera below the floor
SHOTS.append(shot("v2a_under_front", 16, 20, {"uf": B + "under_front.blend"},
    cam(16, 20, [(16, 180, -40, 2.3, [0, 1.15, 0.20], 35, 0), (20, 180, -46, 1.9, [0, 0.95, 0.20], 35, 1)]), 33, underlight=0.25))
SHOTS.append(shot("v2b_under_rear", 20, 24, {"ur": B + "under_rear.blend"},
    cam(20, 24, [(20, 0, -40, 2.3, [0, -1.30, 0.25], 35, 0), (24, 0, -46, 1.9, [0, -1.15, 0.25], 35, 1)]), 33, underlight=0.25))

# S3 engine bay, n 24-32
SHOTS.append(shot("v3_engine", 24, 32, dict(BODY, top=B + "hardtop.blend"),
    cam(24, 32, [(24, -14, 30, 3.4, [0, -1.35, 0.80], 40, 0), (27, -10, 42, 2.4, [0, -1.30, 0.80], 40, 0),
                 (28.5, -7, 50, 1.85, [0, -1.30, 0.72], 40, 0), (32, -6, 52, 1.70, [0, -1.30, 0.72], 40, 1)]), 62,
    anims={"hood": [dict(t=0, deg=HOOD_UP)], "lid": mv(24, 32, [(24, 0), (26.5, LID_UP)], "deg")}))

# S4a kit rear, n 32-40
objs = dict(BODY, top=B + "hardtop.blend", **{k: K(k) for k in REAR_KIT})
SHOTS.append(shot("v4a_kit_rear", 32, 40, objs,
    cam(32, 40, [(32, -20, 22, 8.6, [0, -0.10, 0.45], 50, 0), (40, -28, 28, 8.2, [0, -0.10, 0.60], 50, 1)]), 62,
    anims={"lid": mv(32, 40, [(32, LID_UP), (33.5, 0)], "deg"), "hood": mv(32, 40, [(32, HOOD_UP), (33.5, 0)], "deg"),
           "top": mv(32, 40, [(32.5, [0, 0, 0]), (34.5, [0, -0.1, 4.6])]),
           "duckbill": mv(32, 40, [(33.5, [0, -0.4, 1.2]), (35, [0, 0, 0])]), "tc_wing_kit": mv(32, 40, [(33.5, [0, -0.4, 1.2]), (35, [0, 0, 0])]),
           "rear_spats": mv(32, 40, [(35.5, [0, -0.8, -0.25]), (37, [0, 0, 0])]), "diffuser": mv(32, 40, [(35.5, [0, -0.8, -0.25]), (37, [0, 0, 0])]),
           "hardtop": mv(32, 40, [(37, [0, 0, 4.6]), (39, [0, 0, 0])])},
    visible={"top": [0, f(32, 40)(34.5)], "hardtop": [f(32, 40)(36.5), 1.01]},
    colors={k: RED for k in REAR_KIT}))

# S4b kit front, n 40-48 (last frame = the pose the CGI inherits)
objs = dict(BODY, **{k: K(k) for k in REAR_KIT + FRONT_KIT})
SHOTS.append(shot("v4b_kit_front", 40, 48, objs,
    cam(40, 48, [(40, -152, 20, 9.0, [0, 0.10, 0.60], 50, 0), (47, -161, 14, 8.05, [0, 0.20, 0.50], 50, 0),
                 (48, -162, 14, 8.0, [0, 0.20, 0.50], 50, 1)]), 62,
    anims={"side_skirts": mv(40, 48, [(40.5, [0, 0, -0.7]), (42, [0, 0, 0])]),
           "hood_vents": mv(40, 48, [(42, [0, 0.2, 0.9]), (43, [0, 0, 0])]),
           "eyelids": mv(40, 48, [(44, [0, 0.3, 0.6]), (45, [0, 0, 0])]),
           "front_bumper": mv(40, 48, [(45, [0, 0.5, -0.95]), (46, [0, 0.5, 0]), (47, [0, 0, 0])])},
    colors={k: RED for k in REAR_KIT + FRONT_KIT}))

CGI = {
    "c1_drive_front": dict(seconds=103 / 30, fps=30, res_pct=75, samples=20, out=R + "c1_drive_front", paint=RED, road_z=-0.037,
        camera=cam(48, 55, [(48, -162, 14, 8.0, [0, 0.20, 0.50], 50, 0), (55, -170, 8, 6.6, [0, 0.30, 0.50], 50, 1)]),
        speed=[{"t": 0, "v": 24}, {"t": 1, "v": 26}]),
    "c2_drive_rear": dict(seconds=162 / 30, fps=30, res_pct=75, samples=20, out=R + "c2_drive_rear", paint=RED, road_z=-0.037,
        camera=cam(55, 66, [(55, -16, 10, 7.5, [0, -0.20, 0.55], 50, 0), (66, -12, 9, 7.5, [0, -0.20, 0.55], 50, 1)]),
        speed=[{"t": 0, "v": 26}, {"t": 0.45, "v": 26}, {"t": 1, "v": 38}],
        pull=[{"t": 5 / 11, "y": 0}, {"t": 1, "y": 14.5}]),
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1); print(name, round(d["seconds"] * 15), "frames")
    for name, d in CGI.items():
        json.dump(d, open(OUT + name + ".json", "w"), indent=1); print(name, round(d["seconds"] * 30), "frames (30 fps)")
