#!/usr/bin/env python3
"""v2 graphics props generator (overlays on full-frame footage).

  python scripts/gen_gfx_v2.py [--project projects/lexus-is350-speedrun-long] [--timeline timeline_v2.json]

Reads edl_v2.json (hud values, cue anchors) and, if given/present, timeline_v2.json (the editor's beat-snapped
event times: events[] with id, tl_in|timeline_in, tl_out|timeline_out, src_in, src_out). Clock values shift with
src_in/src_out, cues are anchored to events (and to source-time anchors inside events), so a re-run follows the snap.
Writes gfx_v2_hud_props.json and gfx_v2_cues_props.json into the project folder.
Corner per event: gfx_v2_corners.json (decided from a frame of every source clip), default = edl hud.corner.
"""
import argparse, json
from pathlib import Path

FPS = 23.976
ap = argparse.ArgumentParser()
ap.add_argument("--project", default="projects/lexus-is350-speedrun-long")
ap.add_argument("--timeline", default=None)
ap.add_argument("--ver", default="v2", help="output suffix: props gfx_<ver>_*.json, clip names *_<ver>")
a = ap.parse_args()
P = Path(a.project)
edl = json.loads((P / "edl_v2.json").read_text())
tlp = Path(a.timeline) if a.timeline else (P / f"timeline_{a.ver}.json")
tl = {}
if tlp.exists():
    for e in json.loads(tlp.read_text()).get("events", []):
        tl[e["id"]] = e
    print("timeline:", tlp, len(tl), "events")
else:
    print("timeline_v2.json not found: using edl_v2 times")
corners = json.loads((P / "gfx_v2_corners.json").read_text())["corners"] if (P / "gfx_v2_corners.json").exists() else {}

EV = {}
ORDER = []
edl_by = {e["id"]: e for e in edl["events"]}
stub_hud = {"visible": False, "corner": "TR", "chapter": ""}
order_src = [e["id"] for e in sorted(tl.values(), key=lambda x: x.get("tl_in", x.get("timeline_in", 0)))] if tl else [e["id"] for e in edl["events"]]
for eid in order_src:
    e = edl_by.get(eid)
    t = tl.get(eid, {})
    if e is None:  # event the editor added/renamed (not in edl_v2): hidden HUD stub, times from the timeline
        print("WARN: event", eid, "not in edl_v2: HUD hidden over it")
        e = {"id": eid, "type": t.get("type", "irl"), "hud": stub_hud, "src_in": t.get("src_in"), "src_out": t.get("src_out"),
             "timeline_in": t.get("tl_in", 0), "timeline_out": t.get("tl_out", 0)}
    ti = t.get("tl_in", t.get("timeline_in", e["timeline_in"]))
    to = t.get("tl_out", t.get("timeline_out", e["timeline_out"]))
    si = t.get("src_in", e.get("src_in"))
    so = t.get("src_out", e.get("src_out"))
    EV[eid] = dict(e, src_map=t.get("src_map"), tin=ti, tout=to, sin=si, sout=so, d_in=(si - e["src_in"]) if si is not None and e.get("src_in") is not None else 0.0,
                   d_out=(so - e["src_out"]) if so is not None and e.get("src_out") is not None else 0.0)
    ORDER.append(eid)
for eid in edl_by:
    if tl and eid not in tl:
        print("WARN: edl event", eid, "is not in the timeline: skipped")
TOTAL = max(v["tout"] for v in EV.values())


class Missing(Exception):
    pass


def srcT(eid, s):
    if eid not in EV:
        print("WARN: srcT on missing event", eid)
        return float("nan")
    e = EV[eid]
    return e["tin"] + (s - e["sin"])


def sec(s):
    m, x = s.split(":")
    return int(m) * 60 + int(x)


def clock(d, e, key):
    """edl hud clock dict -> Remotion ClockState."""
    if d is None:
        return {"k": "hidden"}
    s0, s1 = d.get("start"), d.get("end")
    if s0 is None:
        return {"k": "unknown"}
    if "MIN" in s0:
        return {"k": "final", "label": s0}
    return {"k": "time", "a": sec(s0) + e["d_in"], "b": sec(s1) + e["d_out"]}


def frozen(st):
    return {"k": "time", "a": st["b"], "b": st["b"]} if st["k"] == "time" else st


segs = []


def add(e, t0, t1, **kw):
    h = e["hud"]
    seg = {"id": kw.pop("sid", e["id"]), "t0": t0, "t1": t1, "visible": bool(h.get("visible")), "corner": corners.get(e["id"], h.get("corner", "TR")),
           "chapter": h.get("chapter", ""), "c1": {"k": "hidden"}, "t2": {"k": "hidden"}}
    seg.update(kw)
    segs.append(seg)
    return seg


RED_IDS = ("C_02", "C_03", "C_04", "C_05")
prev_c1 = {"k": "notstarted"}
prev_t2 = {"k": "hidden"}
for eid in ORDER:
    e = EV[eid]
    h = e["hud"]
    t0, t1 = e["tin"], e["tout"]
    if not h.get("visible"):
        add(e, t0, t1)
        continue
    c1 = clock(h.get("clock1"), e, "c1") if "clock1" in h else frozen(prev_c1)
    t2 = clock(h.get("timer2"), e, "t2") if "timer2" in h else frozen(prev_t2)
    if "clock1" not in h and eid != "C_07":
        c1 = frozen(prev_c1)
    extra = {}
    if eid in ("CO_01", "B_01", "B_02"):
        c1 = {"k": "notstarted"}
    if eid in RED_IDS:
        extra.update(red=True, pill="● STILL RUNNING")
    if eid == "C_03":  # card: clock keeps counting 05:09 -> 05:10; glitch for the first 6 frames
        c1 = {"k": "time", "a": prev_c1["b"], "b": prev_c1["b"] + 1}
        g = 6 / FPS
        add(e, t0, t0 + g, c1=c1, t2=t2, glitch=True, sid="C_03a", **extra)
        add(e, t0 + g, t1, c1=c1, t2=t2, sid="C_03b", **extra)
        prev_c1 = c1
        continue
    if eid == "C_02":
        extra["glitch"] = True
    if eid == "C_07":  # card carries the big fast-forward clock; HUD keeps only the chapter tag
        c1 = {"k": "ff", "a": prev_c1["b"], "b": sec("11:56")}
        add(e, t0, t1, c1=c1, t2=t2, hideClock=True)
        prev_c1 = {"k": "time", "a": sec("11:56"), "b": sec("11:56")}
        continue
    if eid == "P_05":
        extra["glyph"] = ">> 20x"
        if e.get("src_map"):  # speed-ramped time-lapse: true clock per timeline frame (541: clock = src - 74.6)
            c1 = {"k": "map", "vals": [round(v - 74.6, 3) for v in e["src_map"]]}
    if eid == "P_01":  # grey until "go" (src 74.6)
        tg = srcT(eid, 74.6)
        add(e, t0, tg, c1={"k": "notstarted"}, t2=t2, sid="P_01a")
        add(e, tg, t1, c1={"k": "time", "a": 0, "b": 0}, t2=t2, sid="P_01b")
        prev_c1 = {"k": "time", "a": 0, "b": 0}
        continue
    if eid == "C_08":  # TIMER 2 appears at "Now." (src 13.0)
        ta = srcT(eid, 13.0)
        def piece(x0, x1):
            va = c1["a"] + (c1["b"] - c1["a"]) * (x0 - t0) / (t1 - t0)
            vb = c1["a"] + (c1["b"] - c1["a"]) * (x1 - t0) / (t1 - t0)
            return {"k": "time", "a": va, "b": vb}
        add(e, t0, ta, c1=piece(t0, ta), t2={"k": "hidden"}, sid="C_08a")
        add(e, ta, ta + 2.5, c1=piece(ta, ta + 2.5), t2={"k": "time", "a": 0, "b": 2}, sub="AFTER REBOOT", sid="C_08b")
        add(e, ta + 2.5, t1, c1=piece(ta + 2.5, t1), t2={"k": "time", "a": 2, "b": sec(h["timer2"]["end"])}, sid="C_08c")
        prev_c1, prev_t2 = c1, {"k": "time", "a": sec(h["timer2"]["end"]), "b": sec(h["timer2"]["end"])}
        T2_APPEAR = ta
        continue
    if eid == "T_07":  # watch stops at src 56.0 (G07): TIMER 2 08:29 -> 08:32 then paused
        ts = srcT(eid, 56.0)
        add(e, t0, ts, c1=c1, t2={"k": "time", "a": sec("08:29"), "b": sec("08:32")}, sid="T_07a")
        add(e, ts, t1, c1=c1, t2={"k": "paused", "a": sec("08:32"), "b": sec("08:32")}, sid="T_07b")
        prev_c1, prev_t2 = c1, {"k": "paused", "a": sec("08:32"), "b": sec("08:32")}
        continue
    if eid == "T_08":
        t2 = {"k": "paused", "a": sec("08:32"), "b": sec("08:32")}
    if eid == "TM_01":  # exact legible anchors: watch 20:24.95 at src 9.0, phone 32:53.18 at src 16.14, owner numbers at src 17.6
        s_in = e["sin"]
        c0, w0 = 32 * 60 + 53.18 - (16.14 - s_in), 20 * 60 + 24.95 - (9.0 - s_in)
        ta, tb, tf = srcT(eid, 9.0), srcT(eid, 16.14), srcT(eid, 17.6)
        c_9 = c0 + (9.0 - s_in)
        add(e, t0, ta, c1={"k": "time", "a": c0, "b": c_9}, t2={"k": "time", "a": w0, "b": 20 * 60 + 24.95}, sid="TM_01a")
        add(e, ta, tb, c1={"k": "time", "a": c_9, "b": 32 * 60 + 53.18}, t2={"k": "time", "a": 20 * 60 + 24.95, "b": 20 * 60 + 24.95}, sid="TM_01b")
        add(e, tb, tf, c1={"k": "time", "a": 32 * 60 + 53.18, "b": 32 * 60 + 53.18}, t2={"k": "time", "a": 20 * 60 + 24.95, "b": 20 * 60 + 24.95}, sid="TM_01c")
        add(e, tf, t1, c1={"k": "final", "label": "32 MIN"}, t2={"k": "final", "label": "20 MIN"}, sid="TM_01d")
        prev_c1, prev_t2 = {"k": "final", "label": "32 MIN"}, {"k": "final", "label": "20 MIN"}
        continue
    if h.get("clock1") is None and "clock1" in h:
        c1 = {"k": "unknown"}
    add(e, t0, t1, c1=c1, t2=t2, **extra)
    if c1["k"] != "hidden":
        prev_c1 = c1
    if t2["k"] != "hidden":
        prev_t2 = t2

try:
    T2_APPEAR
except NameError:
    T2_APPEAR = 1e9

# monotone, gap-free: extend each segment's end to the next start (timeline is contiguous in the EDL)
segs.sort(key=lambda s: s["t0"])
for i in range(len(segs) - 1):
    segs[i]["t1"] = segs[i + 1]["t0"]

chips = [
    {"text": "2 HR", "t0": srcT("CO_01", 18.0), "hl": False},
    {"text": "30 MIN", "t0": srcT("B_01", 22.4), "hl": False},
    {"text": "15 MIN", "t0": srcT("B_02", 29.7), "hl": True},
]
chips = [c for c in chips if c["t0"] == c["t0"]]
hud = {"fps": FPS, "width": 1920, "height": 270, "durationInFrames": round(TOTAL * FPS), "segments": segs, "chips": chips,
       "chipsOut": EV["B_02"]["tout"] if "B_02" in EV else 0, "t2Appear": T2_APPEAR, "plateAlpha": 0.55}
(P / f"gfx_{a.ver}_hud_props.json").write_text(json.dumps(hud, indent=1))
print("HUD frames", hud["durationInFrames"], "segments", len(segs))

# ---- per-cue clips ----
cues = []


def cue(cid, comp, t_in, t_out, file, alpha, place, **props):
    if t_in is None or t_out is None or t_in != t_in or t_out != t_out:
        print("WARN: cue", cid, "skipped (anchor event missing)")
        return
    fr = round((t_out - t_in) * FPS)
    file = file.replace("_v2.", f"_{a.ver}.") if "_v2." in file else (file.replace("_C02.", f"_C02_{a.ver}.") if file.startswith("FX_") else file)
    cues.append({"cue": cid, "comp": comp, "file": file, "alpha": alpha, "in": round(t_in, 3), "out": round(t_out, 3), "frames": fr, "placement": place,
                 "props": {"cue": cid, "frames": fr, **props}})


g = {c["id"]: c for c in edl["gfx_cues"]}
class _EV(dict):
    def __missing__(self, k):
        print("WARN: missing event", k)
        return {"tin": float("nan"), "tout": float("nan")}


ev = _EV(EV)


def A(x, off=0.0):
    return None if x is None else x + off
# title overlay: the hook question lands in the bet footage (CO_03 scan tease was removed): first 3 s of B_02 (host, clear left wall), fallback B_01
hook = "B_02" if "B_02" in EV else ("B_01" if "B_01" in EV else None)
if hook:
    cue("G01_v2", "CueV2", ev[hook]["tin"] + 0.25, ev[hook]["tin"] + 3.25, "G01_v2.mov", True, f"lower-left x60-720 y520 (plate) over {hook}", text="HOW FAST CAN WE\n3D-SCAN AN\nENTIRE CAR?", sub=g["G01_v2"]["sub"], x=60, y=500, w=640)
else:
    print("WARN: G01_v2 skipped (no B_02/B_01)")
cue("G03_v2", "CueV2", ev["B_02"]["tout"] - 0.85, ev["B_02"]["tout"], "G03_v2.mov", True, "lower-left x80-900 y640 (plate)", text=g["G03_v2"]["text"], x=80, y=640, w=820)
cue("STING1_v2", "CueV2", ev["P_03"]["tin"], ev["P_03"]["tin"] + 1.6, "STING1_v2.mov", True, "lower-left x80-900 y700 (plate, slides in/out)", text="PART 1 · SPRAY", x=80, y=700, w=860)
cue("STING2_v2", "CueV2", ev["Q_01"]["tin"], ev["Q_01"]["tin"] + 1.6, "STING2_v2.mov", True, "same as STING1_v2", text="PART 2 · SCAN", x=80, y=700, w=860)
cue("G_SPRAY_v2", "CueV2", ev["P_06"]["tin"] + 0.298, ev["P_07"]["tout"], "G_SPRAY_v2.mov", True, "lower-right x1020-1840 y640 (plate)", text=g["G_SPRAY_v2"]["text"], x=1020, y=640, w=820, align="right")
try:
    g8in = srcT("TM_01", 13.2)
    cue("G08_v2", "CueV2", g8in, ev["TM_01"]["tout"], "G08_v2.mov", True, "lower-left x60-620 y560 (narrower than x80-900 to stay clear of the phone at src 16)", text=g["G08_v2"]["text"][:1] + ['TIMER 2 · RESTARTED AFTER THE CRASH · 20 MIN'],
        x=60, y=560, w=560, beats=[round((srcT("TM_01", 14.4) - g8in) * FPS), round((srcT("TM_01", 17.2) - g8in) * FPS)])
except ValueError:
    print("WARN: G08_v2 skipped (anchor missing)")
cue("G09_v2", "CueV2", ev["TM_02"]["tin"], ev["TM_02"]["tout"], "G09_v2.mov", True, "lower-left x80-900 y640 (plate)", text=g["G09_v2"]["text"], sub=g["G09_v2"]["sub"], x=80, y=640, w=820)
cue("G10_v2", "ScanLabel", ev["M6"]["tin"] + 1.0, ev["M6"]["tout"] - 0.3, "G10_v2.mov", True, "bottom-left over black, halo", text=g["G10_v2"]["text"], sub=g["G10_v2"]["sub"], pos="bl", plate=False, bottom=44)
try:
    # edl_v2: from src 13.75 to end -1.65 s. The editor may play CON_01 shorter (fallback cut), so keep >= 3 s and end with the event.
    c1in = max(ev["CON_01"]["tin"], min(srcT("CON_01", 13.75), ev["CON_01"]["tout"] - 3.2))
    c1out = ev["CON_01"]["tout"] if srcT("CON_01", 13.75) > ev["CON_01"]["tout"] - 3.2 else ev["CON_01"]["tout"] - 1.65
    c1out = min(c1out, c1in + 5.2)  # v4 (editor): the long CON_01 is the host to camera - show the answer ~5 s, then leave
    nf = round((c1out - c1in) * FPS)
    cue("CON_G1_v2", "CueV2", c1in, c1out, "CON_G1_v2.mov", True, "top-left x60-760 y60 (plates; sky is bright)", text=g["CON_G1_v2"]["text"], x=60, y=60, w=700, beats=[0, round(nf * 0.3), round(nf * 0.62)])
except ValueError:
    print("WARN: CON_G1_v2 skipped (anchor missing)")
# CTA wording per owner (was "LINK IN THE DESCRIPTION"); text is split at the domain: small line above, large mono domain
cue("CON_G3_v2", "CueV2", ev["CON_02"]["tin"] + 3.5, ev["CON_02"]["tout"], "CON_G3_v2.mov", True, "lower-left x80 y840 (content-sized plate) over black below the car", text="SCANS AVAILABLE AT ILLUMAESTHETIC.COM", x=80, y=840, w=900)
cue("G05a_v2", "CardV2", ev["C_03"]["tin"], ev["C_03"]["tout"], "G05a_v2.mp4", False, "BLACK CARD 1/3 full frame; HUD overlay stays on top", text=g["G05a_v2"]["text"])
cue("G05b_v2", "CardV2", ev["C_07"]["tin"], ev["C_07"]["tout"], "G05b_v2.mp4", False, "BLACK CARD 2/3 full frame; carries the big CLOCK 1 fast-forward (HUD shows chapter tag only)", text=g["G05b_v2"]["text"], **{"from": EV["C_06"]["hud"] and sec(EV["C_06"]["hud"]["clock1"]["end"]) , "to": sec("11:56")})
cue("G15_v2", "CardV2", ev["END"]["tin"], ev["END"]["tout"], "G15_v2.mp4", False, "BLACK CARD 3/3 end card, logo 900 px", text="ILLUMAESTHETIC")
if "RESULTS_CARD" in EV:
    cue("G_RESULTS_v3", "CardV2", ev["RESULTS_CARD"]["tin"], ev["RESULTS_CARD"]["tout"], "G_RESULTS_v3.mp4", False, "BLACK CARD full frame: RESULTS PREVIEW, HUD hidden", text="RESULTS PREVIEW")
cue("FX_GLITCH_C02", "FxGlitch", ev["C_02"]["tin"], ev["C_02"]["tout"], "FX_GLITCH_C02.mov", True, "full-frame glitch treatment over the frozen picture (scanlines, red edge, tear bands); editor adds RGB split + desaturate on the picture", text="")
(P / f"gfx_{a.ver}_cues_props.json").write_text(json.dumps(cues, indent=1))
print(len(cues), "cues")
