"""Every car render of the reel, one Blender at a time, skipping what exists.   python tools/renders.py [stills|whips|all]
Stills -> $W/cars3/<view>_<state>.png (60 % of 2560x1440, 32 samples; colour previews 45 %, 16); whips -> $W/cars3/whip_<key>/w_NN.png (30 %, 8)."""
import subprocess, sys, json, os
from pathlib import Path
P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]
W = Path("/home/user/media/work/gta6-mr2-spyder"); CARS = W / "cars3"
M = Path("/home/user/media/gta6-mr2-spyder"); GLB = M / "glbs/mr2-reel.glb"       # tools/reel_model.py: the lookbook GLB with the owner's v1 corrections; WHEEL = M / "glbs/wheel6_hd_scantyre.glb"
ORDER = ["front_bumper", "eyelids", "hood_vents", "side_skirts", "rear_spats", "diffuser", "hardtop", "duckbill", "tc_wing"]     # lookbook partOrder + the TC wing (v2)
REPL = {"front_bumper": ["body_front_bumper_stock", "trim_front_bumper_stock"], "hardtop": ["trim_soft_top_stock"], "hood_vents": ["body_hood_cut"],
        "side_skirts": ["body_fender_cut"], "diffuser": ["exhaust_stock"]}
ALT = {"diffuser": ["exhaust_diffuser"]}             # nodes that only exist with a part: hidden until it is fitted
NP = len(ORDER)
SILVER = ("#a8abaf", "metallic"); YELLOW = ("#f4c400", "gloss")
OEM = [("#a8abaf", "metallic"), ("#b0b3b6", "metallic"), ("#4f5256", "metallic"), ("#0c0c0d", "gloss"), ("#f2f2ee", "gloss"), ("#c4121c", "gloss"),
       ("#1f4f9a", "pearl"), ("#f4c400", "gloss")]
EXPO = {"M": 0, "F": -0.3, "H": -0.4, "D": 0, "E": -0.6, "T": -0.9, "A": -1.1, "S": 0, "W": 0}
BRONZE = "#8c6b3f"; DROP = 0.045


def hide(n):
    h = ["part_" + p for p in ORDER[n:]]
    for p in ORDER[n:]:
        h += ALT.get(p, [])
    for p in ORDER[:n]:
        h += REPL.get(p, [])
    return ",".join(h)


def state(name):
    """-> (hide list, paint, finish, extra args)"""
    if name.startswith("s"):
        return hide(int(name[1:])), *SILVER, []
    if name.startswith("c"):
        return hide(NP), *OEM[int(name[1:])], []
    if name == "ky":
        return hide(NP), *YELLOW, []
    if name == "low":
        return hide(NP), *YELLOW, ["--drop", str(DROP)]
    if name == "fin":
        return hide(NP), *YELLOW, ["--drop", str(DROP), "--wheels", str(WHEEL), "--wheel-color", BRONZE]
    raise SystemExit(name)


def render(cam, view, st, out, pct, samples):
    if Path(out).exists():
        return
    h, paint, fin, extra = state(st)
    cmd = [sys.executable, "-m", "ive", "kit-render", "--", "--glb", str(GLB), "--hide", h, "--paint", paint, "--finish", fin, "--camera", str(cam),
           "--res", "2560x1440", "--res-pct", str(pct), "--samples", str(samples), "--rig-json", str(P / "rig_shop.json"), "--ground", "shadow",
           "--exposure", str(EXPO[view]), "--out", str(out)] + extra
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print(("ok  " if Path(out).exists() else "FAIL") + " " + str(out), flush=True)
    if not Path(out).exists():
        print(r.stdout[-1500:], r.stderr[-1500:])


STILLS = {"M": [f"s{i}" for i in range(NP + 1)] + [f"c{i}" for i in range(1, 7)] + ["ky", "low", "fin"], "F": ["s0", "s1", "s2"], "H": ["s2", "s3"], "D": ["s3", "s4"],
          "E": ["s4", "s5", "s6"], "T": ["s6", "s7"], "A": ["s7", "s8", "s9"], "S": ["ky", "low"], "W": ["low", "fin"]}
# Whips. A whip INTO a part screen shows the car as it is before that purchase, a whip back shows it after (owner, v1: "at the 0:01
# transition the aftermarket bumper flashes on the car"). Under the whip's blur some steps look alike, so states are grouped in looks:
LOOK = {0: "A", 1: "B", 2: "B", 3: "B", 4: "C", 5: "C", 6: "C", 7: "D", 8: "D", 9: "E"}     # bumper / skirts / hardtop / wing change the look
# key "<from>_<to>_<look>" -> (camera dir, reversed?, state, exposure view). A whip not listed plays the opposite one of the same look backwards.
WHIPS = {"M_F_A": ("M_F", 0, "s0", "F"), "F_M_B": ("M_F", 1, "s1", "F"), "M_H_B": ("M_H", 0, "s2", "H"), "M_D_B": ("M_D", 0, "s3", "D"),
         "D_M_C": ("M_D", 1, "s4", "D"), "M_E_C": ("M_E", 0, "s5", "E"), "M_T_C": ("M_T", 0, "s6", "T"), "T_M_D": ("M_T", 1, "s7", "T"),
         "M_A_D": ("M_A", 0, "s8", "A"), "A_M_E": ("M_A", 1, "s9", "A"), "M_S_Y": ("M_S", 0, "low", "S"), "M_W_Y": ("M_W", 0, "low", "W"),
         "W_M_Z": ("M_W", 1, "fin", "W")}

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"; CARS.mkdir(exist_ok=True)
    if what in ("stills", "all"):
        for v, sts in STILLS.items():
            for s in sts:
                prev = s.startswith("c")
                render(P / f"cam_{v}.json", v, s, CARS / f"{v}_{s}.png", 45 if prev else 60, 16 if prev else 32)
    if what in ("whips", "all"):
        for key, (d, rev, st, ev) in WHIPS.items():
            a, b = d.split("_")
            if not (P / f"whip_{d}").exists():
                subprocess.run([sys.executable, str(P / "tools/whipcams.py"), a, b, "8"], check=True)
            (CARS / f"whip_{key}").mkdir(exist_ok=True)
            for k in range(8):
                src = 7 - k if rev else k
                render(P / f"whip_{d}/cam_{src:02d}.json", ev, st, CARS / f"whip_{key}/w_{k:02d}.png", 30, 8)
