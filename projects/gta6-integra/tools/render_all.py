"""Render list for the Integra reel: every car still and whip frame compose4.py loads from $W/cars3.

    python projects/gta6-integra/tools/render_all.py test      low-res framing tests, one per view
    python projects/gta6-integra/tools/render_all.py stills    all stills (skips files that exist)
    python projects/gta6-integra/tools/render_all.py whips     all whip frames
One Blender at a time (lessons: parallel renders took 6x longer).
"""
import subprocess, sys, json
from pathlib import Path

P = Path(__file__).resolve().parents[1]; ROOT = P.parents[1]
W = Path("/home/user/media/work/gta6-integra"); CARS = W / "cars3"
GLB = "/home/user/media/gta6-integra/glbs/eps-acura-integra-de-v29.glb"
WHEEL = "/home/user/media/gta6-integra/wheels/wheel6_hd_scantyre.glb"
ORDER = ["front_lip", "fender_flares", "side_skirts", "rear_spats", "duckbill", "sport_wing"]      # lookbook part order = purchase order
WHITE, GREY = "#1f4aa5", "#848586"         # entrance colour (Apex Blue Pearl, my sRGB approximation; the name WHITE is historical); the lookbook's photographed grey (final)
# colour run between them, as swatches and as previews on the car: see ui4.OEM (same order, first and last are WHITE and GREY)
RUN = ["#16306e", "#a3121c", "#c7801d", "#0e0f12", "#f2f0e9", "#c9cbcc", "#a8acb0", "#4f5256"]
EXPO = {"A": -1.3, "E": -0.4}
# R looks at the rear glass from the side of the yellow spray-booth doors: the painted panorama mirrored there as flat yellow and
# green blocks. That view uses a softened panorama with the booth block desaturated.
RIG = {"R": "rig_shop_soft.json"}
DROP = 0.045
BRONZE = "#7a5a36"


def hide(n):
    h = ["part_" + p for p in ORDER[n:]]
    if n >= 5:
        h.append("body_duckbill_stock")
    return ",".join(h)


def state(key):
    """key = VIEW_name -> (camera view, parts on, paint, drop, wheels)"""
    view, name = key.split("_", 1)
    table = {"stock": (0, WHITE, 0, 0), "p1": (1, WHITE, 0, 0), "p2": (2, WHITE, 0, 0), "p3": (3, WHITE, 0, 0), "p4": (4, WHITE, 0, 0),
             "p5": (5, WHITE, 0, 0), "kit": (6, WHITE, 0, 0), "grey": (6, GREY, 0, 0), "low": (6, GREY, DROP, 0), "final": (6, GREY, DROP, 1)}
    if name.startswith("c"):
        return view, 6, RUN[int(name[1:]) - 1], 0, 0
    n, paint, drop, wh = table[name]
    return view, n, paint, drop, wh


STILLS = ["M_stock", "F_stock", "F_p1", "M_p1", "R_p1", "R_p2", "M_p2", "D_p2", "D_p3", "M_p3", "E_p3", "E_p4", "M_p4", "A_p4", "A_p5", "M_p5",
          "A_kit", "M_kit"] + [f"M_c{k}" for k in range(1, len(RUN) + 1)] + ["M_grey", "S_grey", "S_low", "M_low", "W_low", "W_final", "M_final"]
# whips: (from view, to view, car state during the move)
WHIPS = [("M", "F", "stock"), ("F", "M", "p1"), ("M", "R", "p1"), ("R", "M", "p2"), ("M", "D", "p2"), ("D", "M", "p3"), ("M", "E", "p3"), ("E", "M", "p4"),
         ("M", "A", "p4"), ("A", "M", "p5"), ("M", "A", "p5"), ("A", "M", "kit"), ("M", "S", "grey"), ("S", "M", "low"), ("M", "W", "low"), ("W", "M", "final")]


def render(key, cam, out, pct, samples):
    view, n, paint, drop, wh = state(key)
    if Path(out).exists():
        return
    a = ["python", "-m", "ive", "kit-render", "--", "--glb", GLB, "--hide", hide(n), "--paint", paint, "--finish", "pearl" if paint == WHITE else "gloss" if paint == GREY else "metallic",
         "--camera", str(cam), "--res", "2560x1440", "--res-pct", str(pct), "--rig-json", str(P / RIG.get(view, "rig_shop.json")), "--samples", str(samples),
         "--exposure", str(EXPO.get(view, 0.0)), "--out", str(out)]
    if drop:
        a += ["--drop", str(drop)]
    if wh:
        a += ["--wheels", WHEEL, "--wheel-color", BRONZE]
    r = subprocess.run(a, cwd=ROOT, capture_output=True, text=True)
    print(key, Path(out).name, "ok" if Path(out).exists() else r.stdout[-600:] + r.stderr[-600:], flush=True)


def main():
    mode = sys.argv[1]; CARS.mkdir(exist_ok=True)
    if mode == "test":
        for key in ["F_p1", "R_p2", "D_p3", "E_p4", "A_kit", "S_grey", "W_low", "R_p1", "D_p2"]:
            render(key, P / f"cam_{key[0]}.json", W / "test" / f"t_{key}.png", 30, 8)
    elif mode == "stills":
        for key in (sys.argv[2:] or STILLS):
            col = key.split("_")[1].startswith("c")
            render(key, P / f"cam_{key[0]}.json", CARS / f"{key}.png", 45 if col else 60, 16 if col else 36)
    elif mode == "whips":
        for a, b, st in WHIPS:
            if not (P / f"whip_{a}_{b}").exists():
                subprocess.run(["python", str(P / "tools/whipcams.py"), a, b, "8"], check=True)
            d = CARS / f"whip_{a}_{b}_{st}"; d.mkdir(exist_ok=True)
            for k in range(8):
                render(f"{b}_{st}", P / f"whip_{a}_{b}" / f"cam_{k:02d}.json", d / f"w_{k:02d}.png", 30, 8)


if __name__ == "__main__":
    main()
