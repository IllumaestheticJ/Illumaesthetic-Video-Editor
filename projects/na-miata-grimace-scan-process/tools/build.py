"""Build project.yaml + overlay.json + webzoom.json for the NB Miata scan reel from the beat grid.
Grid (max-rise onsets of the track, tools/kickgrid.py + 5 ms envelope check): t_n = T0 + P*n.
Cuts land on whole frames round(t*30); first clip one frame short (assembler cut compensation, FG2 lesson);
15 fps renders get src_fps = 30*N/(slot+4) so minterpolate's 2N-3 output fills the slot (Huracan lesson)."""
import json, os, glob
FPS = 30
T0, P = 0.52, 0.50112
W = "/home/user/media/work/miata"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tb(n): return T0 + P * n
def fr(t): return int(round(t * FPS))

# (id, end beat index, spec)
shots = [
    ("irl_grimace", 2, dict(src="/home/user/media/miata/dropbox/v0607_113440.mov", in_=0.0, note="Grimace (#558) sweeps past at Sonoma - hook")),
    ("irl_front", 5, dict(src="/home/user/media/miata/irl/irl_front.mp4", end_at=1.877, note="scanner close-up -> stock NB front 3/4; ends on the solved frame (187.70 s)")),
    ("scan_ground", 15, dict(src=f"{W}/renders/s1_ground", render=True, note="1:1 ON THE DROP -> Control Ground scan, pull back")),
    ("irl_side", 20, dict(src="/home/user/media/miata/irl/irl_side.mp4", end_at=2.7945, note="tech walks in with the scanner -> door/rear arch, front corner on the jack; ends on the solved frame (204.70 s)")),
    ("scan_jacked", 30, dict(src=f"{W}/renders/s2_jacked", render=True, note="1:1 -> Strut Tower Jacked Exterior scan, pull back")),
    ("scan_bar", 40, dict(src=f"{W}/renders/s3_bar", render=True, note="engine bay: strut bar lifts out, turns 180 (front + back)")),
    ("scan_reassy", 48, dict(src=f"{W}/renders/s4_reassy", render=True, note="reassembly: bar drops back onto the towers")),
    ("scan_end", 56, dict(src=f"{W}/renders/s5_end_graded", render=True, note="full car orbit lands on the listing photo angle, grades to listing grey")),
]
DISSOLVE = 0.5
END_BEAT = 68  # riff ends ~34.5 s

timeline = []; cuts = []
start_f = 0
for k, (sid, nb, s) in enumerate(shots):
    end_f = fr(tb(nb)); slot = end_f - start_f
    dur_f = slot - (1 if k == 0 else 0)
    clip = {"id": sid, "dur": round(dur_f / FPS, 4), "src": s["src"]}
    if s.get("render"):
        n = len(glob.glob(os.path.join(s["src"], "*.png"))) or 75
        clip["src_fps"] = round(FPS * n / (slot + 4), 4); clip["interpolate"] = True
    elif "end_at" in s:  # IRL clip that must END on its solved frame
        clip["in"] = round(s["end_at"] - dur_f / FPS, 4); clip["out"] = s["end_at"]
    else:
        clip["in"] = s["in_"]; clip["out"] = round(s["in_"] + dur_f / FPS, 4)
    clip["note"] = s["note"]
    timeline.append(clip); cuts.append(end_f / FPS)
    start_f = end_f
    if k < len(shots) - 1:
        tr = {"type": "cut"}
        if sid in ("irl_front", "irl_side"): tr["note"] = "1:1 perspective cut on the beat"
        timeline.append({"transition": tr})
# end card: dissolve into the listing WebZoom
end_f = fr(tb(END_BEAT))
timeline.append({"transition": {"type": "dissolve", "duration": DISSOLVE, "note": "scan (listing angle, listing grey) -> listing page"}})
web_dur_f = end_f - start_f + int(DISSOLVE * FPS)
timeline.append({"id": "website", "dur": round(web_dur_f / FPS, 4), "src": f"{W}/out/webzoom_nb.mp4",
                 "note": "NB 3D scan listing, zoom out; title, logo, then URL fades in last"})
total_f = end_f

def F(beat, off=0): return fr(tb(beat)) + off
items = [
    {"kind": "brackets", "from": F(5, 3), "duration": F(15) - F(5) - 8},
    {"kind": "counter", "from": F(6), "duration": F(10) - F(6), "label": "TRIANGLES CAPTURED", "value": 24997127, "x": 0.08, "y": 0.1},
    {"kind": "label", "from": F(10), "duration": F(15) - F(10) - 6, "title": "STOCK NB MIATA", "sub": "CONTROL SCAN · ON THE GROUND", "x": 0.08, "y": 0.1},
    {"kind": "brackets", "from": F(20, 3), "duration": F(30) - F(20) - 8},
    {"kind": "label", "from": F(21), "duration": F(25) - F(21), "title": "ONE CORNER JACKED", "sub": "SAME SCAN · NO BRACING", "x": 0.08, "y": 0.1},
    {"kind": "label", "from": F(25), "duration": F(30) - F(25) - 6, "title": "+1.695 MM", "sub": "ENGINE BAY WIDTH VS CONTROL", "x": 0.08, "y": 0.1},
    {"kind": "label", "from": F(31), "duration": F(35) - F(31), "title": "960.948 MM", "sub": "ENGINE BAY WIDTH · CONTROL", "x": 0.08, "y": 0.1},
    {"kind": "label", "from": F(35), "duration": F(40) - F(35) - 6, "title": "STRUT BRACE", "sub": "SCANNED ON + OFF THE CAR", "x": 0.08, "y": 0.1},
    {"kind": "label", "from": F(41), "duration": F(48) - F(41) - 6, "title": "+0.731 MM", "sub": "JACKED WITH STRUT BRACE (BARE +1.695)", "x": 0.08, "y": 0.1},
]
overlay = {"width": 1080, "height": 1920, "fps": FPS, "durationInFrames": total_f, "accent": "#e8ecf2", "items": items}
webzoom = {"width": 1080, "height": 1920, "fps": FPS, "durationInFrames": web_dur_f, "src": "web_nb_listing.png",
           "imgW": 2880, "imgH": 1640, "focusX": 982, "focusY": 838, "startScale": 0.758, "zoomFrames": 91,
           "url": "ILLUMAESTHETIC.COM", "title": "SCAN DATA NOW AVAILABLE", "logo": "illumaesthetic_logo.png", "logoWidth": 640}
proj = {
    "project": "na-miata-grimace-scan-process", "format": "reel-9x16",
    "output": {"path": f"{W}/out/na_miata_grimace_scan_v1.mp4", "width": 1080, "height": 1920, "fps": FPS, "crf": 16, "preset": "slow"},
    "music": {"path": "/home/user/media/work/music/na-miata-grimace-scan-process_track.mp3", "start": 0, "fade_out": 0.8},
    "beats": [round(c, 3) for c in cuts] + [round(end_f / FPS, 3)],
    "timeline": timeline,
    "overlays": [{"src": f"{W}/out/hud_nb.mov", "start": 0}],
}
import yaml
with open(os.path.join(OUT, "project.yaml"), "w") as f:
    f.write("# NA Miata 'Grimace' / stock NB chassis-scan reel v1 (240SX format). Generated by tools/build.py - edit there.\n")
    f.write(f"# Beat grid t_n = {T0} + {P} n (max-rise onsets); drop = beat 5 ({tb(5):.3f} s); riff ends beat {END_BEAT}.\n")
    yaml.safe_dump(proj, f, sort_keys=False, width=200)
json.dump(overlay, open(os.path.join(OUT, "overlay.json"), "w"), indent=1)
json.dump(webzoom, open(os.path.join(OUT, "webzoom.json"), "w"), indent=1)
print("total %.3f s, cuts" % (total_f / FPS), [round(c, 3) for c in cuts])
