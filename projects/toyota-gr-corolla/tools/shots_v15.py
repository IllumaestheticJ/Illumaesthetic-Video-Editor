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
OUT = "/home/user/media/work/grc/renders15"
SPECS = "/home/user/media/work/grc/specs15"
CAR = f"{B}/car8.blend"   # car4w + FARO stock bumper (plate kept)
FBASE = f"{B}/fbase5.blend"
HBASE, XBASE_H, CBASE_H = f"{B}/hbase_all2.blend", f"{B}/xbase_h3.blend", f"{B}/cbase_h3.blend"
HOODBASE, HOOD = f"{B}/fbase5_nh2.blend", f"{B}/hood2f.blend"   # hood traced on its shut lines (hoodtrace.py)
HOOD_PIVOT = [0, -1.112, 0.924]   # traced hood's rear edge (raw y -2104, z 346)
FB = f"{B}/fbumper8.blend"
RB, RBI, DF, HATCH = f"{B}/rbumper.blend", f"{B}/rbinner.blend", f"{B}/diffuser_p.blend", f"{B}/hatch3.blend"
WING = f"{B}/wrc_wing3.blend"   # WRC V3 scan -> CMM WRC Left+Right endplate scans (engineering frame) -> our car (eng_to_ours: 0.8 deg, 4/59/30 mm)
CAR9 = f"{B}/car9.blend"   # car8 minus the factory side covers (+12 mm recessed backing) + mirrored right-rear wheel
COVL, COVR = f"{B}/coverL.blend", f"{B}/coverR.blend"   # factory spoiler side covers, traced (sidecover.py)
CASTROL = f"{B}/car9_castrol3.blend"   # v13c: livery alpha = graphics mask (white base sweeps, graphics tape on)
OLDWL, OLDWR = f"{B}/oldwheelsL.blend", f"{B}/oldwheelsR.blend"   # scanned wheels cut out at the corrected centres
NEWWL, NEWWR = f"{B}/motegiL.blend", f"{B}/motegiR.blend"   # Motegi MF TL6 + AR1, game-model materials, corrected stance
CASTROL_V13B = f"{B}/car9_castrol2.blend"   # v13b: + game-model surface classes (livery2.py, class_attr.py)
CASTROL_V13 = f"{B}/car9_castrol.blend"   # car9 minus old wheels + Castrol livery face colours (livery.py: website GLB texture)
MOTEGI = f"{B}/motegi5.blend"   # v13b: corrected stance (wheelplace.py) + game-model wheel materials
MOTEGI_V13 = f"{B}/motegi4.blend"   # Motegi MF TL6 17x9.5 + AR1 tyres (game-model render wheels) on our hub centres
CNL, CNR = f"{B}/canardL.blend", f"{B}/canardR.blend"   # Epsilon GR Corolla canards (Projects_/Corolla GR/3d Printed Parts/Cannard), eng frame -> our car
LIP, SKL, SKR, SPL, SPR = (f"{B}/{n}.blend" for n in ("v2lip", "v2skirtL", "v2skirtR", "v2spatL", "v2spatR"))   # Epsilon Aero V2 kit, engineering frame -> our car (eng_to_ours)
JRIC = f"{B}/jr_ic.blend"   # Jackson Racing intercooler CAD from the user (core_7.6.23.stp), already in the car frame
UB, LB, FD, RD, RDV, IC = (f"{B}/{n}.blend" for n in ("ubeam", "lbeam", "fbducts", "raddu", "raddiv", "ic"))
RB_PIVOT = [0, 1.91, 0.52]
HATCH_PIVOT = [0, 1.33, 1.41]   # top edge of the hatch (raw y 330-342, z 828), 75 deg = closed 47.6 deg down -> open 27.4 deg up
HATCH_OPEN = [75, 0, 0]
Z3 = [0, 0, 0]
E = 2.45
LEN = {"f2_castrol": (140, 30), "r1_front": (70, 30), "r2_rear": (70, 30), "r3_hatch": (70, 30), "r4_wing": (70, 30), "f1_360": (140, 30), "w1_wing": (70, 30), "j1_jr360": (70, 30), "b5_jric": (70, 30), "a1_whole": (70, 15), "d1_clean": (70, 15), "k1_hood": (70, 30), "b1_fbumper": (70, 30), "h1_hatch": (70, 30), "h2_hatchoff": (70, 30), "c1_rbumper": (70, 30), "c2_crash": (70, 15)}


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
        part(COVL, [k(0), k(0.1), k(0.5, [0.25, 0.2, 0.15], ease="out"), k(1.25, [0.6, 1.3, 4.8], ease="in2")]),
        part(COVR, [k(0), k(0.1), k(0.5, [-0.25, 0.2, 0.15], ease="out"), k(1.25, [-0.6, 1.3, 4.8], ease="in2")]),
        part(WING, [k(0, [0, 0.35, 1.4]), k(0.7, [0, 0.35, 1.4]), k(1.45, Z3, ease="out")])],
        "cam": [cam(0, [2.15, 4.4, 2.05], [0, 1.55, 1.15], 30), cam(E, [1.95, 4.15, 1.95], [0, 1.55, 1.15], 30)]},
    # finale: full 360 of the assembled car (2 bars, constant speed); each V2 part rises into place as the camera passes
    "f1_360": {"base": [CAR9, WING], "parts": [
        part(LIP, [k(0, [0, -0.6, -10.0]), k(0.2, [0, -0.6, -10.0]), k(0.95, Z3, ease="out")]),
        part(CNL, [k(0, [0.2, -0.4, -10.0]), k(0.45, [0.2, -0.4, -10.0]), k(1.2, Z3, ease="out")]),
        part(CNR, [k(0, [-0.2, -0.4, -10.0]), k(0.45, [-0.2, -0.4, -10.0]), k(1.2, Z3, ease="out")]),
        part(SKL, [k(0, [0.3, 0, -10.0]), k(1.35, [0.3, 0, -10.0]), k(2.05, Z3, ease="out")]),
        part(SPL, [k(0, [0, 0.3, -10.0]), k(2.5, [0, 0.3, -10.0]), k(3.15, Z3, ease="out")]),
        part(SPR, [k(0, [0, 0.3, -10.0]), k(2.5, [0, 0.3, -10.0]), k(3.15, Z3, ease="out")]),
        part(SKR, [k(0, [-0.3, 0, -10.0]), k(3.6, [-0.3, 0, -10.0]), k(4.25, Z3, ease="out")])],
        "cam": [cam(0.0000, [-5.9201, -2.2547, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.0993, [-5.58, -3.0247, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.1986, [-5.1403, -3.7424, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.2979, [-4.6089, -4.3952, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.3972, [-3.9952, -4.9712, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.4965, [-3.3101, -5.4603, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.5958, [-2.566, -5.8537, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.6951, [-1.7761, -6.1445, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.7944, [-0.9545, -6.3273, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.8937, [-0.1158, -6.3989, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(0.9931, [0.7249, -6.3582, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.0924, [1.5527, -6.2057, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.1917, [2.3527, -5.9442, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.2910, [3.1108, -5.5784, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.3903, [3.8134, -5.1148, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.4896, [4.4478, -4.5617, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.5889, [5.0029, -3.929, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.6882, [5.4687, -3.2279, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.7875, [5.8368, -2.4709, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.8868, [6.1008, -1.6717, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(1.9861, [6.2559, -0.8444, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.0854, [6.2993, -0.0038, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.1847, [6.2302, 0.8351, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.2840, [6.05, 1.6573, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.3833, [5.7617, 2.4481, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.4826, [5.3706, 3.1934, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.5819, [4.8836, 3.88, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.6812, [4.3095, 4.4955, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.7806, [3.6584, 5.0289, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.8799, [2.9421, 5.4708, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(2.9792, [2.1732, 5.8133, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.0785, [1.3655, 6.0502, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.1778, [0.5334, 6.1774, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.2771, [-0.3081, 6.1925, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.3764, [-1.1442, 6.0952, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.4757, [-1.9599, 5.8874, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.5750, [-2.7405, 5.5727, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.6743, [-3.4723, 5.1567, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.7736, [-4.1421, 4.6469, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.8729, [-4.7379, 4.0524, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(3.9722, [-5.2491, 3.3837, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.0715, [-5.6667, 2.6529, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.1708, [-5.9831, 1.8729, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.2701, [-6.1927, 1.0577, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.3694, [-6.2918, 0.2219, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.4688, [-6.2785, -0.6197, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.5681, [-6.1532, -1.4521, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.6674, [-5.918, -2.2603, 1.55], [0.0, -0.1, 0.5], 26, ease="lin"), cam(4.7667, [-5.5772, -3.0299, 1.55], [0.0, -0.1, 0.5], 26, ease="lin")]},
    # 1:1 transition (user: "uninstall and reinstall new wheels ... as a 1:1 transition", "add the castrol livery"): same
    # camera as the 360's last frame, cut on the downbeat to the Castrol livery + Motegi wheels; the orbit carries on at the
    # same angular speed, round the front and left side, and lands (held 2 frames) on the camera solved from
    # the user's IMG_2005.mov at 6.70 s (irl/cam_pnp0.json) for the 1:1 cut scan -> IRL
    "f2_castrol": {"base": [CASTROL, WING, LIP, SKL, SKR, SPL, SPR, CNL, CNR],
                   "parts": [part(OLDWL, [k(0), k(0.15), k(0.55, [0.35, 0, 0], ease="out"), k(1.15, [0.8, 0, -7.0], ease="in2")]), part(OLDWR, [k(0), k(0.15), k(0.55, [-0.35, 0, 0], ease="out"), k(1.15, [-0.8, 0, -7.0], ease="in2")]),
                             part(NEWWL, [k(0, [0.8, 0, -12.0]), k(0.95, [0.8, 0, -12.0]), k(1.4, [0.35, 0, 0], ease="out"), k(1.85, Z3)]), part(NEWWR, [k(0, [-0.8, 0, -12.0]), k(0.95, [-0.8, 0, -12.0]), k(1.4, [-0.35, 0, 0], ease="out"), k(1.85, Z3)])],
                   "sweep": [{"t": 0, "v": -3.3}, {"t": 0.9, "v": -3.3}, {"t": 2.2, "v": 3.6, "ease": "inout"}],
                   "tape": [{"t": 0, "v": -3.4}, {"t": 2.0, "v": -3.4}, {"t": 3.7, "v": 3.5, "ease": "inout"}], "cam": [cam(0.0000, [-5.9201, -2.2547, 1.55], [0.0, -0.1, 0.5], 26.0, ease="lin"), cam(0.0761, [-5.6708, -2.8492, 1.5493], [0.0003, -0.0985, 0.5007], 26.002, ease="lin"), cam(0.1522, [-5.3664, -3.4159, 1.5474], [0.0013, -0.094, 0.5026], 26.007, ease="lin"), cam(0.2283, [-5.0099, -3.9498, 1.5442], [0.0029, -0.0867, 0.5058], 26.015, ease="lin"), cam(0.3044, [-4.6048, -4.4464, 1.5398], [0.0052, -0.0766, 0.5102], 26.025, ease="lin"), cam(0.3806, [-4.155, -4.9013, 1.5343], [0.008, -0.0639, 0.5157], 26.039, ease="lin"), cam(0.4567, [-3.6647, -5.3108, 1.5276], [0.0114, -0.0486, 0.5223], 26.056, ease="lin"), cam(0.5328, [-3.1388, -5.6714, 1.5199], [0.0153, -0.0309, 0.5301], 26.075, ease="lin"), cam(0.6089, [-2.582, -5.9803, 1.5112], [0.0197, -0.0108, 0.5388], 26.097, ease="lin"), cam(0.6850, [-1.9997, -6.2352, 1.5015], [0.0247, 0.0115, 0.5485], 26.122, ease="lin"), cam(0.7611, [-1.397, -6.4341, 1.4908], [0.0301, 0.036, 0.5591], 26.148, ease="lin"), cam(0.8372, [-0.7796, -6.5759, 1.4793], [0.0359, 0.0625, 0.5706], 26.177, ease="lin"), cam(0.9133, [-0.1531, -6.6598, 1.4669], [0.0422, 0.0909, 0.583], 26.208, ease="lin"), cam(0.9894, [0.4772, -6.6858, 1.4537], [0.0489, 0.1212, 0.5962], 26.241, ease="lin"), cam(1.0656, [1.1057, -6.6543, 1.4398], [0.056, 0.1532, 0.6101], 26.276, ease="lin"), cam(1.1417, [1.727, -6.5664, 1.4252], [0.0634, 0.1869, 0.6247], 26.312, ease="lin"), cam(1.2178, [2.336, -6.4235, 1.4098], [0.0712, 0.222, 0.64], 26.351, ease="lin"), cam(1.2939, [2.9279, -6.2278, 1.3939], [0.0793, 0.2586, 0.6559], 26.391, ease="lin"), cam(1.3700, [3.498, -5.9818, 1.3774], [0.0877, 0.2966, 0.6724], 26.432, ease="lin"), cam(1.4461, [4.0421, -5.6883, 1.3604], [0.0964, 0.3357, 0.6894], 26.475, ease="lin"), cam(1.5222, [4.5564, -5.3509, 1.3429], [0.1053, 0.376, 0.7069], 26.519, ease="lin"), cam(1.5983, [5.0375, -4.973, 1.3249], [0.1144, 0.4173, 0.7248], 26.564, ease="lin"), cam(1.6744, [5.4824, -4.5587, 1.3065], [0.1237, 0.4595, 0.7432], 26.609, ease="lin"), cam(1.7506, [5.8886, -4.1121, 1.2878], [0.1332, 0.5025, 0.7619], 26.656, ease="lin"), cam(1.8267, [6.2543, -3.6375, 1.2688], [0.1429, 0.5463, 0.7809], 26.704, ease="lin"), cam(1.9028, [6.578, -3.1393, 1.2495], [0.1527, 0.5906, 0.8002], 26.752, ease="lin"), cam(1.9789, [6.8587, -2.622, 1.2299], [0.1626, 0.6355, 0.8197], 26.801, ease="lin"), cam(2.0550, [7.0959, -2.0899, 1.2102], [0.1727, 0.6808, 0.8393], 26.851, ease="lin"), cam(2.1311, [7.2898, -1.5476, 1.1904], [0.1827, 0.7263, 0.8592], 26.9, ease="lin"), cam(2.2072, [7.4407, -0.9991, 1.1705], [0.1929, 0.7721, 0.8791], 26.95, ease="lin"), cam(2.2833, [7.5497, -0.4485, 1.1505], [0.203, 0.818, 0.899], 27.0, ease="lin"), cam(2.3594, [7.6179, 0.1003, 1.1305], [0.2131, 0.8639, 0.9189], 27.05, ease="lin"), cam(2.4356, [7.6472, 0.6436, 1.1106], [0.2233, 0.9097, 0.9388], 27.1, ease="lin"), cam(2.5117, [7.6395, 1.1782, 1.0908], [0.2333, 0.9552, 0.9587], 27.149, ease="lin"), cam(2.5878, [7.5972, 1.7011, 1.0711], [0.2434, 1.0005, 0.9783], 27.199, ease="lin"), cam(2.6639, [7.5227, 2.2095, 1.0515], [0.2533, 1.0454, 0.9978], 27.248, ease="lin"), cam(2.7400, [7.4189, 2.701, 1.0322], [0.2631, 1.0897, 1.0171], 27.296, ease="lin"), cam(2.8161, [7.2885, 3.1736, 1.0132], [0.2728, 1.1335, 1.0361], 27.344, ease="lin"), cam(2.8922, [7.1348, 3.6255, 0.9945], [0.2823, 1.1765, 1.0548], 27.391, ease="lin"), cam(2.9683, [6.9607, 4.0555, 0.9761], [0.2916, 1.2187, 1.0732], 27.436, ease="lin"), cam(3.0444, [6.7694, 4.4623, 0.9581], [0.3007, 1.26, 1.0911], 27.481, ease="lin"), cam(3.1206, [6.564, 4.8454, 0.9406], [0.3096, 1.3003, 1.1086], 27.525, ease="lin"), cam(3.1967, [6.3477, 5.2041, 0.9236], [0.3183, 1.3394, 1.1256], 27.568, ease="lin"), cam(3.2728, [6.1236, 5.5384, 0.9071], [0.3267, 1.3774, 1.1421], 27.609, ease="lin"), cam(3.3489, [5.8946, 5.8482, 0.8912], [0.3348, 1.414, 1.158], 27.649, ease="lin"), cam(3.4250, [5.6637, 6.1337, 0.8758], [0.3426, 1.4491, 1.1733], 27.688, ease="lin"), cam(3.5011, [5.4335, 6.3955, 0.8612], [0.35, 1.4828, 1.1879], 27.724, ease="lin"), cam(3.5772, [5.2068, 6.6342, 0.8473], [0.3571, 1.5148, 1.2018], 27.759, ease="lin"), cam(3.6533, [4.9861, 6.8503, 0.8341], [0.3638, 1.5451, 1.215], 27.792, ease="lin"), cam(3.7294, [4.7736, 7.0449, 0.8217], [0.3701, 1.5735, 1.2274], 27.823, ease="lin"), cam(3.8056, [4.5716, 7.2186, 0.8102], [0.3759, 1.6, 1.2389], 27.852, ease="lin"), cam(3.8817, [4.3821, 7.3725, 0.7995], [0.3813, 1.6245, 1.2495], 27.878, ease="lin"), cam(3.9578, [4.2069, 7.5074, 0.7898], [0.3863, 1.6468, 1.2592], 27.903, ease="lin"), cam(4.0339, [4.0479, 7.6243, 0.7811], [0.3907, 1.6669, 1.2679], 27.925, ease="lin"), cam(4.1100, [3.9065, 7.724, 0.7734], [0.3946, 1.6846, 1.2757], 27.944, ease="lin"), cam(4.1861, [3.7841, 7.8071, 0.7667], [0.398, 1.6999, 1.2823], 27.961, ease="lin"), cam(4.2622, [3.6819, 7.8744, 0.7612], [0.4008, 1.7126, 1.2878], 27.975, ease="lin"), cam(4.3383, [3.6011, 7.9264, 0.7568], [0.4031, 1.7227, 1.2922], 27.986, ease="lin"), cam(4.4144, [3.5425, 7.9634, 0.7536], [0.4047, 1.73, 1.2954], 27.993, ease="lin"), cam(4.4906, [3.507, 7.9856, 0.7517], [0.4057, 1.7345, 1.2973], 27.998, ease="lin"), cam(4.5667, [3.495, 7.993, 0.751], [0.406, 1.736, 1.298], 28.0, ease="lin"), cam(4.7667, [3.495, 7.993, 0.751], [0.406, 1.736, 1.298], 28.0, ease="lin")]},
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
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]}, **{k: s[k] for k in ("tape", "sweep") if k in s},
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
