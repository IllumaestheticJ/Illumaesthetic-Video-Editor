"""edl.json -> Remotion props for the HudRail strip and the per-cue cards (lexus-is350-speedrun-long)."""
import json, sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "projects/lexus-is350-speedrun-long")
FPS = 23.976
edl = json.loads((P / "edl.json").read_text())
HIDE_DERIVED = True  # clock_known=false timers render as "running, no digits"


def sec(s):
    m, x = s.split(":")
    return int(m) * 60 + int(x)


def tstate(ev, key, prev):
    h = ev["hud"]
    a, b = h.get(key + "_start"), h.get(key + "_end")
    if "not started" in h.get("basis", "") and key == "clock1":
        return {"k": "notstarted"}
    if h.get("final"):
        return {"k": "final", "label": "32 MIN" if key == "clock1" else "20 MIN"}
    if h.get("mode") in ("overlay",) or (not h.get("clock_known") and a is None and key == "timer2"):
        return prev  # hold
    if key == "clock1" and a is None:
        return {"k": "unknown"} if ev["timeline_in"] > 100 else prev
    if a is None:
        return prev
    if not h["clock_known"] and HIDE_DERIVED:
        return {"k": "unknown"}
    return {"k": "time", "a": sec(a), "b": sec(b)}


def frozen(st):
    if st["k"] == "time":
        return {"k": "time", "a": st["b"], "b": st["b"]}
    return st


segs = []
c1 = {"k": "notstarted"}
t2 = {"k": "hidden"}
for ev in edl["events"]:
    h = ev["hud"]
    t0, t1 = ev["timeline_in"], ev["timeline_out"]
    mode = "hidden" if not h["visible"] else ("overlay" if ev["type"] == "scan" else "plate")
    chap = h.get("chapter", "")
    if h.get("final") or ev["id"] in ("E62", "E63", "E71"):
        c1 = {"k": "final", "label": "32 MIN"}
        t2 = {"k": "final", "label": "20 MIN"}
    elif ev["id"] == "E27":
        c1 = {"k": "ff", "a": 339, "b": sec("11:56")}  # 05:39 = last legible value shown in E26
    elif h["visible"]:
        if ev["type"] in ("card", "scan"):
            c1, t2 = frozen(c1), frozen(t2)
        else:
            c1n = tstate(ev, "clock1", c1)
            t2n = tstate(ev, "timer2", t2) if (h.get("timer2_start") is not None or t2["k"] != "hidden") else t2
            if h.get("timer2_start") is not None and not h["clock_known"] and HIDE_DERIVED:
                t2n = {"k": "unknown"}
            if h.get("clock1_display") and h.get("clock1_start") is None:
                c1n = {"k": "unknown"}
            c1, t2 = c1n, t2n
    seg_c1, seg_t2 = c1, t2
    entry = {"id": ev["id"], "t0": t0, "t1": t1, "mode": mode, "chapter": chap, "c1": seg_c1, "t2": seg_t2}
    # E29: TIMER 2 appears at "Now." (G06 in = 102.0)
    if ev["id"] == "E29":
        a = dict(entry, t1=102.0, t2={"k": "hidden"})
        b = dict(entry, t0=102.0, id="E29b")
        segs += [a, b]
        continue
    # E38: TIMER 2 runs 08:29 -> 08:32 until the watch stops (G07 in = 132.011), then paused
    if ev["id"] == "E38":
        a = dict(entry, t1=132.011, t2={"k": "time", "a": sec("08:29"), "b": sec("08:32")})
        b = dict(entry, t0=132.011, id="E38b", t2={"k": "paused", "a": sec("08:32"), "b": sec("08:32")})
        t2 = b["t2"]
        segs += [a, b]
        continue
    if t2["k"] == "time" and ev["id"] in ("E39", "E40", "E42"):
        entry["t2"] = t2 = {"k": "paused", "a": sec("08:32"), "b": sec("08:32")}
    # E41 scan insert inside the pause keeps paused; after E42 timer resumes (E43 is 08:46)
    if ev["id"] == "E41":
        entry["t2"] = t2 = {"k": "paused", "a": sec("08:32"), "b": sec("08:32")}
    segs.append(entry)
    # E5-E7 (bet): clock shown compact with the prediction tally

# conclusion_edl.json replaces E71: rail visible until CON_05 (scan), hidden from there
cp = P / "conclusion_edl.json"
con = json.loads(cp.read_text()) if cp.exists() else None
if con:
    i = next(i for i, x in enumerate(segs) if x["id"] == "E71")
    e71 = segs[i]
    cut = next(e for e in con["events"] if e["id"] == "CON_05")["timeline_in"]
    segs[i:i + 1] = [dict(e71, t1=cut, id="E71/CON_01-04"), dict(e71, t0=cut, id="CON_05", mode="hidden")]
# merge nothing; chips and crash marker are event-time based
chips = [
    {"text": "2 HR", "t0": 12.6, "hl": False},
    {"text": "30 MIN", "t0": 14.55, "hl": False},
    {"text": "15 MIN", "t0": 15.65, "hl": True},
]
rail = {
    "fps": FPS, "width": 1920, "height": 160,
    "durationInFrames": round(edl["stats"]["total"] * FPS),
    "segments": segs, "chips": chips, "chipsOut": 22.0,
    "crash": [79.0, 91.2], "ffCard": [88.2, 91.2], "timer2Appear": 102.0,
}
(P / "gfx_rail_props.json").write_text(json.dumps(rail, indent=1))
print("rail frames", rail["durationInFrames"], "segments", len(segs))
for s in segs[:0]:
    print(s)

cues = {c["id"]: c for c in edl["gfx_cues"]}
out = {}
for cid, c in cues.items():
    if cid in ("G02", "G06", "G07", "G14", "RAIL_CAP"):
        continue
    extra = {"G01": {"pos": "lower3", "plate": True}, "G10": {"pos": "bl"}, "G11": {"pos": "bl"},
             "G12": {"pos": "top"}, "G13": {"pos": "top"}, "G08": {"row2At": 80}}.get(cid, {})
    out[cid] = {**extra, "comp": "ScanLabel" if cid in ("G01", "G10", "G11", "G12", "G13") else "GfxCard", "cue": cid, "in": c["timeline_in"], "out": c["timeline_out"],
                "frames": round((c["timeline_out"] - c["timeline_in"]) * FPS),
                "text": c["text"].replace("HOW FAST CAN WE ", "HOW FAST CAN WE\n") if cid == "G01" else c["text"], "sub": c.get("sub", "")}
if con:
    for c in con["gfx_cues"]:
        if c["id"] in ("CON_G1", "CON_G2", "CON_G3"):
            g3 = c["id"] == "CON_G3"
            out[c["id"]] = {**({"pos": "bl"} if g3 else {}), "comp": "ScanLabel" if g3 else "GfxCard", "cue": c["id"], "in": c["timeline_in"],
                            "out": c["timeline_out"], "frames": round((c["timeline_out"] - c["timeline_in"]) * FPS),
                            "text": c["text"], "sub": c.get("sub") or ""}
(P / "gfx_cards_props.json").write_text(json.dumps(out, indent=1))
print(list(out))
