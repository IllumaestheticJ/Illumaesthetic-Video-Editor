"""Build project.yaml + overlay.json + webzoom.json for the NB Miata scan reel (v4) from the beat grid.
Music: 'Invincible' - Deaf Kev (TikTok CML). Grid on the track: t_k = DROP + P*k (k=0 = the drop, spectral-flux
phase/period search, 25 ms rms). Video beat n = k + LEAD, so the IRL opener plays the last LEAD beats of the breakdown and
the 1:1 cut lands on the drop. Cuts on whole frames round(t*30); first clip one frame short (assembler cut compensation,
FG2 lesson); 15 fps renders get src_fps = 30*N/(slot+4) so minterpolate's 2N-3 output fills the slot (Huracan lesson)."""
import json, os, glob
FPS = 30
DROP, P = 145.2633, 0.46671
LEAD = 6  # beats of IRL before the drop
W = "/home/user/media/work/miata"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RC = 24000 / 1001  # rough-cut frame rate

def tb(n): return P * n          # video time of video beat n (n = LEAD is the drop)
def fr(t): return int(round(t * FPS))

# (id, end video beat, spec)
shots = [
    ("irl_bay", LEAD, dict(src="/home/user/media/miata/irl/irl_bay.mp4", end_at=round(68 / RC, 4),
                           note="tech scanning the engine bay (rough cut 372.79-375.58), wide canvas window on a blurred fill; ends on the solved frame 9005")),
    ("scan_bay", LEAD + 8, dict(src=f"{W}/renders/s1_bay", render=True, note="1:1 ON THE DROP -> Engine Bay Control scan (car frame), push in")),
    ("scan_front", LEAD + 24, dict(src=f"{W}/renders/s2_front", render=True,
                                   note="front-left 3/4: bumper (Bumper Only scan) comes off the Frontend Stripped scan, push in on the crash beam")),
    ("irl_side", LEAD + 26, dict(src="/home/user/media/miata/irl/irl_side.mp4", end_at=2.7945, min_in=1.76,
                                 note="crew scanning the door, front corner on the jack (rough cut 203.77-204.70, one continuous shot); ends on the solved frame")),
    ("scan_side", LEAD + 34, dict(src=f"{W}/renders/s3_side", render=True,
                                  note="1:1 -> Strut Tower Jacked Exterior scan, pull back + orbit to the front-right 3/4 (whole car, jacked corner)")),
    ("scan_end", LEAD + 38, dict(src=f"{W}/renders/s5_tail", render=True, note="full car lands on the listing photo angle, grades to listing grey (s5 frames 25-60)")),
]
DISSOLVE = 0.5
END_BEAT = LEAD + 50

timeline = []; cuts = []
start_f = 0
for k, (sid, nb, s) in enumerate(shots):
    end_f = fr(tb(nb)); slot = end_f - start_f
    dur_f = slot - (1 if k == 0 else 0)
    clip = {"id": sid, "dur": round(dur_f / FPS, 4), "src": s["src"]}
    if s.get("render"):
        n = len(glob.glob(os.path.join(s["src"], "*.png"))) or 56
        clip["src_fps"] = round(FPS * n / (slot + 4), 4); clip["interpolate"] = True
    else:  # IRL clip that must END on its solved frame
        clip["in"] = round(max(s["end_at"] - dur_f / FPS, s.get("min_in", 0)), 4); clip["out"] = s["end_at"]
    clip["note"] = s["note"]
    timeline.append(clip); cuts.append(end_f / FPS)
    start_f = end_f
    if k < len(shots) - 1:
        tr = {"type": "cut"}
        if sid.startswith("irl"): tr["note"] = "1:1 perspective cut on the beat"
        timeline.append({"transition": tr})
end_f = fr(tb(END_BEAT))
timeline.append({"transition": {"type": "dissolve", "duration": DISSOLVE, "note": "scan (listing angle, listing grey) -> listing page"}})
web_dur_f = end_f - start_f + int(DISSOLVE * FPS)
timeline.append({"id": "website", "dur": round(web_dur_f / FPS, 4), "src": f"{W}/out/webzoom_nb_v4.mp4",
                 "note": "NB 3D scan listing, zoom out; title, logo, then URL fades in last"})
total_f = end_f

def F(beat, off=0): return fr(tb(beat)) + off
L = LEAD
# Only scan facts: triangle counts from the STL headers, scan/state names from the file names. No bracing-test numbers.
items = [
    {"kind": "brackets", "from": F(L, 3), "duration": F(L + 8) - F(L) - 8},
    {"kind": "label", "from": F(L + 1), "duration": F(L + 8) - F(L + 1) - 6, "title": "ENGINE BAY", "sub": "4,997,392 TRIANGLES", "x": 0.08, "y": 0.1},
    {"kind": "label", "from": F(L + 13), "duration": F(L + 18) - F(L + 13), "title": "FRONT BUMPER REMOVED", "sub": "4,994,051 TRIANGLES", "x": 0.08, "y": 0.1},
    {"kind": "label", "from": F(L + 18), "duration": F(L + 24) - F(L + 18) - 6, "title": "CRASH BEAM", "sub": "FRONTEND STRIPPED SCAN", "x": 0.08, "y": 0.1},
    {"kind": "brackets", "from": F(L + 26, 3), "duration": F(L + 34) - F(L + 26) - 8},
    {"kind": "label", "from": F(L + 28), "duration": F(L + 34) - F(L + 28) - 6, "title": "FULL EXTERIOR", "sub": "24,993,431 TRIANGLES", "x": 0.08, "y": 0.1},
]
overlay = {"width": 1080, "height": 1920, "fps": FPS, "durationInFrames": total_f, "accent": "#e8ecf2", "items": items}
webzoom = {"width": 1080, "height": 1920, "fps": FPS, "durationInFrames": web_dur_f, "src": "web_nb_listing.png",
           "imgW": 2880, "imgH": 1640, "focusX": 982, "focusY": 838, "startScale": 0.758, "zoomFrames": 91,
           "url": "ILLUMAESTHETIC.COM", "title": "SCAN DATA NOW AVAILABLE", "logo": "illumaesthetic_logo.png", "logoWidth": 640}
proj = {
    "project": "na-miata-grimace-scan-process", "format": "reel-9x16",
    "output": {"path": f"{W}/out/nb_miata_scan_v4.mp4", "width": 1080, "height": 1920, "fps": FPS, "crf": 16, "preset": "slow"},
    "music": {"path": "/home/user/media/work/music/nb-miata_invincible.mp3", "start": round(DROP - P * LEAD, 4), "fade_out": 0.8},
    "beats": [round(c, 3) for c in cuts] + [round(end_f / FPS, 3)],
    "timeline": timeline,
    "overlays": [{"src": f"{W}/out/hud_nb_v4.mov", "start": 0}],
}
import yaml
with open(os.path.join(OUT, "project.yaml"), "w") as f:
    f.write("# Stock NB Miata chassis-scan reel v4 (240SX format; NB only, rough cut used only for the 1:1 IRL->scan shots). Generated by tools/build.py - edit there.\n")
    f.write(f"# Music 'Invincible' - Deaf Kev (TikTok CML, song_clip_id 6761071663921498114), not in git. Track grid t_k = {DROP} + {P} k; drop = video {tb(LEAD):.3f} s.\n")
    yaml.safe_dump(proj, f, sort_keys=False, width=200)
json.dump(overlay, open(os.path.join(OUT, "overlay.json"), "w"), indent=1)
json.dump(webzoom, open(os.path.join(OUT, "webzoom.json"), "w"), indent=1)
print("total %.3f s, cuts" % (total_f / FPS), [round(c, 3) for c in cuts])
