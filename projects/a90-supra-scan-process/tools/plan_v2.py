"""Write the v2 shot specs (direction.md) for tools/xshots.py. Key times are absolute song seconds -> shot fractions.
Every shot renders TAIL extra seconds (3 frames @15) so minterpolate's tail freeze falls outside the used dur."""
import json, math
D = "projects/a90-supra-scan-process/shots/"; B = "/home/user/media/work/a90sp/blend/"
TAIL = 0.2; K = 36 / 20.25            # all shots on a 36 mm sensor; phone lens mm * K
cb = {"pos": [-5.41507, -0.47587, 0.98018], "look": None, "lens": 28 * K, "roll": None}
camB = json.load(open("projects/a90-supra-scan-process/match/cam_B.json"))
import numpy as np
R = np.array(camB["blender"]["rotation_matrix"]); pB = np.array(camB["blender"]["location"]); f = -R[:, 2]
lookB = (pB + 4 * f).tolist()
up = np.array([0, 0, 1.0]); r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
rollB = math.degrees(math.atan2(np.dot(np.cross(u, R[:, 1]), -f), np.dot(u, R[:, 1])))
L = json.load(open("projects/a90-supra-scan-process/match/cam_listing.json"))
RL = np.array(L["blender"]["rotation_matrix"]); pL = np.array(L["blender"]["location"]); fL = -RL[:, 2]
q = np.array([0, 0, 0.5]); lookL = (pL + fL * np.dot(q - pL, fL)).tolist()
dxy = pL[:2] - np.array(lookL[:2]); azL = math.degrees(math.atan2(dxy[1], dxy[0])); distL = float(np.linalg.norm(dxy))

def shot(name, t0, dur, objects, cams, **extra):
    sec = dur + TAIL
    fr = lambda t: round((t - t0) / sec, 5)
    for o in objects:
        for k in o.get("keys", []):
            k["t"] = fr(k["t"])
    for c in cams:
        c["t"] = fr(c["t"])
    s = {"seconds": round(sec, 4), "sensor": 36, "cam_interp": "seg", "objects": objects, "cam": cams,
         "_note": f"v2 {name}: song {t0:.3f}-{t0 + dur:.3f} s (+{TAIL} s tail). Plan: direction.md"}
    s.update(extra)
    json.dump(s, open(D + name + ".json", "w"), indent=1)

FB = [0.85, -0.55, -0.5]; FE = [0.0, -0.4, -0.75]; FBD = [0.85, -0.55, -1.05]  # FBD: dropped clear while the camera pushes in
base = {"blend": B + "base_explode2.blend"}
# s1 rear: cam_B hold, push in + swing to the low rear-right corner. Nothing moves.
shot("v2_s1_rear", 3.182, 3.75,
     [dict(base), {"blend": B + "fbump.blend"}, {"blend": B + "fender.blend"}, {"blend": B + "rbump.blend"}],
     [{"t": 3.182, "pos": pB.tolist(), "look": lookB, "lens": 28 * K, "roll": rollB},
      {"t": 3.582, "pos": pB.tolist(), "look": lookB, "lens": 28 * K, "roll": rollB},
      {"t": 6.932, "pos": [-3.55, -1.95, 0.85], "look": [-1.75, -0.35, 0.55], "lens": 28 * K, "roll": 0.0}])
# s2 front hero
P0 = [5.10, -3.10, 1.30]; P1 = [4.875, -2.79, 1.15]
shot("v2_s2_front", 8.182, 6.25,
     [dict(base), {"blend": B + "fender.blend"}, {"blend": B + "rbump.blend"},
      {"blend": B + "fbump.blend", "keys": [{"t": 8.182}, {"t": 8.582}, {"t": 9.432, "loc": FB},
                                           {"t": 10.682, "loc": FB, "rot": [0, 0, 180]}, {"t": 11.307, "loc": FB, "rot": [0, 0, 180]}, {"t": 13.182, "loc": FBD, "rot": [0, 0, 180]}, {"t": 14.432, "loc": FBD, "rot": [0, 0, 180]}]}],
     [{"t": 8.182, "pos": P0, "look": [1.6, -0.15, 0.5], "lens": 28 * K},
      {"t": 9.432, "pos": P0, "look": [1.6, -0.15, 0.5], "lens": 28 * K},
      {"t": 10.682, "pos": P1, "look": [2.0, -0.1, 0.3], "lens": 28 * K},
      {"t": 11.307, "pos": P1, "look": [2.0, -0.1, 0.3], "lens": 28 * K},
      {"t": 13.182, "pos": [3.30, -1.20, 0.95], "look": [1.75, -0.10, 0.45], "lens": 35 * K},
      {"t": 14.432, "pos": [3.30, -1.50, 0.95], "look": [1.75, -0.40, 0.45], "lens": 35 * K, "ease": "linear"}])
# s3 fender
C0 = [0.95, -3.05, 0.80]; C1 = [0.925, -2.725, 0.75]
shot("v2_s3_fender", 14.432, 2.5,
     [dict(base), {"blend": B + "rbump.blend"},
      {"blend": B + "fbump.blend", "keys": [{"t": 14.432, "loc": FBD, "rot": [0, 0, 180]}, {"t": 16.932, "loc": FBD, "rot": [0, 0, 180]}]},
      {"blend": B + "fender.blend", "keys": [{"t": 14.432}, {"t": 15.057}, {"t": 15.682, "loc": FE}, {"t": 16.932, "loc": FE}]}],
     [{"t": 14.432, "pos": C0, "look": [0.78, -0.88, 0.45], "lens": 35 * K},
      {"t": 15.682, "pos": C0, "look": [0.78, -0.88, 0.45], "lens": 35 * K},
      {"t": 16.932, "pos": C1, "look": [0.70, -0.75, 0.60], "lens": 35 * K}])
# s4 x-ray: same pose switch, fender + bumper home, pull back, arc to cam_listing, morph
A0 = {"az": -73.0, "dist": 6.8, "z": 2.4, "look": [round(v, 5) for v in lookL], "lens": 45.0}
shot("v2_s4_xray", 16.932, 6.5,
     [dict(base), {"blend": B + "rbump.blend"},
      {"blend": B + "fender.blend", "keys": [{"t": 16.932, "loc": FE}, {"t": 17.557, "loc": [0, 0, 0]}]},
      {"blend": B + "fbump.blend", "keys": [{"t": 16.932, "loc": FBD, "rot": [0, 0, 180]}, {"t": 17.557, "loc": FB, "rot": [0, 0, 180]},
                                           {"t": 18.182, "loc": [0, 0, 0], "rot": [0, 0, 0]}]}],
     [{"t": 16.932, "pos": C1, "look": [0.70, -0.75, 0.60], "lens": 35 * K},
      dict(A0, t=18.182),
      {"t": 22.182, "az": round(azL, 4), "dist": round(distL, 5), "z": round(float(pL[2]), 5), "look": [round(v, 5) for v in lookL],
       "lens": L["focal_mm"], "roll": -1.4439},
      {"t": 23.432, "pos": [round(v, 5) for v in pL.tolist()], "look": [round(v, 5) for v in lookL], "lens": L["focal_mm"], "roll": -1.4439}],
     look="xray", accent="0.8,0.82,0.86", clay_color="0.073,0.075,0.073", morph_bg="0.0098,0.0118,0.0094")
s = json.load(open(D + "v2_s4_xray.json")); sec = s["seconds"]
s["morph"] = [round((22.0 - 16.932) / sec, 4), round((22.932 - 16.932) / sec, 4)]
json.dump(s, open(D + "v2_s4_xray.json", "w"), indent=1)
print("rollB", rollB, "listing az/dist", azL, distL, "lookL", lookL)
