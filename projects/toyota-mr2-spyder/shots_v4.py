"""v4 shot list: the two kit-install shots re-done with the scan NESTED the lookbook way (tools/kit_nest2.py: the scan under
each part's `*_stock` piece, and any scan skin still covering a part, is a separate object hidden as the part lands), kit
parts in their lookbook materials (paint red; wing carbon, diffuser and bumper grille black), and the CGI drive in the v4
city (tools/city_env.py).  v1_front / v2a / v2b / v3_engine are unchanged from shots_v3.py.
    python projects/toyota-mr2-spyder/shots_v4.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shots as S
import shots_v3 as V

B, OUT, R, RED, mv, cam = S.B, S.OUT, S.RENDERS, V.RED, V.mv, V.cam
BLK = [0.02, 0.02, 0.022]
NEST = json.load(open("/home/user/media/toyota-mr2-spyder/nest/nest2.json"))
BODY = {"base": B + "n_base_keep.blend", "hood": B + "n_hood_keep.blend", "lid": B + "n_lid_keep.blend"}
CUTS = {k: B + "n_" + k + ".blend" for k in NEST if k.startswith("cut_")}          # cut_<part>__<obj>
KIT = {"duckbill": "k_duckbill", "tc_wing_kit": "k_tc_wing_kit", "rear_spats": "k_rear_spats", "diffuser": "k_diffuser",
       "hardtop": "k_hardtop", "hwin": "n_hardtop_window", "side_skirts": "k_side_skirts", "hood_vents": "k_hood_vents",
       "eyelids": "k_eyelids", "fb_paint": "k_front_bumper__paint", "fb_black": "k_front_bumper__plastic_black"}
COL = {k: (BLK if k in ("tc_wing_kit", "diffuser", "fb_black", "hwin") else RED) for k in KIT}
PART_OF = {"hwin": "hardtop", "fb_paint": "front_bumper", "fb_black": "front_bumper"}
REAR = ["duckbill", "tc_wing_kit", "rear_spats", "diffuser", "hardtop", "hwin"]
FRONT = ["side_skirts", "hood_vents", "eyelids", "fb_paint", "fb_black"]
HINGES = dict(S.HINGES, **{c: S.HINGES[c.split("__")[1]] for c in CUTS if c.split("__")[1] in S.HINGES})


def build(name, n0, n1, kit, camera, frames, moves, land, body_anims, visible):
    """moves: part -> keys (beats); land: part -> beat it is home. Cut scan pieces vanish a quarter beat before that."""
    t = lambda n: (n - n0) / (n1 - n0)
    objs = dict(BODY, **CUTS, **{k: B + KIT[k] + ".blend" for k in kit})
    anims = dict(body_anims); vis = dict(visible)
    for k in kit:
        p = PART_OF.get(k, k)
        if p in moves:
            anims[k] = mv(n0, n1, moves[p])
    for c in CUTS:
        part, obj = c[4:].split("__")
        if obj in body_anims:
            anims[c] = body_anims[obj]                      # cut pieces of the hood / lid hinge with it
        vis[c] = [0, 0] if land.get(part, 1e9) <= n0 else [0, min(1.01, t(land.get(part, 1e9) - 0.25))]
    return V.shot(name, n0, n1, objs, camera, frames, anims=anims, visible=vis, colors={k: COL[k] for k in kit}, hinges=HINGES)


SHOTS = []
f = V.f(32, 40)
SHOTS.append(build("k4a_kit_rear", 32, 40, REAR,
    cam(32, 40, [(32, -20, 22, 8.6, [0, -0.10, 0.45], 50, 0), (40, -28, 28, 8.2, [0, -0.10, 0.60], 50, 1)]), 62,
    {"duckbill": [(33.5, [0, -0.4, 1.2]), (35, [0, 0, 0])], "tc_wing_kit": [(33.5, [0, -0.4, 1.2]), (35, [0, 0, 0])],
     "rear_spats": [(35.5, [0, -0.8, -0.25]), (37, [0, 0, 0])], "diffuser": [(35.5, [0, -0.8, -0.25]), (37, [0, 0, 0])],
     "hardtop": [(37, [0, 0, 4.6]), (39, [0, 0, 0])]},
    {"duckbill": 35, "tc_wing_kit": 35, "rear_spats": 37, "diffuser": 37, "hardtop": 39},
    {"lid": mv(32, 40, [(32, V.LID_UP), (33.5, 0)], "deg"), "hood": mv(32, 40, [(32, V.HOOD_UP), (33.5, 0)], "deg"),
     "top": mv(32, 40, [(32.5, [0, 0, 0]), (34.5, [0, -0.1, 4.6])])},
    {"top": [0, f(34.5)], "hardtop": [f(36.5), 1.01], "hwin": [f(36.5), 1.01]}))
SHOTS[-1][1]["objects"]["top"] = B + "hardtop.blend"
SHOTS.append(build("k4b_kit_front", 40, 48, REAR + FRONT,
    cam(40, 48, [(40, -152, 20, 9.0, [0, 0.10, 0.60], 50, 0), (47, -161, 14, 8.05, [0, 0.20, 0.50], 50, 0),
                 (48, -162, 14, 8.0, [0, 0.20, 0.50], 50, 1)]), 62,
    {"side_skirts": [(40.5, [0, 0, -0.7]), (42, [0, 0, 0])], "hood_vents": [(42, [0, 0.2, 0.9]), (43, [0, 0, 0])],
     "eyelids": [(44, [0, 0.3, 0.6]), (45, [0, 0, 0])], "front_bumper": [(45, [0, 0.5, -0.95]), (46, [0, 0.5, 0]), (47, [0, 0, 0])]},
    {"duckbill": 40, "tc_wing_kit": 40, "rear_spats": 40, "diffuser": 40, "hardtop": 40,
     "side_skirts": 42, "hood_vents": 43, "eyelids": 45, "front_bumper": 47}, {}, {}))

c1 = json.load(open(OUT + "c1_drive_front_x.json")); c2 = json.load(open(OUT + "c2_drive_rear.json"))
c1.update(out=R + "c3_drive_front", light_range=[-330, 130]); c2.update(out=R + "c4_drive_rear", light_range=[-70, 480])
CGI = {"c3_drive_front": c1, "c4_drive_rear": c2}

if __name__ == "__main__":
    for name, d in SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1); print(name, len(d["objects"]), "objects")
    for name, d in CGI.items():
        json.dump(d, open(OUT + name + ".json", "w"), indent=1); print(name, round(d["seconds"] * d["fps"]), "frames")
