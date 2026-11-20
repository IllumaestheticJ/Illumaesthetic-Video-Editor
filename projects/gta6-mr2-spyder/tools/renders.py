"""Every car render of the reel, one Blender at a time, skipping what exists.   python tools/renders.py [stills|whips|all]
Stills -> $W/cars3/<view>_<state>.png (60 % of 2560x1440, 32 samples; colour previews 45 %, 16); whips -> $W/cars3/whip_<key>/w_NN.png (30 %, 8)."""
import subprocess, sys, json, os
from pathlib import Path
P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]
W = Path("/home/user/media/work/gta6-mr2-spyder"); CARS = W / "cars3"
M = Path("/home/user/media/gta6-mr2-spyder"); GLB = M / "glbs/eps-toyota-mr2-spyder-v2.glb"; WHEEL = M / "glbs/wheel6_hd_scantyre.glb"
ORDER = ["front_bumper", "eyelids", "hood_vents", "side_skirts", "rear_spats", "diffuser", "hardtop", "duckbill"]     # lookbook partOrder
REPL = {"front_bumper": ["body_front_bumper_stock", "trim_front_bumper_stock"], "hardtop": ["trim_soft_top_stock"]}
SILVER = ("#a8abaf", "metallic"); YELLOW = ("#f4c400", "gloss")
OEM = [("#a8abaf", "metallic"), ("#b0b3b6", "metallic"), ("#4f5256", "metallic"), ("#0c0c0d", "gloss"), ("#f2f2ee", "gloss"), ("#c4121c", "gloss"),
       ("#1f4f9a", "pearl"), ("#f4c400", "gloss")]
EXPO = {"M": 0, "F": -0.3, "H": -0.4, "D": 0, "E": -0.6, "T": -0.9, "A": -1.1, "S": 0, "W": 0}
BRONZE = "#8c6b3f"; DROP = 0.045


def hide(n):
    h = ["part_" + p for p in ORDER[n:]]
    for p in ORDER[:n]:
        h += REPL.get(p, [])
    return ",".join(h)


def state(name):
    """-> (hide list, paint, finish, extra args)"""
    if name.startswith("s"):
        return hide(int(name[1:])), *SILVER, []
    if name.startswith("c"):
        return hide(8), *OEM[int(name[1:])], []
    if name == "ky":
        return hide(8), *YELLOW, []
    if name == "low":
        return hide(8), *YELLOW, ["--drop", str(DROP)]
    if name == "fin":
        return hide(8), *YELLOW, ["--drop", str(DROP), "--wheels", str(WHEEL), "--wheel-color", BRONZE]
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


STILLS = {"M": [f"s{i}" for i in range(9)] + [f"c{i}" for i in range(1, 7)] + ["ky", "low", "fin"], "F": ["s0", "s1", "s2"], "H": ["s2", "s3"], "D": ["s3", "s4"],
          "E": ["s4", "s5", "s6"], "T": ["s6", "s7"], "A": ["s7", "s8"], "S": ["ky", "low"], "W": ["low", "fin"]}
# whip key -> (camera dir, reversed?, state, exposure view). The return whips reuse the outward frames reversed (a 61 px blur hides one part);
# only the hardtop and the wheels change enough to be rendered again.
WHIPS = {"M_F": ("M_F", 0, "s1", "F"), "M_H": ("M_H", 0, "s3", "H"), "M_D": ("M_D", 0, "s4", "D"), "M_E": ("M_E", 0, "s5", "E"), "M_T": ("M_T", 0, "s6", "T"),
         "T_M": ("M_T", 1, "s7", "T"), "M_A": ("M_A", 0, "s8", "A"), "M_S": ("M_S", 0, "low", "S"), "M_W": ("M_W", 0, "low", "W"), "W_M": ("M_W", 1, "fin", "W")}

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
