"""IS350 reels: timelines (single source of truth), music assembly, gfx props, captions.

Every reel is a list of shots on a 30 fps reel timeline. Times are seconds; frame of a cut = round(t*30).
Imported by build.py and qa.py. Run directly to print the timelines:  python tools/reels.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
SPANS = json.loads((PROJ / "spans.json").read_text())["spans"]
W = Path("/home/user/media/work/is350-reels")
SRC, BUILD, OUT, REND, MUS = W / "src", W / "build", W / "out", W / "renders", W / "music"
FPS = 30
SRC_FPS = 24000 / 1001
CTA = "SCANS AVAILABLE AT\nILLUMAESTHETIC.COM"
NAMES = {"R1": "is350_reel_R1_crash", "R2": "is350_reel_R2_real_to_scan", "R3": "is350_reel_R3_how_long"}

# ---------------------------------------------------------------- captions (source clock; word times from large-v3 / medium.en
# and the 10-20 ms energy envelope; corrected text). (text, src_t0, src_t1)
CAPS = {
    "R1_BET": [("I think I can do it in less than", 26.26, 27.72), ("the length of a YouTube video.", 27.72, 29.30), ("15 minutes.", 29.62, 30.45)],
    "R1_GO": [("Yeah. Three, two, one...", 71.55, 74.20), ("Go!", 74.39, 74.95)],
    "R1_CRASH": [("How you feeling halfway through it?", 376.94, 379.28), ("It just crashed.", 379.38, 380.70),
                 ("It's never crashed on me before.", 380.80, 383.15)],
    "R1_NOW": [("Start a secondary timer.", 12.60, 13.85), ("Now.", 13.95, 14.65)],
    "R1_TIMEA": [("20 minutes.", 9.70, 10.85)],
    "R1_TIMEB": [("And the other one,", 13.60, 14.45), ("32 minutes.", 14.53, 17.35)],
    "R3_QAUD": [("How long do you think it'll take", 15.00, 16.54), ("to scan this car?", 16.54, 17.42)],
    "R3_2H": [("I'll say two hours.", 17.50, 18.75)],
    "R3_30": [("Maybe 30 minutes.", 22.16, 23.30)],
    "R3_15": [("15 minutes.", 29.62, 30.65)],
    "R3_OPT": [("Is this the most optimal", 122.30, 124.11), ("scanning position?", 124.11, 125.45), ("Yeah.", 125.55, 126.05)],
    "R3_TIME": [("Time.", 7.33, 8.35)],
}
# word spans that must stay audible (dialogue protection + ducking): derived from CAPS
CLOCK1_541 = 74.57  # CLOCK 1 = FX30541 src - 74.57 (phone 00:00.43 at 75.0; 04:58.86 at 373.4)
CLOCK1_542 = 716.75  # CLOCK 1 = FX30542 src + 716.75 (phone 12:20.75 at 542@24)


def S(span, t0, t1, kind="irl", audio=None, audio_span=None, end_on_match=False, gain_db=0.0, scan=None, scan_from=0.0):
    return dict(span=span, t0=t0, t1=t1, kind=kind, audio=audio, audio_span=audio_span, end_on_match=end_on_match,
                gain_db=gain_db, scan=scan, scan_from=scan_from)


def r1():
    bet0, go0 = 0.0, 4.45
    go_on = go0 + (74.39 - 71.45)                     # "go" onset on the reel = 7.39
    # wind-up beats (agent's stem: speed 1.0 -> 1.5 over 8 s, last 6.48 s used): cut times inside it are snapped by build
    crash0 = 10.85
    crashed = crash0 + (379.72 - 376.70)              # 13.87 = DEAD STOP
    now0 = crash0 + (383.25 - 376.70)                 # 17.40
    t_now = now0 + (13.95 - 12.40)                    # 18.95 = comeback drop
    ta = t_now + 0.8; tb = t_now + 2.4; res = t_now + 6.8; logo = t_now + 9.6; end = logo + 1.6
    shots = [
        S("R1_BET", bet0, go0), S("R1_GO", go0, 8.05), S("R1_SPRAY", 8.05, 9.25, gain_db=-16), S("R1_SCAN", 9.25, crash0, gain_db=-16),
        S("R1_CRASH", crash0, now0), S("R1_NOW", now0, ta), S("R1_TIMEA", ta, tb), S("R1_TIMEB", tb, res),
        S(None, res, logo, kind="scan", scan="V_RES_FULL"), S(None, logo, end, kind="logo"),
    ]
    anchors = dict(go=go_on, crashed=crashed, now=t_now, res=res, logo=logo, end=end, music0=go_on - 6.4)
    sh = {s["span"]: s for s in shots if s["span"]}

    def rt(span, src):  # reel time of a source time inside a shot
        return sh[span]["t0"] + (src - SPANS[span]["a"])
    c = lambda span, a, b: dict(rows=[{"label": "CLOCK 1", "v0": a, "v1": b}])
    items = [
        {"kind": "title", "t0": 0, "t1": go0, "lines": ["HOW LONG TO 3D-SCAN", "A WHOLE CAR?"]},
        {"kind": "pills", "t0": rt("R1_BET", 29.62), "t1": go0, "y": 1200, "pills": [{"text": "THE BET: 15 MIN", "at": rt("R1_BET", 29.62), "hl": True}]},
        {"kind": "clock", "t0": go_on, "t1": 8.05, "fadeIn": True, "rows": [{"label": "CLOCK 1", "v0": 0, "v1": 75.05 - CLOCK1_541}]},
        {"kind": "clock", "t0": 8.05, "t1": 9.25, "rows": [{"label": "CLOCK 1", "v0": 120.30 - CLOCK1_541, "v1": 121.50 - CLOCK1_541}]},
        {"kind": "clock", "t0": 9.25, "t1": crash0, "rows": [{"label": "CLOCK 1", "v0": 322.0 - CLOCK1_541, "v1": 323.6 - CLOCK1_541}]},
        {"kind": "clock", "t0": crash0, "t1": now0, "red": True, "pill": "CRASHED", "pillAt": crashed,
         "rows": [{"label": "CLOCK 1", "v0": 376.70 - CLOCK1_541, "v1": 383.25 - CLOCK1_541}]},
        {"kind": "clock", "t0": now0, "t1": t_now, "rows": [{"label": "CLOCK 1", "v0": 12.40 + CLOCK1_542, "v1": 13.95 + CLOCK1_542}]},
        {"kind": "tag", "t0": now0, "t1": t_now, "text": "SCANNER REBOOTED", "y": 420},
        {"kind": "clock", "t0": t_now, "t1": ta, "rows": [{"label": "TIMER 2", "v0": 0, "v1": 14.75 - 13.95},
                                                          {"label": "CLOCK 1", "v0": 13.95 + CLOCK1_542, "v1": 14.75 + CLOCK1_542}]},
        {"kind": "clock", "t0": ta, "t1": rt("R1_TIMEB", 14.53), "rows": [{"label": "TIMER 2", "v0": 0, "text": "20:24"}]},
        {"kind": "clock", "t0": rt("R1_TIMEB", 14.53), "t1": res, "rows": [{"label": "TIMER 2", "v0": 0, "text": "20:24"},
                                                                            {"label": "CLOCK 1", "v0": 0, "text": "32:53"}]},
        {"kind": "result", "t0": res, "t1": logo, "y": 250, "rows": [
            {"value": "32 MIN", "label": "FROM GO", "at": res}, {"value": "20 MIN", "label": "WITHOUT THE CRASH", "at": res + 0.4}],
         "footer": {"text": "THE BET WAS 15", "at": res + 1.2}},
        {"kind": "logo", "t0": logo, "t1": end, "cta": CTA},
    ]
    music = dict(kind="R1", anchors=anchors)
    return dict(id="R1", shots=shots, items=items, music=music, anchors=anchors, end=end)


def r2():
    b = 1.6217
    t = [0, b, 2 * b, 3 * b, 4 * b, 5 * b, 6 * b, 8 * b]   # 12.9739 = D2 after the 8-beat cut
    d2 = t[7]; q = 0.405433
    v1 = d2 + 6 * q; logo = v1 + 6 * q; end = logo + 1.6
    shots = [
        S("R2_REAR", t[0], t[1], end_on_match=True), S(None, t[1], t[2], kind="scan", scan="V_MATCH_REAR"),
        S("R2_P2", t[2], t[3], end_on_match=True), S(None, t[3], t[4], kind="scan", scan="V_PAIR_2"),
        S("R2_P3", t[4], t[5], end_on_match=True), S(None, t[5], t[6], kind="scan", scan="V_PAIR_3"),
        S("R2_FRONT", t[6], d2, end_on_match=True), S(None, d2, v1, kind="scan", scan="V_MATCH_FRONT"),
        S(None, v1, logo, kind="scan", scan="V_RES_FULL"), S(None, logo, end, kind="logo"),
    ]
    items = [
        {"kind": "title", "t0": 0, "t1": t[2] - 0.2, "lines": ["REAL CAR", "→ 3D SCAN"]},
        {"kind": "label", "t0": v1 + 0.2, "t1": logo, "y": 1290, "text": "LEXUS IS350 · FULL SCAN", "sub": "32 MIN FROM GO · 20 WITHOUT THE CRASH"},
        {"kind": "logo", "t0": logo, "t1": end, "cta": CTA},
    ]
    anchors = dict(d1=b, d2=d2, logo=logo, end=end, cut_from=6 * b, cut_to=8 * b)
    return dict(id="R2", shots=shots, items=items, music=dict(kind="R2", anchors=anchors), anchors=anchors, end=end)


def r3():
    p = 0.68961
    k = lambda n: round(n * p, 4)
    shots = [S("R3_QPIC", 0, k(4), audio_span="R3_QAUD"), S("R3_2H", k(4), k(6)), S("R3_30", k(6), k(8), audio="fadein2"), S("R3_15", k(8), k(10))]
    for i, m in enumerate(["R3_M1", "R3_M2", "R3_M3", "R3_M6", "R3_M4", "R3_M7", "R3_M5"]):
        shots.append(S(m, k(10 + i), k(11 + i), gain_db=-18))
    hit, logo = k(28), k(36)
    shots += [S("R3_OPT", k(17), k(23)), S("R3_TIME", k(23), k(25)), S("R3_FRONT", k(25), hit, end_on_match=True),
              S(None, hit, k(31), kind="scan", scan="V_MATCH_FRONT"), S(None, k(31), logo, kind="scan", scan="V_RES_FULL"),
              S(None, logo, logo + 1.6, kind="logo")]
    sh = {s["span"]: s for s in shots if s["span"]}
    rt = lambda span, src: sh[span]["t0"] + (src - SPANS[span]["a"])
    r = k(31)
    items = [
        {"kind": "title", "t0": 0, "t1": k(10), "lines": ["HOW LONG DOES IT", "TAKE TO 3D-SCAN", "A WHOLE CAR?"]},
        {"kind": "pills", "t0": rt("R3_2H", 17.70), "t1": k(10), "y": 1200, "pills": [
            {"text": "2 HOURS?", "at": rt("R3_2H", 17.70)}, {"text": "30 MIN?", "at": rt("R3_30", 22.24)},
            {"text": "15 MIN", "at": rt("R3_15", 29.62), "hl": True}]},
        {"kind": "result", "t0": r, "t1": logo, "y": 240, "rows": [
            {"value": "32 MIN", "label": "FROM GO", "at": r}, {"value": "20 MIN", "label": "WITHOUT THE CRASH", "at": k(32)}],
         "footer": {"text": "THE BET WAS 15", "at": k(33)}},
        {"kind": "logo", "t0": logo, "t1": logo + 1.6, "cta": CTA},
    ]
    anchors = dict(hit=hit, mute0=k(27), logo=logo, end=logo + 1.6)
    return dict(id="R3", shots=shots, items=items, music=dict(kind="R3", anchors=anchors), anchors=anchors, end=logo + 1.6)


REELS = {"R1": r1, "R2": r2, "R3": r3}


def captions(reel):
    """Caption items on the reel clock, clipped to their shot; never before the first word."""
    out = []
    for s in reel["shots"]:
        aspan = s["audio_span"] or s["span"]
        if not aspan or aspan not in CAPS:
            continue
        a = SPANS[aspan]["a"]
        for text, c0, c1 in CAPS[aspan]:
            t0, t1 = s["t0"] + (c0 - a), min(s["t1"], s["t0"] + (c1 - a))
            if t1 - t0 > 0.1:
                out.append({"kind": "cap", "t0": round(t0, 4), "t1": round(t1, 4), "lines": wrap(text)})
    return out


def wrap(text, n=28):
    if len(text) <= n:
        return [text]
    words, best = text.split(), None
    for i in range(1, len(text.split())):
        l1, l2 = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(l1), len(l2))
        if best is None or score < best[0]:
            best = (score, [l1, l2])
    return best[1]


def speech_spans(reel):
    """(t0, t1) on the reel clock where a kept line is spoken (for ducking and the dialogue check)."""
    return [(c["t0"], c["t1"]) for c in captions(reel)]


if __name__ == "__main__":
    for rid, fn in REELS.items():
        r = fn()
        print(rid, "end", round(r["end"], 3), {k: round(v, 3) for k, v in r["anchors"].items()})
        for s in r["shots"]:
            print("  ", f"{s['t0']:7.3f}-{s['t1']:7.3f}", round(s["t1"] - s["t0"], 3), s["kind"], s["span"] or s["scan"] or "")
