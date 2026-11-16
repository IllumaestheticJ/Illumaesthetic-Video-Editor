"""v11 (user on v9: "jackson racing intercooler, with the logo - do a quick 360 of the entire part then install it. you
have it installed 180 degrees rotated wrong (flip top to bottom)"; no GR Corolla-specific intercooler exists on the
engineering Drive - only a CSF GR Corolla oil cooler - so the GR Yaris (same G16E) part stays). csf_ic_flip = the finned
part rotated 180 deg about the fore-aft axis through its centre (top<->bottom, ports still rearward). jr_360 = camera
orbit round the part alone (the part is the static base; constant speed). b5 = install only (the stock unit is already out).

v10 (user on v8: "add in the jackson racing intercooler when the stock intercooler comes off"; the STEP is in the
engineering Drive's CSF folder: 'GR Yaris Intercooler/Yaris IC - Hardpipe Version_05.10_0.5in extended.stp' (G16E, shared
with the GR Corolla). Meshed with gmsh, axes mapped CAD (z, x, y) -> car (x, y, z) (ports rearward), seated on the stock
intercooler's envelope (centred, front faces flush); red fit check chk5/csf_fit_1.jpg. b5 = swap on the next bar; the hood
shot shows it installed.

v9 (user on v7: "the hood is cut wrong" -> hood traced on its shut lines along the hood normal: cowl seam,
fender shut lines, front crease; tools/hoodtrace.py).

v8 (user on v6: "please have the front bumper use the other full car scan - this one is missing a huge chunk of the
front bumper" [FARO stock bumper: farobumper.py; NOT the facelift Complete Car], "rear trunk isn't cut out correctly"
[hatch3 traced on its shut lines: hatchtrace.py], "we don't show the hood opening" [k1: hood hinges open on its rear
edge over the engine bay scan, then lifts off]). Every later shot keeps bumper/hood/hatch off.

v7: Short-form Temerario restart (user on v5: "completely start this over, using the short form temerario skill, and
graphify"). Shot specs -> JSON for tools/shot.py.

    python projects/toyota-gr-corolla/tools/shots_v7.py frames|preview|final [shot ...]

Music: GT2 'Going Up North' FROM ITS BEGINNING (skill), 102.95 BPM, bar 2.3312 s, downbeats 0.50 + 2.3312k; video
starts at music 0.47 so the first hit lands on frame 1. Ten one-bar shots, logo where the drums thin out (23.8 s).
Rules applied (graphify feedback index + lessons): bumper comes off FIRST and whole (user v5: the bumper part was
missing a chunk -> fbumper6 = bumper scan + every car face cut off as bumper skin that the scan lacks); nothing of a
removed part stays on the car; headlights stay (fbase5); the bay scan stays behind the under-bumper parts; the hatch
hinges open THEN comes off (GR86 rule) over the real cargo area of the 'trunk open' state; the diffuser leaves with
the rear bumper; every later rear shot keeps the hatch off; one action per bar; plates kept; labels from file names.
Reused renders (same base/camera/keys as here): a1/d1 = renders5, b2-b4 = renders6 (fbase5).
"""
import json
import os
import sys

B = "/home/user/media/work/grc/blend"
OUT = "/home/user/media/work/grc/renders14"
SPECS = "/home/user/media/work/grc/specs14"
CAR = f"{B}/car8.blend"   # car4w + FARO stock bumper (plate kept)
FBASE = f"{B}/fbase5.blend"
HBASE, XBASE_H, CBASE_H = f"{B}/hbase_all2.blend", f"{B}/xbase_h3.blend", f"{B}/cbase_h3.blend"
HOODBASE, HOOD = f"{B}/fbase5_nh2.blend", f"{B}/hood2f.blend"   # hood traced on its shut lines (hoodtrace.py)
HOOD_PIVOT = [0, -1.112, 0.924]   # traced hood's rear edge (raw y -2104, z 346)
FB = f"{B}/fbumper8.blend"
RB, RBI, DF, HATCH = f"{B}/rbumper.blend", f"{B}/rbinner.blend", f"{B}/diffuser_p.blend", f"{B}/hatch3.blend"
WING = f"{B}/wrc_wing2.blend"   # Epsilon Aero WRC wing scan (WRC V3.stl) ICP-registered to the CMM WRC Left+Right endplate scans (car frame)
CAR9 = f"{B}/car9.blend"   # car8 minus the factory side covers (+12 mm recessed backing) + mirrored right-rear wheel
COVL, COVR = f"{B}/coverL.blend", f"{B}/coverR.blend"   # factory spoiler side covers, traced (sidecover.py)
LIP, SKL, SKR, SPL, SPR = (f"{B}/{n}.blend" for n in ("v2lip", "v2skirtL", "v2skirtR", "v2spatL", "v2spatR"))   # Epsilon Aero V2 kit (car frame)
JRIC = f"{B}/jr_ic.blend"   # Jackson Racing intercooler CAD from the user (core_7.6.23.stp), already in the car frame
UB, LB, FD, RD, RDV, IC = (f"{B}/{n}.blend" for n in ("ubeam", "lbeam", "fbducts", "raddu", "raddiv", "ic"))
RB_PIVOT = [0, 1.91, 0.52]
HATCH_PIVOT = [0, 1.33, 1.41]   # top edge of the hatch (raw y 330-342, z 828), 75 deg = closed 47.6 deg down -> open 27.4 deg up
HATCH_OPEN = [75, 0, 0]
Z3 = [0, 0, 0]
E = 2.45
LEN = {"r1_front": (70, 30), "r2_rear": (70, 30), "r3_hatch": (70, 30), "r4_wing": (70, 30), "f1_360": (140, 30), "w1_wing": (70, 30), "j1_jr360": (70, 30), "b5_jric": (70, 30), "a1_whole": (70, 15), "d1_clean": (70, 15), "k1_hood": (70, 30), "b1_fbumper": (70, 30), "h1_hatch": (70, 30), "h2_hatchoff": (70, 30), "c1_rbumper": (70, 30), "c2_crash": (70, 15)}


def cam(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": loc, "target": tgt, "focal": focal, "ease": ease}


def k(t, loc=Z3, rot=Z3, ease="inout"):
    return {"t": t, "loc": loc, "rot": rot, "ease": ease}


def part(blend, keys, pivot=None):
    d = {"blend": blend, "keys": keys}
    if pivot:
        d["pivot"] = pivot
    return d


H_CAM_END = cam(E, [2.35, 5.0, 2.15], [0, 1.35, 1.0], 28)
C1_END = cam(E, [1.15, 4.2, 0.75], [0, 2.05, 0.6], 32)
SHOTS = {
    # bumper first, whole, straight forward then up and out; everything behind it stays seated
    "b1_fbumper": {"base": [FBASE], "parts": [part(p, []) for p in (UB, LB, FD, RD, RDV, IC)] + [
        part(FB, [k(0), k(0.1), k(0.7, [0, -0.55, 0.12], ease="out"), k(1.65, [0, -0.85, 2.9], [150, 0, 0], ease="in2")])],
        "cam": [cam(0, [-2.3, -4.75, 0.85], [0, -1.85, 0.4], 30), cam(E, [-1.95, -4.35, 0.72], [0, -1.9, 0.36], 30)]},
    # whole car (FARO stock bumper), song opening
    "a1_whole": {"base": [CAR], "cam": [cam(0, [-4.4, -6.3, 1.6], [0, -0.3, 0.6]),
                                        cam(E, [-3.0, -4.75, 1.08], [0, -0.55, 0.55], ease="out")]},
    # the Jackson Racing intercooler alone: one quick 360 (camera orbit at constant speed, part centred)
    "j1_jr360": {"base": [JRIC], "cam": [cam(0.0000, [-0.0228, -3.4509, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.1021, [-0.424, -3.3981, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.2042, [-0.7978, -3.2432, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.3063, [-1.1188, -2.9969, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.4083, [-1.3651, -2.6759, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.5104, [-1.52, -2.3021, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.6125, [-1.5728, -1.9009, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.7146, [-1.52, -1.4997, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.8167, [-1.3651, -1.1259, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(0.9188, [-1.1188, -0.8049, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.0208, [-0.7978, -0.5586, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.1229, [-0.424, -0.4037, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.2250, [-0.0228, -0.3509, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.3271, [0.3784, -0.4037, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.4292, [0.7522, -0.5586, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.5312, [1.0732, -0.8049, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.6333, [1.3195, -1.1259, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.7354, [1.4744, -1.4997, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.8375, [1.5272, -1.9009, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(1.9396, [1.4744, -2.3021, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(2.0417, [1.3195, -2.6759, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(2.1438, [1.0732, -2.9969, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(2.2458, [0.7522, -3.2432, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(2.3479, [0.3784, -3.3981, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin"), cam(2.4500, [-0.0228, -3.4509, 0.6868], [-0.0228, -1.9009, 0.3268], 30, ease="lin")]},
    # install: slides in from the front and seats (b4's end camera)
    "b5_jric": {"base": [FBASE], "parts": [
        part(JRIC, [k(0, [0, -1.0, -1.2]), k(0.45, [0, -1.0, -1.2]), k(1.05, [0, -0.55, 0.05], ease="out"),
                    k(1.6, Z3, ease="inout")])],
        "cam": [cam(0, [-0.5, -4.25, 0.78], [0, -2.3, 0.3], 32), cam(E, [-0.42, -4.1, 0.74], [0, -2.3, 0.3], 32)]},
    # hood hinges open on its rear edge over the engine bay scan, then lifts off (GR86 rule: open THEN off)
    "k1_hood": {"base": [HOODBASE], "parts": [part(JRIC, []), part(HOOD, [k(0), k(0.2), k(1.1, Z3, [-62, 0, 0]), k(1.3, Z3, [-62, 0, 0]),
                                                          k(2.0, [0, 0.4, 2.6], [-80, 0, 0], ease="in2")], HOOD_PIVOT)],
                "cam": [cam(0, [-2.5, -4.7, 2.3], [0, -1.5, 0.75], 28), cam(E, [-2.2, -4.3, 2.1], [0, -1.5, 0.72], 28)]},
    # ---- reassembly (user on v11: the wing goes on AS the car reassembles; reverse of the teardown, front first) ----
    # front: hood comes back down and closes, then ducts, beams and the bumper fly home (JR intercooler stays seated)
    "r1_front": {"base": [HOODBASE], "parts": [part(JRIC, []),
        part(HOOD, [k(0, [0, 0.4, 2.6], [-80, 0, 0]), k(0.55, Z3, [-62, 0, 0], ease="out2"), k(0.65, Z3, [-62, 0, 0]),
                    k(1.15, Z3, Z3)], HOOD_PIVOT),
        part(RD, [k(0, [0, -0.65, 1.5]), k(0.35, [0, -0.65, 1.5]), k(0.85, [0, -0.55, 0], ease="out"), k(1.1, Z3)]),
        part(RDV, [k(0, [0, -0.6, 1.3]), k(0.45, [0, -0.6, 1.3]), k(0.95, [0, -0.5, 0], ease="out"), k(1.2, Z3)]),
        part(FD, [k(0, [0, -0.6, -2.0]), k(0.55, [0, -0.6, -2.0]), k(1.05, [0, -0.5, 0], ease="out"), k(1.3, Z3)]),
        part(UB, [k(0, [0, -0.6, 1.5]), k(0.7, [0, -0.6, 1.5]), k(1.2, [0, -0.45, 0], ease="out"), k(1.45, Z3)]),
        part(LB, [k(0, [0, -0.6, -0.9]), k(0.8, [0, -0.6, -0.9]), k(1.3, [0, -0.45, 0], ease="out"), k(1.55, Z3)]),
        part(FB, [k(0, [0, -0.85, 2.9], [150, 0, 0]), k(0.9, [0, -0.85, 2.9], [150, 0, 0]),
                  k(1.6, [0, -0.55, 0.12], ease="out"), k(1.95, Z3)])],
        "cam": [cam(0, [-2.6, -4.9, 1.9], [0, -1.75, 0.6], 28), cam(E, [-2.3, -4.5, 1.6], [0, -1.8, 0.55], 28)]},
    # rear: crash beam back on the kick (state swap), bumper + diffuser fly home together
    "r2_rear": {"base": [XBASE_H], "parts": [part(b, [k(0, [0, 0.8, 1.8], [150, 0, 0]), k(0.3, [0, 0.8, 1.8], [150, 0, 0]),
                                                      k(1.1, [0, 0.55, 0.15], ease="out"), k(1.5, Z3)], RB_PIVOT)
                                             for b in (RB, RBI, DF)],
                "cam": [cam(0, [2.3, 5.8, 1.25], [0, 2.1, 0.75], 30), cam(E, [1.95, 5.3, 1.05], [0, 2.1, 0.7], 30)]},
    # hatch comes back down open, seats on its hinge, closes
    "r3_hatch": {"base": [HBASE], "parts": [part(HATCH, [k(0, [0, 0.5, 3.0], [95, 0, 0]), k(0.2, [0, 0.5, 3.0], [95, 0, 0]),
                                                         k(0.85, [0, 0.15, 0.35], HATCH_OPEN, ease="out"),
                                                         k(1.05, Z3, HATCH_OPEN), k(1.75, Z3, Z3)], HATCH_PIVOT)],
                 "cam": [cam(0, [2.3, 5.1, 2.15], [0, 1.35, 1.0], 28), cam(E, [2.55, 5.5, 2.3], [0, 1.3, 1.0], 28)]},
    # factory side covers come off (Epsilon guide step 2), WRC wing comes down and seats on its registered pose
    "r4_wing": {"base": [CAR9], "parts": [
        part(COVL, [k(0), k(0.1), k(0.5, [0.25, 0.2, 0.15], ease="out"), k(1.0, [0.9, 0.7, 1.8], ease="in2")]),
        part(COVR, [k(0), k(0.1), k(0.5, [-0.25, 0.2, 0.15], ease="out"), k(1.0, [-0.9, 0.7, 1.8], ease="in2")]),
        part(WING, [k(0, [0, 0.35, 1.4]), k(0.7, [0, 0.35, 1.4]), k(1.45, Z3, ease="out")])],
        "cam": [cam(0, [2.15, 4.4, 2.05], [0, 1.55, 1.15], 30), cam(E, [1.95, 4.15, 1.95], [0, 1.55, 1.15], 30)]},
    # finale: full 360 of the assembled car (2 bars, constant speed); each V2 part rises into place as the camera passes
    "f1_360": {"base": [CAR9, WING], "parts": [
        part(LIP, [k(0, [0, -0.6, -10.0]), k(0.2, [0, -0.6, -10.0]), k(0.95, Z3, ease="out")]),
        part(SKL, [k(0, [0.3, 0, -10.0]), k(1.35, [0.3, 0, -10.0]), k(2.05, Z3, ease="out")]),
        part(SPL, [k(0, [0, 0.3, -10.0]), k(2.5, [0, 0.3, -10.0]), k(3.15, Z3, ease="out")]),
        part(SPR, [k(0, [0, 0.3, -10.0]), k(2.5, [0, 0.3, -10.0]), k(3.15, Z3, ease="out")]),
        part(SKR, [k(0, [-0.3, 0, -10.0]), k(3.6, [-0.3, 0, -10.0]), k(4.25, Z3, ease="out")])],
        "cam": [cam(0.0000, [-5.9201, -2.2547, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.0993, [-5.58, -3.0247, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.1986, [-5.1403, -3.7424, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.2979, [-4.6089, -4.3952, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.3972, [-3.9952, -4.9712, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.4965, [-3.3101, -5.4603, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.5958, [-2.566, -5.8537, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.6951, [-1.7761, -6.1445, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.7944, [-0.9545, -6.3273, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.8937, [-0.1158, -6.3989, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.9931, [0.7249, -6.3582, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.0924, [1.5527, -6.2057, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.1917, [2.3527, -5.9442, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.2910, [3.1108, -5.5784, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.3903, [3.8134, -5.1148, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.4896, [4.4478, -4.5617, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.5889, [5.0029, -3.929, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.6882, [5.4687, -3.2279, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.7875, [5.8368, -2.4709, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.8868, [6.1008, -1.6717, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.9861, [6.2559, -0.8444, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.0854, [6.2993, -0.0038, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.1847, [6.2302, 0.8351, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.2840, [6.05, 1.6573, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.3833, [5.7617, 2.4481, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.4826, [5.3706, 3.1934, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.5819, [4.8836, 3.88, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.6812, [4.3095, 4.4955, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.7806, [3.6584, 5.0289, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.8799, [2.9421, 5.4708, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.9792, [2.1732, 5.8133, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.0785, [1.3655, 6.0502, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.1778, [0.5334, 6.1774, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.2771, [-0.3081, 6.1925, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.3764, [-1.1442, 6.0952, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.4757, [-1.9599, 5.8874, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.5750, [-2.7405, 5.5727, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.6743, [-3.4723, 5.1567, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.7736, [-4.1421, 4.6469, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.8729, [-4.7379, 4.0524, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.9722, [-5.2491, 3.3837, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.0715, [-5.6667, 2.6529, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.1708, [-5.9831, 1.8729, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.2701, [-6.1927, 1.0577, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.3694, [-6.2918, 0.2219, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.4688, [-6.2785, -0.6197, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.5681, [-6.1532, -1.4521, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.6674, [-5.918, -2.2603, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.7667, [-5.5772, -3.0299, 1.55], [0.0, -0.1, 0.5], 26, ease="lin")]},
    # Epsilon Aero WRC wing: clean car from high rear-left; wing comes down from above, slightly rearward, and seats
    "w1_wing": {"base": [CAR], "parts": [part(WING, [k(0, [0, 0.35, 1.1]), k(0.3, [0, 0.35, 1.1]),
                                                     k(1.25, [0, 0, 0], ease="out")])],
                "cam": [cam(0, [2.7, 5.0, 2.45], [0, 1.45, 1.15], 34), cam(E, [2.45, 4.7, 2.3], [0, 1.45, 1.15], 34)]},
    "d1_clean": {"base": [CAR], "parts": [part(WING, [])], "cam": [cam(0, [3.85, 4.95, 1.4], [0, 0.4, 0.58], 30),
                                        cam(E, [3.68, 4.78, 1.29], [0, 0.4, 0.55], 30, ease="out")]},
    # hatch hinges open on its top edge (rear-left, high), parks open
    "h1_hatch": {"base": [HBASE], "parts": [part(HATCH, [k(0), k(0.3), k(1.7, Z3, HATCH_OPEN)], HATCH_PIVOT)],
                 "cam": [cam(0, [2.6, 5.5, 2.3], [0, 1.3, 1.0], 28), H_CAM_END]},
    # same camera: the open hatch lifts up and back off the car, out of the top of the frame
    "h2_hatchoff": {"base": [HBASE], "parts": [part(HATCH, [k(0, Z3, HATCH_OPEN), k(0.15, Z3, HATCH_OPEN),
                                                            k(0.7, [0, 0.15, 0.35], HATCH_OPEN, ease="out"),
                                                            k(1.6, [0, 0.5, 3.0], [95, 0, 0], ease="in2")], HATCH_PIVOT)],
                    "cam": [cam(0, H_CAM_END["loc"], H_CAM_END["target"], 28), cam(E, [2.15, 4.7, 1.9], [0, 1.4, 0.95], 28)]},
    # rear bumper WITH its diffuser (user rule), hatch already off
    "c1_rbumper": {"base": [XBASE_H], "parts": [part(b, [k(0), k(0.15), k(0.85, [0, 0.55, 0.15], ease="out"),
                                                          k(1.85, [0, 0.8, 1.8], [150, 0, 0], ease="in2")], RB_PIVOT)
                                                 for b in (RB, RBI, DF)],
                   "cam": [cam(0, [2.0, 6.0, 0.93], [0, 2.25, 0.88]), C1_END]},
    # same camera as c1's end: swap to 'crash bar removed' on the kick
    "c2_crash": {"base": [CBASE_H], "cam": [cam(0, C1_END["loc"], C1_END["target"], 32),
                                            cam(E, [0.75, 4.05, 0.74], [-0.05, 2.03, 0.6], 32)]},
}


def spec(name, mode):
    s = SHOTS[name]
    frames30, fps = LEN[name]
    fps = 15 if mode != "final" else fps
    n = -(-frames30 * fps // 30) + 3
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": n / fps, "fps": fps, "res": "1080x1920",
          "res_pct": 75 if mode == "final" else 30, "samples": 12 if mode == "final" else 6,
          "out": f"{OUT}/{mode}/{name}"}
    if mode == "frames":
        sp["frames"] = ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
