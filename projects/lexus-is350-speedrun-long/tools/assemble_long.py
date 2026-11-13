"""L1 long-form assembler (IS350 speed run, 1920x1080, 23.976 fps). Resumable; re-run to pick up finished scan renders.

    python projects/lexus-is350-speedrun-long/tools/assemble_long.py            # plan + video + audio + master
    python .../assemble_long.py plan                                            # only timeline.json
    python .../assemble_long.py video|audio|master|check

Inputs (read-only): edl.json, conclusion_edl.json (Version A replaces E71), scan_shots.md, gfx/*, music/mix_full.wav,
footage. Editorial settings: tools/editor.json (crops, blur tracks, music map). Output: timeline.json (project dir) and
/home/user/media/work/is350-long/out/{is350_long_v1_rough.mp4, stems/*.wav, mix.wav}.

Per event a picture segment is rendered (IRL graded with the FX3A S-Log3->709 LUT, cropped to 1920x920, blurred,
rail composited at y=920 from HUD_RAIL.mov retimed per event; scans full frame; cards full frame; alpha labels) and
cached under build/seg/<id>.mp4 with a key. Only changed segments re-render; the final is a stream-copy concat of the
segments (all x264 crf 18, same params) muxed with the AAC mix, so a scan render landing costs one segment + remux.
"""
from __future__ import annotations

import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import music_grid as mg  # noqa: E402

FPS = 24000 / 1001
REPO = Path("/home/user/Illumaesthetic-Video-Editor")
P = REPO / "projects/lexus-is350-speedrun-long"
W = Path("/home/user/media/work/is350-long")
B = W / "build"
OUT = W / "out"
GFX = W / "gfx"
LUT = REPO / "projects/toyota-mr2-spyder-scan-process/grade/fx3a_slog3cine_to_709.cube"
CFG = json.load(open(P / "tools/editor.json"))
NICE = ["nice", "-n", "10"]
SR = 48000


def F(t: float) -> int:
    return int(round(t * FPS + 1e-9))


def T(f: int) -> float:
    return f / FPS


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def atomic_json(path: Path, obj):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1))
    os.replace(tmp, path)


# ----------------------------------------------------------------------------------------------------------- words
_words: dict = {}


def words(clip: str) -> list:
    if clip not in _words:
        d = json.load(open(W / f"transcripts/{clip}.json"))
        _words[clip] = [(w["word"].strip(), float(w["start"]), float(w["end"])) for s in d["segments"] for w in s.get("words", [])]
    return _words[clip]


def words_in(clip, a, b):
    return [w for w in words(clip) if w[2] > a + 0.02 and w[1] < b - 0.02]


def word_onset(clip: str, approx: float) -> float:
    """Refine a Whisper word start to the speech-band energy rise (Whisper starts are often the previous word's end)."""
    src = f"/home/user/media/lexus-is350/dropbox/{clip}.MP4"
    a0 = approx - 0.25
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a0:.3f}", "-i", src, "-t", "0.6", "-ac", "1", "-ar", "16000",
                          "-af", "highpass=f=200,lowpass=f=4000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    n = 160
    e = np.sqrt(np.convolve(x ** 2, np.ones(n) / n, "same"))
    lo = np.percentile(e[: int(0.2 * 16000)], 30)
    seg = e[int(0.1 * 16000): int(0.5 * 16000)]
    pk = seg.max()
    thr = lo + 0.35 * (pk - lo)
    i = np.where(seg > thr)[0]
    return a0 + 0.1 + (i[0] / 16000 if len(i) else 0.15)


# ----------------------------------------------------------------------------------------------------------- plan
def load_events() -> list[dict]:
    edl = json.load(open(P / "edl.json"))
    con = json.load(open(P / "conclusion_edl.json"))
    drops = CFG["drop_events"]
    out, removed = [], []
    for e in edl["events"]:
        if e["id"] in drops:
            removed.append((e["timeline_in"], e["timeline_out"]))
            continue
        if e["id"] == "E71":
            out += [dict(c, section="10 CONCLUSION") for c in con["events"]]
            continue
        out.append(e)
    evs = []
    for e in out:
        shift = sum(b - a for a, b in removed if a < e["timeline_in"] - 1e-6)
        a = e.get("audio") or {}
        mode = (a.get("mode") or "").lower()
        am = "sync" if mode.startswith("sync") else ("room" if mode.startswith("room tone") else "music")
        ev = {"id": e["id"], "section": e["section"], "type": e["type"], "source": e["source"],
              "src_in": float(e["src_in"]), "src_out": float(e["src_out"]),
              "edl_in": float(e["timeline_in"]), "edl_out": float(e["timeline_out"]),
              "tl_in": float(e["timeline_in"]) - shift, "tl_out": float(e["timeline_out"]) - shift,
              "audio": am, "hud_visible": (e.get("hud") or {}).get("visible", True), "gfx": e.get("gfx") or [],
              "blur_note": e.get("blur")}
        if a.get("source_audio"):
            sa = a["source_audio"]
            ev["sync_audio"] = {"clip": Path(sa["source"]).stem, "src_in": float(sa["src_in"]), "src_out": float(sa["src_out"])}
        if ev["type"] == "irl":
            ev["clip"] = Path(ev["source"]).stem
        if ev["type"] == "scan":
            ev["shot"] = ev["source"].split()[0]
        if ev["type"] == "card":
            ev["card"] = ev["source"].split(":")[1]
        c = CFG["events"].get(ev["id"], {})
        ev.update({k: v for k, v in c.items() if k != "why"})
        evs.append(ev)
    return evs


def place_music(evs):
    """Music placements in timeline seconds. Each: piece, chunks [(tl_a, tl_b, mix_a)], gain_db, fades, grid."""
    by = {e["id"]: e for e in evs}
    A = {}
    for name, (eid, clip, approx) in CFG["anchors"].items():
        e = by[eid]
        A[name] = e["tl_in"] + (word_onset(clip, approx) - e["src_in"])
    A["title"] = by["E04"]["tl_in"]
    A["bet"] = by["E05"]["tl_in"]
    A["crashcard"] = by["E27"]["tl_in"]
    A["card32"] = by["E62"]["tl_in"]
    A["lift"] = by["E67"]["tl_in"]
    A["p7"] = by["CON_05"]["tl_in"] + CFG["music"]["p7_after_con05"]
    A["end"] = evs[-1]["tl_out"]
    grids = {}

    def grid(pid):
        if pid not in grids:
            g = CFG["music"]["grids"][pid]
            grids[pid] = mg.measure(g["a"], g["b"], g["bpm"])
        return grids[pid]

    def beat_near(pid, m, phase_bar=False):
        g = grid(pid)
        n = round((m - g["t_first"]) / g["period"])
        if phase_bar:
            n = 4 * round((n - g["downbeat_phase"]) / 4) + g["downbeat_phase"]
        b = g["t_first"] + n * g["period"]
        k = mg.nearest_attack(b, g, 0.04)
        return k if k is not None else b

    M = CFG["music"]
    pl = []
    # cold open + title: P4 late region, a bar line on the cut into the title
    m_t = beat_near("P4b", M["P4_cold_title_mix"], True)
    pl.append({"piece": "P4b", "tl_a": 0.0, "tl_b": A["bet"], "mix_at_a": m_t - A["title"], "gain_db": M["gain"]["P4"],
               "fade_in": 0.02, "fade_out": 0.03})
    # bet: P5 bed from the cut into E05 until just before "go"
    m5 = beat_near("P5", M["P5_in_mix"], True)
    pl.append({"piece": "P5", "tl_a": A["bet"], "tl_b": A["go"] - 0.04, "mix_at_a": m5, "gain_db": M["gain"]["P5"],
               "fade_in": 0.02, "fade_out": 1.0})
    # go -> crashed: P1
    m1 = beat_near("P1", M["P1_in_mix"], True)
    pl.append({"piece": "P1", "tl_a": A["go"], "tl_b": A["crashed"], "mix_at_a": m1, "gain_db": M["gain"]["P1"],
               "fade_in": 0.005, "fade_out": 0.03})
    # crash card -> "Now.": P3 sub pulse, low ("loading" pad)
    m3 = beat_near("P3", M["P3_in_mix"], True)
    pl.append({"piece": "P3", "tl_a": A["crashcard"], "tl_b": A["now"], "mix_at_a": m3, "gain_db": M["gain"]["P3"],
               "fade_in": 0.4, "fade_out": 0.03})
    # "Now." -> "Time.": P4
    m4 = beat_near("P4", M["P4_in_mix"], True)
    pl.append({"piece": "P4", "tl_a": A["now"], "tl_b": A["time"], "mix_at_a": m4, "gain_db": M["gain"]["P4"],
               "fade_in": 0.005, "fade_out": 0.04})
    # result: P8, lift on the front 1:1 cut, quiet intro extended by whole 32-beat repeats
    g8 = grid("P8i")
    grid("P8")
    lift = M["P8_lift_mix"]
    J = 32 * g8["period"]
    L = A["lift"] - A["card32"]
    nj = max(0, math.ceil((L - (lift - M["P8_intro_min_mix"])) / J))
    m_s = lift + nj * J - L
    chunks = []
    if nj:
        # play m_s .. jump point, then jump back by J (nj times) on grid beats; 12 ms crossfades
        jp = beat_near("P8i", lift - 2 * g8["period"])
        segs, cur, tl = [], m_s, A["card32"]
        for k in range(nj):
            chunks.append((tl, tl + (jp - cur), cur))
            tl += jp - cur
            cur = jp - J
        chunks.append((tl, A["p7"] + M["xfade_p8_p7"], cur))
    else:
        chunks.append((A["card32"], A["p7"] + M["xfade_p8_p7"], m_s))
    pl.append({"piece": "P8", "chunks": chunks, "tl_a": A["card32"], "tl_b": A["p7"] + M["xfade_p8_p7"],
               "gain_db": M["gain"]["P8"], "fade_in": 1.0, "fade_out": M["xfade_p8_p7"], "lift_tl": A["lift"]})
    # outro: P7 tail, on a P7 bar line, native fade lands across the end card
    m7 = beat_near("P7", M["P7_in_mix"], True)
    pl.append({"piece": "P7", "tl_a": A["p7"], "tl_b": A["end"], "mix_at_a": m7, "gain_db": M["gain"]["P7"],
               "fade_in": M["xfade_p8_p7"], "fade_out": 0.3})
    for p in pl:
        if "chunks" not in p:
            p["chunks"] = [(p["tl_a"], p["tl_b"], p["mix_at_a"])]
        p["grid_id"] = {"P4b": "P4b", "P8": "P8i"}.get(p["piece"], p["piece"])
    return pl, A, {k: {kk: v for kk, v in g.items() if kk not in ("attacks", "strength")} for k, g in grids.items()}, grids


def tl_to_mix(p, t):
    for a, b, m in p["chunks"]:
        if a - 1e-6 <= t <= b + 1e-6:
            return m + (t - a)
    return None


def mix_to_tl(p, m):
    out = []
    for a, b, m0 in p["chunks"]:
        t = a + (m - m0)
        if a <= t <= b:
            out.append(t)
    return out


def snap(evs, pl, grids, A):
    """Snap each cut to the nearest measured beat (+-0.15 s) of the music under it; constraints per EDL timing_note."""
    fixed = {A["lift"]}  # the lift cut is the anchor itself
    report = []
    clipdur = {}

    def cdur(clip):
        if clip not in clipdur:
            clipdur[clip] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                                  f"/home/user/media/lexus-is350/dropbox/{clip}.MP4"], capture_output=True, text=True).stdout)
        return clipdur[clip]

    def sync_ok(e, old, new):
        if e["audio"] != "sync" or e["type"] != "irl":
            return True
        lo, hi = min(old, new), max(old, new)
        for w, s, en in words(e["clip"]):
            if lo - 0.03 < s < hi + 0.03 or lo - 0.03 < en < hi + 0.03 or s + 0.02 < new < en - 0.02:
                return False
        return True

    for i in range(len(evs) - 1):
        a, b = evs[i], evs[i + 1]
        t = a["tl_out"]
        rec = {"cut": f"{a['id']}|{b['id']}", "t_edl": round(t, 3), "moved": 0.0, "why": ""}
        if any(abs(t - x) < 1e-3 for x in fixed) or b["id"] in CFG.get("no_snap", []):
            rec["why"] = "anchor (music placed to it)" if any(abs(t - x) < 1e-3 for x in fixed) else "no_snap"
            report.append(rec); continue
        p = next((p for p in pl if p["tl_a"] + 0.05 < t < p["tl_b"] - 0.05), None)
        if p is None:
            rec["why"] = "no music under this cut (room tone)"; report.append(rec); continue
        m = tl_to_mix(p, t)
        g = grids["P8"] if (p["piece"] == "P8" and m > 1113.0) else grids[p["grid_id"]]
        n0 = round((m - g["t_first"]) / g["period"])
        cands = []
        free = all(x["audio"] != "sync" for x in (a, b))
        win = CFG["snap_window_free"] if free else CFG["snap_window"]
        for n in range(n0 - 2, n0 + 3):
            bm = g["t_first"] + n * g["period"]
            k = mg.nearest_attack(bm, g, 0.04)
            bm = k if k is not None else bm
            for tt in mix_to_tl(p, bm):
                d = tt - t
                if abs(d) <= win:
                    bar = (n - g["downbeat_phase"]) % 4 == 0
                    cands.append((abs(d) - (0.05 if bar and b["id"] in CFG.get("prefer_bar", []) else 0), d, bar, k is not None))
        cands.sort()
        done = False
        for _, d, bar, measured in cands:
            ok = True
            if a["type"] == "irl":
                if a.get("match_out_frame") is None:
                    ok &= sync_ok(a, a["src_out"], a["src_out"] + d) and a["src_out"] + d < cdur(a["clip"]) - 0.05
            if b["type"] == "irl":
                ok &= sync_ok(b, b["src_in"], b["src_in"] + d) and b["src_in"] + d >= 0
            ok &= (a["tl_out"] + d - a["tl_in"]) > 0.6 and (b["tl_out"] - b["tl_in"] - d) > 0.6
            if a["type"] == "scan" and not a.get("allow_long"):
                ok &= (a["tl_out"] + d - a["tl_in"]) <= a["src_out"] + 0.45
            if not ok:
                continue
            a["tl_out"] += d; b["tl_in"] += d
            if a["type"] == "irl":
                if a.get("match_out_frame") is not None:
                    a["src_in"] -= d
                else:
                    a["src_out"] += d
            if b["type"] == "irl":
                b["src_in"] += d
            rec.update(moved=round(d, 3), why=f"{p['piece']} {'bar' if bar else 'beat'}{'' if measured else ' (grid, no attack)'}")
            done = True
            break
        if not done:
            rec["why"] = f"{p['piece']}: no beat within {win} s that keeps sync words / limits"
        report.append(rec)
    return report


def plan():
    evs = load_events()
    pl, A, gsum, grids = place_music(evs)
    rep = snap(evs, pl, grids, A)
    # frames
    f = 0
    for e in evs:
        e["in_f"] = F(e["tl_in"]) if e is not evs[0] else 0
    for i, e in enumerate(evs):
        e["out_f"] = evs[i + 1]["in_f"] if i + 1 < len(evs) else F(e["tl_out"])
        e["n"] = e["out_f"] - e["in_f"]
        e["tl_in"], e["tl_out"] = T(e["in_f"]), T(e["out_f"])
        if e["type"] == "irl":
            if e.get("match_out_frame") is not None:
                e["src_end_f"] = e["match_out_frame"]
                e["src_start_f"] = e["src_end_f"] - e["n"] + 1
            else:
                e["src_start_f"] = F(e["src_in"])
                e["src_end_f"] = e["src_start_f"] + e["n"] - 1
            e["src_in"], e["src_out"] = T(e["src_start_f"]), T(e["src_end_f"] + 1)
        else:
            e["src_in"], e["src_out"] = 0.0, T(e["n"])
        e["edl_in_f"], e["edl_n"] = F(e["edl_in"]), F(e["edl_out"]) - F(e["edl_in"])
        if e.get("sync_audio"):  # J-cut audio under a card keeps its offset to the card start
            sa = e["sync_audio"]
            sa["src_out"] = min(sa["src_out"], sa["src_in"] + e["tl_out"] - e["tl_in"])
    tl = {"project": "lexus-is350-speedrun-long", "fps": "24000/1001", "frames_total": evs[-1]["out_f"],
          "duration_s": round(T(evs[-1]["out_f"]), 4), "built_by": "tools/assemble_long.py plan",
          "note": "Final timeline after dropping E41 (no cabin geometry), replacing E71 with conclusion Version A and beat snap. "
                  "Times in seconds and frames (frame = round(t*fps)); src_in/src_out are seconds in the source clip (for IRL "
                  "exact frame bounds). sync_speech: event carries sync dialogue -> caption from the word JSON in that src range. "
                  "Caption zone: rail centre x 410-1510, y 920-1080, kept empty in picture.",
          "anchors_s": {k: round(v, 3) for k, v in A.items()}, "music": [], "events": [], "cuts": rep, "grids": gsum}
    for p in pl:
        tl["music"].append({"piece": p["piece"], "tl_in": round(p["tl_a"], 3), "tl_out": round(p["tl_b"], 3), "gain_db": p["gain_db"],
                            "chunks_tl_in_tl_out_mix_in": [[round(a, 4), round(b, 4), round(m, 4)] for a, b, m in p["chunks"]]})
    for e in evs:
        o = {"id": e["id"], "section": e["section"], "type": e["type"],
             "tl_in": round(e["tl_in"], 4), "tl_out": round(e["tl_out"], 4), "in_frame": e["in_f"], "out_frame": e["out_f"],
             "frames": e["n"], "source": e["source"], "src_in": round(e["src_in"], 4), "src_out": round(e["src_out"], 4),
             "sync_speech": e["audio"] == "sync", "audio": e["audio"],
             "edl_tl_in": e["edl_in"], "edl_tl_out": e["edl_out"]}
        if e["type"] == "irl":
            o["src_frames"] = [e["src_start_f"], e["src_end_f"]]
            o["word_json"] = str(W / f"transcripts/{e['clip']}.json")
        if e.get("sync_audio"):
            o["sync_audio"] = e["sync_audio"]; o["sync_speech"] = True
            o["word_json"] = str(W / f"transcripts/{e['sync_audio']['clip']}.json")
        tl["events"].append(o)
    atomic_json(P / "timeline.json", tl)
    atomic_json(B / "plan_internal.json", {"events": evs, "music": pl, "anchors": A})
    log("plan:", len(evs), "events,", tl["duration_s"], "s; snapped",
        sum(1 for r in rep if r["moved"]), "of", len(rep), "cuts")
    return evs, pl, A


# ----------------------------------------------------------------------------------------------------------- video
def probe_wh(src):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
    return int(o[0]), int(o[1])


def reader(cmd, w, h, ch=3):
    p = subprocess.Popen(NICE + cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=w * h * ch * 2)
    sz = w * h * ch
    while True:
        buf = p.stdout.read(sz)
        if len(buf) < sz:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, ch)
    p.stdout.close(); p.wait()


def scan_status() -> dict:
    st = {}
    for line in open(P / "scan_shots.md"):
        m = re.match(r"\|\s*(\w+)\s*\|\s*(\w+)\s*\|", line)
        if m:
            st[m.group(1)] = m.group(2)
    return st


def scan_source(shot: str):
    pv = W / f"renders/{shot}/{shot}_preview.mp4"
    st = scan_status().get(shot, "")
    if pv.exists() and st == "done":
        return "final", str(pv)
    look = sorted(glob.glob(str(W / f"scan3d/look/pv_{shot}/f_*.png")))
    if look:
        return "preview", look
    return "black", None


_font = {}


def font(sz):
    from PIL import ImageFont
    if sz not in _font:
        _font[sz] = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf", sz) \
            if os.path.exists("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf") else \
            ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", sz)
    return _font[sz]


def tag(img: np.ndarray, text: str):
    """Small red PLACEHOLDER tag, top-right (never in the rail's caption zone)."""
    from PIL import Image, ImageDraw
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    f = font(26)
    x1, y1, x2, y2 = d.textbbox((0, 0), text, font=f)
    w, h = x2 - x1 + 24, y2 - y1 + 16
    x0, y0 = 1920 - 40 - w, 40
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(170, 20, 20))
    d.text((x0 + 12 - x1, y0 + 8 - y1), text, font=f, fill=(255, 255, 255))
    return np.asarray(im)


def blur_boxes(e) -> list:
    tr = json.load(open(P / "tools/blur_tracks.json")) if (P / "tools/blur_tracks.json").exists() else {}
    return tr.get(e["id"], {}).get("boxes", [])  # [[src_frame, x, y, w, h], ...] in pre-crop coords


def apply_blur(fr: np.ndarray, boxes_at: list):
    import cv2
    out = fr.copy()
    H, Wd = fr.shape[:2]
    for x, y, w, h in boxes_at:
        pad = int(max(w, h) * 0.35) + 8
        x0, y0, x1, y1 = max(0, int(x - pad)), max(0, int(y - pad)), min(Wd, int(x + w + pad)), min(H, int(y + h + pad))
        if x1 <= x0 or y1 <= y0:
            continue
        roi = out[y0:y1, x0:x1]
        k = int(max(w, h) * 0.5) | 1
        bl = cv2.GaussianBlur(cv2.resize(roi, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA), (0, 0), max(2, k / 8))
        bl = cv2.resize(bl, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
        m = np.zeros((y1 - y0, x1 - x0), np.float32)
        cx0, cy0 = int(x - x0), int(y - y0)
        m[max(0, cy0 - 6):cy0 + int(h) + 6, max(0, cx0 - 6):cx0 + int(w) + 6] = 1
        m = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
        out[y0:y1, x0:x1] = (roi * (1 - m) + bl * m).astype(np.uint8)
    return out


def boxes_for(boxes, sf):
    """interpolate the tracked boxes (several objects allowed: key 'obj') at source frame sf"""
    res = []
    objs = {}
    for b in boxes:
        objs.setdefault(b[5] if len(b) > 5 else 0, []).append(b)
    for _, bl in objs.items():
        bl = sorted(bl)
        fs = [b[0] for b in bl]
        if sf < fs[0] - 1 or sf > fs[-1] + 1:
            continue
        if sf <= fs[0]:
            res.append(bl[0][1:5]); continue
        if sf >= fs[-1]:
            res.append(bl[-1][1:5]); continue
        j = int(np.searchsorted(fs, sf))
        a, b = bl[j - 1], bl[j]
        u = (sf - a[0]) / max(1, b[0] - a[0])
        res.append([a[k] + (b[k] - a[k]) * u for k in range(1, 5)])
    return res


def irl_frames(e):
    src = e["source"]
    w, h = probe_wh(src)
    vf = []
    if (w, h) != (1920, 1080):
        vf.append("scale=1920:1080:flags=lanczos")
    vf += ["format=rgb48le", f"lut3d=file={LUT}:interp=tetrahedral"]
    rot = e.get("rotate")
    if rot:
        vf.append(f"transpose={rot}")
    vf.append("format=rgb24")
    ow, oh = (1080, 1920) if rot else (1920, 1080)
    ss = (e["src_start_f"] - 0.5) / FPS
    cmd = ["ffmpeg", "-v", "error", "-threads", "2", "-ss", f"{max(0, ss):.4f}", "-i", src, "-frames:v", str(e["n"]),
           "-vf", ",".join(vf), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    boxes = blur_boxes(e)
    y0 = int(e.get("crop_y", 80))
    import cv2
    k = 0
    last = None
    for fr in reader(cmd, ow, oh):
        sf = e["src_start_f"] + k
        if boxes:
            fr = apply_blur(fr, boxes_for(boxes, sf))
        if rot:  # pillarbox the upright 1080x1920 picture on a blurred, darkened copy of itself
            bg = cv2.resize(fr, (1920, int(1920 * 1920 / 1080)), interpolation=cv2.INTER_AREA)
            c = (bg.shape[0] - 920) // 2 + int(e.get("bg_shift", 0))
            bg = cv2.GaussianBlur(cv2.resize(bg[c:c + 920], (480, 230)), (0, 0), 9)
            bg = (cv2.resize(bg, (1920, 920)) * 0.35).astype(np.uint8)
            fh = 920
            fw = int(round(1080 * fh / 1920 / 2)) * 2
            fg = cv2.resize(fr, (fw, fh), interpolation=cv2.INTER_AREA)
            x = (1920 - fw) // 2
            bg[:, x:x + fw] = fg
            top = bg
        else:
            top = fr[y0:y0 + 920]
        out = np.zeros((1080, 1920, 3), np.uint8)
        out[:920] = top
        last = out
        k += 1
        yield out
    while k < e["n"]:  # never short
        k += 1
        yield last


def card_frames(e):
    src = str(GFX / f"{e['card']}.mp4")
    last = None
    k = 0
    for fr in reader(["ffmpeg", "-v", "error", "-i", src, "-frames:v", str(e["n"]), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], 1920, 1080):
        last = fr; k += 1
        yield fr
    while k < e["n"]:
        k += 1
        yield last


def scan_frames(e):
    import cv2
    kind, src = scan_source(e["shot"])
    sw = CFG["scan"].get(e["shot"], {})
    if kind == "final":
        swap = sw.get("swap_at")
        pngdir = W / f"renders/{e['shot']}/png"
        k, last = 0, None
        for fr in reader(["ffmpeg", "-v", "error", "-i", src, "-frames:v", str(e["n"]), "-vf", "scale=1920:1080",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], 1920, 1080):
            t = k / FPS
            if swap is not None:  # held frames around a same-camera state swap (no interpolated blend across it)
                rf = t * 8
                if abs(rf - round(rf)) > 1e-3 and math.floor(rf) + 1 == round(swap * 8):
                    p = pngdir / f"f_{math.floor(rf) + 1:04d}.png"
                    if p.exists():
                        fr = cv2.cvtColor(cv2.resize(cv2.imread(str(p)), (1920, 1080)), cv2.COLOR_BGR2RGB)
            last = fr; k += 1
            yield fr
        while k < e["n"]:
            k += 1
            yield last
        return
    if kind == "preview":
        keys = [(int(Path(p).stem.split("_")[1]), p) for p in src]
        cache = {}
        label = f"PLACEHOLDER {e['shot']} (preview frames)"
        for k in range(e["n"]):
            sf = k / FPS * 8 + 1  # 8 fps render frame number (1-based)
            idx = max([i for i, _ in keys if i <= sf + 1e-6] or [keys[0][0]])
            p = dict(keys)[idx]
            if p not in cache:
                im = cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB)
                cache[p] = tag(cv2.resize(im, (1920, 1080), interpolation=cv2.INTER_CUBIC), label)
            yield cache[p]
        return
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (1920, 1080), (0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font(56)
    d.text((960, 460), e["shot"], font=f, fill=(200, 200, 200), anchor="mm")
    d.text((960, 540), "scan render pending", font=font(30), fill=(140, 140, 140), anchor="mm")
    fr = tag(np.asarray(im), f"PLACEHOLDER {e['shot']}")
    for _ in range(e["n"]):
        yield fr


def overlay_streams(e):
    """alpha cards (G01, G10-G13, CON_G3) as (start_frame_in_event, generator of RGBA frames)"""
    res = []
    for cue in e["gfx"]:
        p = GFX / f"{cue}.mov"
        if not p.exists() or cue == "HUD_RAIL":
            continue
        off = F(CFG["overlay_offsets"][cue])
        n = max(0, e["n"] - off)
        if n:
            res.append((off, reader(["ffmpeg", "-v", "error", "-i", str(p), "-frames:v", str(n), "-f", "rawvideo",
                                     "-pix_fmt", "rgba", "-"], 1920, 1080, 4)))
    return res


def rail_frames(e):
    """HUD_RAIL frames for this event: rail[edl_in + k], held on its own last frame if the event got longer."""
    a = e["edl_in_f"]
    nmax = e["edl_n"]
    need = min(e["n"], nmax)
    gen = reader(["ffmpeg", "-v", "error", "-ss", f"{(a - 0.5) / FPS:.4f}", "-i", str(GFX / "HUD_RAIL.mov"), "-frames:v", str(need),
                  "-f", "rawvideo", "-pix_fmt", "rgba", "-"], 1920, 160, 4)
    last = None
    for k in range(e["n"]):
        if k < need:
            last = next(gen, last)
        yield last


def over(dst, rgba, y=0):
    a = rgba[..., 3:4].astype(np.float32) / 255.0
    h = rgba.shape[0]
    reg = dst[y:y + h].astype(np.float32)
    dst[y:y + h] = (reg * (1 - a) + rgba[..., :3].astype(np.float32) * a + 0.5).astype(np.uint8)


def seg_key(e):
    k = {kk: e.get(kk) for kk in ("id", "type", "source", "src_start_f", "n", "crop_y", "rotate", "gfx", "edl_in_f", "edl_n", "bg_shift")}
    k["v"] = CFG["seg_version"]
    if e["type"] == "irl":
        k["blur"] = blur_boxes(e)
    if e["type"] == "scan":
        kind, src = scan_source(e["shot"])
        k["scan"] = [kind, src if isinstance(src, str) else (src or [])]
        if isinstance(src, str):
            k["mtime"] = os.path.getmtime(src)
        k["swap"] = CFG["scan"].get(e["shot"], {})
    return hashlib.sha1(json.dumps(k, sort_keys=True, default=str).encode()).hexdigest()[:16]


def render_segment(e):
    d = B / "seg"
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"{e['in_f']:06d}_{e['id']}.mp4"
    key = seg_key(e)
    meta = out.with_suffix(".json")
    if out.exists() and meta.exists() and json.load(open(meta)).get("key") == key:
        return out, False
    for old in glob.glob(str(d / f"*_{e['id']}.*")):
        os.remove(old)
    gen = {"irl": irl_frames, "card": card_frames, "scan": scan_frames}[e["type"]](e)
    ovs = overlay_streams(e)
    rail = rail_frames(e)
    tmp = out.with_suffix(".tmp.mp4")
    enc = subprocess.Popen(NICE + ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080",
                                   "-r", "24000/1001", "-i", "-", "-c:v", "libx264", "-preset", CFG["x264_preset"], "-crf", "18",
                                   "-threads", "2", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                                   "-colorspace", "bt709", "-g", "48", "-bf", "2", "-x264-params", "open-gop=0",
                                   "-movflags", "+faststart", "-f", "mp4", str(tmp)], stdin=subprocess.PIPE)
    n = 0
    for k in range(e["n"]):
        fr = next(gen).copy()
        for off, g in ovs:
            if k >= off:
                o = next(g, None)
                if o is not None:
                    over(fr, o)
        r = next(rail)
        if r is not None:
            over(fr, r, 920)
        enc.stdin.write(fr.tobytes())
        n += 1
    enc.stdin.close(); enc.wait()
    if enc.returncode != 0 or n != e["n"]:
        raise RuntimeError(f"segment {e['id']} failed ({n}/{e['n']})")
    os.replace(tmp, out)
    atomic_json(meta, {"key": key, "frames": n, "id": e["id"]})
    return out, True


def video(evs):
    t0 = time.time()
    keep = set()
    for e in evs:
        o, did = render_segment(e)
        keep.add(o.name)
        if did:
            log(f"segment {e['id']} {e['n']} f rendered ({time.time() - t0:.0f} s)")
    for f in glob.glob(str(B / "seg/*.mp4")):
        if Path(f).name not in keep:
            os.remove(f)
            if os.path.exists(f[:-4] + ".json"):
                os.remove(f[:-4] + ".json")
    lst = B / "concat.txt"
    lst.write_text("".join("file '%s'\n" % (B / "seg" / ("%06d_%s.mp4" % (e["in_f"], e["id"]))) for e in evs))
    subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                           str(B / "picture.tmp.mp4")], check=True)
    os.replace(B / "picture.tmp.mp4", B / "picture.mp4")
    log("picture.mp4 concatenated")


# ----------------------------------------------------------------------------------------------------------- audio
def wav_read(path):
    from scipy.io import wavfile
    sr, a = wavfile.read(path)
    a = a.astype(np.float32)
    if a.dtype != np.float32 or np.abs(a).max() > 2:
        a = a / 32768.0
    return a


def src_audio(clip, a, b, af):
    raw = subprocess.run(NICE + ["ffmpeg", "-v", "error", "-ss", f"{a:.4f}", "-i", f"/home/user/media/lexus-is350/dropbox/{clip}.MP4",
                                 "-t", f"{b - a:.4f}", "-vn", "-af", af, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    n = int(round((b - a) * SR))
    if len(x) < n:
        x = np.r_[x, np.zeros(n - len(x), np.float32)]
    return x[:n]


def lufs(x: np.ndarray, sr=SR, mono=True) -> float:
    """integrated loudness (BS.1770 K-weighting + gating), mono speech counted as dual-mono (+3 dB like a centred stereo mix)"""
    from scipy.signal import lfilter
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    chans = [x] if x.ndim == 1 else [x[:, i] for i in range(x.shape[1])]
    blk, hop = int(0.4 * sr), int(0.1 * sr)
    pw = None
    for c in chans:
        y = lfilter(b2, a2, lfilter(b1, a1, c))
        e = np.array([np.mean(y[i:i + blk] ** 2) for i in range(0, max(1, len(y) - blk), hop)])
        pw = e if pw is None else pw + e
    if x.ndim == 1 and mono:
        pw = pw * 2
    lk = -0.691 + 10 * np.log10(pw + 1e-12)
    g = pw[lk > -70]
    if not len(g):
        return -70.0
    rel = -0.691 + 10 * np.log10(g.mean()) - 10
    g2 = pw[(lk > -70) & (lk > rel)]
    return float(-0.691 + 10 * np.log10(g2.mean() + 1e-12))


def fade(x, a_s, b_s):
    na, nb = int(a_s * SR), int(b_s * SR)
    if na:
        x[:na] *= np.linspace(0, 1, na) ** 1.0
    if nb:
        x[-nb:] *= np.linspace(1, 0, nb)
    return x


def resample_441(x):
    from scipy.signal import resample_poly
    return resample_poly(x, 160, 147, axis=0).astype(np.float32)


def audio(evs, pl, anchors):
    A = CFG["audio"]
    N = evs[-1]["out_f"]
    total = int(round(T(N) * SR))
    dia = np.zeros(total, np.float32)
    room = np.zeros(total, np.float32)
    speech = np.zeros(total, np.float32)  # 1 where a word is spoken (for ducking)
    rep = []
    clipgain = {}
    lines = []
    for e in evs:
        if e["audio"] != "sync":
            continue
        if e.get("sync_audio"):
            sa = e["sync_audio"]; clip, a, b = sa["clip"], sa["src_in"], sa["src_out"]
        else:
            clip, a, b = e["clip"], e["src_in"], e["src_out"]
        af = A["clean"] + ("," + A["declip"] if clip in A["declip_clips"] else "")
        x = src_audio(clip, a, b, af)
        L = lufs(x)
        g = A["dialogue_lufs"] - L
        g = float(np.clip(g, -6, A["max_gain_db"]))
        x = x * 10 ** (g / 20)
        fade(x, 0.012, 0.012)
        i0 = int(round(e["tl_in"] * SR))
        dia[i0:i0 + len(x)] += x[: total - i0]
        clipgain.setdefault(clip, []).append(g)
        for w, s, en in words_in(clip, a, b):
            ws, we = int((e["tl_in"] + max(s, a) - a) * SR), int((e["tl_in"] + min(en, b) - a) * SR)
            speech[max(0, ws):min(total, we)] = 1
        lines.append({"id": e["id"], "clip": clip, "lufs_raw": round(L, 1), "gain_db": round(g, 1)})
    # dialogue bus: gentle compression, re-level, peak limit (whisper-level lines and spray-gun transients in one bus)
    dia = dialogue_bus(dia, A)
    # room tone: room-tone events use their own audio; the music-less bridges get a continuous bed from a word-free stretch
    for e in evs:
        if e["audio"] == "room" and e["type"] == "irl" and CFG["audio"].get("room_events_own_audio"):
            clip = e["clip"]
            x = src_audio(clip, e["src_in"], e["src_out"], A["clean"])
            g = float(np.median(clipgain.get(clip, [0]))) + A["room_rel_db"]
            x = fade(x * 10 ** (g / 20), 0.02, 0.02)
            i0 = int(round(e["tl_in"] * SR))
            room[i0:i0 + len(x)] += x[: total - i0]
    for br in CFG["room_bridges"]:
        a_t, b_t = anchors[br["from"]] + br.get("from_off", 0), anchors[br["to"]] + br.get("to_off", 0)
        clip, sa, sb = br["clip"], br["src"][0], br["src"][1]
        bed = src_audio(clip, sa, sb, A["clean"])
        g = float(np.median(clipgain.get(clip, [0]))) + br["rel_db"]
        n = int((b_t - a_t) * SR)
        out = np.zeros(n, np.float32)
        L = len(bed); xf = int(0.25 * SR); pos = 0
        while pos < n:  # loop the bed with 250 ms crossfades
            seg = bed.copy()
            seg[:xf] *= np.linspace(0, 1, xf); seg[-xf:] *= np.linspace(1, 0, xf)
            m = min(L, n - pos)
            out[pos:pos + m] += seg[:m]
            pos += L - xf
        out = fade(out * 10 ** (g / 20), 0.3, 0.3)
        i0 = int(a_t * SR)
        room[i0:i0 + n] += out[: total - i0]
    # music
    from scipy.io import wavfile
    sr_m, mix = wavfile.read(str(W / "music/mix_full.wav"), mmap=True)
    mus = np.zeros((total, 2), np.float32)
    for p in pl:
        buf = np.zeros((total, 2), np.float32)
        for ci, (a_t, b_t, m) in enumerate(p["chunks"]):
            m0, m1 = m - 0.02, m + (b_t - a_t) + 0.02
            x = mix[int(m0 * sr_m):int(m1 * sr_m)].astype(np.float32) / 32768.0
            x = resample_441(x)
            off = int(round(0.02 * SR))
            n = int(round((b_t - a_t) * SR))
            seg = x[off:off + n].copy()
            if len(seg) < n:
                seg = np.r_[seg, np.zeros((n - len(seg), 2), np.float32)]
            xf = int(0.012 * SR)
            if ci > 0:
                seg[:xf] *= np.linspace(0, 1, xf)[:, None]
            if ci < len(p["chunks"]) - 1:  # 12 ms crossfade overlap into the next chunk
                tail = x[off + n: off + n + xf].copy()
                tail *= np.linspace(1, 0, len(tail))[:, None]
                j = int(round(b_t * SR))
                buf[j:j + len(tail)] += tail[: total - j]
                seg[-1:] *= 1
            i0 = int(round(a_t * SR))
            buf[i0:i0 + n] += seg[: total - i0]
        i0, i1 = int(round(p["tl_a"] * SR)), min(total, int(round(p["tl_b"] * SR)))
        env = np.zeros(total, np.float32)
        env[i0:i1] = 1
        fi, fo = int(p["fade_in"] * SR), int(p["fade_out"] * SR)
        if fi:
            env[i0:i0 + fi] = np.linspace(0, 1, fi)
        if fo:
            env[i1 - fo:i1] = np.linspace(1, 0, fo)
        mus += buf * env[:, None] * 10 ** (p["gain_db"] / 20)
    # ducking: -12 dB under words, 120 ms attack (pre-roll), 450 ms release
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    pre = int(0.12 * SR)
    sp = np.r_[speech[pre:], np.zeros(pre, np.float32)]
    sp = np.maximum(sp, speech)
    nrel = int(0.45 * SR)
    c = np.r_[0.0, np.cumsum(sp, dtype=np.float64)]
    idx = np.arange(len(sp))
    sp = ((c[idx + 1] - c[np.maximum(0, idx + 1 - nrel)]) > 0.5).astype(np.float32)  # hold 450 ms after each word
    sp = uniform_filter1d(sp, size=int(0.15 * SR))
    duck = 10 ** (A["duck_db"] * sp / 20)
    mus *= duck[:, None]
    # stems (stereo)
    stems = {"dialogue": np.stack([dia, dia], 1), "music": mus, "fx_room": np.stack([room, room], 1)}
    mixd = stems["dialogue"] + stems["music"] + stems["fx_room"]
    Lm = lufs(mixd, mono=False)
    gain = A["target_lufs"] - Lm
    for k in stems:
        stems[k] *= 10 ** (gain / 20)
    mixd *= 10 ** (gain / 20)
    (B / "audio").mkdir(exist_ok=True)
    np.save(B / "audio/mix_pre.npy", mixd)
    for k, v in stems.items():
        write_wav(B / f"audio/{k}.wav", v)
    atomic_json(B / "audio/report.json", {"lines": lines, "mix_lufs_pre": Lm, "master_gain_db": gain})
    log(f"audio: {len(lines)} sync lines, pre-master {Lm:.1f} LUFS, gain {gain:+.1f} dB")


def dialogue_bus(x, A):
    from scipy.io import wavfile
    (B / "audio").mkdir(exist_ok=True)
    src, dst = B / "audio/dia_raw.wav", B / "audio/dia_comp.wav"
    wavfile.write(src, SR, x.astype(np.float32))
    subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", A["dia_comp"], "-c:a", "pcm_f32le", str(dst)], check=True)
    _, y = wavfile.read(dst)
    y = y.astype(np.float32)
    y *= 10 ** ((A["dialogue_lufs"] - lufs(y)) / 20)
    wavfile.write(src, SR, y)
    lim = f"alimiter=limit={10 ** (A['dia_peak_dbfs'] / 20):.4f}:attack=2:release=60:level=disabled"
    subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", lim, "-c:a", "pcm_f32le", str(dst)], check=True)
    _, y = wavfile.read(dst)
    os.remove(src); os.remove(dst)
    y = y.astype(np.float32)[: len(x)]
    return np.r_[y, np.zeros(len(x) - len(y), np.float32)]


def write_wav(path, x):
    """32-bit float WAV (no clipping: stems are not limited, only the final mix is)"""
    from scipy.io import wavfile
    tmp = str(path) + ".tmp.wav"
    wavfile.write(tmp, SR, np.asarray(x, np.float32))
    os.replace(tmp, path)


def master(evs):
    A = CFG["audio"]
    mixd = np.load(B / "audio/mix_pre.npy")
    write_wav(B / "audio/mix_pre.wav", mixd)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "stems").mkdir(exist_ok=True)
    gain_trim = 0.0
    for it in range(4):
        af = f"volume={gain_trim:.3f}dB,alimiter=limit={10 ** (A['limit_dbfs'] / 20):.4f}:attack=3:release=60:level=disabled"
        subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-i", str(B / "audio/mix_pre.wav"), "-af", af, "-ar", "48000",
                               "-c:a", "pcm_s24le", str(OUT / "is350_long_v1_mix.wav")], check=True)
        r = loudness(OUT / "is350_long_v1_mix.wav")
        log(f"master pass {it}: I={r['I']} LUFS TP={r['TP']} dBTP")
        if abs(r["I"] - A["target_lufs"]) <= 0.3 and r["TP"] <= -1.0:
            break
        gain_trim += A["target_lufs"] - r["I"] if r["TP"] <= -1.0 else -0.5
    for k in ("dialogue", "music", "fx_room"):
        os.replace(B / f"audio/{k}.wav", OUT / f"stems/is350_long_v1_stem_{k}.wav") if (B / f"audio/{k}.wav").exists() else None
    os.remove(B / "audio/mix_pre.wav")
    tmp = OUT / "is350_long_v1_rough.tmp.mp4"
    subprocess.run(NICE + ["ffmpeg", "-v", "error", "-y", "-i", str(B / "picture.mp4"), "-i", str(OUT / "is350_long_v1_mix.wav"),
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
                           "-shortest", "-movflags", "+faststart", str(tmp)], check=True)
    os.replace(tmp, OUT / "is350_long_v1_rough.mp4")
    log("wrote", OUT / "is350_long_v1_rough.mp4")


def loudness(path):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    s = o[o.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1))
    TP = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))
    LRA = float(re.search(r"LRA:\s+(-?[\d.]+) LU", s).group(1))
    return {"I": I, "TP": TP, "LRA": LRA}


# ----------------------------------------------------------------------------------------------------------- main
def main():
    stages = sys.argv[1:] or ["plan", "video", "audio", "master"]
    B.mkdir(parents=True, exist_ok=True)
    evs, pl, A = plan()
    if "video" in stages:
        video(evs)
    if "audio" in stages:
        audio(evs, pl, A)
    if "master" in stages:
        master(evs)


if __name__ == "__main__":
    main()
